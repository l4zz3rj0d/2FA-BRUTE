## What this script does

This script brute-forces a 4-digit password recovery code on a vulnerable password reset endpoint and identifies the valid code by analyzing server responses.


## What YOU need to change

Edit only these fields:
```
url = "<reset-password-url>"
```
Replace with the password reset endpoint

`<email>`
Replace with valid email

## When this script works

This script works only if:

- Recovery codes are numeric (0000–9999)

- No proper rate limiting

- Reset endpoint responds differently for valid vs invalid codes

- Server trusts spoofed headers (X-Forwarded-For)

- Session is reused (requests.session())



## How to run
python3 brute-force.py


## Expected output:

[*] Trying code: 0420
[+] Found valid recovery code: 7351
[✓] Found valid recovery code: 7351

## Notes

Threaded for speed (ThreadPoolExecutor)

Header rotation attempts IP-based bypass

Delay added to reduce server tantrums

Modify response string if the error message differs
