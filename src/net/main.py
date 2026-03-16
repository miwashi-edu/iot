import sys
import subprocess
import ipaddress
import typer

app = typer.Typer(add_completion=False)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    netmask: str = typer.Argument(None, help="Network to scan, e.g. 192.168.0.0/24"),
):
    if ctx.invoked_subcommand is not None:
        return

    if not netmask:
        print("Missing network argument", file=sys.stderr, flush=True)
        raise typer.Exit(code=1)

    print(f"Scanning network: {netmask}...", flush=True)

    try:
        network = ipaddress.ip_network(netmask, strict=False)
    except ValueError as e:
        print(f"Error: invalid network '{netmask}': {e}", file=sys.stderr, flush=True)
        raise typer.Exit(code=1)

    try:
        for ip in network.hosts():
            ip_str = str(ip)

            result = subprocess.run(
                ["ping", "-n", "-c", "1", "-W", "1", ip_str],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            if result.returncode == 0:
                print(ip_str, flush=True)

    except KeyboardInterrupt:
        print("\nScan interrupted.", flush=True)
        raise typer.Exit(code=0)


if __name__ == "__main__":
    app()
