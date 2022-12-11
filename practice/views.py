from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from practice.tree_camera import VideoCamera_tree
from practice.warrior_camera import VideoCamera_warrior
from practice.goddess_camera import VideoCamera_goddess
from practice.tree_pose_estimation import Pose_video_tree
from practice.warrior_pose_estimation import Pose_video_warrior
from practice.goddess_pose_estimation import Pose_video_goddess

# Create your views here.
def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
def practice(request):
	return render(request, 'practice.html')


def tree(request):
	return render(request,'tree.html')
def treeView(request):
	return StreamingHttpResponse(gen(VideoCamera_tree(Pose_video_tree)),
					content_type='multipart/x-mixed-replace; boundary=frame')


def warrior(request):
	return render(request,'warrior.html')
def warriorView(request):
	return StreamingHttpResponse(gen(VideoCamera_warrior(Pose_video_warrior)),
					content_type='multipart/x-mixed-replace; boundary=frame')

				
def goddess(request):
	return render(request,'goddess.html')
def goddessView(request):
	return StreamingHttpResponse(gen(VideoCamera_goddess(Pose_video_goddess)),
					content_type='multipart/x-mixed-replace; boundary=frame')
