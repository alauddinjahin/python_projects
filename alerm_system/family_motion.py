import cv2
import imutils
import dlib
# https://github.com/NeuralNine/youtube-tutorials/blob/main/Live%20Face%20Recognition/main.py
def motion_detection_webcam():
    global some_threshold;
    capture = cv2.VideoCapture(0)

    _, prev_frame = capture.read()
    prev_frame = imutils.resize(prev_frame, width=500)
    prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    prev_frame = cv2.GaussianBlur(prev_frame, (21, 21), 0)

    face_detector = dlib.get_frontal_face_detector()

    while True:
        _, current_frame = capture.read()

        if current_frame is None:
            break

        current_frame = imutils.resize(current_frame, width=500)
        gray_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        difference = cv2.absdiff(prev_frame, gray_frame)
        _, threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > some_threshold:
                # Motion detected in this region, perform necessary actions
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(current_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Check if any faces are present in the region
                region_with_motion = current_frame[y:y + h, x:x + w]
                region_gray = cv2.cvtColor(region_with_motion, cv2.COLOR_BGR2GRAY)

                # Perform face detection in the region
                faces = face_detector(region_gray)

                if len(faces) == 0:
                    # No faces detected, trigger motion alert
                    print("Motion Alert! No family members in the frame.")

        cv2.imshow('Motion Detection', current_frame)

        prev_frame = gray_frame.copy()

        if cv2.waitKey(30) == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

# if __name__ == "__main__":
    some_threshold = 1000  # Adjust this threshold to detect significant motion regions
    motion_detection_webcam()
