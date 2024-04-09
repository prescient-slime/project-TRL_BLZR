
import cv2
import os

def extract_frames(video_path, output_dir):
    # Create output directory if not exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate interval
    interval = total_frames // 500
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        # Check if it's time to save a frame
        if frame_count % interval == 0:
            frame_name = f"frame_{frame_count:04d}.jpg"
            cv2.imwrite(os.path.join(output_dir, frame_name), frame)

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = "your_video_file.mp4"
    output_directory = "subset_frames"

    extract_frames(video_path, output_directory)
