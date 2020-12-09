import face_recognition
import cv2
import pygame
from transitions import Machine
import time

picture_of_me = face_recognition.load_image_file("me.png")
my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

class FSM(object):
    states = ['MachineActive', 'MachineInactive']
    def __init__(self,name):
        self.name = name
        self.machine = Machine(model=self, states=FSM.states, initial='MachineInactive')
        self.machine.add_transition(trigger='identified', source = 'MachineInactive', dest = 'MachineActive')
        self.machine.add_transition(trigger='not_identified', source = 'MachineActive', dest = 'MachineInactive')
       
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False
pygame.init()
height,width,channel = frame.shape
screen = pygame.display.set_mode((width, height))
font = pygame.font.SysFont(None, 50)
img1 = font.render('Sneh', True, (0,0,0))
img2 = font.render('Unknown',True,(0,0,0))
img3 = font.render('Application is inactive',True,(0,0,0))
recognizer = FSM("Machine")
while rval:
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frame1 = frame.swapaxes(0, 1)
    pygame.surfarray.blit_array(screen, frame1)
    pygame.display.update()
    face_locations = face_recognition.face_locations(frame)
    if len(face_locations)>0:
        if recognizer.state == 'MachineInactive':
            recognizer.identified()
        unknown_face_encoding = face_recognition.face_encodings(frame,face_locations)    	
        results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding[0])
        if results[0] == True:
            screen.blit(img1,(face_locations[0][2],(face_locations[0][3]+face_locations[0][1])/2))
            pygame.display.update()
        else:
            screen.blit(img2,(face_locations[0][2],(face_locations[0][3]+face_locations[0][1])/2))
            pygame.display.update()

    else:
    	if recognizer.state =='MachineActive':
            recognizer.not_identified()
            screen.blit(img3,(width/2,height/2))
            pygame.display.update()
    time.sleep(1)
    rval, frame = vc.read()
vc.release()