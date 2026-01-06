# LinkedIn-style Django Demo App

Simple LinkedIn-style social network built with Django.  
Features basic authentication, user profiles, posts, following, and private messaging with a clean UI and Persian-friendly content.

## Features

- Email-based sign up and login
- User profiles with avatar, headline, bio
- Default avatar when no image is uploaded
- Home feed with posts from you and people you follow
- Create, edit, and delete your own posts (from feed and profile)
- Follow/unfollow other users
- Followers and following lists from profile
- Private messaging between two users
  - Conversations list with last message preview
  - Message bubbles (you on the right, other on the left)
  - Auto-refresh of messages via AJAX
- User search (name, email, headline)
- Basic RTL support for Persian text: posts, messages, and previews
- Seed command to generate Persian demo data

## Requirements

- Python 3.10+ (project currently uses a virtualenv)
- SQLite (default Django DB)

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the project

From the project root:

```bash
python manage.py migrate
python manage.py runserver
```

The app will be available at:

http://127.0.0.1:8000/

## Demo data (Persian users, posts, relations)

There is a management command that seeds Persian demo data:

```bash
python manage.py seed_persian_data
```

This will:

- Clear existing users, profiles, posts, follows, conversations, messages
- Create 10 Persian users:
  - Emails: `user1@user.com` ... `user10@user.com`
  - Password (all): `1234`
- Create multiple posts for each user
- Add random follow relations between users
- Create random conversations and Persian messages

After seeding you can log in, for example:

- Email: `user1@user.com`
- Password: `1234`

## Running tests

Run the Django test suite:

```bash
python manage.py test
```

