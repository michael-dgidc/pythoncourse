import json
import random
import os

def generate_square(size, offset_x, offset_y):
    return [
        [offset_x, offset_y],
        [offset_x + size, offset_y],
        [offset_x + size, offset_y + size],
        [offset_x, offset_y + size]
    ]

def generate_triangle(side, offset_x, offset_y):
    # Simple equilateral-ish triangle
    h = side * 0.866
    return [
        [offset_x, offset_y],
        [offset_x + side, offset_y],
        [offset_x + side / 2, offset_y + h]
    ]

def save_shape(shape, label, filename):
    data = {"label": label, "vertices": shape}
    with open(filename, 'w') as f:
        json.dump(data, f)

os.makedirs("shapes_ai/training/squares", exist_ok=True)
os.makedirs("shapes_ai/training/triangles", exist_ok=True)
os.makedirs("shapes_ai/test", exist_ok=True)

# Generate 20 squares
for i in range(20):
    size = random.uniform(5, 20)
    ox = random.uniform(0, 50)
    oy = random.uniform(0, 50)
    shape = generate_square(size, ox, oy)
    save_shape(shape, "square", f"shapes_ai/training/squares/square_{i}.json")

# Generate 20 triangles
for i in range(20):
    side = random.uniform(5, 20)
    ox = random.uniform(0, 50)
    oy = random.uniform(0, 50)
    shape = generate_triangle(side, ox, oy)
    save_shape(shape, "triangle", f"shapes_ai/training/triangles/triangle_{i}.json")

# Generate some test files
for i in range(10):
    is_square = random.choice([True, False])
    label = "square" if is_square else "triangle"
    size = random.uniform(5, 20)
    ox = random.uniform(0, 50)
    oy = random.uniform(0, 50)
    if is_square:
        shape = generate_square(size, ox, oy)
    else:
        shape = generate_triangle(size, ox, oy)
    
    test_data = {"label": label, "vertices": shape}
    with open(f"shapes_ai/test/test_{i}.json", 'w') as f:
        json.dump(test_data, f)

print("Data generation complete.")
