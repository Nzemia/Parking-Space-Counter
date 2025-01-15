import cv2
import pickle
import cvzone
import numpy as np

# Load the image to get its dimensions
image_sample = cv2.imread("CarParking.png")
image_height, image_width, _ = image_sample.shape

# Video feed
cap = cv2.VideoCapture("CarParkingVideo.mp4")

with open("Car Park Positions", "rb") as f:
    positionList = pickle.load(f)

width, height = 35, 15

def check_parking_space(imageProcessed):
    spaceCounter = 0
    for position in positionList:
        x, y = position

        # Crop
        imageCrop = imageProcessed[y:y + height, x:x + width]
        # cv2.imshow(str(x * y), imageCrop)

        # Count the white pixels
        count = cv2.countNonZero(imageCrop)

        # If the count is less than 140, then the parking space is empty
        if count < 140:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        # cv2.rectangle(image, position, (position[0] + width, position[1] + height), (255, 0, 255), 2)
        cv2.rectangle(image, position, (position[0] + width, position[1] + height), color, thickness)

        # text count in rectangles
        cvzone.putTextRect(image, str(count), (x, y + height - 3), scale=0.5, thickness=1, offset=0, colorR=color)


    cvzone.putTextRect(image, f"Free: {spaceCounter}/{len(positionList)}", (100, 50), scale = 3, thickness = 5, offset = 20, colorR=(0, 200, 0))


while True:
    # Loop back to the start of the video on reaching the end
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, image = cap.read()

    # Resize the video frame to match the image dimensions
    image = cv2.resize(image, (image_width, image_height))

    # Convert to grayscale
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageBlur = cv2.GaussianBlur(imageGray, (3, 3), 1)

    # Adaptive thresholding to get the binary image
    imageThreshold = cv2.adaptiveThreshold(imageBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)

    # Median blur to remove noise
    imageMedian = cv2.medianBlur(imageThreshold, 5)

    # Dilate to fill the gaps
    kernel = np.ones((3, 3), np.uint8)
    imageDilate = cv2.dilate(imageMedian, kernel, iterations=1)

    check_parking_space(imageDilate)

    cv2.imshow("Image", image)
    # cv2.imshow("Image Blur", imageBlur)
    # cv2.imshow("Image Threshold", imageThreshold)
    # cv2.imshow("Image Median", imageMedian)

    cv2.waitKey(10)