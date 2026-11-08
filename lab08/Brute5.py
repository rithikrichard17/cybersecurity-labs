#!/usr/bin/env python3
import hashlib, itertools, string, multiprocessing as mp, time, sys

SALT = b"www.exploringsecurity.com"
CHARSET = string.ascii_letters + string.digits  # 62 chars

targets = {
    "Sparky": "2834da08d58330d8dafbb2ac1c0f85f6b3b135ef",
    "JillC":  "f44f3b09df53c1c11273def13cacd8922a86d48c",
}

def search_chunk(first_chars):
    found = {}
    for fc in first_chars:
        for rest in itertools.product(CHARSET, repeat=4):  # length 5 total
            pw = fc + "".join(rest)
            h = hashlib.sha1(SALT + pw.encode()).hexdigest()
            for user, target in targets.items():
                if h == target and user not in found:
                    found[user] = pw
        if len(found) == len(targets):
            break
    return found

if __name__ == "__main__":
    t0 = time.time()
    chars = list(CHARSET)
    nproc = 2
    chunks = [chars[i::nproc] for i in range(nproc)]
    with mp.Pool(nproc) as pool:
        results = pool.map(search_chunk, chunks)
    t1 = time.time()
    merged = {}
    for r in results:
        merged.update(r)
    print(f"Length-5 search done in {t1-t0:.1f}s")
    for user in targets:
        print(f"  {user}: {merged.get(user, 'NOT FOUND (len 5)')}")