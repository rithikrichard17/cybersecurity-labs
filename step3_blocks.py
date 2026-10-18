
from pathlib import Path
from collections import Counter

# Read the original challenge file
data = Path("aes.bmp.enc").read_bytes()

print("Total file size:", len(data), "bytes")

# Analyse the suspected encrypted pixel data
ciphertext = data[54:]

# AES processes data in blocks of 16 bytes
block_size = 16

blocks = [
    ciphertext[i:i + block_size]
    for i in range(0, len(ciphertext), block_size)
]

# Count how often each block appears
counts = Counter(blocks)

print("Total blocks:", len(blocks))
print("Unique blocks:", len(counts))
print(
    "Repeated block types:",
    sum(count > 1 for count in counts.values())
)

print("\nMost common blocks:")
for block, count in counts.most_common(10):
    print(block.hex(), "->", count, "occurrences")
