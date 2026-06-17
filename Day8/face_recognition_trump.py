import face_recognition
import cv2
import os

def identify_trump(reference_image_path, test_image_path):
    """
    Identifies if President Trump is in the test image based on a reference image.
    
    Args:
        reference_image_path (str): Path to a clear photo of Trump.
        test_image_path (str): Path to the photo you want to check.
    """
    
    # Check if files exist
    if not os.path.exists(reference_image_path):
        print(f"Error: Reference image not found at {reference_image_path}")
        return
    if not os.path.exists(test_image_path):
        print(f"Error: Test image not found at {test_image_path}")
        return

    print("Loading images and encoding faces...")
    
    # Load the reference image (training data)
    trump_image = face_recognition.load_image_file(reference_image_path)
    # Get the face encoding for the first face found in the image
    trump_encodings = face_recognition.face_encodings(trump_image)
    
    if len(trump_encodings) == 0:
        print("Error: No face found in the reference image.")
        return
    
    trump_encoding = trump_encodings[0]

    # Load the test image
    unknown_image = face_recognition.load_image_file(test_image_path)
    
    # Find all faces and their encodings in the test image
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    print(f"Found {len(face_encodings)} face(s) in the test image.")

    # Loop through each face found in the test image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare the face with the reference encoding
        # tolerance: lower is more strict, default is 0.6
        matches = face_recognition.compare_faces([trump_encoding], face_encoding, tolerance=0.6)
        
        name = "Unknown"
        if matches[0]:
            name = "Donald Trump"
            print("MATCH FOUND: This is Donald Trump!")
        else:
            print("No match found for this face.")

        # Optional: Use OpenCV to draw a box around the face and label it
        # (This part requires a GUI environment to display, or you can save the result)
        cv2.rectangle(unknown_image, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(unknown_image, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Save the result
    result_path = "result.jpg"
    # face_recognition uses RGB, OpenCV uses BGR
    result_image_bgr = cv2.cvtColor(unknown_image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(result_path, result_image_bgr)
    print(f"Result saved to {result_path}")

if __name__ == "__main__":
    # INSTRUCTIONS:
    # 1. Place a photo of Donald Trump in this folder and name it 'trump_reference.jpg'
    # 2. Place the photo you want to test in this folder and name it 'test_photo.jpg'
    # 3. Run this script.
    
    identify_trump("trump_reference.jpg", "test_photo.jpg")
