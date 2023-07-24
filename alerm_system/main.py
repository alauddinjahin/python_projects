import threading
import winsound
import cv2
import imutils
from deepface import DeepFace

WEBCAM_RAW_RES = (640, 480)
FRAMERATE = 20
# https://github.com/NeuralNine/youtube-tutorials/blob/main/Live%20Face%20Recognition/main.py
capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

_, start_frame = capture.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

alarm = False
alarm_mode = False
alarm_count = 0

reference_img = cv2.imread("ref.jpg")
face_match = False
counter = 0


#
# def check_face(frame):
#     global face_match
#
#     try:
#         if DeepFace.verify(frame, reference_img.copy(), enforce_detection=False)['verified']:
#             face_match = True
#         else:
#             face_match = False
#     except ValueError:
#         face_match = False


def beep_alarm():
    global alarm
    global alarm_mode
    global face_match

    for _ in range(5):
        if not alarm_mode:
            break

        if not face_match:
            winsound.Beep(2500, 1000)
            print('Alarm', alarm_mode)

    alarm = False


def motion_detection():
    global alarm_count
    global alarm
    global start_frame
    global counter
    global face_match
    global reference_img

    while True:
        _, frame = capture.read()
        frame = imutils.resize(frame, width=500)

        if counter % 50 == 0:
            try:
                result = DeepFace.verify(frame, reference_img.copy(), enforce_detection=False)
                if result['verified']:
                    face_match = True
                else:
                    face_match = False
            except ValueError:
                face_match = False

        counter += 1

        toggle_alarm_by_face_detection(False if face_match else True)

        # if counter % 30 == 0:
        # try:
        #     threading.Thread(target=check_face, args=(frame.copy(),)).start()
        # except ValueError:
        #     pass

        # counter += 1

        if alarm_mode:
            # frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
            frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_bw = cv2.GaussianBlur(frame_bw, (21, 21), 0)

            difference = cv2.absdiff(frame_bw, start_frame)
            threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
            start_frame = frame_bw

            if threshold.sum() > 300:
                alarm_count += 1
            else:
                if alarm_count > 0:
                    alarm_count -= 1

            cv2.imshow('Camera', threshold)

        else:
            cv2.imshow('Camera', frame)

        # if not face_match:
        if alarm_count > 20:
            print(face_match, 'face_match')

            if not alarm:
                alarm = True
                threading.Thread(target=beep_alarm).start()

        key_pressed = cv2.waitKey(30)

        if key_pressed == ord('t'):
            toggle_alarm()

        if key_pressed == ord('q'):
            exit_program()


def toggle_alarm():
    global alarm_mode
    global alarm_count
    alarm_mode = not alarm_mode
    alarm_count = 0


def toggle_alarm_by_face_detection(mode=False):
    global alarm_mode
    alarm_mode = mode
    # print(mode,'mode')


def exit_program():
    global alarm_mode
    capture.release()
    cv2.destroyAllWindows()
    alarm_mode = False


if __name__ == "__main__":
    motion_detection()
