import json
import os
import math

class SimpleShapeAI:
    def __init__(self):
        self.model_data = []
        self.cache_file = "shapes_ai/model_cache.json"

    def extract_features(self, vertices):
        # Feature: Number of vertices
        num_vertices = len(vertices)
        
        # Feature: Perimeter^2 / Area (Isoperimetric quotient related)
        # For a square: P=4s, A=s^2 => P^2/A = 16s^2 / s^2 = 16
        # For an equilateral triangle: P=3s, A=(sqrt(3)/4)s^2 => P^2/A = 9s^2 / (0.433s^2) approx 20.78
        
        perimeter = 0
        for i in range(num_vertices):
            p1 = vertices[i]
            p2 = vertices[(i + 1) % num_vertices]
            perimeter += math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        
        # Area using Shoelace formula
        area = 0
        for i in range(num_vertices):
            p1 = vertices[i]
            p2 = vertices[(i + 1) % num_vertices]
            area += (p1[0] * p2[1] - p2[0] * p1[1])
        area = abs(area) / 2.0
        
        iq = (perimeter ** 2) / area if area > 0 else 0
        
        return {
            "num_vertices": num_vertices,
            "iq": iq
        }

    def train(self, training_dir):
        print("Training model...")
        self.model_data = []
        for root, dirs, files in os.walk(training_dir):
            for file in files:
                if file.endswith(".json"):
                    path = os.path.join(root, file)
                    with open(path, 'r') as f:
                        data = json.load(f)
                        features = self.extract_features(data["vertices"])
                        features["label"] = data["label"]
                        self.model_data.append(features)
        
        # Cache results
        with open(self.cache_file, 'w') as f:
            json.dump(self.model_data, f)
        print(f"Model trained on {len(self.model_data)} samples and cached.")

    def load_model(self):
        if os.path.exists(self.cache_file):
            print("Loading model from cache...")
            with open(self.cache_file, 'r') as f:
                self.model_data = json.load(f)
            return True
        return False

    def predict(self, vertices):
        features = self.extract_features(vertices)
        
        # Simple KNN (k=3)
        distances = []
        for sample in self.model_data:
            # Euclidean distance between features (normalized or just raw for this simple case)
            # Since num_vertices is very discriminative, it will dominate.
            d = math.sqrt((features["num_vertices"] - sample["num_vertices"])**2 + 
                          (features["iq"] - sample["iq"])**2)
            distances.append((d, sample["label"]))
        
        distances.sort(key=lambda x: x[0])
        neighbors = distances[:3]
        
        counts = {}
        for _, label in neighbors:
            counts[label] = counts.get(label, 0) + 1
        
        return max(counts, key=counts.get)

def main():
    ai = SimpleShapeAI()
    
    # Check cache first
    if not ai.load_model():
        ai.train("shapes_ai/training")
    
    test_folder = "shapes_ai/test"
    print(f"\nIterating through test files in: {test_folder}")
    
    test_files = [f for f in os.listdir(test_folder) if f.endswith(".json")]
    correct = 0
    for test_file in test_files:
        path = os.path.join(test_folder, test_file)
        with open(path, 'r') as f:
            data = json.load(f)
            prediction = ai.predict(data["vertices"])
            actual = data.get("label", "unknown")
            status = "PASS" if prediction == actual else "FAIL"
            print(f"File: {test_file} -> Predicted: {prediction} (Actual: {actual}) [{status}]")
            if prediction == actual:
                correct += 1
    
    print(f"\nAccuracy: {correct}/{len(test_files)} ({correct/len(test_files)*100:.1f}%)")

if __name__ == "__main__":
    main()
