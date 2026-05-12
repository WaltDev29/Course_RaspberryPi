from tkinter import *
from PIL import Image, ImageTk, ImageFilter, ImageOps
import time
import threading
import cv2
import random
from tensorflow.keras.models import load_model
import numpy as np
from pathlib import Path    

BASEDIR = Path(__file__).parent/"models"


value= None
model = load_model(BASEDIR/"keras_model.h5")
data = np.ndarray(shape = (1,224,224,3), dtype = np.float32)
size = (224,224)

def readLabels():
    try:
        f = open(BASEDIR/"labels.txt", 'r')
        list_labels = []
        while True:
            line = f.readline()
            if not line: break
            getlabel = line.split(' ')
            getlabel = getlabel[1].split('\n')
            list_labels.append(getlabel[0])
        f.close()
    except Exception as e:
        print(e)
    return list_labels


def show_frame():
    ret, frame = cap.read()
    processImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    recog = cv2.resize(processImage, (224,224))

    processImage = cv2.resize(processImage, (640, 480))
    processImage = Image.fromarray(processImage)
    processImage = ImageTk.PhotoImage(image=processImage)
    lmain.processImage = processImage
    lmain.configure(image=processImage)
    recog = Image.fromarray(recog)
    recog = ImageOps.fit(recog, size, Image.ANTIALIAS)
    image_array = np.asarray(recog)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    imglabel = readLabels()
    obj = []
    for i in prediction[0]:
        v = int(float(i)*1000)/10
        obj.append(v)
    value.set(imglabel[int(obj.index(max(obj)))] + " " + str(max(obj)) + " %")

    #prediction = str(random.randrange(1,10))
    #value.set(str(prediction))
    lmain.after(1, show_frame)

try:
    root = Tk()         
    root.title('Camera')
    root.geometry("640x520+10+10")

    lmain = Label(root)
    lmain.pack()

    value = StringVar()
    value.set("텍스트")
    msg = Label(root, background="yellow", textvariable= value)
    msg.pack()

    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture("http://localhost:8090/?action=stream")
    
    show_frame()
    root.mainloop()           
except KeyboardInterrupt:
    sys.exit()

