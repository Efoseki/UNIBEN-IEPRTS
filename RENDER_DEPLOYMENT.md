# UNIBEN IEPRTS — Render Deployment

## Important
This package is intentionally flattened so that `render.yaml` is at the **root of the repository**. Render Blueprints look for `render.yaml` at the repository root unless a different Blueprint path is explicitly configured.

## Recommended method
1. Create a GitHub repository, e.g. `uniben-ieprts`.
2. Put the **contents of this folder directly in the repository root**. Do not put the whole `UNIBEN_IEPRTS_Render_Fixed` folder inside another folder.
3. Commit and push to the `main` branch.
4. In Render, choose **New → Blueprint**.
5. Connect the GitHub repository and select the `main` branch.
6. Render should detect `/render.yaml` automatically.
7. Review the web service and PostgreSQL database, then deploy the Blueprint.

## If you are creating a Web Service manually
Use:

**Root Directory:** leave blank (repository root)

**Build Command:**
```text
pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate && python manage.py seed_prs
```

**Start Command:**
```text
gunicorn problem_reporting.wsgi:application
```

Set:
- `SECRET_KEY` = a generated secret
- `DEBUG` = `False`
- `DATABASE_URL` = your Render PostgreSQL internal connection string
- `CSRF_TRUSTED_ORIGINS` = your actual HTTPS Render URL, e.g. `https://your-service-name.onrender.com`

## After the first successful deployment
Open the Render Shell and run:
```text
python manage.py createsuperuser
```

Then use:
```text
/admin/
```

## If Render says `render.yaml not found`
Check that the file is actually at the repository root and that you selected the branch containing it. Render's default Blueprint path is `render.yaml` at the repository root.
