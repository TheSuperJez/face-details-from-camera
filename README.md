# Python AWS face details
* This is a PROOF OF CONCEPT for capturing data from web cam and processing it using AWS rekognition and OpenCV.
* There are some issue, that might (or might not) will be fixed, such as multi face detection.

## Installing dependencies
```
pip2 install -r requirements.txt
```

## Running
```
python2 main2.py
```

## Requeriments (install-deps.sh)
```
Python 2.7
pip
dlib
awscli
```

## Known Issues
* The program only stores/displays data for one face
* It has some delay because of the AWS Rekognition petition (It could be improved using AWS Kinesis)
