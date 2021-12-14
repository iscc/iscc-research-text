# -*- coding: utf-8 -*-
from itext import __version__
import click
from click_default_group import DefaultGroup
from loguru import logger as log


@click.group(cls=DefaultGroup, default="run", default_if_no_args=False)
@click.version_option(version=__version__, message="ISCC TEXT RESEARCH - %(version)s")
def cli():
    pass


@click.command()
def run():
    log.info("Hello ISCC Text Reserch")


cli.add_command(run)


if __name__ == "__main__":
    cli()
