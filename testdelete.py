import os
import requests
from options import Options

def register_face(user_id):

    opts = Options()



    response = requests.post(opts.endpoint("vision/face/delete"),
                             data={"userid": user_id}).json()

    print(f"Registration response: {response}")

def main():
    register_face("Recognize")

    
if __name__ == "__main__":
    main()
