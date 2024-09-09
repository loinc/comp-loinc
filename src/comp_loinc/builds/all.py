"""Wrapper CLI to create all artefacts at once."""
import typer

from comp_loinc.cli import comploinc_file_cli_all


cli = typer.Typer()


@cli.command()
def main(fast_run: bool = typer.Option(False, "--fast-run", help="Files will be created with only 100 entries each.")):
    """Wrapper CLI to create all artefacts at once."""
    comploinc_file_cli_all(fast_run)


if __name__ == "__main__":
    cli()
