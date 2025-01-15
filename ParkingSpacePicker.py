import cv2
import pickle



width, height = 35, 15

# Load the saved positions
try:
    with open("Car Park Positions", "rb") as f:
        positionList = pickle.load(f)
except:
    positionList = []

def mouse_click(events, x, y, flags, params):
    #mark rectangles
    if events == cv2.EVENT_LBUTTONDOWN:
        positionList.append((x, y))

    # delete the unwanted/marked wrong rectangles
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, position in enumerate(positionList):
            x1, y1 = position
            if x1 < x < x1 + width and y1 < y < y1 + height:
                positionList.pop(i)

    with open("Car Park Positions", "wb") as f:
        pickle.dump(positionList, f)





while True:
    image = cv2.imread("CarParking.png")
    for position in positionList:
        cv2.rectangle(image, position, (position[0] + width, position[1] + height), (255, 0, 255), 2)

    cv2.imshow("Image", image)
    cv2.setMouseCallback("Image", mouse_click)
    cv2.waitKey(1)


