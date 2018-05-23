import sys
import cPickle
import datetime
import cv2
import boto3
import time
import cPickle
from multiprocessing import Pool
import pytz

#Get the Client
#session = boto3.Session(profile_name='personal')
session = boto3.Session()
rekog_client = session.client("rekognition", region_name='us-east-1')

#Camera Parameters
camera_index = 0
width = 1280
height = 720

# Image details global data (TODO change this for a class), as currently only one face is suported
x1 = None
y1 = None
x2 = None
y2 = None
gender = None
age = None
smile = None
mustache = None
beard = None
emotion = None

"""
Function to send frame to AWS Rekognition
frame: OpenCV/Numpy image
frame_count: variable to control the capture_rate
enable_rekog: Variable for disabling rekognition petition
"""
def send_frame(frame, frame_count, enable_rekog=False):
    try:
        _, buff = cv2.imencode(".jpg", frame)
        img_bytes = bytearray(buff)
        if enable_rekog:
            response = rekog_client.detect_faces(
                Image={
                    'Bytes': img_bytes
                },
                Attributes=['ALL']
            )
    except Exception as e:
        print e
    return response

"""
Function to process the response from AWS Rekognition
response: AWS rekognition response
"""
def get_data(response):
    #Global data (TODO change this for a class), as currently only one face is suported
    global x1
    global y1
    global y2
    global x2
    global gender
    global age
    global smile
    global mustache
    global beard
    global emotion

    #Get the faces
    faces = response['FaceDetails']
    boxes = []
    for face in faces:
        #For each face, get the data
        boxes.append (face['BoundingBox'])
        gender = face['Gender']['Value']
        age = 'Age: ' + str(face['AgeRange']['Low']) + '-' + str(face['AgeRange']['High'])
        smile = 'Smile: ' + str(face['Smile']['Value'])
        mustache = 'Mustache: ' + str(face['Mustache']['Value'])
        beard = 'Beard: ' + str(face['Beard']['Value'])
        emotion_map = find_emotion(face['Emotions'])
        emotion = emotion_map['Type']

    #Get the face bounding box
    for box in boxes:
        x1 = int(box['Left'] * width)
        y1 = int(box['Top'] * height)
        x2 = int(box['Left'] * width + box['Width'] * width)
        y2 = int(box['Top'] * height + box['Height']  * height)

"""
Function find the emotion with max Confidence
emotions: emotion map from AWS response
"""
def find_emotion(emotions):
    num={'Confidence': 0.0, 'Type': None}
    for item in emotions:
        if item['Confidence']>num['Confidence']:
            num=item
    return num


def main():
    #Capture set up
    capture_rate = 30
    cap = cv2.VideoCapture(0)
    pool = Pool(processes=2)
    frame_count = 0
    while True:
        ret, frame = cap.read()
        #Resize the captured image
        frame = cv2.resize(frame, (width, height))

        #If we cannot get the frame, exit
        if ret is False:
            break

        #capture rate for AWS rekognition petition
        if frame_count % capture_rate == 0:
            pool.apply_async(send_frame, (frame, frame_count, True), callback=get_data)      
        frame_count += 1
        
        #if we have data, we draw it (TODO change this buch of variables for a class)
        if x1 != None and y1 != None and x2 != None and y2 != None:
            cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (255,0,0), 2)
            font = cv2.FONT_HERSHEY_COMPLEX_SMALL
            cv2.putText(frame, gender ,(x1,y1 + 20), font, 1,(0,0,0),2,cv2.LINE_AA)
            cv2.putText(frame, age ,(x1,y1 + 40), font, 1,(0,0,0),2,cv2.LINE_AA)
            cv2.putText(frame, smile ,(x1,y1 + 60), font, 1,(0,0,0),2,cv2.LINE_AA)
            cv2.putText(frame, mustache ,(x1,y1 + 80), font, 1,(0,0,0),2,cv2.LINE_AA)
            cv2.putText(frame, beard ,(x1,y1 + 100), font, 1,(0,0,0),2,cv2.LINE_AA)
            cv2.putText(frame, emotion ,(x1,y1 + 120), font, 1,(0,0,0),2,cv2.LINE_AA)
        #Show the frame
        cv2.imshow('frame', frame)
        #Pressing Q for exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    #Release the camera and windows
    cap.release()
    cv2.destroyAllWindows()
    return



if __name__ == '__main__':
    main()