import time
import cv2
import numpy as np
import ndsi  # Main requirement
from pupil_detectors import Detector2D

detector = Detector2D()
SENSOR_TYPES = ["video", "gaze"]
SENSORS = {}
SENSORS_NAMES = ["PIM Research Phone", "Gaze", "PI left v1", "PI right v1", "PI world v1"]


def main():
    # Start auto-discovery of Pupil Invisible Companion devices
    network = ndsi.Network(formats={ndsi.DataFormat.V4}, callbacks=(on_network_event,))
    network.start()

    try:
        #
        world_img = np.zeros((1088, 1080, 3))
        left_camera_img = np.zeros((192, 192, 3))
        right_camera_img = np.zeros((192, 192, 3))
        gaze = (0, 0)
        left_center_of_pupil = (0, 0)
        left_axes_of_pupil = (0, 0)
        left_angle_of_pupil = 0
        right_center_of_pupil = (0, 0)
        right_axes_of_pupil = (0, 0)
        right_angle_of_pupil = 0
        previous_left_x_center_of_pupil = 0
        previous_left_y_center_of_pupil = 0
        previous_right_x_center_of_pupil = 0
        previous_right_y_center_of_pupil = 0
        left_gray = None
        right_gray = None
        left_x_difference = 0
        left_y_difference = 0
        right_x_difference = 0
        right_y_difference = 0
        # left_confidence = 0
        # right_confidence = 0
        display_left_x_difference = 0
        display_left_y_difference = 0
        display_left_confidence = 0
        display_right_x_difference = 0
        display_right_y_difference = 0
        display_right_confidence = 0
        left_array = []
        right_array = []
        is_left_pupil_exist = False
        is_right_pupil_exist = False
        left_start_time = time.time()
        right_start_time = time.time()
        overlay_threshold = 5

        # Event loop, runs until interrupted
        while network.running:
            # Check for recently connected/disconnected devices
            if network.has_events:
                network.handle_event()

            # Iterate over all connected devices
            for sensor in SENSORS.values():

                # We only consider gaze and video
                if sensor.type not in SENSOR_TYPES:
                    continue

                # Fetch recent sensor configuration changes,
                while sensor.has_notifications:
                    sensor.handle_notification()

                # Fetch recent gaze data
                for data in sensor.fetch_data():
                    if data is None:
                        continue

                    # Assign the image information to display image
                    if sensor.name == "PI world v1":
                        world_img = data.bgr

                    elif sensor.name == "Gaze":
                        gaze = (int(data[0]), int(data[1]))

                    elif sensor.name == "PI left v1":
                        left_camera_img = data.bgr
                        left_gray = cv2.cvtColor(left_camera_img, cv2.COLOR_BGR2GRAY)

                    elif sensor.name == "PI right v1":
                        right_camera_img = data.bgr
                        right_gray = cv2.cvtColor(right_camera_img, cv2.COLOR_BGR2GRAY)

            # Detect the pupil from input image
            if left_gray is not None:
                result = detector.detect(left_gray)
                ellipse = result["ellipse"]
                # axes_of_pupil = tuple(int(v / 2) for v in ellipse["axes"])
                # if len(axes_of_pupil) == 2 and axes_of_pupil[0] is not 0:
                #     axe_ratio = axes_of_pupil[1] / axes_of_pupil[0]
                # else:
                #     axe_ratio = 0
                center_of_pupil = ellipse["center"]
                x_center_of_pupil = 0
                y_center_of_pupil = 0
                if len(center_of_pupil) == 2:
                    x_center_of_pupil = center_of_pupil[0]
                    y_center_of_pupil = center_of_pupil[1]
                    left_x_difference = previous_left_x_center_of_pupil - x_center_of_pupil
                    left_y_difference = previous_left_y_center_of_pupil - y_center_of_pupil
                    previous_left_x_center_of_pupil = x_center_of_pupil
                    previous_left_y_center_of_pupil = y_center_of_pupil
                angle_of_pupil = ellipse["angle"]
                left_confidence = result['confidence']
                # diameter_of_pupil = result["diameter"]

                # Define the conditions to remove false position detection
                # between_angle = 80 <= angle_of_pupil <= 100
                is_correct_location = (90 <= x_center_of_pupil <= 160) and (35 <= y_center_of_pupil <= 115)
                is_overlay_center_of_pupil = (-overlay_threshold <= left_x_difference <= overlay_threshold) and \
                                             (-overlay_threshold <= left_y_difference <= overlay_threshold)
                # if axe_ratio >= 1.1 and is_overlay_center_of_pupil and diameter_of_pupil >= 12 \
                #         and is_correct_location and left_confidence >= 0.6:

                # When all conditions are true, add the information into array to be used with timer
                if is_correct_location and is_overlay_center_of_pupil and left_confidence >= 0.6:
                    left_center_of_pupil = tuple(int(v) for v in ellipse["center"])
                    left_axes_of_pupil = tuple(int(v / 2) for v in ellipse["axes"])
                    left_angle_of_pupil = angle_of_pupil
                    left_array.append((True, left_x_difference, left_y_difference, left_confidence))
                    left_display = x_center_of_pupil
                else:
                    left_center_of_pupil = (0, 0)
                    left_axes_of_pupil = (0, 0)
                    left_angle_of_pupil = 0
                    left_array.append((False, left_x_difference, left_y_difference, left_confidence))

                # Create timer for time interval to be used in graph
                current_time = time.time()
                time_difference = current_time - left_start_time
                if time_difference >= 0.2:
                    # Reverse the array to check the last pupil detection
                    reverse = left_array[::-1]
                    is_found = False
                    raw_display_left_x_difference = 0
                    raw_display_left_y_difference = 0
                    raw_display_left_confidence = 0
                    for value in reverse:
                        if value[0] is True:
                            raw_display_left_x_difference = value[1]
                            raw_display_left_y_difference = value[2]
                            raw_display_left_confidence = value[3]
                            is_left_pupil_exist = True
                            is_found = True
                            break

                    # If pupil is not found, assign the raw values with first element values
                    if not is_found:
                        raw_display_left_x_difference = left_array[len(left_array) - 1][1]
                        raw_display_left_y_difference = left_array[len(left_array) - 1][2]
                        raw_display_left_confidence = left_array[len(left_array) - 1][3]
                        is_left_pupil_exist = False

                    # Assign display values with the raw values
                    display_left_x_difference = raw_display_left_x_difference
                    display_left_y_difference = raw_display_left_y_difference
                    display_left_confidence = raw_display_left_confidence
                    left_start_time = current_time
                    left_array.clear()

            # Detect the pupil from input image
            if right_gray is not None:
                result = detector.detect(right_gray)
                ellipse = result["ellipse"]
                # axes_of_pupil = tuple(int(v / 2) for v in ellipse["axes"])
                # if len(axes_of_pupil) == 2 and axes_of_pupil[0] is not 0:
                #     axe_ratio = axes_of_pupil[1] / axes_of_pupil[0]
                # else:
                #     axe_ratio = 0
                center_of_pupil = ellipse["center"]
                x_center_of_pupil = 0
                y_center_of_pupil = 0
                if len(center_of_pupil) == 2:
                    x_center_of_pupil = center_of_pupil[0]
                    y_center_of_pupil = center_of_pupil[1]
                    right_x_difference = previous_right_x_center_of_pupil - x_center_of_pupil
                    right_y_difference = previous_right_y_center_of_pupil - y_center_of_pupil
                    previous_right_x_center_of_pupil = x_center_of_pupil
                    previous_right_y_center_of_pupil = y_center_of_pupil
                angle_of_pupil = ellipse["angle"]
                right_confidence = result['confidence']
                # diameter_of_pupil = result["diameter"]

                # Define the conditions to remove false position detection
                # between_angle = 80 <= angle_of_pupil <= 100
                is_correct_location = (90 <= x_center_of_pupil <= 160) and (77 <= y_center_of_pupil <= 157)
                is_overlay_center_of_pupil = (-overlay_threshold <= right_x_difference <= overlay_threshold) and \
                                             (-overlay_threshold <= right_y_difference <= overlay_threshold)
                # if axe_ratio >= 1.1 and is_overlay_center_of_pupil and diameter_of_pupil >= 12 \
                #         and is_correct_location and right_confidence >= 0.6:

                # When all conditions are true, add the information into array to be used with timer
                if is_correct_location and is_overlay_center_of_pupil and right_confidence >= 0.6:
                    right_center_of_pupil = tuple(int(v) for v in ellipse["center"])
                    right_axes_of_pupil = tuple(int(v / 2) for v in ellipse["axes"])
                    right_angle_of_pupil = angle_of_pupil
                    right_array.append((True, right_x_difference, right_y_difference, right_confidence))
                else:
                    right_center_of_pupil = (0, 0)
                    right_axes_of_pupil = (0, 0)
                    right_angle_of_pupil = 0
                    right_array.append((False, right_x_difference, right_y_difference, right_confidence))

                # Create timer for time interval to be used in graph
                current_time = time.time()
                time_difference = current_time - right_start_time
                if time_difference >= 0.2:
                    # Reverse the array to check the last pupil detection
                    reverse = right_array[::-1]
                    is_found = False
                    raw_display_right_x_difference = 0
                    raw_display_right_y_difference = 0
                    raw_display_right_confidence = 0
                    for value in reverse:
                        if value[0] is True:
                            raw_display_right_x_difference = value[1]
                            raw_display_right_y_difference = value[2]
                            raw_display_right_confidence = value[3]
                            is_right_pupil_exist = True
                            is_found = True
                            break

                    # If pupil is not found, assign the raw values with first element values
                    if not is_found:
                        raw_display_right_x_difference = right_array[len(right_array) - 1][1]
                        raw_display_right_y_difference = right_array[len(right_array) - 1][2]
                        raw_display_right_confidence = right_array[len(right_array) - 1][3]
                        is_right_pupil_exist = False

                    # Assign display values with the raw values
                    display_right_x_difference = raw_display_right_x_difference
                    display_right_y_difference = raw_display_right_y_difference
                    display_right_confidence = raw_display_right_confidence
                    right_start_time = current_time
                    right_array.clear()

            # Show world video with gaze overlay
            cv2.circle(
                world_img,
                gaze,
                10, (0, 0, 255), 2
            )

            # Draw ellipse on the pupils if it is detected
            cv2.ellipse(
                left_camera_img,
                left_center_of_pupil,
                left_axes_of_pupil,
                left_angle_of_pupil,
                0, 360,  # start/end angle for drawing
                (0, 0, 255)  # color (BGR): red
            )
            cv2.ellipse(
                right_camera_img,
                right_center_of_pupil,
                right_axes_of_pupil,
                right_angle_of_pupil,
                0, 360,  # start/end angle for drawing
                (0, 0, 255)  # color (BGR): red
            )

            # Define the color of box depends on conditions whether pupil is detected or not
            if is_left_pupil_exist:
                display_color_for_left_box = (0, 255, 0)
            else:
                display_color_for_left_box = (0, 0, 255)
            if is_right_pupil_exist:
                display_color_for_right_box = (0, 255, 0)
            else:
                display_color_for_right_box = (0, 0, 255)

            # Visualizing correct eye position with rectangle boxes
                # cv2.rectangle(left_camera_img, (100, 45), (150, 105), (0, 255, 0), 2)
                # cv2.rectangle(right_camera_img, (100, 87), (150, 147), (0, 255, 0), 2)
                # cv2.rectangle(left_camera_img, (95, 40), (155, 110), display_color_for_left_box, 2)
                # cv2.rectangle(right_camera_img, (95, 82), (155, 152), display_color_for_right_box, 2)
            cv2.rectangle(left_camera_img, (90, 35), (160, 115), display_color_for_left_box, 2)
            cv2.rectangle(right_camera_img, (90, 77), (160, 157), display_color_for_right_box, 2)
            left_image = cv2.rotate(left_camera_img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
            right_image = cv2.rotate(right_camera_img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)

            # Display XError, YError and Confidence
            if left_image is not None:
                if is_left_pupil_exist:
                    left_display_color = (0, 255, 0)
                else:
                    left_display_color = (0, 0, 255)
                cv2.putText(left_image, f"XError  {round(display_left_x_difference, 2)}", (90, 160),
                            cv2.FONT_HERSHEY_TRIPLEX,
                            0.3,
                            left_display_color, 1)
                cv2.putText(left_image, f"YError  {round(display_left_y_difference, 2)}", (90, 170),
                            cv2.FONT_HERSHEY_TRIPLEX,
                            0.3,
                            left_display_color, 1)
                cv2.putText(left_image, f"Confidence  {round(display_left_confidence * 100, 2)}%", (90, 180),
                            cv2.FONT_HERSHEY_TRIPLEX,
                            0.3,
                            left_display_color, 1)
            if left_image is not None:
                if is_right_pupil_exist:
                    right_display_color = (0, 255, 0)
                else:
                    right_display_color = (0, 0, 255)
                cv2.putText(right_image, f"XError  {round(display_right_x_difference, 2)}", (90, 160),
                            cv2.FONT_HERSHEY_TRIPLEX,
                            0.3,
                            right_display_color, 1)
                cv2.putText(right_image, f"YError  {round(display_right_y_difference, 2)}", (90, 170),
                            cv2.FONT_HERSHEY_TRIPLEX,
                            0.3,
                            right_display_color, 1)
                cv2.putText(right_image, f"Confidence  {round(display_right_confidence * 100, 2)}%", (90, 180),
                            cv2.FONT_HERSHEY_TRIPLEX,
                            0.3,
                            right_display_color, 1)

            # Join left and right image side by side
            h_stack = np.hstack((left_image, right_image))
            cv2.imshow("Side Cameras (Left & Right)", h_stack)
            cv2.waitKey(1)

    # Catch interruption and disconnect gracefully
    except (KeyboardInterrupt, SystemExit):
        network.stop()


# This function is to be used as the call back function of main NDSI network
def on_network_event(network, event):
    # Handle gaze sensor attachment
    if event["subject"] == "attach" and event["sensor_type"] in SENSOR_TYPES and event["sensor_name"] in SENSORS_NAMES:
        # Create new sensor and refresh the control
        sensor = network.sensor(event["sensor_uuid"])
        sensor.set_control_value("streaming", True)
        sensor.refresh_controls()

        # Add sensor into SENSORS dictionary
        SENSORS[event["sensor_uuid"]] = sensor
        print(f"Added sensor {sensor}...")

    # Handle gaze sensor detachment
    if event["subject"] == "detach" and event["sensor_uuid"] in SENSORS:
        # Known sensor has disconnected, remove from list
        SENSORS[event["sensor_uuid"]].unlink()
        del SENSORS[event["sensor_uuid"]]
        print(f"Removed sensor {event['sensor_uuid']}...")


main()
