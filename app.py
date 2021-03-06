from flask import Flask, Response, render_template
import cv2
import numpy as np

app = Flask(__name__)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
cap = cv2.VideoCapture(0)

@app.route('/')
def index():
    # return "Default Message"
    return render_template("index.html")

def gen(cap):
    while(1):
        ret,img = cap.read()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.3,5)
        for(x,y,w,h) in faces:
            cv2.rectangle(img,(x,y), (x+w,y+h), (255,0,0), 2)
            roi_gray = gray[y:y+h,x:x+w]
            roi_color = img[y:y+h,x:x+w]
            # eyes = eye_cascade.detectMultiScale(roi_gray)
            # for(ex,ey,ew,eh) in eyes:
            #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        ret, jpeg = cv2.imencode('.jpg', img)
        # save frame as JPG file
        frame = jpeg.tobytes()
        # Converting image into bytes
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
# # def index():
    global cap
    return Response(gen(cap),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=2204, threaded=True)
    app.run(debug=True)