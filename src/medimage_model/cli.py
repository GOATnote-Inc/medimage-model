"""Command-line entry point: medimage-model <command>."""

from __future__ import annotations

import click

import medimage_model


@click.group()
@click.version_option(medimage_model.__version__, prog_name="medimage-model")
def main() -> None:
    """medimage-model — open commercial-OK brain-MR multimodal reasoning model."""


@main.command()
def smoke() -> None:
    """Verify the package imports and primitives are reachable."""
    click.echo(f"medimage-model {medimage_model.__version__} OK")


if __name__ == "__main__":
    main()
