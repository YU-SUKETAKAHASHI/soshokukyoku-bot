import cv2
import numpy as np
import subprocess
import time
from flask import flash
from flask import Flask, request, redirect, url_for

SAVE_PATH = "./input"
filepath ="face.jpg"
#face_detect_count = 0
#count = 1
face_cascade = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./models/haarcascade_eye.xml')



cap = cv2.VideoCapture(0)#引数を0にすると、webカメラが起動するらしい
while True:
    #time1 = time.clock()
    ret, img = cap.read()
    img = cv2.flip(img, 1)#反転
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("img",img)
    faces = face_cascade.detectMultiScale(gray, 1.9, 5)#顔として認識した正方形の左上の座標がx,yに、左上の点から右下の点までの距離がw,hに格納されている
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)#画像に描き込み　第二引数に正方形の左上、第三引数に右下、第四引数に線の色、第四に線の太さ
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

        #if time1/count > 10:
        for rect in faces:
                # 切り取った画像出力
            cv2.imwrite(SAVE_PATH + "/" + filepath, img[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]])

                #face_detect_count = face_detect_count + 1
            #subprocess.check_call(['python','webup.py'])
            subprocess.check_call(['python','detect_push.py'])
                #end_time = time.clock()
            #print(time1)
                #count += 1

            time.sleep(10)

            cv2.imshow("img",img)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    if cv2.waitKey(30) == 27:
        break
# キャプチャをリリースして、ウィンドウをすべて閉じる
cap.release()
cv2.destroyAllWindows()
#
