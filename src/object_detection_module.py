"""
REST-based node that interfaces with WEI and provides a Object detection with camera interface
"""

from pathlib import Path
import subprocess

import cv2
import numpy as np
from fastapi.datastructures import State
from wei.modules.rest_module import RESTModule
from wei.types.module_types import LocalFileModuleActionResult
from wei.types.step_types import (
    ActionRequest,
    StepFileResponse,
    StepResponse,
    StepStatus,
)
from wei.utils import extract_version

rest_module = RESTModule(
    name="object_detection_node",
    version=extract_version(Path(__file__).parent.parent / "pyproject.toml"),
    description="An example REST object detection implementation",
    model="object_detection",
)
rest_module.arg_parser.add_argument(
    "--camera_address", type=str, help="the camera address", default="/dev/video0"
)


@rest_module.action(
    name="detect", description="An action that takes a picture and runs YOLO object detection",
    results=[
        LocalFileModuleActionResult(
            label="file", description="the coordinate file returned"
        ),
    ],
)
def detect(
    state: State,
    action: ActionRequest,
) -> StepResponse:
    """Function to take a picture and detect object"""
    result_0 = subprocess.run(['pwd'], capture_output=True, text=True)
    print('Output:', result_0.stdout)
    result = subprocess.run(['ls', '-lrth'], capture_output=True, text=True)
    print('Output:', result.stdout)
    file_path = Path("~/.wei/temp").expanduser() / "GeneratedCode.h"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    image_path = Path("~/.wei/temp").expanduser() / "image.jpg"
    image_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        camera = cv2.VideoCapture(state.camera_address)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
        for _ in range(20):
            _, frame = camera.read()
        jpeg_quality = 85  # Adjust this value as needed
        params = [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality]
        cv2.imwrite(str(image_path), frame, params)
        camera.release()
    except Exception:
        print("Camera unavailable, returning empty image")
        blank_image = np.zeros(shape=[512, 512, 3], dtype=np.uint8)
        cv2.imwrite(str(image_path), blank_image)
    
    try:
        subprocess.run(['bash', '-c', 'cd .. && pwd']) 
        subprocess.run(["/home/app/object_detection_module/src/photoAndPosition.sh", image_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error calling shell script: {e}")   

    def takePhotoAndGetLocation():

        cubeLocation = [0,0]
        cylinderLocation = [0,0]
        cubeHoleLocation = [0,0]

        # Read the contents of the file "2"
        file_path = "/home/app/.wei/temp/output.txt"
        try:
            with open(file_path, 'r') as f:
                left_x = 0
                top_y = 0
            
                for line in f:
                    # Parse each line to extract object, percentage, left_x, and top_y
                    if line.strip():  # Check if line is not empty
                        parts = line.split()
                        if len(parts) >= 7:
                            object_name = parts[0].rstrip(':')

                            left_x = int(parts[3])
                            top_y = int(parts[5])

                            del_x = int(parts[7])
                            del_y = int(parts[9][:-1])

                            left_x = left_x + del_x/2.0
                            top_y = top_y + del_y/2.0

                            if(object_name == 'cube'):
                                cubeLocation = [left_x,top_y]
                            elif(object_name == 'cylinder'):
                                cylinderLocation = [left_x,top_y]
                            else:
                                cubeHoleLocation = [left_x,top_y]

                # Output the result
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except Exception as e:
            print(f"Error occurred: {e}")
        return cubeLocation,cylinderLocation,cubeHoleLocation 

    def getValues():
        
        #Drop
        x1 = 548
        y1 = 868
        dx1 = 102
        dy1 = 87

        #Pickup
        x2 = 152
        y2 = 523
        dx2 = 105 
        dy2 = 89

        a = x1+(dx1/2)
        b = y2+(dy2/2)

        da = x1 - x2
        db = y1 - y2

        return a,b,da,db

    def transformImgtoRobot(coordImg):
        a,b,da,db = getValues()
        if (len(coordImg) != 0):
            X = ((400.0/db) * -1*(b - coordImg[1]))
            Y = ((400.0/da) * (a - coordImg[0])) 
            # print(X,Y)
            return [X,Y]
        
        return [0,0]
    
    def writeToFile(left_x,left_y,nameX,nameY,left_x1,left_y1,nameX1,nameY1):
        output_file = "/home/app/.wei/temp/GeneratedCode.h"  # Output file with modified content
        try:
            with open(output_file, 'w') as fout:
                fout.write(f"#define {nameX} {left_x}\n")
                fout.write(f"#define {nameY} {left_y}\n")
                fout.write(f"#define {nameX1} {left_x1}\n")
                fout.write(f"#define {nameY1} {left_y1}\n")

        except FileNotFoundError:
            print(f"Error: File '{output_file}' not found.")
        except Exception as e:
            print(f"Error occurred while processing file '{output_file}': {e}")


    cubeImg,cylinderImg,cubeHoleImg = takePhotoAndGetLocation()

    cubeRobot  = transformImgtoRobot(cubeImg)
    cylinderRobot = transformImgtoRobot(cylinderImg)
    cubeHoleRobot = transformImgtoRobot(cubeHoleImg)

    writeToFile(cylinderRobot[0],cylinderRobot[1],'GOTOXB','GOTOYB',cubeHoleRobot[0],cubeHoleRobot[1],'GOTOXL','GOTOYL')

    return StepFileResponse(StepStatus.SUCCEEDED, files={"file": str(file_path)})

if __name__ == "__main__":
    rest_module.start()
