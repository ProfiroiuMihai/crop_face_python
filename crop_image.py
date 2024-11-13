import cv2
import os
import numpy as np
import sys

def crop_and_resize_faces(folder_path, target_width=300, target_height=400, face_to_image_ratio=0.425, zoom_factor=1.2):
    output_folder = os.path.join(folder_path, 'output')
    os.makedirs(output_folder, exist_ok=True)
    
  # In the crop_and_resize_faces function, modify the cascade file path handling:
    if getattr(sys, 'frozen', False):
        # If running as executable
        cascade_path = os.path.join(sys._MEIPASS, 'cv2', 'data', 'haarcascade_frontalface_default.xml')
    else:
        # If running as script
        cascade_path = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')
    
    face_cascade = cv2.CascadeClassifier(cascade_path)
    
    if face_cascade.empty():
        print("Error: Couldn't load face cascade classifier")
        return

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)
            image = cv2.imread(img_path)
            
            if image is None:
                print(f"Failed to read image {filename}")
                continue
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(faces) == 0:
                print(f"No face detected in {filename}")
                continue
            
            # Select the largest face (assuming it's the main face)
            x, y, w, h = max(faces, key=lambda rect: rect[2] * rect[3])

            # Calculate the desired face height
            desired_face_height = int(target_height * face_to_image_ratio)
            scale_factor = desired_face_height / h
            
            # Calculate the required crop size while maintaining aspect ratio
            crop_height = int(target_height / scale_factor)
            crop_width = int(target_width / scale_factor)
            
            # Apply zoom factor
            crop_height = int(crop_height / zoom_factor)
            crop_width = int(crop_width / zoom_factor)
            
            # Calculate center of the face
            center_x = x + w // 2
            center_y = y + h // 2
            
            # Calculate crop coordinates
            start_x = max(0, center_x - crop_width // 2)
            start_y = max(0, center_y - crop_height // 2)
            end_x = min(image.shape[1], start_x + crop_width)
            end_y = min(image.shape[0], start_y + crop_height)
            
            # Adjust start coordinates if end coordinates exceed image dimensions
            if end_x == image.shape[1]:
                start_x = max(0, end_x - crop_width)
            if end_y == image.shape[0]:
                start_y = max(0, end_y - crop_height)
            
            # Crop the region
            cropped_region = image[start_y:end_y, start_x:end_x]
            
            # Create a black canvas of target size
            final_image = np.zeros((target_height, target_width, 3), dtype=np.uint8)
            
            # Resize cropped region maintaining aspect ratio
            aspect_ratio = crop_width / crop_height
            target_aspect_ratio = target_width / target_height
            
            if aspect_ratio > target_aspect_ratio:
                # Width is the limiting factor
                new_width = target_width
                new_height = int(target_width / aspect_ratio)
                top_padding = (target_height - new_height) // 2
                resized = cv2.resize(cropped_region, (new_width, new_height))
                final_image[top_padding:top_padding+new_height, :] = resized
            else:
                # Height is the limiting factor
                new_height = target_height
                new_width = int(target_height * aspect_ratio)
                left_padding = (target_width - new_width) // 2
                resized = cv2.resize(cropped_region, (new_width, new_height))
                final_image[:, left_padding:left_padding+new_width] = resized
            
            # Save the result
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.jpg")
            cv2.imwrite(output_path, final_image)
            print(f"Cropped and resized image saved to {output_path}")

def main():
    # Get the directory where the executable/script is located
    if getattr(sys, 'frozen', False):
        # If running as executable
        folder_path = os.path.dirname(sys.executable)
    else:
        # If running as script
        folder_path = os.path.dirname(os.path.abspath(__file__))
    
    print(f"Processing images in: {folder_path}")
    
    try:
        crop_and_resize_faces(folder_path, zoom_factor=1)
        print("\nProcessing complete!")
        print("Press Enter to exit...")
        input()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Press Enter to exit...")
        input()

if __name__ == "__main__":
    main()