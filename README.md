# Professional Port Scanner

A fast, multi-threaded port scanner built with Python.
Detects open ports, identifies services, and saves scan reports.

## Author
**Pujan Rasaili** | BSc Software Engineering | University of Bedfordshire

## Features
- Multi-threaded scanning for fast results
- 4 scan modes: Quick, Standard, Full, Custom
- Identifies 20+ common services (HTTP, SSH, FTP, MySQL etc.)
- Color-coded terminal output
- Saves scan reports to text file
- Input validation for hostnames and IPs

## Technologies Used
- Python 3.13
- Socket programming
- Threading
- Colorama

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python scanner.py
```

## Scan Modes
| Mode | Ports Scanned |
|------|--------------|
| Quick | Top 20 common ports |
| Standard | Ports 1-1024 |
| Full | Ports 1-65535 |
| Custom | Your chosen range |

## Output
Scan reports saved as `scan_<host>_<timestamp>.txt`
