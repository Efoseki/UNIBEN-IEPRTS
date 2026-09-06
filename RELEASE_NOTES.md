# UNIBEN IEPRTS — Updated Release

Official project title implemented throughout the application:

**UNIBEN Infrastructure and Environmental Problem Reporting and Tracking System**

Short system label used in compact interface areas: **UNIBEN IEPRTS**.

## Major updates in this release
- Rebranded the navigation, page titles, footer, login/registration screens, tracking interface and administration area.
- Replaced “Infrastructural” with “Infrastructure” in the main classification and included a migration to normalize existing data.
- Updated newly generated tracking references to `UNIBEN-IEPRTS-YYYYMMDD-XXXXXX` while leaving existing historical references valid.
- Added a redesigned UNIBEN-themed hero graphic emphasizing reporting and tracking.
- Added dedicated account registration.
- Rebuilt the problem-report form with category-dependent fields, photo evidence, severity, campus location and optional browser geolocation.
- Fixed the submission redirect so a new report opens directly on its tracking page.
- Added role-aware operational dashboards.
- Added an authorized **Manage Reports** interface with search and status/category filters.
- Added selective processing of individual reported problems, including department assignment, officer assignment, status updates, response/action notes, expected resolution date and resolution summary.
- Added a visible tracking-history timeline for reporters and the public tracking screen.
- Enhanced Django Admin for searching, filtering and processing reports.
- Added reporter notification records when a report is submitted or updated.
- Updated Render service/database names and deployment documentation.

## Status workflow
Submitted → Under Review → Assigned → In Progress → Resolved → Closed

A report may also be marked Rejected when appropriate.

## Important production-media note
The application supports multiple uploaded photographs. Render's default web-service filesystem is ephemeral, so production deployments that need durable uploaded photos should use persistent disk or an external object-storage provider.


## Anonymous reporting update
- Problem reporting no longer requires authentication.
- Unauthenticated submissions are automatically anonymous.
- Authenticated users may choose anonymous reporting.
- Anonymous reporters receive a unique reference and use the public tracking page to follow progress.
- Notifications and account-linked dashboard history are retained only for identified authenticated submissions.
