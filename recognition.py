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
                             data={"min_confidence": 0.1}).json()

    for user in response["predictions"]:
        print(f'Recognized as: {user["userid"]}')

def camera_capture(user_id):
    
    opts = Options()
    cap = cv2.VideoCapture(0)

    frame_index = 0
    predictions = {}
    skip_frame  = 5

    while cap.isOpened():

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        valid, frame = cap.read()            
        if not valid:
            break;

        frame_index += 1
        
        if skip_frame > 1:
            if frame_index % skip_frame != 0:
               continue;

        retval, new_frame = cv2.imencode('.jpg', frame)

        response = requests.post(opts.endpoint("vision/face"),
                                 files={"image":new_frame}).json()

        predictions = response['predictions']

        print(f"Frame {frame_index}: {len(predictions)} predictions")

        num_prediction_json = len(predictions)

        for i in range(num_prediction_json):
            red, green, blue = 200, 100, 200
            frame = cv2.rectangle(frame, 
                                  (predictions[i]['x_min'], predictions[i]['y_min']),
                                  (predictions[i]['x_max'], predictions[i]['y_max']), 
                                  (red, green, blue), 1)
        
        cv2.imshow('Image Viewer', frame)
        
    cap.release()
    cv2.destroyAllWindows()


def main():
    opts = Options()  # Initialize Options class here

    print("Choose option:")
    print("1. Register with an existing image")
    print("2. Register using the camera")
    print("3. Recognize using an existing image")

    choice = input("Enter your choice (1, 2, or 3): ")

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
        img_path = input("Enter the path to the existing image for recognition: ")
        recognize_face(img_path, opts)
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
