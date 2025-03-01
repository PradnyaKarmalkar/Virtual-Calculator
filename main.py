import cv2
from cvzone.HandTrackingModule import HandDetector

class Button:
    def __init__(self, pos, width, height , value):

        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos,(self.pos[0] + self.width,self.pos[1]+self.height),
                      (225, 225,225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50,50,50),3)

        cv2.putText(img, self.value, (self.pos[0] + 40, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)

    def checkList(self,x,y):
        if self.pos[0] < x < self.pos[0]+self.width and \
                self.pos[1]<y< self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (225, 225, 225), cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (50, 50, 50), 3)

            cv2.putText(img, self.value, (self.pos[0] + 20, self.pos[1] + 70), cv2.FONT_HERSHEY_PLAIN,
                        5, (0, 0, 0), 5)

            return True
        else:
            return False




#webcam
cap = cv2.VideoCapture(0)   # Adjust the camera index as needed, typically 0 or 1
cap.set(3, 1280)
cap.set(4, 720)

# Create a hand detector object
detector = HandDetector(detectionCon=0.8, maxHands=1)  # You can adjust the detection confidence


#Creating Button
buttonListValues=[['7','8','9','*'],
                  ['4','5','6','-'],
                  ['1','2','3','+'],
                  ['0','/','.','=']]
buttonList = []
for x in range(4):
    for y in range(4):
        xpos = x * 100 + 800
        ypos = y * 100 + 150
        buttonList.append(Button((xpos, ypos), 100, 100, buttonListValues[y][x]))

    #Varibles
myEquation = ''
delayCounter = 0


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Find hands in the image
    hands, img=detector.findHands(img, flipType=False)

    #Draw all buttons
    cv2.rectangle(img, (800, 50), (800+400, 70+100),
                  (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (800, 50), (800+400, 70+100),
                  (50, 50, 50), 3)
    for button in buttonList:
        button.draw(img)

    #Check for Hand
    if hands:
        lmlist = hands[0]['lmList']
        print("Hand Landmarks:", lmlist)# Print the hand landmarks for debugging

        # Extract (x, y) coordinates from each hand landmark
        landmark_points = [(lm[0], lm[1]) for lm in lmlist]

        length, _, img = detector.findDistance(landmark_points[8], landmark_points[12], img)
        print("Length:", length)  # Print the length for debugging
        if length < 50:
            x, y = landmark_points[8] # Example: Get the coordinates of the first hand landmark
            for i,button in enumerate(buttonList):
                if button.checkList(x, y) and delayCounter ==0:
                    myValue = buttonListValues[int(i%4)][int(i/4)]
                    if myValue == "=":
                        myEquation = str(eval(myEquation))
                    else:
                        myEquation += myValue
                    delayCounter = 1

            # Pass the coordinates to the checkList method
    if delayCounter !=0:
        delayCounter +=1
        if delayCounter>10:
            delayCounter=0



    #Display the Equation
    cv2.putText(img, myEquation, (810, 120), cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)

    # Display the image with hand landmarks
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('c'):
        myEquation = ''


