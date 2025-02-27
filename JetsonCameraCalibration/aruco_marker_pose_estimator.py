from __future__ import print_function  
import cv2  
import numpy as np  
from scipy.spatial.transform import Rotation as R
import math  


# Dictionary that was used to generate the ArUco marker
aruco_dictionary_name = "DICT_5X5_1000"

# The different ArUco dictionaries built into the OpenCV library. 
ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL
}

# Side length of the ArUco marker in meters 
aruco_marker_side_length = 0.0785

# Calibration parameters yaml file
camera_calibration_parameters_filename = 'calibration_chessboard.yaml'

def euler_from_quaternion(x, y, z, w):
    """
    Convert a quaternion into euler angles (roll, pitch, yaw)
    roll is rotation around x in radians (counterclockwise)
    pitch is rotation around y in radians (counterclockwise)
    yaw is rotation around z in radians (counterclockwise)
    """
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)

    return roll_x, pitch_y, yaw_z  # in radians

def main():
    """
    Main method of the program.
    """
    # Check that we have a valid ArUco marker
    if ARUCO_DICT.get(aruco_dictionary_name, None) is None:
        print("[INFO] ArUCo tag of '{}' is not supported".format(aruco_dictionary_name))
        SystemExit.exit(0)

    # Load the camera parameters from the saved file
    cv_file = cv2.FileStorage(camera_calibration_parameters_filename, cv2.FILE_STORAGE_READ)
    mtx = cv_file.getNode('K').mat()
    dst = cv_file.getNode('D').mat()
    cv_file.release()

    # Load the ArUco dictionary
    print("[INFO] detecting '{}' markers...".format(aruco_dictionary_name))
    this_aruco_dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[aruco_dictionary_name])
    this_aruco_parameters = cv2.aruco.DetectorParameters()

    # Start the video stream
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Detect ArUco markers in the video frame
        corners, marker_ids, rejected = cv2.aruco.detectMarkers(frame, this_aruco_dictionary, parameters=this_aruco_parameters)

        # Check if at least one marker was detected
        if marker_ids is not None:
            # Draw markers
            cv2.aruco.drawDetectedMarkers(frame, corners, marker_ids)

            # Estimate pose
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, aruco_marker_side_length, mtx, dst)

            for i, marker_id in enumerate(marker_ids):
                marker_id_int = int(marker_id[0])  # Extract integer ID

                transform_translation_x = tvecs[i][0][0]
                transform_translation_y = tvecs[i][0][1]
                transform_translation_z = tvecs[i][0][2]

                # Compute rotation
                rotation_matrix = np.eye(3)
                rotation_matrix, _ = cv2.Rodrigues(rvecs[i][0])
                r = R.from_matrix(rotation_matrix)
                quat = r.as_quat()

                roll_x, pitch_y, yaw_z = euler_from_quaternion(*quat)
                roll_x, pitch_y, yaw_z = map(math.degrees, (roll_x, pitch_y, yaw_z))

                print(f"ArUco ID: {marker_id_int}")  # Print ArUco ID
                print(f"Translation: X={transform_translation_x}, Y={transform_translation_y}, Z={transform_translation_z}")
                print(f"Rotation (Euler): Roll={roll_x}, Pitch={pitch_y}, Yaw={yaw_z}\n")

                # Draw the axes
                cv2.drawFrameAxes(frame, mtx, dst, rvecs[i], tvecs[i], 0.05)

        # Display the frame
        cv2.imshow('frame', frame)

        # Quit if "q" is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    print(__doc__)
    main()
