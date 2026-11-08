#!/usr/bin/env python3
import hashlib, itertools, string, sys

SALT = "www.exploringsecurity.com"

targets = {
    "Sparky":   "2834da08d58330d8dafbb2ac1c0f85f6b3b135ef",
    "Mark123":  "92e54f10103a3c511853c7098c04141f114719c1",
    "superman": "437fbc6892b38db6ac5bdbe2eab3f7bc924527d9",
    "security": "fafa4483874ec051989d53e1e432ba3a6c6b9143",
    "Tomtom":   "06f6fe0f73c6e197ee43eff4e5f7d10fb9e438b2",
    "JillC":    "f44f3b09df53c1c11273def13cacd8922a86d48c",
}

def crack(user, charset, min_len=5, max_len=7):
    target = targets[user]
    tried = 0
    for length in range(min_len, max_len+1):
        for combo in itertools.product(charset, repeat=length):
            pw = "".join(combo)
            tried += 1
            if tried % 5_000_000 == 0:
                print(f"  ...{user} tried {tried:,}", file=sys.stderr)
            if hashlib.sha1((SALT+pw).encode()).hexdigest() == target:
                return pw, tried
    return None, tried

if __name__ == "__main__":
    user = sys.argv[1]
    charset = string.digits
    pw, tried = crack(user, charset)
    if pw:
        print(f">>> {user}: '{pw}' (after {tried:,} tries)")
    else:
        print(f"--- no match for {user} ({tried:,} tries)")