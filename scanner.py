import socket
import threading
import ipaddress
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

open_ports = []
lock = threading.Lock()

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 135: "RPC",
    139: "NetBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    3306: "MySQL", 3389: "RDP", 5900: "VNC", 8080: "HTTP-Alt",
    8443: "HTTPS-Alt", 27017: "MongoDB", 5432: "PostgreSQL", 6379: "Redis"
}

def print_banner():
    print(Fore.CYAN + "=" * 60)
    print(Fore.CYAN + "        PROFESSIONAL PORT SCANNER")
    print(Fore.CYAN + "        By: Pujan Rasaili | Bedfordshire University")
    print(Fore.CYAN + "=" * 60)

def scan_port(host, port, timeout):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        if result == 0:
            service = COMMON_PORTS.get(port, "Unknown")
            with lock:
                open_ports.append((port, service))
                print(Fore.GREEN + f"  [OPEN]  Port {port:<6} | Service: {service}")
        sock.close()
    except (socket.error, OSError):
        pass

def validate_host(host):
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        try:
            socket.gethostbyname(host)
            return True
        except socket.gaierror:
            return False

def get_scan_range():
    print(Fore.YELLOW + "\nSelect scan type:")
    print("  [1] Quick Scan   (Top 20 common ports)")
    print("  [2] Standard Scan (Ports 1-1024)")
    print("  [3] Full Scan     (Ports 1-65535)")
    print("  [4] Custom Range")

    choice = input(Fore.WHITE + "\nEnter choice (1-4): ").strip()

    if choice == "1":
        return list(COMMON_PORTS.keys()), "Quick"
    elif choice == "2":
        return range(1, 1025), "Standard"
    elif choice == "3":
        return range(1, 65536), "Full"
    elif choice == "4":
        start = int(input("Start port: "))
        end = int(input("End port: "))
        return range(start, end + 1), "Custom"
    else:
        print(Fore.RED + "Invalid choice. Using Quick Scan.")
        return list(COMMON_PORTS.keys()), "Quick"

def save_results(host, scan_type):
    filename = f"scan_{host}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w") as f:
        f.write(f"Port Scan Report\n")
        f.write(f"{'='*40}\n")
        f.write(f"Target : {host}\n")
        f.write(f"Type   : {scan_type}\n")
        f.write(f"Date   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*40}\n\n")
        if open_ports:
            for port, service in sorted(open_ports):
                f.write(f"[OPEN] Port {port} - {service}\n")
        else:
            f.write("No open ports found.\n")
    print(Fore.YELLOW + f"\n  Results saved to: {filename}")

def start_scan():
    print_banner()

    host = input(Fore.WHITE + "\nEnter target IP or hostname: ").strip()

    if not validate_host(host):
        print(Fore.RED + "Invalid host. Please enter a valid IP or hostname.")
        return

    try:
        resolved_ip = socket.gethostbyname(host)
    except socket.gaierror:
        resolved_ip = host

    ports, scan_type = get_scan_range()
    timeout = 0.5

    print(Fore.CYAN + f"\n  Target   : {host} ({resolved_ip})")
    print(Fore.CYAN + f"  Scan Type: {scan_type}")
    print(Fore.CYAN + f"  Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(Fore.CYAN + "-" * 60)
    print(Fore.WHITE + "\n  Scanning...\n")

    start_time = datetime.now()
    threads = []

    for port in ports:
        t = threading.Thread(target=scan_port, args=(resolved_ip, port, timeout))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    duration = (datetime.now() - start_time).seconds

    print(Fore.CYAN + "\n" + "-" * 60)
    print(Fore.CYAN + f"  Scan Complete!")
    print(Fore.CYAN + f"  Open ports found : {len(open_ports)}")
    print(Fore.CYAN + f"  Duration         : {duration}s")
    print(Fore.CYAN + "=" * 60)

    save = input(Fore.YELLOW + "\nSave results to file? (y/n): ").strip().lower()
    if save == "y":
        save_results(host, scan_type)

if __name__ == "__main__":
    start_scan()