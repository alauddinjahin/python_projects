import cv2
import numpy as np
import sounddevice as sd
from pydub import AudioSegment
import wave
import pyaudio

# Constants for audio recording
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 100  # Adjust the recording duration as needed
WAVE_OUTPUT_FILENAME = "output_audio.mp3"


def record_audio():
    print("Recording audio...")
    audio_frames = sd.rec(int(RATE * RECORD_SECONDS), samplerate=RATE, channels=CHANNELS, dtype='int16')
    sd.wait()
    print("Recording finished!")

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)  # 2 bytes per sample (16-bit audio)
    wf.setframerate(RATE)
    wf.writeframes(audio_frames.tobytes())
    wf.close()

def play_audio():
    audio = AudioSegment.from_mp3(WAVE_OUTPUT_FILENAME)
    audio.play()

def record_webcam_with_audio(output_file, resolution=(640, 480), fps=30.0):
    # Start capturing from the webcam
    capture = cv2.VideoCapture(0)

    # Get the video frame dimensions
    frame_width = int(capture.get(3))
    frame_height = int(capture.get(4))

    # Create video writer object to save the frames as MP4 video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    # Record audio using sounddevice
    record_audio()

    while True:
        # Read a frame from the webcam
        ret, frame = capture.read()
        if not ret:
            break

        # Write the frame to the output video file
        out.write(frame)

        # Display the live frame
        cv2.imshow('Live Webcam', frame)

        # Press 'q' to stop recording and playback the audio
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video writer and webcam capture
    out.release()
    capture.release()
    cv2.destroyAllWindows()

    # Playback the recorded audio
    play_audio()


if __name__ == "__main__":
    output_file = "output_video_with_audio.mp4"
    record_webcam_with_audio(output_file)
