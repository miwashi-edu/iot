import typer
import sys
import socket
import subprocess
import ipaddress

app = typer.Typer(no_args_is_help=True)

@app.command()
def scan(netmask: str = typer.Argument(..., help="Netmask to scan (e.g., 192.168.1.0/24)")):
    """Scan the network for active IP addresses using the provided netmask."""
    print(f"Scanning network: {netmask}...")
    
    try:
        network = ipaddress.ip_network(netmask, strict=False)
    except ValueError as e:
        print(f"Error: Invalid netmask '{netmask}'. {e}")
        raise typer.Exit(code=1)

    # Simple ping sweep for the entire network
    # Note: On MacOS, -t 1 is 1 second timeout. -c 1 is 1 packet.
    # We scan all addresses in the network including network and broadcast
    # because the user might want to scan a specific IP or a very small range.
    try:
        for ip in network:
            ip_str = str(ip)
            # Using ping -c 1 -t 1 ip
            try:
                result = subprocess.run(
                    ["ping", "-n", "-c", "1", "-W", "3", ip_str],
                    capture_output=True,
                    text=True,
                    timeout=3,
                )
                if result.returncode == 0:
                    print(ip_str)
                else:
                    error_msg = result.stderr.strip()
                    output = f"{ip_str} (error: {error_msg})" if error_msg else ip_str
                    typer.secho(output, fg=typer.colors.RED, err=True)
            except (subprocess.TimeoutExpired, KeyboardInterrupt):
                raise
    except KeyboardInterrupt:
        print("\nScan interrupted by user. Exiting...")
        raise typer.Exit(code=0)

@app.command()
def other():
    """Dummy command to avoid command name being collapsed."""
    pass

if __name__ == "__main__":
    app()
