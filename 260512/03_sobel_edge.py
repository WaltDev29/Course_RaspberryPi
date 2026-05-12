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

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edge = cv2.Sobel(gray, -1, 1, 0)
    cv2.imshow('edge', edge)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break 

cap.release()
cv2.destroyAllWindows()