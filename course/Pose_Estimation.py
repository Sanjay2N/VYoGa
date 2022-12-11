import cv2
import threading 
import numpy as np 
import mediapipe as mp 
from keras.models import load_model 
from playsound import playsound

mpPose = mp.solutions.pose
pose =mpPose.Pose(model_complexity=0)
drawing = mp.solutions.drawing_utils
model  = load_model("course\model.h5")
label = np.load("course\labels.npy")

tree=cv2.resize(cv2.imread("static\\tree.jpg"),(450,600),interpolation = cv2.INTER_NEAREST )
warrior=cv2.resize(cv2.imread("static\\warrior.jpg"),(400,600),interpolation = cv2.INTER_NEAREST)
goddess=cv2.resize(cv2.imread("static\\goddess.jpg"),(400,600),interpolation = cv2.INTER_NEAREST)

count=0
second=0
mcount=0
flag = 0
score = 120
count_vriksha,count_virabhadra,count_utkata = 42,42,42
def Pose_video( frame):
    global count,second,mcount,count_vriksha,count_virabhadra,count_utkata,score,flag
    def inFrame(lst):
        if lst[28].visibility > 0.6 and lst[27].visibility > 0.6 and lst[15].visibility>0.6 and lst[16].visibility>0.6:
            return True 
        second=0
        return False
    lst = []
    frm = cv2.flip(frame, 1)
    frm=cv2.resize(frm, (600, 600),interpolation = cv2.INTER_NEAREST)
    res =pose.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
    if res.pose_landmarks and inFrame(res.pose_landmarks.landmark):
        for i in res.pose_landmarks.landmark:
            lst.append(i.x - res.pose_landmarks.landmark[0].x)
            lst.append(i.y - res.pose_landmarks.landmark[0].y)

        lst = np.array(lst).reshape(1,-1)

        p = model.predict(lst)
        pred = label[np.argmax(p)]
        
        if p[0][np.argmax(p)] > 0.75:
            if count==0 and pred==label[3]:
                flag = 0
                second+=1
                cv2.putText(frm, str(second//2) , (15,550),cv2.FONT_ITALIC, 1.3, (255,0,0),2)
                
                if second//2==30:
                    flag = 0
                    count+=1
                    second=0
                    score = score - (40 - count_vriksha)
            
            elif count==1 and pred==label[1]:
                flag = 0
                second+=1
                cv2.putText(frm, str(second//2) , (15,550),cv2.FONT_ITALIC, 1.3, (255,0,0),2)
                if second//2==30:
                    flag = 0
                    count+=1
                    second=0
                    score = score - (40 - count_virabhadra)
                    
            elif count==2 and pred==label[2]:
                flag = 0
                second+=1
                cv2.putText(frm, str(second//2) , (15,550),cv2.FONT_ITALIC , 1.3, (255,0,0),2)
                if second//2==30:
                    flag = 0
                    count+=1
                    second=0
                    score = score - (40 - count_utkata)

            if pred==label[0]:
                second=0
                cv2.putText(frm, str(second//2) , (15,550),cv2.FONT_ITALIC , 1.3, (255,0,0),2)
                if count==0 and flag==0:
                    flag = 1
                    count_vriksha-=2
                if count==1 and flag==0:
                    flag = 1
                    count_virabhadra-=2
                if count==2 and flag==0:
                    flag = 1
                    count_utkata-=2
                
             
                
        else:
            second = 0
        drawing.draw_landmarks(frm, res.pose_landmarks, mpPose.POSE_CONNECTIONS,
                            connection_drawing_spec=drawing.DrawingSpec(color=(255,255,255), thickness=6 ),
                            landmark_drawing_spec=drawing.DrawingSpec(color=(0,0,255), circle_radius=3, thickness=3))


    else:
        
        second=0
        mcount+=1
        if mcount%70==0:
            mcount=0
            second=0
            
            t1 = threading.Thread(target=playsound, args=(r"static\bodyfit.mp3",))
            t1.start()
            
    imgpose=tree
    if count==0:
        imgpose=tree
    elif count==1:
        imgpose=goddess
    elif count==2:
        imgpose=warrior
    
    xscore = int((score/120)*100)
    if count ==3:
        count=0
        if  xscore>85:
            courseim=cv2.resize(cv2.imread("static\\course\\gold.jpg"),(1520,620),interpolation = cv2.INTER_NEAREST)
        elif xscore>65:
            courseim=cv2.resize(cv2.imread("static\\course\\silver.jpg"),(1520,620),interpolation = cv2.INTER_NEAREST)
        else:
            courseim=cv2.resize(cv2.imread("static\\course\\bronz.jpg"),(1520,620),interpolation = cv2.INTER_NEAREST)
            
            
        cv2.destroyAllWindows()
        cv2.putText(courseim, "Course Is Completed" , (470,100),cv2.FONT_HERSHEY_SIMPLEX, 1.9, ( 52, 50, 168),3)
        cv2.putText(courseim, "YOUR SCORECARD:" , (470,200),cv2.FONT_HERSHEY_SIMPLEX, 1.2, ( 50, 168, 162),2)
        cv2.putText(courseim, "VRIKSHASANA - "+str(int((count_vriksha/42)*100))+" %" , (470,300),cv2.FONT_HERSHEY_SIMPLEX, 1, ( 78, 50, 168),2)
        cv2.putText(courseim, "VIRABHADRASANA - "+str(int((count_virabhadra/42)*100))+" %" , (470,350),cv2.FONT_HERSHEY_SIMPLEX, 1, (78, 50, 168),2)
        cv2.putText(courseim, "UTKATA KONASANA - "+str(int((count_utkata/42)*100))+" %" , (470,400),cv2.FONT_HERSHEY_SIMPLEX, 1, ( 78, 50, 168),2)
        cv2.putText(courseim, "PERCENTAGE SCORE - "+str(xscore)+"%" , (470,500),cv2.FONT_HERSHEY_SIMPLEX, 1, ( 127, 50, 168),2)
        t2 = threading.Thread(target=playsound, args=("static\course\course_Welldone.mp3",))
        t2.start()
        return courseim,False
    else:
        im_h = cv2.hconcat([frm, imgpose])
        return im_h,True
        



