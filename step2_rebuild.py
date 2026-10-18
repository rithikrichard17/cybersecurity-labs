
from pathlib import Path
import struct

# Read the encrypted challenge file
data = Path("aes.bmp.enc").read_bytes()

# For this preliminary reconstruction, skip the first 54 bytes
pixels = data[54:]

# Assumed image properties
width = 640
height = 480
bits_per_pixel = 24

# Calculate BMP row size, including padding
row_size = ((width * bits_per_pixel + 31) // 32) * 4
pixel_data_size = row_size * height

if len(pixels) != pixel_data_size:
    raise ValueError(
        f"Unexpected pixel-data size: {len(pixels)}"
    )

# Build the BMP file header (14 bytes)
file_header = struct.pack(
    "<2sIHHI",
    b"BM",
    54 + pixel_data_size,
    0,
    0,
    54
)

# Build the BMP information header (40 bytes)
info_header = struct.pack(
    "<IIIHHIIIIII",
    40,
    width,
    height,
    1,
    bits_per_pixel,
    0,
    pixel_data_size,
    2835,
    2835,
    0,
    0
)

# Save the reconstructed image
Path("reconstructed.bmp").write_bytes(
    file_header + info_header + pixels
)

print("Reconstruction complete!")
print("Image dimensions:", width, "x", height)
print("Output file: reconstructed.bmp")
