# Business Rules

## Company

- Every Country belongs to one Company.
- Every Department belongs to one Company.
- Every Job Title belongs to one Company.

## Department

- Department names must be unique within a company.
- Departments may have a parent department.
- Parent department must belong to the same company.

## Employee

- Employee ID is supplied by HR.
- Employee IDs are unique.
- Employees may exist without a User account.
- An Employee cannot be their own Manager.
- Department must belong to Employee Company.
- Job Title must belong to Employee Company.
- Site must belong to Employee Company.

## Assets

(Coming Soon)