import os
import random
from PIL import Image, ImageDraw

def generate_square_img(size, offset_x, offset_y, img_size=(100, 100)):
    img = Image.new('L', img_size, color=0)
    draw = ImageDraw.Draw(img)
    draw.rectangle([offset_x, offset_y, offset_x + size, offset_y + size], fill=255)
    return img

def generate_triangle_img(side, offset_x, offset_y, img_size=(100, 100)):
    img = Image.new('L', img_size, color=0)
    draw = ImageDraw.Draw(img)
    h = side * 0.866
    points = [
        (offset_x, offset_y + h),
        (offset_x + side, offset_y + h),
        (offset_x + side / 2, offset_y)
    ]
    draw.polygon(points, fill=255)
    return img

os.makedirs("shapes_ai_png/training/squares", exist_ok=True)
os.makedirs("shapes_ai_png/training/triangles", exist_ok=True)
os.makedirs("shapes_ai_png/test", exist_ok=True)

# Generate 20 squares
for i in range(20):
    size = random.uniform(20, 50)
    ox = random.uniform(0, 40)
    oy = random.uniform(0, 40)
    img = generate_square_img(size, ox, oy)
    img.save(f"shapes_ai_png/training/squares/square_{i}.png")

# Generate 20 triangles
for i in range(20):
    side = random.uniform(20, 50)
    ox = random.uniform(0, 40)
    oy = random.uniform(0, 40)
    img = generate_triangle_img(side, ox, oy)
    img.save(f"shapes_ai_png/training/triangles/triangle_{i}.png")

# Generate 10 test files
for i in range(10):
    is_square = random.choice([True, False])
    label = "square" if is_square else "triangle"
    size = random.uniform(20, 50)
    ox = random.uniform(0, 40)
    oy = random.uniform(0, 40)
    if is_square:
        img = generate_square_img(size, ox, oy)
    else:
        img = generate_triangle_img(side, ox, oy)
    img.save(f"shapes_ai_png/test/test_{i}_{label}.png")

print("PNG Data generation complete.")
