import cv2
vidcap = cv2.VideoCapture('GSearch2.avi')
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite("frame%05d.jpg" % count, image)     # save frame as JPEG file      
  success,image = vidcap.read()
  print('Read a new frame: ', success, str(count))
  count += 1
