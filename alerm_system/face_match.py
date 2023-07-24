import cv2
import imutils
from deepface import DeepFace


def match_faces_live(ref_image_path):
    # Load the reference image
    reference_image = cv2.imread(ref_image_path)

    # Get the face embeddings for the reference image
    # reference_face_embedding = DeepFace.represent(reference_image, model_name='Facenet', enforce_detection=False)

    capture = cv2.VideoCapture(0)

    while True:
        _, frame = capture.read()

        # Resize the frame for faster processing
        frame = imutils.resize(frame, width=500)

        # Perform face detection and extract faces using DeepFace with 'ssd' backend
        # detected_faces = DeepFace.extract_faces(frame)

        result = DeepFace.verify(frame, reference_image.copy(), enforce_detection=False)
        print(result['verified'])
        # Display the frame with annotations
        cv2.imshow('Live Face Matching', frame)

        # Press 'q' to quit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    reference_image_path = 'ref.jpg'  # Replace with your reference image path
    match_faces_live(reference_image_path)
