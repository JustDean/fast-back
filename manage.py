from typing import Optional

import uvicorn
import typer
import alembic.config
from os import environ, system

# it is required for uvicorn to run this app
from web.app import app  # noqa


cli = typer.Typer()


@cli.command()
def runserver() -> None:
    port = int(environ.get("PORT", 8080))
    log_level = environ.get("LOG_LEVEL", "debug")
    uvicorn.run("manage:app", port=port, log_level=log_level)


@cli.command()
def makemigrations(migrate_msg: Optional[str] = typer.Argument(None)) -> None:
    alembicArgs = ["revision", "--autogenerate"]
    if migrate_msg:
        alembicArgs = [*alembicArgs, "-m", migrate_msg]
    alembic.config.main(argv=alembicArgs)


@cli.command()
def migrate(commit: Optional[str] = typer.Argument(None)) -> None:
    alembicArgs = ["upgrade", "head"]
    if commit:
        alembicArgs = ["downgrade", commit]
    alembic.config.main(argv=alembicArgs)


@cli.command()
def admin() -> None:
    system("python admin/manage.py runserver --noreload")


if __name__ == "__main__":
    cli()
