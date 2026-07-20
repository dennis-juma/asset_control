# Asset Management System Architecture

## Overview

The Asset Management System is an enterprise-grade web application developed using Django.

The system manages the complete lifecycle of organizational assets including:

- Registration
- Assignment
- Movement
- Maintenance
- Disposal
- Reporting

---

## Technology Stack

Backend
- Python 3.12+
- Django 5.x
- Django REST Framework

Database
- PostgreSQL

Frontend
- Bootstrap 5
- HTML5
- JavaScript

Authentication
- Custom Django User Model

Storage
- Local Media
- AWS S3 (Future)

---

## Application Architecture

The project follows a modular architecture.

accounts/
organizations/
sites/
departments/
job_titles/
employees/
vendors/
assets/
assignments/
maintenance/
reports/
dashboard/
api/

Each application owns its own:

- Models
- Admin
- Forms
- Views
- URLs
- Tests
- Services

---

## Core Design Principles

- UUID primary keys
- Soft Delete
- Audit Trail
- Active/Inactive records
- Slug support
- Service Layer
- Clean Architecture
- PostgreSQL optimized