from django.shortcuts import render, redirect
import os
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

from .models import trialProducts
# Create your views here.
# def try_on(request):
    
#     return render(request, 'tryon.html')


def try_on(request):
    if request.method == 'GET':
        trialProds = trialProducts.objects.all()
        return render(request, 'tryon.html', {"trialProds" : trialProds})
    else:
        # product = request.POST.get('product')
        product = request.POST.get('product')
        tryprod = trialProducts.objects.get(id = product)
        shirtPath = tryprod.image
        shirtPath = str(shirtPath)
        print("this iso static path....", shirtPath)
        tryon_shirt(shirtPath)


        return redirect ('try_on')







def tryon_shirt(shirtPath):
    # webcam video capture
    cap = cv2.VideoCapture(0)
    detector = PoseDetector()
    fixedRatio = 262/190 # already checked shirt width and shoulder point distance    then calculated ratio
    shirtRatioHeightWidth = 581 / 440 # dimension of shirt image
    # to running a wabcam
    while cap.isOpened():
        success, img = cap.read()
        # find pose on image
        img = detector.findPose(img, draw=False)
        # img = pose.pose_detector.drawPose(img, None)

        # give landmark points, draw a border around the pose
        lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
        # if pose detected
        if lmList:
                lm11 = lmList[11][1:3] # right shoulder x,y cordinates
                lm12 = lmList[12][1:3] # left shoulder x,y cordinates

                imgShirt = cv2.imread(shirtPath,cv2.IMREAD_UNCHANGED)
                weidthOfShort = int((lm11[0]-lm12[0])*fixedRatio)

                imgShirt = cv2.resize(imgShirt,(weidthOfShort, int(weidthOfShort*shirtRatioHeightWidth)))
                currentScale =  (lm11[0] - lm12[0]) / 190
                offset = int(44*currentScale), int(48*currentScale)
                try :
                    # overlay shirt on body image
                    img = cvzone.overlayPNG(img, imgShirt, (lm12[0]-offset[0], lm12[1]-offset[1]))
                except:
                    pass

        cv2.imshow("Image", img)
        k = cv2.waitKey(1) & 0xFF    
        # Check if 'ESC' is pressed and break the loop.
        if(k == 27):
            break

    cap.release()
    cv2.destroyAllWindows() 
