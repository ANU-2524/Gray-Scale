import cv2 
# Code to capture only one frame from webcam with having grey scale effect !!

# capp = cv2.VideoCapture(0)
# read , frame = capp.read()
# grayy = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
# cv2.imwrite("grayy_imagee.png" , grayy)
# cv2.imshow("Grayy Imagee" , grayy) # clicked image show on screen 
# cv2.waitKey(0) # waits until any key get pressed ! 
# cv2.destroyAllWindows()
# capp.release()

# ---*--*--*--- #

# To make connection with webcam and 0 for the choice of camera.
cappp = cv2.VideoCapture(0)

# Checking , webcam opened or not. In case of error , it get exit !
if not cappp.isOpened() :
    print("Error Occured : Camera is not accessible !")
    exit() 
    
while True :
    read , frame = cappp.read() 
    if not read :
        print("Error Occured : Failed to read frame !")
        break 
    # cv2.cvtColor() function used to convert color space of the image !
    grayyy = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
    cv2.imshow("Grayyy Video" , grayyy )
    key = cv2.waitKey(1) & 0xFF
    if (key == ord('q')) :
        print("Camera closed !")
        exit()
    if (key == ord('s')) :
        cv2.imwrite("Grayyy_Video_Frame.png" , grayyy)
        print("Grayyy Video Frame Saved !!!")
    
        
cappp.release() 
cappp.destroyAllWindows()