#!/usr/bin/env python3
import hashlib, itertools, string, sys

SALT = "www.exploringsecurity.com"

targets = {
    "Sparky":   "2834da08d58330d8dafbb2ac1c0f85f6b3b135ef",
    "Mark123":  "92e54f10103a3c511853c7098c04141f114719c1",
    "superman": "437fbc6892b38db6ac5bdbe2eab3f7bc924527d9",
    "JillC":    "f44f3b09df53c1c11273def13cacd8922a86d48c",
}

# Common password list (5-7 chars, well-known top passwords globally)
common = """
password 123456 12345678 123123 111111 1234567 12345 1234567 qwerty
abc123 monkey dragon letmein trustno1 baseball football sunshine
iloveyou master login princess qazwsx michael jennife superman
batman spiderm thomas charlie jordan hunter shadow jessica michelle
daniel buster soccer hockey killer george andrew lauren austin
martin donald taylor robert andrea melissa amanda jasmine jasper
chelsea maggie samsung tigger pepper sophie cooper phoenix
flower mustang access yankees ranger gators eagles
tomtom tigger buster sparky sparky1 sparky12 sparky123
mark123 markie mark12 mark1234 marky1 marky12
superman1 superman12 superman2 clark01 kryptonite
jillc jillc1 jillc12 jillc123 jillian jilly01 jill123
qwerty1 qwerty12 asdfgh zxcvbn 1qaz2wsx trustme
welcome welcome1 admin123 letmein1 freedom whatever
summer winter spring autumn hello123 hello12
""".split()

def mutate(word):
    outs = set()
    w = word.lower()
    outs.add(w)
    outs.add(w.capitalize())
    outs.add(word)
    for suf in ["", "1", "12", "123", "01", "007", "99", "2010", "2009", "2011"]:
        outs.add(w + suf)
        outs.add(w.capitalize() + suf)
    return outs

def build_wordlist(usernames):
    words = set()
    for w in common:
        words |= mutate(w)
    for u in usernames:
        base = u.lower().rstrip(string.digits)
        words |= mutate(base)
        words |= mutate(u)
    # restrict to policy: alphanumeric, length 5-7
    final = [w for w in words if 5 <= len(w) <= 7 and w.isalnum()]
    return sorted(set(final))

def crack(user, wordlist):
    target = targets[user]
    for pw in wordlist:
        h = hashlib.sha1((SALT + pw).encode()).hexdigest()
        if h == target:
            return pw
        # also try pass+salt just in case
        h2 = hashlib.sha1((pw + SALT).encode()).hexdigest()
        if h2 == target:
            return pw + " [pass+salt mode]"
    return None

if __name__ == "__main__":
    wl = build_wordlist(list(targets.keys()))
    print(f"Wordlist size: {len(wl)}")
    for user in targets:
        pw = crack(user, wl)
        print(f"{user}: {pw if pw else 'NOT FOUND in wordlist'}")