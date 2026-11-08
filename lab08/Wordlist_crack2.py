#!/usr/bin/env python3
import hashlib, itertools, string

SALT = "www.exploringsecurity.com"

targets = {
    "Sparky": "2834da08d58330d8dafbb2ac1c0f85f6b3b135ef",
    "JillC":  "f44f3b09df53c1c11273def13cacd8922a86d48c",
}

# Much larger curated common-password / pattern set (5-7 char alnum focus)
common = """
password 123456 12345678 123123 111111 1234567 qwerty qwerty1
abc123 monkey dragon letmein trustno1 baseball football sunshine
iloveyou master login princess qazwsx michael jennifer superman
batman spiderman thomas charlie jordan hunter shadow jessica michelle
daniel buster soccer hockey killer george andrew lauren austin
martin donald taylor robert andrea melissa amanda jasmine jasper
chelsea maggie samsung tigger pepper sophie cooper phoenix
flower mustang access yankees ranger gators eagles dolphin
panther orange purple yellow silver golden bronze copper
wizard dragon1 ginger cookie bubble cherry maggie1
summer1 winter1 spring1 autumn1 hello123 freedom1 whatever1
sparky sparkle sparky1 sparky12 sparky22 sparky99 sparky01
spark1 spark12 spark01 sparks1 jilly jillyc jillyc1
jillian jillyb jilly01 jilly12 jillc01 jillc12 jillian1
jillc2009 jillc10 jc12345 jc123456
dog123 cat123 bird123 fish123 love123 star123 moon123
sunny1 happy12 smiley1 angel12 pretty1 lucky12
thunder lightnin blaze99 flame12 spark99
007bond 1q2w3e4 zaq1zaq1 iloveu1 cutiepie
london1 dublin1 ireland1 galway1 cork1234 belfast1
liverp liverpo chelsea1 arsenal gunners1
rangers celtic1 glasgow1
guinness shamrock paddy123 irish123
2009jill 2010jill jillc2010
sparky2009 sparky2010 sparky2011
""".split()

def mutate(word):
    outs = set()
    w = word.lower()
    outs.add(w)
    outs.add(w.capitalize())
    outs.add(word)
    outs.add(word.upper())
    suffixes = ["", "1","2","3","12","13","22","23","99","00","01","07","09","10",
                "11","123","1234","2009","2010","2011"]
    for suf in suffixes:
        outs.add(w+suf)
        outs.add(w.capitalize()+suf)
    return outs

def build_wordlist():
    words = set()
    for w in common:
        words |= mutate(w)
    final = [w for w in words if 5 <= len(w) <= 7 and w.isalnum()]
    return sorted(set(final))

def crack(user, wordlist):
    target = targets[user]
    for pw in wordlist:
        if hashlib.sha1((SALT+pw).encode()).hexdigest() == target:
            return pw
        if hashlib.sha1((pw+SALT).encode()).hexdigest() == target:
            return pw + " [pass+salt]"
    return None

if __name__ == "__main__":
    wl = build_wordlist()
    print(f"Wordlist size: {len(wl)}")
    for user in targets:
        pw = crack(user, wl)
        print(f"{user}: {pw if pw else 'NOT FOUND'}")