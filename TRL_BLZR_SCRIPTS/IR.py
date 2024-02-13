from picamera import PiCamera 
import keyboard

#Script for automatic IR footage storage. This will create a single file of video
#and will overwrite previous file once this script is ran again. If we intend to
#store every single flight video, then I propose the creation of a naming standard.

camera.start_preview() #Create a preview window
camera.start_recording('/home/Desktop/video.h264') #Starts recording of IR camera, and saves in given path once done

input("Press enter key to stop recording...")      #Wait for user to hit enter 

camera.stop_recording()                            #Once user has hit enter, stop recording
camera.stop_preview()                              #Kill preview window
print("VIDEO HAS BEEN SAVED AS: video.h264")       #Give user name of video created
