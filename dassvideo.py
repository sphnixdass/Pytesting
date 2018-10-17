#https://docs.opencv.org/3.4/d0/d86/tutorial_py_image_arithmetics.html
import cv2
import os

image_folder = 'images'
video_name = 'video.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
images = sorted(images)
print(images)
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, -1, 12.0, (width,height))

for image in images:
    print(image)
    #font = cv2.FONT_HERSHEY_SIMPLEX
    #cv2.putText(image,'GCS POC by ISOL team',(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)
    video.write(cv2.imread(os.path.join(image_folder, image)))
    

cv2.destroyAllWindows()
video.release()
