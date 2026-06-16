import click
import os


@click.group()
def cli():
    pass


@cli.command()
def migrate():
    """Run latest migrations"""
    os.system("alembic upgrade head")


@cli.command()
def rollback():
    """Rollback one migration"""
    os.system("alembic downgrade -1")


@cli.command()
def seed():
    """Seed database"""
    os.system("python seed.py")


@cli.command()
def reset():
    """Reset database"""

    os.system("alembic downgrade base")
    os.system("alembic upgrade head")
    os.system("python seed.py")


if __name__ == "__main__":
    cli()