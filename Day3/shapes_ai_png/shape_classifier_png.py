import json
import os
import math
from PIL import Image

class ShapeAIPNG:
    def __init__(self):
        self.model_data = []
        self.cache_file = "shapes_ai_png/model_cache_png.json"

    def extract_features(self, img_path):
        img = Image.open(img_path).convert('L')
        width, height = img.size
        pixels = img.load()

        # Simple feature: Area (number of white pixels)
        # Simple feature: Perimeter (pixels on the edge of the shape)
        white_pixels = []
        for y in range(height):
            for x in range(width):
                if pixels[x, y] > 128:
                    white_pixels.append((x, y))

        if not white_pixels:
            return {"area": 0, "iq": 0}

        area = len(white_pixels)
        
        # Approximate perimeter by counting white pixels with at least one black neighbor
        perimeter = 0
        for x, y in white_pixels:
            is_edge = False
            # Check 8-connectivity to be more robust
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0: continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        if pixels[nx, ny] <= 128:
                            is_edge = True
                            break
                    else:
                        is_edge = True
                        break
                if is_edge: break
            if is_edge:
                perimeter += 1
        
        # Isoperimetric quotient (P^2 / A)
        iq = (perimeter ** 2) / area if area > 0 else 0
        
        # Debug print to see values
        # print(f"Path: {img_path}, Area: {area}, Perimeter: {perimeter}, IQ: {iq}")
        
        return {
            "area": area,
            "iq": iq
        }

    def train(self, training_dir):
        print("Training model from PNG images...")
        self.model_data = []
        for label in ["squares", "triangles"]:
            label_dir = os.path.join(training_dir, label)
            if not os.path.exists(label_dir):
                continue
            
            actual_label = "square" if label == "squares" else "triangle"
            
            for file in os.listdir(label_dir):
                if file.endswith(".png"):
                    path = os.path.join(label_dir, file)
                    features = self.extract_features(path)
                    features["label"] = actual_label
                    self.model_data.append(features)
        
        # Cache results
        with open(self.cache_file, 'w') as f:
            json.dump(self.model_data, f)
        print(f"Model trained on {len(self.model_data)} PNG samples and cached.")

    def load_model(self):
        if os.path.exists(self.cache_file):
            print("Loading PNG model from cache...")
            with open(self.cache_file, 'r') as f:
                self.model_data = json.load(f)
            return True
        return False

    def predict(self, img_path):
        features = self.extract_features(img_path)
        
        # Simple KNN (k=3)
        distances = []
        for sample in self.model_data:
            # We use iq mainly, as area depends on size
            # Since squares and triangles have different IQs, this should work.
            # Normalizing distance slightly
            d = abs(features["iq"] - sample["iq"])
            distances.append((d, sample["label"]))
        
        distances.sort(key=lambda x: x[0])
        neighbors = distances[:3]
        
        counts = {}
        for _, label in neighbors:
            counts[label] = counts.get(label, 0) + 1
        
        return max(counts, key=counts.get)

def main():
    ai = ShapeAIPNG()
    
    # Check cache first
    if not ai.load_model():
        ai.train("shapes_ai_png/training")
    
    test_folder = "shapes_ai_png/test"
    print(f"\nIterating through test PNG files in: {test_folder}")
    
    test_files = [f for f in os.listdir(test_folder) if f.endswith(".png")]
    correct = 0
    for test_file in test_files:
        path = os.path.join(test_folder, test_file)
        prediction = ai.predict(path)
        
        # Infer actual label from filename (test_i_label.png)
        if "square" in test_file:
            actual = "square"
        elif "triangle" in test_file:
            actual = "triangle"
        else:
            actual = "unknown"
            
        status = "PASS" if prediction == actual else "FAIL"
        print(f"File: {test_file} -> Predicted: {prediction} (Actual: {actual}) [{status}]")
        if prediction == actual:
            correct += 1
    
    if len(test_files) > 0:
        print(f"\nAccuracy: {correct}/{len(test_files)} ({correct/len(test_files)*100:.1f}%)")
    else:
        print("No test files found.")

if __name__ == "__main__":
    main()
