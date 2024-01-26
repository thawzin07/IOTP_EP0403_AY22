import os
import requests
from options import Options
import cv2

def register_face(img_path, user_id, opts):

    filepath = os.path.join(opts.imageDir + "/Faces", img_path)
    image_data = open(filepath, "rb").read()

    response = requests.post(opts.endpoint("vision/face/register"),
                             files={"image": image_data},
                             data={"userid": user_id}).json()

    print(f"Registration response: {response}")
    
def recognize_face(img_path, opts):
    filepath = os.path.join(opts.imageDir + "/Faces", img_path)
    image_data = open(filepath, "rb").read()

    response = requests.post(opts.endpoint("vision/face/recognize"),
                             files={"image": image_data},
                             data={"min_confidence": 0.6}).json()

    for user in response["predictions"]:
        sure = {user["userid"]}
        print(f'Recognized as: {user["userid"]}')

def delete_face(user_id):

    opts = Options()
    response = requests.post(opts.endpoint("vision/face/delete"),
                             data={"userid": user_id}).json()

    print(f"Registration response: {response}")

        
def camera_capture(user_id):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None

    # Capture a frame
    ret, frame = cap.read()

    # Save the captured frame to a file
    img_path = f"D:/IOTP/FR/Graphics/{user_id}_camera_capture.jpg"

    cv2.imwrite(img_path, frame)

    # Release the camera
    cap.release()

    return img_path

def camera_capture2():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None

    # Capture a frame
    ret, frame = cap.read()

    # Save the captured frame to a file
    img_path = f"D:/IOTP/FR/Graphics/camera_capture.jpg"

    cv2.imwrite(img_path, frame)

    # Release the camera
    cap.release()

    return img_path

def main():
    opts = Options()  # Initialize Options class here

    print("Choose registration option:")
    print("1. Register with an existing image")
    print("2. Register using the camera")
    print("3. Recognize ME")
    print("4. Delete Image")

    choice = input("Enter your choice (1, 2, 3 or 4): ")

    if choice == "1":
        img_path = input("Enter the path to the existing image: ")
        user_id = input("Enter the user ID: ")
        register_face(img_path, user_id, opts)
    elif choice == "2":
        user_id = input("Enter the user ID: ")
        captured_image_path = camera_capture(user_id)
        if captured_image_path:
            register_face(captured_image_path, user_id, opts)
    elif choice == "3":
        user_id = "Recognize"
        captured_image_path = camera_capture(user_id)
        if captured_image_path:
            recognize_face(captured_image_path, opts)
    elif choice == "4":
        captured_image_path = camera_capture2()
        if captured_image_path:
            recognize_face(captured_image_path, opts)
        delete = input("Are you sure to delete the image recognized as {sure}")
        user_id = sure 
        captured_image_path = camera_capture(user_id)
        if captured_image_path:
            delete_face(user_id)
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
