# eduAgent Docs (English)

# Documentation for the edu_loyiha project

**Repository:** [github.com/xusanboyf32/edu_loyiha](https://github.com/xusanboyf32/edu_loyiha?referrer=grok.com)

License:  MIT License

**Languages:** Python (46.4%), HTML (53.6%)

**Framework:** Django (backend), SQLite (database)

**Advanced:** Telegram bot integration

# Avaible in languages: [🇷🇺](https://www.notion.so/eduAgent-Docs-2d9c4ac536288050ab5bc7755cae9c05?pvs=21) | [🇺🇸](https://www.notion.so/eduAgent-Docs-English-2d9c4ac53628809b95f8c8319f44292a?pvs=21) | [🇺🇿](https://www.notion.so/eduAgent-Docs-O-zbekcha-2d9c4ac5362880e38de1d7826f9c28cc?pvs=21)

## Project Description

edu_loyiha is an educational project (loyiha means "project" in Uzbek), which is a Django-based web application for online learning. The project includes course management, student management, authentication, chat with AI, and a Telegram bot for interaction.

There are scripts for automatic generation of educational content: exercises, math problems, examples and materials for interactive learning (EduPlay).

The project is focused on automating the creation of educational materials and providing a platform for students and courses.

## Project structure

- authentication/ - User authentication module.
- chatai/ - Chat with artificial intelligence (possibly integrating AI for learning assistance).
- config/ - Project configuration files.
- course/ - Course management.
- eduagent/ - Educational agent logic (possibly AI tutor).
- student/ - Student data management.
- media/ - Media files (images, uploads).
- templates/ - Django HTML templates.
- bot.py - Main Telegram bot file.
- Content generation scripts:
    - create_eduplay_content.py
    - create_eduplay_exercises.py
    - create_exercises.py
    - create_math_exercises.py
    - random_examples_generator.py
    - random_examples.json (sample data)
- manage.py - Django's standard management script.
- db.sqlite3 - SQLite database (for development).
- requirements.txt - Python dependencies.
- Documents:
    - API_DOCUMENTATION.md - API description.
    - TELEGRAM_AUTH_GUIDE.md - Telegram authentication guide.

## Installation and launch

1. **Clone the repository:**

```bash
git clone https://github.com/xusanboyf32/edu_loyiha.git
cd edu_loyiha
```

  2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate (Windows: .vevn/Scripts/activate)
```

  3. Install dependencies

```bash
pip install -r requirements.txt
```

  **4. Apply the database migrations:**

```bash
python manage.py migrate
```

    5. Create a superuser (optional for the admin area):

```bash
python manage.py createsuperuser
```

    6.  Start the development server:

```bash
python manage.py runserver
```

Will be available at http://127.0.0.1:8000/

     7. Launch Telegram bot:

- Configure the bot token in the code (see TELEGRAM_AUTH_GUIDE.md).
- Launch

```bash
python bot.py
```

## Content generation

The project includes scripts to create learning content:

- python create_math_exercises.py - Generate math exercises.
- python create_exercises.py - Generic exercises.
- Similarly for EduPlay content.

These scripts are useful for automatically populating the database with courses and tasks.

## API

A detailed description of the endpoints API is available in the API_DOCUMENTATION.md file.

## Telegram integration

Guidelines for authentication and bot setup are in TELEGRAM_AUTH_GUIDE.md.

## Development and contribution

The project is open under an MIT license. You can fork the repository and send Pull Requests.

**Recommendations:**

- Don't commit db.sqlite3 in production (use PostgreSQL or another database).
- Add .env for secrets (bot tokens, etc).

If you have questions or suggestions - create an Issue in the repository!