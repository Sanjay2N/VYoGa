import cv2
import numpy as np 
import mediapipe as mp 
from keras.models import load_model 
from playsound import playsound
import threading

mcount=0
Carray=[0,0,0,0,0,0,0,0,0,0]
prev=0
cou = 0
vtime=3
mpPose = mp.solutions.pose
pose = mpPose.Pose()
drawing = mp.solutions.drawing_utils

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

def rhand_angle(pose_list):
    pt15x , pt15y = pose_list[15*2],pose_list[(15*2)+1]
    pt13x , pt13y = pose_list[13*2],pose_list[(13*2)+1]
    pt11x , pt11y = pose_list[11*2],pose_list[(11*2)+1]
    return calculate_angle([pt15x,pt15y],[pt13x,pt13y],[pt11x,pt11y])

def lhand_angle(pose_list):
    pt16x , pt16y = pose_list[16*2],pose_list[(16*2)+1]
    pt14x , pt14y = pose_list[14*2],pose_list[(14*2)+1]
    pt12x , pt12y = pose_list[12*2],pose_list[(12*2)+1]
    return calculate_angle([pt16x,pt16y],[pt14x,pt14y],[pt12x,pt12y])

def rhand(pose_list):
    pt23x , pt23y = pose_list[23*2],pose_list[(23*2)+1]
    pt11x , pt11y = pose_list[11*2],pose_list[(11*2)+1]
    pt13x , pt13y = pose_list[13*2],pose_list[(13*2)+1]
    return calculate_angle([pt23x,pt23y],[pt11x,pt11y],[pt13x,pt13y])

def lhand(pose_list):
    pt24x , pt24y = pose_list[24*2],pose_list[(24*2)+1]
    pt12x , pt12y = pose_list[12*2],pose_list[(12*2)+1]
    pt14x , pt14y = pose_list[14*2],pose_list[(14*2)+1]
    return calculate_angle([pt24x,pt24y],[pt12x,pt12y],[pt14x,pt14y])



mpPoseobj = mp.solutions.pose
spose = mpPoseobj.Pose(static_image_mode=False)

image = cv2.imread(r"static\practice\goddess\Utkata_Konasana.jpg")

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
actual_rhand = rhand_angle(actual_pose_list)
actual_lhand = lhand_angle(actual_pose_list)
actual_rhand_arm = rhand(actual_pose_list)
actual_lhand_arm = lhand(actual_pose_list)

