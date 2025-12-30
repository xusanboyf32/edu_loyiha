import logging
import os
import sys
import signal
import asyncio
from datetime import timedelta

import django

from aiogram import Bot, Dispatcher, types
from  aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,
    InlineKeyboardButton, ReplyKeyboardRemove
)
from aiogram import F
from asgiref.sync import sync_to_async

os.environ.setdefault("DJANGO_SETTINGS_MODULE","config.settings")
django.setup()


from django.utils import timezone
import pytz
from authentication.models import TelegramAuth
from django.core.cache import cache
from django.conf import settings


# Logger sozlash
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(module)s %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)


logger = logging.getLogger(__name__)
logger.info("Bot started")


# Konfiguratsiya -> settingsda token .envdan settings olgan
API_TOKEN = settings.TELEGRAM_BOT_TOKEN

# Bu token bor yo'qligini tekshirish kodi agar bolmas xatolik chiqadi
if not API_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not found in settings")
    sys.exit(1)


bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# botni shundoq toxtatish
shutdown_event = asyncio.Event()


# signal handler
def signal_handler(signum,frame):
    # bu log shunchaki ma'lumot chiqishi uchun
    logger.info(f"Received {signum}, shutting down...")
    shutdown_event.set()


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def get_retry_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Kodni yangilash", callback_data="retry_code")]
    ])
    return kb

# ===================== START KOMANDASI KODI ===============================


@dp.message(Command("start"))
async def start(message: types.Message):
    try:
        args = message.text.split(" ")[1] if len(message.text.split(" ")) > 1 else None
        chat_id = message.chat.id

        logger.info(f"Start command received from chat_id: {chat_id}, args: {args}")

        if not args or not args.startswith("login_"):
            await message.answer("Iltimos, faqat sayt orqali berilgan havola orqali kirishni so'rang.")
            return

        session_token = args


        try:
            auth = await sync_to_async(TelegramAuth.objects.get)(
                session_token=session_token,
                # is_used=False
            )

            auth.chat_id = chat_id
            await sync_to_async(auth.save)()

            if await sync_to_async(lambda: auth.is_expired)():
                await message.answer("Sessiya muddati o'tgan. Iltimos, saytdan qayta urinib ko'ring.")
                return


            logger.info(f"Session found and updated for chat_id: {chat_id}")

        except TelegramAuth.DoesNotExist:
            logger.warning(f"Session not found token: {session_token}")
            await message.answer("Sessiya topilmadi. Iltimos , saytdan boshlang")
            return
        except Exception as e:
            logger.error(f"Database error in start command: {e}")
            await message.answer("Xatolik yuz berdi. Iltimos qayta urinib ko'ring.")
            return

        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="📞 Telefon raqami yuborish", request_contact=True)]],
            resize_keyboard=True
        )

        await message.answer("Iltimos telefon raqamingizni yuboring.",reply_markup=kb)

    except Exception as e:
        logger.error(f"Unexpected error in start command: {e}")
        await message.answer("Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")


@dp.message(F.contact)
async def handle_contact(message: types.Message):
    try:
        phone = message.contact.phone_number
        chat_id = message.chat.id

        logger.info(f"[DEBUG] Contact received from chat_id: {chat_id}, phone: {phone}")

        try:
            pending = await sync_to_async(
                lambda: TelegramAuth.objects.filter(
                    chat_id=chat_id,
                    phone_number__isnull=True,
                    # is_used=False,
                    created_at__gte=timezone.now() - timezone.timedelta(minutes=10)
                ).order_by('-created_at').first()
            )()
            if not pending:
                await message.answer("Faol sessiya topilmadi. Iltimos , saytdan qayta boshlang.")
                return

            # DEBUG boshlang'ich holat
            logger.info(f"[DEBUG-1] BEFOR any change: is_used={pending.is_used}")


        except Exception as e:
            logger.error(f"Database error in handle_contact: {e}")
            return


