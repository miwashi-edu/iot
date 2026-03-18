import typer

app = typer.Typer(no_args_is_help=True)


@app.command()
def greet(
    name: str = typer.Argument("World", help="Name to greet"),
) -> None:
    """Greet someone by name."""
    typer.echo(f"Hello, {name}!")


@app.command()
def version() -> None:
    """Show the current version."""
    typer.echo("iot version 0.2.0")


@app.command()
def hello() -> None:
    """Print a basic hello message."""
    typer.echo("Hello from iot!")


def main() -> None:
    app()


if __name__ == "__main__":
    main()