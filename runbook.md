# Database Migration Runbook

## Project

Week 8 - Database Migrations with Alembic, PostgreSQL, SQLAlchemy, Pytest

---

# 1. Migration Workflow

## Create Migration

```bash
alembic revision --autogenerate -m "message"
```

Example:

```bash
alembic revision --autogenerate -m "create posts table"
```

---

## Apply Migration

```bash
alembic upgrade head
```

Applies all pending migrations.

---

## Rollback Last Migration

```bash
alembic downgrade -1
```

Reverts the most recent migration.

---

## Rollback to Base

```bash
alembic downgrade base
```

Removes all migrations.

---

## Check Current Revision

```bash
alembic current
```

---

## View Migration History

```bash
alembic history
```

---

# 2. Migration Rules

## Always Write downgrade()

Every migration must contain:

```python
def upgrade():
    pass

def downgrade():
    pass
```

If upgrade adds something, downgrade must remove it.

---

## Safe Operations

### Create Table

```python
op.create_table(...)
```

### Add Column

```python
op.add_column(...)
```

### Create Index

```python
op.create_index(...)
```

### Add Nullable Column

```python
op.add_column(
    "users",
    sa.Column("phone", sa.String(), nullable=True)
)
```

Preferred for production systems.

---

## Risky Operations

### Drop Column

```python
op.drop_column(...)
```

May cause data loss.

### Drop Table

```python
op.drop_table(...)
```

Removes all data.

### Change Data Type

```python
Integer -> String
```

Requires validation.

---

# 3. Zero-Downtime Migration Rules

## Safe

```python
op.add_column(
    "users",
    sa.Column("phone", sa.String(), nullable=True)
)
```

## Unsafe

```python
op.add_column(
    "users",
    sa.Column("phone", sa.String(), nullable=False)
)
```

Existing rows may fail validation.

---

## Expand / Contract Pattern

### Expand

Add new column.

### Migrate Data

Move existing values.

### Contract

Remove old column.

---

# 4. Database Backup

## Create Backup

```bash
pg_dump -U postgres -f backup.sql user_analytics_db
```

---

## Restore Backup

```bash
psql -U postgres -d user_analytics_clone -f backup.sql
```

---

# 5. Database Cloning

## Create Clone Database

```sql
CREATE DATABASE user_analytics_clone;
```

---

## Restore Backup

```bash
psql -U postgres -d user_analytics_clone -f backup.sql
```

---

## Verify

```sql
SELECT * FROM users;
SELECT * FROM posts;
```

---

# 6. Database Seeding

## Install Faker

```bash
pip install faker
```

---

## Run Seed Script

```bash
python seed.py
```

---

## Idempotent Seeding Rule

Always check existing data before inserting.

Example:

```python
if db.query(User).count() == 0:
    # insert users
```

Prevents duplicate records.

---

# 7. DB Manager Commands

## Migrate

```bash
python db_manager.py migrate
```

Runs:

```bash
alembic upgrade head
```

---

## Rollback

```bash
python db_manager.py rollback
```

Runs:

```bash
alembic downgrade -1
```

---

## Seed

```bash
python db_manager.py seed
```

Runs:

```bash
python seed.py
```

---

## Reset

```bash
python db_manager.py reset
```

Runs:

```bash
alembic downgrade base
alembic upgrade head
python seed.py
```

Development only.

---

# 8. Environment Rules

## Development

Allowed:

```bash
python db_manager.py reset
```

```bash
alembic downgrade base
```

```bash
alembic upgrade head
```

---

## Staging

Workflow:

```text
Production Backup
      ↓
Restore Clone
      ↓
Run Migration
      ↓
Validate
```

No reset operations.

---

## Production

Rules:

* Always backup first
* Test in staging first
* Only run upgrade
* Never run reset
* Never delete production data manually

Allowed:

```bash
alembic upgrade head
```

Not Allowed:

```bash
alembic downgrade base
```

```bash
python db_manager.py reset
```

---

# 9. Production Migration Runbook

## Step 1

Review migration code.

---

## Step 2

Create backup.

```bash
pg_dump -U postgres -f prod_backup.sql production_db
```

---

## Step 3

Validate migration in staging.

---

## Step 4

Run migration.

```bash
alembic upgrade head
```

---

## Step 5

Verify schema.

```sql
SELECT * FROM users;
```

---

## Step 6

Verify application functionality.

---

## Step 7

Monitor logs and errors.

---

# 10. Migration Testing

## Run Tests

```bash
python -m pytest
```

---

## Migration Test Checklist

* Upgrade succeeds
* Tables created
* Downgrade succeeds
* Tables removed
* No migration errors

---

# 11. Commands Summary

```bash
alembic revision --autogenerate -m "message"

alembic upgrade head

alembic downgrade -1

alembic downgrade base

alembic current

alembic history

python seed.py

python db_manager.py migrate

python db_manager.py rollback

python db_manager.py seed

python db_manager.py reset

python -m pytest
```

---

