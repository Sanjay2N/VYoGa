import cv2
from practice.goddess_pose_estimation import Pose_video_goddess

# load our serialized face detector model from disk
class VideoCamera_goddess(object):
    def __init__(self,Pose_video):
        self.video = cv2.VideoCapture(0)
        self.Pose_video=Pose_video_goddess
        
    def __del__(self):
        self.video.release()
    def get_frame(self):
        success, image = self.video.read()
        image,tag=self.Pose_video(image)
		# call the detection here
        if tag:
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()
        else:
            self.video.release()
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()      