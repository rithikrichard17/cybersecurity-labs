#!/usr/bin/env python3
"""
Salted hash cracker for the lab.
Target hashes are 40 hex chars -> SHA-1.
Salt format hint: CommonHash($salt,$pass) -> assume sha1(salt + pass), but we
also try sha1(pass + salt) just in case the function reverses internally.

Salt candidates: the only "extra" piece of data embedded in the case file is
the site domain, so we try a handful of plausible forms of it.

Password policy (from Pass_modified date vs May 2010):
  - modified before 2010-05 -> digits only, length 5-7
  - modified on/after 2010-05 -> alphanumeric, length 5-7
"""
import hashlib
import itertools
import string
import sys
import datetime

targets = {
    "Sparky":   ("2834da08d58330d8dafbb2ac1c0f85f6b3b135ef", "2011-05-09"),
    "Mark123":  ("92e54f10103a3c511853c7098c04141f114719c1", "2010-06-03"),
    "superman": ("437fbc6892b38db6ac5bdbe2eab3f7bc924527d9", "2011-01-01"),
    "security": ("fafa4483874ec051989d53e1e432ba3a6c6b9143", "2010-01-11"),
    "Tomtom":   ("06f6fe0f73c6e197ee43eff4e5f7d10fb9e438b2", "2009-12-03"),
    "JillC":    ("f44f3b09df53c1c11273def13cacd8922a86d48c", "2010-12-20"),
}

cutoff = datetime.date(2010, 5, 1)

salt_candidates = [
    "exploringsecurity.com",
    "www.exploringsecurity.com",
    "exploringsecurity",
]

def charset_for(user):
    pm = datetime.date.fromisoformat(targets[user][1])
    if pm < cutoff:
        return string.digits
    else:
        return string.ascii_letters + string.digits

def hashes_for(salt, pw):
    return {
        "salt+pass": hashlib.sha1((salt + pw).encode()).hexdigest(),
        "pass+salt": hashlib.sha1((pw + salt).encode()).hexdigest(),
    }

def crack_user(user, max_len=7, min_len=5, verbose_every=2_000_000):
    target_hash, pm = targets[user]
    charset = charset_for(user)
    tried = 0
    for salt in salt_candidates:
        for length in range(min_len, max_len + 1):
            for combo in itertools.product(charset, repeat=length):
                pw = "".join(combo)
                tried += 1
                if tried % verbose_every == 0:
                    print(f"  ...[{user}] tried {tried:,}", file=sys.stderr)
                for mode, h in hashes_for(salt, pw).items():
                    if h == target_hash:
                        return pw, salt, mode, tried
    return None, None, None, tried

if __name__ == "__main__":
    import sys
    only = sys.argv[1] if len(sys.argv) > 1 else None
    users = [only] if only else list(targets.keys())
    for user in users:
        charset = charset_for(user)
        print(f"[{user}] charset={'digits' if charset==string.digits else 'alnum'} "
              f"len=5-7 salts_tried={len(salt_candidates)}", flush=True)
        pw, salt, mode, tried = crack_user(user)
        if pw:
            print(f"  >>> CRACKED {user}: password='{pw}' salt='{salt}' mode={mode} (after {tried:,} attempts)")
        else:
            print(f"  --- no match for {user} after {tried:,} attempts")