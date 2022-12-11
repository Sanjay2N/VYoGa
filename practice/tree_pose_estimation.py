import cv2
import threading 
from PIL import Image
import numpy as np 
import mediapipe as mp 
from keras.models import load_model 
from playsound import playsound


def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle

def rleg_angle(pose_list):
    pt27x , pt27y = pose_list[27*2],pose_list[(27*2)+1]
    pt25x , pt25y = pose_list[25*2],pose_list[(25*2)+1]
    pt23x , pt23y = pose_list[23*2],pose_list[(23*2)+1]    
    return calculate_angle([pt27x,pt27y],[pt25x,pt25y],[pt23x,pt23y])

def lleg_angle(pose_list):
    pt28x , pt28y = pose_list[28*2],pose_list[(28*2)+1]
    pt26x , pt26y = pose_list[26*2],pose_list[(26*2)+1]
    pt24x , pt24y = pose_list[24*2],pose_list[(24*2)+1]
    return calculate_angle([pt28x,pt28y],[pt26x,pt26y],[pt24x,pt24y])
cou = 0
mcount=0
Carray=[0,0]
prev=0
mpPose = mp.solutions.pose
pose =mpPose.Pose(model_complexity=0)
drawing = mp.solutions.drawing_utils

model  = load_model("practice\model_vrikshasana.h5")
label = np.load("practice\labels_vrikshasana.npy")
#modified
mpPoseobj = mp.solutions.pose
spose = mpPoseobj.Pose(static_image_mode=False)
image = cv2.imread(r"static\practice\tree\tree.jpg")

image_input = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# get results using mediapipe
static_res = spose.process(image_input)
actual_pose_list = []
if static_res.pose_landmarks:
            for i in static_res.pose_landmarks.landmark:
                actual_pose_list.append(i.x)
                actual_pose_list.append(i.y)
else:
    print("Image Is Not Clear")

actual_rleg = rleg_angle(actual_pose_list)
actual_lleg = lleg_angle(actual_pose_list)
#end 
def Pose_video_tree( frame):
    global cou,mcount,Carray,prev
    
    def inFrame(lst):
        if lst[28].visibility > 0.6 and lst[27].visibility > 0.6 and lst[15].visibility>0.6 and lst[16].visibility>0.6:
            return True 
        
        return False
    lst = []
    
    frm = cv2.flip(frame, 1)
    frm=cv2.resize(frm, (600, 600),interpolation = cv2.INTER_NEAREST)
        
    res =pose.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

   
    webcam_list = []
    if res.pose_landmarks and inFrame(res.pose_landmarks.landmark):
        for i in res.pose_landmarks.landmark:
            lst.append(i.x - res.pose_landmarks.landmark[0].x)
            lst.append(i.y - res.pose_landmarks.landmark[0].y)
            webcam_list.append(i.x)
            webcam_list.append(i.y)

        lst = np.array(lst).reshape(1,-1)

        p = model.predict(lst)
        pred = label[np.argmax(p)]

        if p[0][np.argmax(p)] > 0.75:
            cou+=1
            cv2.putText(frm, pred , (50,30),cv2.FONT_ITALIC, 1, (125, 6, 6),3)
            if(pred!="Nothing"):
                if(cou%5==0):
                    rleg = rleg_angle(webcam_list)
                    lleg = lleg_angle(webcam_list)
                    
                    if(lleg<actual_lleg and lleg<(actual_lleg-20) ):
                        Carray[0]+=1
                        if prev!=0:
                            Carray[prev]=0
                            prev=0
                        
                        if Carray[0]%4==0:
                            Carray[0]=0
                            t2 = threading.Thread(target=playsound, args=(r"static\practice\tree\tree_l_leg.mp3",))
                            t2.start()

                    if(rleg>actual_rleg and rleg>(actual_rleg+40)):
                        Carray[1]+=1
                        if prev!=1:
                            Carray[prev]=0
                            prev=1
                        if Carray[1]%4==0:
                            Carray[1]=0
                            t3 = threading.Thread(target=playsound, args=(r"static\practice\tree\tree_r_leg.mp3",))
                            t3.start()
                    cou=0

            else:
                Carray=[0,0]
        drawing.draw_landmarks(frm, res.pose_landmarks, mpPose.POSE_CONNECTIONS,
                            connection_drawing_spec=drawing.DrawingSpec(color=(255,255,255), thickness=6 ),
                            landmark_drawing_spec=drawing.DrawingSpec(color=(0,0,255), circle_radius=3, thickness=3))

        mcount=0
    else:
        mcount+=1
        if mcount%70==0:
            mcount=0
            t1=threading.Thread(target=playsound,args=(r"static\bodyfit.mp3",))
            t1.start()
    
    
    return frm,True


 






