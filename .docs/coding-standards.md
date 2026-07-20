# Coding Standards

## Python

- Follow PEP 8
- Use Black formatting
- Type hints where appropriate

## Django

One app per business domain.

Every app contains

models/
admin/
migrations/
tests/

Model files are separated by entity.

Example

models/
    employee.py
    choices.py

Never place multiple large models in one file.

## Models

Use BaseModel for all business entities.

Never duplicate business logic.

Use:

clean()

for validation.

Use:

save()

only when necessary.

## Naming

Class

Employee

Table

employees_employee

Foreign Keys

employee

department

site

Never use abbreviations.