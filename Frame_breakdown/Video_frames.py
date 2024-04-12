import cv2
import os
import math

def extract_frames(video_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    cap = cv2.VideoCapture(video_path)

    # Get total number of frames
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate interval to get 500 frames
    interval = math.ceil(total_frames / 500)

    frame_count = 0
    saved_frames = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Check if current frame is part of the subset
        if frame_count % interval == 0:
            # Save frame to output directory
            frame_path = os.path.join(output_dir, f"frame_{saved_frames}.jpg")
            cv2.imwrite(frame_path, frame)
            saved_frames += 1

        if saved_frames >= 500:
            break

        frame_count += 1

    cap.release()

video_path = "test.mp4"
output_dir = "output_frames"
extract_frames(video_path, output_dir)