#  shu qismi kod jonatadi hamda 2 daqiqa muddati boladi codeni eskirish
        import random
        code = str(random.randint(1000,9999))
        login_url = f"{settings.SITE_URL}/login/"

        logger.info(f"[DEBUG-2] BEFORE field updates: is_used={pending.is_used}")

        pending.phone_number = phone
        pending.code = code
        pending.expires_at = timezone.now() + timezone.timedelta(minutes=2)

        logger.info(f"[DEBUG-3] AFTER field updates, BEFORE save: is_used={pending.is_used}")

        # Aniq False qilib qo'yish
        pending.is_used = False
        logger.info(f"[DEBUG-4] EXPLICITLY set False, BEFORE save: is_used={pending.is_used}")

        # SAVE
        await sync_to_async(pending.save)()

        # DEBUG: Save qilishdan keyin
        logger.info(f"[DEBUG-5] IMMEDIATELY after save: is_used={pending.is_used}")

        logger.info(f"Code generated for session: {pending.session_token}")

        await message.answer(
            f"🔐 Tasdiqlash kodingiz: `{code}`\n\n"
            f"⏳ Kod 2 daqiqa amal qiladi.\n\n"
            f"👉 Kirish uchun: [Bu yerga bosing]({login_url})",
            parse_mode="Markdown",
            reply_markup=get_retry_kb()
        )

        await message.answer("✅ Kod yuborildi!",reply_markup=ReplyKeyboardRemove())

    except Exception as e:
        logger.error(f"Unexpected error in handle_contact: {e}")
        await message.answer("Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")

# KOD YANGILASH

@dp.callback_query(F.data == "retry_code")
async def retry_code(callback: types.CallbackQuery):
    try:
        user_id = callback.from_user.id
        chat_id = callback.message.chat.id

        logger.info(f"Retry code requested by chat_id: {chat_id}")

        try:
            pending = await sync_to_async(
                lambda: TelegramAuth.objects.filter(
                    chat_id=chat_id,
                    phone_number__isnull=False,
                    # is_used=False,
                    created_at__gte=timezone.now() - timezone.timedelta(minutes=10)
                ).order_by('-created_at').first()
            )()
            if not pending:
                await callback.message.edit_text("Faol sessiya topilmadi. Iltimos, saytdan qayta boshlang.")
                await callback.answer()
                return

        except Exception as e:
            logger.error(f"Database error in retry_code: {e}")
            await callback.answer("Xatolik yuz berdi.")
            return

    # limit borligi 3 martadan ko'p marta kod olmaydi
        cache_key = f"retry_limit_{pending.session_token}"
        attempts = cache.get(cache_key, 0)
        if attempts >= 3:
            await callback.message.edit_text("Siz juda ko'p urinish qildingiz. 5 daqiqa kutishingiz kerak.")
            await callback.answer()
            return


        import random
        new_code = str(random.randint(1000,9999))
        pending.code = new_code
        pending.expires_at = timezone.now() + timedelta(minutes=2)
        await sync_to_async(pending.save)()

        cache.set(cache_key, attempts + 1,300)

        login_url = f"{settings.SITE_URL}/login/"

        await callback.message.edit_text(
            f"🔄 Yangi kod: `{new_code}`\n\n⏳ 2 daqiqa amal qiladi.\n\n"
            f"👉 Kirish uchun: [Bu yerga bosing]({login_url})",
            parse_mode="Markdown",
            reply_markup=get_retry_kb()
        )
        await callback.answer("Yangi kod yuborildi.")

        logger.info(f"New code generated for session: {pending.session_token}")



    except Exception as e:
        logger.error(f"Unexpected error in retry_code: {e}")
        await callback.answer("Xatolik yuz berdi")



# main START qismi kodning

async def main():
    logger.info("Starting Telegram bot...")


    try:
        # bot ma'lumotlarini olish
        bot_info = await bot.get_me()
        logger.info(f"Bot started: @{bot_info.username}")

        # Pollling boshqarish
        await dp.start_polling(bot, handle_signals=False)

    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise
    finally:
        logger.info("Bot stopped")


# botni grace full bilan tugatish yani tosattan emas etap etap TO'LIQ to'xtatish
async def run_with_graceful_shutdown():
    try:
        bot_task = asyncio.create_task(main())
        # Shutdown signalls kutish
        shutdown_task = asyncio.create_task(shutdown_event.wait())

        # birinchi tugagan taskni kutish
        done, pending = await asyncio.wait(
            [bot_task, shutdown_task],
            return_when=asyncio.FIRST_COMPLETED
        )

        # QOLGAN TASKLARNI BEKOR QILISH
        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        # Agar bot task tugagan bo'lsa, xatolik bo'lgan deb hisoblaymiz
        if bot_task in done:
            exception = bot_task.exception()
            if exception:
                raise exception


    except KeyboardInterrupt:
        logger.info("Received keybord interrupt")
    except Exception as e:
        logger.error(f"Bot error: {e}")
        raise
    finally:
        try:
            await bot.session.close()
            logger.info("Bot session closed")
        except Exception as e:
            logger.error(f"Error closing bot session: {e}")

if __name__ == "__main__":

    try:
        asyncio.run(run_with_graceful_shutdown())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)




