from typing import Optional

import os
import uvicorn
import typer
import alembic.config

# it is required for uvicorn to run this app
from web.settings import DEBUG, PORT
from web.app import app  # noqa


cli = typer.Typer()


@cli.command()
def runserver() -> None:
    log_level = "debug" if DEBUG else "info"
    uvicorn.run("manage:app", port=PORT, log_level=log_level)


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
    os.system("python admin/manage.py runserver --noreload")


if __name__ == "__main__":
    cli()
