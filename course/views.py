from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from course.camera import VideoCamera
from course.Pose_Estimation import Pose_video
# Create your views here.

def frontpage(request):
    return render(request,'frontpage.html')
def about(request):
    return render(request,'about.html')
def course(request):
	return render(request, 'course.html')

def support(request):
    return render(request,'support.html')

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def courseView(request):

    return StreamingHttpResponse(gen(VideoCamera(Pose_video)),content_type='multipart/x-mixed-replace; boundary=frame')


# Create your views here.
