import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

################################
wCam, hCam = 640, 480
################################

cap = cv2.VideoCapture(0)  # change number based on device
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.HandDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
current_volume = volume.GetMasterVolumeLevel()

#thresholds
MIN_DISTANCE = 50  
MAX_DISTANCE = 300  
volBar = 400

while True:
    success, img = cap.read()
    if not success:
        print("Error: Couldn't read frame.")
        break

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) >= 9:  
        # Thumb tip
        x1, y1 = lmList[4][1], lmList[4][2]
        # Index tip
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)


        length = math.hypot(x2 - x1, y2 - y1)

        if length < MIN_DISTANCE:
            # Increase volume
            if current_volume < maxVol:  
                current_volume += 1.0
                volume.SetMasterVolumeLevel(current_volume, None)
                print("Volume Up")
        elif length > MAX_DISTANCE:
            # Decrease volume
            if current_volume > minVol:  
                current_volume -= 1.0
                volume.SetMasterVolumeLevel(current_volume, None)
                print("Volume Down")

        volBar = np.interp(current_volume, [minVol, maxVol], [400, 150])
        volPer = np.interp(current_volume, [minVol, maxVol], [0, 100])

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    else:
        print("No hand detected or insufficient landmarks. Length of lmList:", len(lmList))
        volBar = np.interp(current_volume, [minVol, maxVol], [400, 150])
        volPer = np.interp(current_volume, [minVol, maxVol], [0, 100])

    # Volume bar
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
