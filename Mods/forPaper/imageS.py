# Python program to explain cv2.putText() method

# importing cv2
import cv2

# path
path = "s1.jpg"

# Reading an image in default mode
# image = cv2.imread(path)
cap = cv2.VideoCapture(0)
ret, image = cap.read()

# Window name in which image is displayed
window_name = 'Image'

# font
font = cv2.FONT_HERSHEY_SIMPLEX

# org
org = (50, 50)

# fontScale
fontScale = 1

# Blue color in BGR
color = (255, 0, 0)

# Line thickness of 2 px
thickness = 1

# Using cv2.putText() method
image = cv2.putText(image, 'Elbows are in correct position', org, font,
                    fontScale, color, thickness, cv2.LINE_AA)

# Displaying the image
cv2.imshow(window_name, image)
cv2.waitKey(0)
