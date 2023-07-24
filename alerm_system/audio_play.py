import cv2
import numpy as np
import sounddevice as sd
import wave
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
import pyaudio

# Constants for audio recording
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 100  # Adjust the recording duration as needed
WAVE_OUTPUT_FILENAME = "output_audio.wav"
audio_frames = []

def record_start():
    global audio_frames
    print("Recording audio...")
    audio_frames = sd.rec(int(RATE * RECORD_SECONDS), samplerate=RATE, channels=CHANNELS, dtype='int16')


def record_end():
    global audio_frames
    sd.wait()
    print("Recording finished!")

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)  # 2 bytes per sample (16-bit audio)
    wf.setframerate(RATE)
    wf.writeframes(audio_frames.tobytes())
    wf.close()
def record_webcam_with_audio(output_file, resolution=(640, 480), fps=30.0):
    # Start capturing from the webcam
    capture = cv2.VideoCapture(0)

    # Get the video frame dimensions
    frame_width = int(capture.get(3))
    frame_height = int(capture.get(4))

    # Create video writer object to save the frames as MP4 video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    # Record audio using sounddevice
    record_start()

    while True:
        # Read a frame from the webcam
        ret, frame = capture.read()
        if not ret:
            break

        # Write the frame to the output video file
        out.write(frame)

        # Display the live frame
        cv2.imshow('Live Webcam', frame)

        # Press 'q' to stop recording
        if cv2.waitKey(1) & 0xFF == ord('q'):
            record_end()
            break

    # Release the video writer and webcam capture
    out.release()
    capture.release()
    cv2.destroyAllWindows()

    # Create a video clip with the recorded video frames
    audio = AudioFileClip(WAVE_OUTPUT_FILENAME)
    video = VideoFileClip(output_file)

    # Create a composite video clip with video and audio
    composite_clip = CompositeVideoClip([video.set_audio(audio)])

    # Write the final video with audio to a file
    composite_clip.write_videofile(output_file, codec='libx264', audio_codec='aac')

if __name__ == "__main__":
    output_file = "output_video_with_audio.mp4"
    record_webcam_with_audio(output_file)
