# Task Tracker

A Django project for tracking work. It has Users, Projects, Tasks and Comments,
and a Django REST Framework API with full CRUD for Tasks.

## Models
- `Project` - name, summary, owner
- `Task` - title, details, project, assignee, status, priority, due date
- `Comment` - text written by a user on a task

## API (Django REST Framework)
Base URL: `/api/tasks/`

| Method | URL | What it does |
|---|---|---|
| GET | `/api/tasks/` | list tasks (filters: `?project=1&status=TODO&priority=HIGH&search=text`) |
| POST | `/api/tasks/` | create a task |
| GET | `/api/tasks/<id>/` | read one task |
| PUT / PATCH | `/api/tasks/<id>/` | update a task |
| DELETE | `/api/tasks/<id>/` | delete a task |
| POST | `/api/tasks/<id>/complete/` | mark a task as done |

## Admin
Tasks can be searched by title and filtered by project, status and priority.

## Run it
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py test
python manage.py createsuperuser
python manage.py runserver
```
Then open http://127.0.0.1:8000/api/tasks/ and http://127.0.0.1:8000/admin/
