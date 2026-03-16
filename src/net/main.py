import sys
import shutil
import subprocess
import ipaddress
import typer

app = typer.Typer(no_args_is_help=True)


@app.command()
def scan(netmask: str = typer.Argument(..., help="Network to scan, e.g. 192.168.0.0/24")):
    print("starting", flush=True)
    print(f"python={sys.executable}", flush=True)
    print(f"ping={shutil.which('ping')}", flush=True)
    print(f"arg={netmask}", flush=True)

    try:
        network = ipaddress.ip_network(netmask, strict=False)
    except ValueError as e:
        print(f"invalid network: {e}", file=sys.stderr, flush=True)
        raise typer.Exit(code=1)

    print(f"scanning {network}", flush=True)

    for ip in network.hosts():
        ip_str = str(ip)
        print(f"trying {ip_str}", flush=True)

        try:
            result = subprocess.run(
                ["ping", "-n", "-c", "1", "-W", "1", ip_str],
                capture_output=True,
                text=True,
                timeout=3,
            )
        except Exception as e:
            print(f"{ip_str} exception: {e}", file=sys.stderr, flush=True)
            continue

        print(
            f"{ip_str} rc={result.returncode} stdout={result.stdout!r} stderr={result.stderr!r}",
            flush=True,
        )

        if result.returncode == 0:
            print(f"UP {ip_str}", flush=True)


if __name__ == "__main__":
    app()
