# Python program to explain cv2.line() method

# importing cv2
import cv2


def getPercentageFromAngle(input, max, min):
    return ((input - min) * 100) / (max - min)


def getClrFromPercentage(percentage):
    if percentage > 50:
        red = 1 - 2 * (percentage - 50) / 100.0
    else:
        red = 1.0

    if percentage > 50:
        green = 1.0
    else:
        green = 2 * percentage / 100.0
    blue = 0.0
    return ((int)(blue * 255), (int)(green * 255), (int)(red * 255))


# path
path = r'D:\Shreeram\Core_Coding\ACOLLEGE_PROJ\Refest\Erg\accuracyChecker\s1.jpg'

# Reading an image in default mode
image = cv2.imread(path)

# Window name in which image is displayed
window_name = 'Image'

# Start coordinate, here (0, 0)
# represents the top left corner of image
start_point = (0, 0)

# End coordinate, here (250, 250)
# represents the bottom right corner of image
end_point = (640, 480)

# Green color in BGR

# Line thickness of 9 px
thickness = 9

# Using cv2.line() method
# Draw a diagonal green line with thickness of 9 px

# Displaying the image
cv2.imshow(window_name, image)
cv2.waitKey(10)

while True:
    inpAngle = (int)(input("Enter Inp"))
    minAngle = (int)(input("Enter Min"))
    maxAngle = (int)(input("Enter Max"))
    color = getClrFromPercentage(
        getPercentageFromAngle(inpAngle, maxAngle, minAngle))
    image = cv2.line(image, (0, 0), (640, 480), color, 9)
    cv2.imshow(window_name, image)
    cv2.waitKey(10)

# while True:
#     inpAngle = (int)(input("Enter"))
#     minAngle = (int)(input("Enter"))
#     maxAngle = (int)(input("Enter"))
#     print(getPercentageFromAngle(inpAngle, maxAngle, minAngle))
