import cv2 as cv
import numpy as np

file = open("./Test_ROV_video_h264_full_marks.dat", "r")
cap = cv.VideoCapture("./Test_ROV_video_h264_full.mp4")
frameNum = 0

if (cap.isOpened()== False):  
    print("Some error")

fish = file.readline().split(' ')
fr = fish.pop(0).split('(')[1][3:-1]
width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)

while(cap.isOpened()): 
    ret, frame = cap.read()
    
    if ret == True:   
        if frameNum == int(fr):
            num = int(fish.pop(0))
            writeFile = open("labels/frame%d.txt" % frameNum, 'a+')
            content = ''
            for i in range(num):
                x, y = int(fish.pop(0)), int(fish.pop(0))
                w, h = int(fish.pop(0)), int(fish.pop(0))
                # frame = cv.rectangle(frame, 
                #                     (x, y),
                #                     (x+w, y+h),
                #                     (255, 255, 0), 
                #                     3) 
                content += '0' + ' ' + \
                                str((x + w/2)/width) + ' ' +\
                                str((y + h/2)/height) + ' ' +\
                                str(w/width) + ' ' +\
                                str(h/height) + '\n'
                
            writeFile.write(content)
            writeFile.close()
            # cv.imshow('Frame', frame)
            cv.imwrite("frames/frame%d.jpg" % frameNum, frame)
            
           

            fish = file.readline().split(' ')
            fr = fish.pop(0).split('(')[1][3:-1]
        frameNum += 1
        if cv.waitKey(25) & 0xFF == ord('q'): 
            break

    else: 
        break
  
cap.release() 
cv.destroyAllWindows() 