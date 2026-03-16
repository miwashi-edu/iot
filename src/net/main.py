import sys
import subprocess
import ipaddress
import typer

app = typer.Typer(no_args_is_help=True)


@app.command()
def scan(
    netmask: str = typer.Argument(
        ..., help="Network to scan, e.g. 192.168.1.0/24"
    )
):
    """Scan a network and print responsive IPs to stdout."""
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
            else:
                print(ip_str, file=sys.stderr, flush=True)

    except KeyboardInterrupt:
        print("\nScan interrupted.", flush=True)
        raise typer.Exit(code=0)


@app.command()
def other():
    """Dummy command."""
    pass


if __name__ == "__main__":
    app()
