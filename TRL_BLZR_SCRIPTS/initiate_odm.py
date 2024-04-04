import os
import subprocess

def initiate_odm(input_folder, output_folder):
    odm_command = f"docker run -v {os.path.abspath(input_folder)}:/code/images -v {os.path.abspath(output_folder)}:/code/odm_orthophoto opendronemap/odm"

    try:
        subprocess.run(odm_command, shell=True, check=True)
        print("ODM processing complete.")
    except subprocess.CalledProcessError as e:
        print(f"OpenDroneMap processing failed: {e}")

if __name__ == "__main__":
    input_folder = "/path/to/video"
    odm_output_directory = "/path/to/output/folder"

    initiate_odm(input_folder, odm_output_directory)