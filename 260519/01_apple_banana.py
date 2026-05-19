from tkinter import *
from PIL import Image, ImageTk, ImageOps
import sys
import cv2
from tensorflow.keras.models import load_model
import numpy as np
from pathlib import Path    

BASEDIR = Path(__file__).parent

value = None
model = load_model(BASEDIR / "keras_model.h5")
imglabel = []   # 전역 라벨

data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
size = (224, 224)

def readLabels():
    try:
        with open(BASEDIR / "labels.txt", 'r') as f:
            list_labels = []
            for line in f:
                getlabel = line.split(' ')[1].strip()
                list_labels.append(getlabel)
        return list_labels
    except Exception as e:
        print("라벨 파일 오류:", e)
        return ["Unknown"]

def show_frame():
    ret, frame = cap.read()

    # 안정성 체크
    if not ret or frame is None:
        print("프레임 읽기 실패")
        lmain.after(100, show_frame)
        return

    processImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 모델 입력용 이미지
    recog = cv2.resize(processImage, (224, 224))

    # 화면 출력용 이미지
    display = cv2.resize(processImage, (640, 480))
    display = Image.fromarray(display)
    display = ImageTk.PhotoImage(image=display)

    lmain.processImage = display
    lmain.configure(image=display)

    # 모델 전처리
    recog = Image.fromarray(recog)
    recog = ImageOps.fit(recog, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(recog)

    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array

    # 예측
    prediction = model.predict(data, verbose=0)

    obj = [int(i * 1000) / 10 for i in prediction[0]]

    idx = obj.index(max(obj))
    label = imglabel[idx] if idx < len(imglabel) else "Unknown"

    value.set(f"{label} {max(obj)} %")

    lmain.after(10, show_frame)  # 너무 빠르지 않게 조정


try:
    root = Tk()
    root.title('Camera')
    root.geometry("640x520+10+10")

    # 라벨 미리 로딩 (중요)
    imglabel = readLabels()

    lmain = Label(root)
    lmain.pack()

    value = StringVar()
    value.set("텍스트")
    msg = Label(root, background="yellow", textvariable=value)
    msg.pack()

    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture("http://localhost:8090/?action=stream")

    ret, frame = cap.read()
    if not ret or frame is None:
        print("카메라 연결 실패")
        sys.exit()

    show_frame()
    root.mainloop()

except KeyboardInterrupt:
    sys.exit()