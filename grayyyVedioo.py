import cv2 
capp = cv2.VideoCapture(0)
read , frame = capp.read()
grayy = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
cv2.imwrite("grayy_imagee.png" , grayy)
cv2.imshow("Grayy Imagee" , grayy) # clicked image show on screen 
cv2.waitKey(0) # waits until any key get pressed ! 
cv2.destroyAllWindows()
capp.release() 