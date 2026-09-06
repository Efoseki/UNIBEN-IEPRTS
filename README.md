# UNIBEN Infrastructure and Environmental Problem Reporting and Tracking System (IEPRTS)

A deployment-ready Django application for the University of Benin that supports end-to-end reporting, assignment, response and tracking of campus infrastructure and environmental problems.

## Core functions
- User registration, login and reporting dashboard
- Infrastructure and environmental category hierarchy
- Problem description, location, severity, optional GPS coordinates and multiple photographs
- Unique tracking reference numbers in the format `UNIBEN-IEPRTS-YYYYMMDD-XXXXXX`
- Public tracking page with status/action timeline
- Authorized problem-management list with search and filtering
- Selective processing of each reported problem
- Department/officer assignment, expected resolution date and resolution summary
- Status workflow: Submitted → Under Review → Assigned → In Progress → Resolved → Closed
- Reporter notifications stored in the application
- Enhanced Django administration
- PostgreSQL/Render and WhiteNoise configuration

## Local setup
1. `python -m venv venv`
2. Activate the environment.
3. `pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py seed_prs`
6. `python manage.py createsuperuser`
7. `python manage.py runserver`

## Authorized report managers
Django superusers and staff can manage all reports. Application users with Profile roles `officer`, `management` or `admin` can also access the report-processing interfaces; officers can be restricted to their assigned department/reports.

## Render deployment
Use `render.yaml` or configure the web service manually. Required production environment values include `SECRET_KEY`, `DEBUG=False` and the PostgreSQL `DATABASE_URL`. Also set `CSRF_TRUSTED_ORIGINS` to the deployed HTTPS origin if needed.

### User-uploaded photographs
Render web-service filesystems are ephemeral. For durable production image storage, configure a persistent disk or an external object-storage service (for example Cloudinary or S3-compatible storage). Local development continues to use `MEDIA_ROOT`.

## Render note
The deployment package includes a root-level `render.yaml`. If Render reports that `render.yaml` cannot be found, make sure the repository contains the contents of this package at its root rather than nesting them inside another directory, or explicitly set the Blueprint path in Render.
