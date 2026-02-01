from PIL import Image
import numpy as np
import glob

# Grab all PNG frames in a folder, sorted
frame_files = sorted(glob.glob("frame_*.png"))

frames = []

# Open each PNG, convert to palette, resize, store
for ffile in frame_files:
    img = Image.open(ffile)
    img = img.convert("P", palette=Image.ADAPTIVE, colors=256)  # 256-color palette
    img = img.resize((160, 120))
    frames.append(np.array(img).flatten())

# Generate Verilog-style arrays for each frame
for i, data in enumerate(frames):
    print(f"localparam [7:0] frame{i} [0:{len(data)-1}] = '{{")
    for j, b in enumerate(data):
        end_char = "\n" if j % 16 == 15 else " "
        print(f"8'h{b:02X},{end_char}", end="")
    print("};\n")

# Generate palette (from first frame)
pal = Image.open(frame_files[0]).convert("P", palette=Image.ADAPTIVE, colors=256).getpalette()[:768]
print("localparam [23:0] palette [0:255] = '{")
for i in range(0, 768, 3):
    print(f"24'h{pal[i]:02X}{pal[i+1]:02X}{pal[i+2]:02X},")
print("};")
