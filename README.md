# HOMIESX

Frontend foundation for the college-independent HOMIESX ecosystem.

## Run the Django server and admin panel

The original static prototype can still be viewed with Live Server. The database-backed site requires Python 3.11+ and Django.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo_content
python manage.py runserver
```

### Enable GitHub student login

Create a GitHub OAuth App at **Settings → Developer settings → OAuth Apps**. Set its callback URL to:

`http://127.0.0.1:8000/student/oauth/github/callback/`

Copy the app's Client ID and Client Secret into your environment as `SOCIAL_AUTH_GITHUB_CLIENT_ID` and `SOCIAL_AUTH_GITHUB_CLIENT_SECRET`, then restart `runserver`. Keep the secret out of source control. Google login uses the same pattern with callback URL `http://127.0.0.1:8000/student/oauth/google/callback/`.

Email/password student login works without social credentials at `/student/login/`.

Open `http://127.0.0.1:8000/` for the Django site and `http://127.0.0.1:8000/admin/` to manage its content. Add one **Site settings** record to control the home page, then create and publish resources, events, opportunities, and projects.

`seed_demo_content` creates only clearly labelled local demo records. It is optional and does not add fake production data.

For production, set `DJANGO_SECRET_KEY` using environment configuration and set `DEBUG = False` / configure `ALLOWED_HOSTS` before deployment.

## Current scope

The landing page, responsive shared navigation, theme preference, student authentication, OAuth entry points, protected Django admin panel, and database-backed public content routes are implemented. GitHub and Google login require provider credentials configured by the site administrator.
