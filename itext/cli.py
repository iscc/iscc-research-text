# -*- coding: utf-8 -*-
from codetiming import Timer
from itext import __version__
from itext import lib
import click
from loguru import logger as log


@click.group()
@click.version_option(version=__version__, message="ISCC TEXT RESEARCH - %(version)s")
def cli():
    pass


@click.command()
@click.option(
    "-n",
    "--nth",
    default=100000,
    show_default=True,
    help="Log measurement every n-th entry",
)
def read(nth):
    """Measure time to read and deserialize unpaywall dataset."""
    log.info("Measuring Unpaywall data read time.")
    pos = 0
    t = Timer("unpaywall", logger=None)
    t.start()
    for entry in lib.reader():
        pos += 1
        if not pos % nth:
            t.stop()
            rps = nth / Timer.timers.mean("unpaywall")
            tt = t.timers.total("unpaywall")
            log.info(f"{int(rps)} entries per second ({pos} read in {tt:.2f} seconds)")
            t.start()
    t.stop()
    tt = t.timers.total("unpaywall")
    log.info(f"{pos} total entries processed in {tt:.2f} seconds)")


cli.add_command(read)


if __name__ == "__main__":
    cli()