def Pose_video_goddess(frame):
    global cou,mcount,Carray,prev
    def inFrame(lst):
        if lst[28].visibility > 0.6 and lst[27].visibility > 0.6 and lst[15].visibility>0.6 and lst[16].visibility>0.6:
            return True 
        return False

    model  = load_model("practice\model_Utkata_Konasana.h5")
    label = np.load("practice\label_Utkata_Konasana.npy")

    frm = cv2.flip(frame, 1)

    res =pose.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
    lst = []
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
            cv2.putText(frm, pred , (120,30),cv2.FONT_ITALIC, 0.8, (125, 6, 6),2)
            if(pred!="Nothing"):
                if(cou%5==0):
                    rleg = rleg_angle(webcam_list)
                    lleg = lleg_angle(webcam_list)
                    rhand_a = rhand_angle(webcam_list)
                    lhand_a = lhand_angle(webcam_list)
                    rhand_san = rhand(webcam_list)
                    lhand_san = lhand(webcam_list)
                    
                    if(rhand_a>actual_rhand+20):
                        Carray[4]+=1
                        # if prev!=4:
                        #     Carray[prev]=0
                        #     prev=4
                        if Carray[4]% vtime==0:
                            Carray[4]=0
                            t5=threading.Thread(target=playsound,args=(r"static\practice\goddess\rhand_a.mp3",))
                            t5.start()
                    elif(lhand_a>actual_lhand+20):
                        Carray[5]+=1
                        # if prev!=5:
                        #     Carray[prev]=0
                        #     prev=5
                        if Carray[5]% vtime==0:
                            Carray[5]=0
                            t6=threading.Thread(target=playsound,args=(r"static\practice\goddess\lhand_a.mp3",))
                            t6.start()
                            
                    elif(rhand_a<actual_rhand-20):
                        Carray[6]+=1
                        # if prev!=6:
                        #     Carray[prev]=0
                        #     prev=6
                        if Carray[6]% vtime==0:
                            Carray[6]=0
                            t7=threading.Thread(target=playsound,args=(r"static\practice\goddess\rhand_a.mp3",))
                            t7.start()
                    elif(lhand_a<actual_lhand-20):
                        Carray[7]+=1
                        # if prev!=7:
                        #     Carray[prev]=0
                        #     prev=7
                        if Carray[7]% vtime==0:
                            Carray[7]=0
                            t8=threading.Thread(target=playsound,args=(r"static\practice\goddess\lhand_a.mp3",))
                            t8.start()
                    elif(rhand_san<(actual_rhand_arm-15)):
                        Carray[8]+=1
                        # if prev!=8:
                        #     Carray[prev]=0
                        #     prev=8
                        if Carray[8]% vtime==0:
                            Carray[8]=0
                            t9=threading.Thread(target=playsound,args=(r"static\practice\goddess\r_sanup.mp3",))
                            t9.start()
                        
                    elif(lhand_san<(actual_lhand_arm-15)):
                        Carray[9]+=1
                        # if prev!=9:
                        #     Carray[prev]=0
                        #     prev=9
                        if Carray[9]% vtime==0:
                            Carray[9]=0
                            t10=threading.Thread(target=playsound,args=(r"static\practice\goddess\l_sanup.mp3",))
                            t10.start()
                    elif(lleg<actual_lleg-30):
                        Carray[0]+=1
                        # if prev!=0:
                        #     Carray[prev]=0
                        #     prev=0
                        if Carray[0]% vtime==0:
                            Carray[0]=0
                            t1=threading.Thread(target=playsound,args=(r"static\practice\goddess\upper_leg.mp3",))
                            t1.start()
                    elif(lleg>actual_lleg+20):
                        Carray[1]+=1
                        # if prev!=1:
                        #     Carray[prev]=0
                        #     prev=1
                        if Carray[1]% vtime==0:
                            Carray[1]=0
                            t2=threading.Thread(target=playsound,args=(r"static\practice\goddess\lower_leg.mp3",))
                            t2.start()

                            
                    elif(rleg<actual_rleg-30):
                        Carray[2]+=1
                        # if prev!=2:
                        #     Carray[prev]=0
                        #     prev=2
                        if Carray[2]% vtime==0:
                            Carray[2]=0
                            t3=threading.Thread(target=playsound,args=(r"static\practice\goddess\upper_leg.mp3",))
                            t3.start()
                    elif(rleg>actual_lleg+20):
                        Carray[3]+=1
                        # if prev!=3:
                        #     Carray[prev]=0
                        #     prev=3
                        if Carray[3]% vtime==0:
                            Carray[3]=0
                            t4=threading.Thread(target=playsound,args=(r"static\practice\goddess\lower_leg.mp3",))
                            t4.start()

                    
                    cou=0
            else:
                Carray=[0,0,0,0,0,0,0,0,0,0]
            
        drawing.draw_landmarks(frm, res.pose_landmarks, mpPose.POSE_CONNECTIONS,
                            connection_drawing_spec=drawing.DrawingSpec(color=(255,255,255), thickness=6 ),
                            landmark_drawing_spec=drawing.DrawingSpec(color=(0,0,255), circle_radius=3, thickness=3))
        
        mcount=0
    else:
        
        mcount+=1
        if mcount%70==0:
            mcount=0
            t11=threading.Thread(target=playsound,args=(r"static\bodyfit.mp3",))
            t11.start()
            
    return frm,True
