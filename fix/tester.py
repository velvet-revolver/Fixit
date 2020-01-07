import cv2
import numpy as np
from PIL import ImageGrab
import autopy


def mouseevents(event, x, y, flags, param):
    global LBtn, RB, LB, CB, xi, yi
    if event == cv2.EVENT_RBUTTONDOWN:
        RB = 1
        xi = ((x * 1920) / 1366)
        yi = ((y * 1080) / 768)

        print(x, y)
        print(xi,yi)
        autopy.mouse.move(xi, yi)



    elif event == cv2.EVENT_LBUTTONDOWN:
        LB = 1

    elif event == cv2.EVENT_MBUTTONDOWN:
        CB = 1


img2 = ImageGrab.grab()
img_np = np.array(img2)

while True:
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

    cv2.imshow("test", frame)
    cv2.namedWindow('test')
    cv2.setMouseCallback('test', mouseevents)

    key = cv2.waitKey(25) & 0xFF

    if key == ord('q'):
        exist = False
        signal = 0
        cv2.destroyAllWindows()
