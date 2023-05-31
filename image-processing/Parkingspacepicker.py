import cv2
import pickle
# created a variable img and embedded the image
# img=cv2.imread('carParkImg.png')


width, height = 107, 48
try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)

except:
    posList = []


def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1+width and y1 < y < y1+height:
                posList.pop(i)

    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)


# while loop for marking vacant spaces
while True:
    img = cv2.imread('carParkImg.png')

    for pos in posList:
        # rectangle function to mark values 1.image,co-ordinates,co-ordinates,color,thickness
        # cv2.rectangle(img,(50,192),(157,240),(255,0,255),2)
        cv2.rectangle(
            img, pos, (pos[0]+width, pos[1]+height), (255, 0, 255), 2)

    # codmmee to display the image
    cv2.imshow("image", img)
    cv2.setMouseCallback("image", mouseClick)

    # delay to show the image
    cv2.waitKey(1)
