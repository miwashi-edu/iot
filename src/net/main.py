import sys
import subprocess
import ipaddress
import typer

app = typer.Typer(no_args_is_help=True)


@app.command()
def scan(
    netmask: str = typer.Argument(..., help="Network to scan, e.g. 192.168.1.0/24")
):
    print(f"Scanning network: {netmask}...", flush=True)

    try:
        network = ipaddress.ip_network(netmask, strict=False)
    except ValueError as e:
        print(f"Invalid network: {e}", file=sys.stderr, flush=True)
        raise typer.Exit(1)

    for ip in network.hosts():
        ip_str = str(ip)
        print(f"trying {ip_str}", flush=True)

        try:
            result = subprocess.run(
                ["ping", "-n", "-c", "1", "-w", "1", ip_str],
                capture_output=True,
                text=True,
                timeout=2,
            )
        except Exception as e:
            print(f"{ip_str} EXCEPTION: {e}", file=sys.stderr, flush=True)
            continue

        print(
            f"{ip_str} rc={result.returncode} "
            f"stdout={result.stdout!r} stderr={result.stderr!r}",
            flush=True,
        )

        if result.returncode == 0:
            print(f"UP {ip_str}", flush=True)


if __name__ == "__main__":
    app()
