import cv2
import sys
imagePath = 'phpG8nhM8.jpg'
face_cascade = cv2.CascadeClassifier('/Users/pangguangde/Downloads/opencv-3.0.0/data/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/Users/pangguangde/Downloads/opencv-3.0.0/data/haarcascades/haarcascade_eye.xml')
# faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") 
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.15,
    minNeighbors=5,
    minSize=(5,5),
    flags=cv2.CASCADE_SCALE_IMAGE 
) 
print "Found {0} faces!".format(len(faces))
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2) 
cv2.imshow("Faces found", image)
cv2.waitKey(0)