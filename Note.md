# Database Migrations with Alembic

## Objective

Learn database migration concepts, Alembic workflow, rollback operations, migration file structure, and production migration practices.

---

# Why Migrations Exist

Database migrations provide a version-controlled way to manage database schema changes.

## Benefits

* Track schema changes over time
* Maintain consistency across environments
* Support rollback functionality
* Improve team collaboration
* Enable automated deployments

## Key Concepts

### Migration

A database schema change stored as code.

### Revision

Unique identifier assigned to each migration.

### Base

Initial state of the migration history.

### Head

Latest migration version.

---

# Alembic Setup

## Install Alembic

```bash
pip install alembic
```

## Initialize Alembic

```bash
alembic init migrations
```

Generated structure:

```text
project/
│
├── alembic.ini
├── migrations/
│   ├── env.py
│   └── versions/
```

---

# Alembic Configuration

Configure database URL inside `alembic.ini`.

```ini
sqlalchemy.url = postgresql://username:password@localhost:5432/database_name
```

Configure metadata inside `env.py`.

```python
target_metadata = Base.metadata
```

---

# Creating Migrations

## Generate Migration

```bash
alembic revision --autogenerate -m "create users table"
```

## Apply Migration

```bash
alembic upgrade head
```

## Rollback Migration

```bash
alembic downgrade -1
```

---

# Migration File Anatomy

Example:

```python
from alembic import op
import sqlalchemy as sa

revision = "123abc"
down_revision = "456xyz"

def upgrade():
    pass

def downgrade():
    pass
```

## upgrade()

Contains changes that should be applied to the database.

Example:

```python
def upgrade():
    op.add_column(
        "users",
        sa.Column("phone_number", sa.String(20))
    )
```

## downgrade()

Contains reverse operations used during rollback.

Example:

```python
def downgrade():
    op.drop_column("users", "phone_number")
```

---

# Common Alembic Operations

## Create Table

```python
op.create_table()
```

## Add Column

```python
op.add_column()
```

## Drop Column

```python
op.drop_column()
```

## Alter Column

```python
op.alter_column()
```

## Create Index

```python
op.create_index()
```

## Drop Index

```python
op.drop_index()
```

---

# Migration Tracking Commands

## Current Migration

```bash
alembic current
```

Shows the migration version currently applied to the database.

## Migration History

```bash
alembic history
```

Displays all migrations and revision history.

---

# Rollback

Rollback last migration:

```bash
alembic downgrade -1
```

Rollback multiple migrations:

```bash
alembic downgrade -2
```

Reapply latest migration:

```bash
alembic upgrade head
```

---

# Zero-Downtime Migrations

A zero-downtime migration allows schema changes without interrupting application availability.

## Safe Migration

Add nullable column:

```python
op.add_column(
    "users",
    sa.Column(
        "phone_number",
        sa.String(20),
        nullable=True
    )
)
```

Reason:

* Existing records can store NULL values.
* No migration failure.

## Unsafe Migration

```python
op.add_column(
    "users",
    sa.Column(
        "phone_number",
        sa.String(20),
        nullable=False
    )
)
```

Reason:

* Existing rows do not contain values.
* Migration may fail.

---

# Expand/Contract Pattern

Production-safe migration strategy.

## Step 1 - Expand

Add nullable column.

```python
nullable=True
```

## Step 2 - Backfill Data

Populate existing records.

```sql
UPDATE users
SET phone_number = 'N/A'
WHERE phone_number IS NULL;
```

## Step 3 - Contract

Make column non-nullable.

```python
op.alter_column(
    "users",
    "phone_number",
    nullable=False
)
```

---

# Other Migration Tools

## Flyway

* SQL-based migrations
* Manual SQL scripts
* Popular in Java ecosystem

## Liquibase

* XML, YAML, JSON, SQL migrations
* Enterprise-grade migration tool

## Django Migrations

* Built into Django ORM
* Auto-generates migration files

## Knex.js

* Migration tool for Node.js
* JavaScript-based migrations

---

# Auto-Generated vs Manual Migrations

## Auto-Generated

Examples:

* Alembic
* Django Migrations

Advantages:

* Faster development
* Less manual effort
* Reduced human error

## Manual SQL

Examples:

* Flyway
* Liquibase

Advantages:

* Full SQL control
* Better for complex production changes

---

# Best Practices

* Always review generated migrations.
* Always write a downgrade function.
* Keep migrations small and focused.
* Test upgrades and downgrades.
* Backup production databases before migration.
* Test migrations in staging before production deployment.

---

# Practical Work Completed

* Alembic installation and setup
* Database configuration
* Migration creation
* Migration execution
* Rollback execution
* Migration history verification
* Current revision verification
* Migration file anatomy study
* Production migration concepts
* Overview of Flyway, Liquibase, Django Migrations, and Knex.js
