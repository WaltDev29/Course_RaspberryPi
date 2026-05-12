import cv2

cap = cv2.VideoCapture("http://192.168.25.227:8090/?action=stream")

if not cap.isOpened():
    print("Cannot open camera")
    exit()


while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break 

cap.release()
cv2.destroyAllWindows()