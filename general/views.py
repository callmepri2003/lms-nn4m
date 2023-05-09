import datetime
from django.shortcuts import render, redirect

from Forum.models import Comment, Reply
from .models import *
from datetime import date, timedelta

from django.http import HttpResponseNotAllowed, JsonResponse
from django.views.decorators.http import require_POST

from .forms import UploadFileForm

from custom_storages import CustomS3Storage
from django.core.files.storage import default_storage
# Create your views here.

def home_view(request):

    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        return redirect('/authentication/login/')

def dashboard_view(request):
    if Tutor.objects.filter(user = request.user).exists():
        return redirect('/tutors/dashboard/')
    return dashboard_view_student(request)

def dashboard_view_student(request):
    return None

def dashboard_view_student(request):
    current_section = None
    user_sections = UcatSectionInstance.objects.filter(student = UcatStudent.objects.get(user = request.user))
    start_dates_ordered = []
    for section in user_sections:
        start_dates_ordered.append(section.start_date)
        if section.current:
            current_section = section
    for section in UcatSection.objects.all():
        
        if len(UcatSectionInstance.objects.filter(section = section, student=UcatStudent.objects.get(user=request.user))) == 0:
            
            student_instance = UcatStudent.objects.get(user=request.user)
            section_instance = section

            # Create a UcatSectionInstance object with the desired attributes
            ucat_section_instance = UcatSectionInstance(
                student=student_instance,
                section=section_instance,
                start_date = datetime.datetime.now().date(),
                current=False,  # or False, depending on the desired value
                skills_mastered=0  # or any other valid integer value
            )

            # Save the UcatSectionInstance object to the database
            ucat_section_instance.save()
    context = {
        'current_section': current_section,
        'start_dates_ordered':start_dates_ordered,
        'tasks': UcatStudent.objects.get(user = request.user).tasks,
        'date1': (UcatStudent.objects.get(user=request.user).enrolment_date).date(),
        'date2': (UcatStudent.objects.get(user=request.user).enrolment_date+ timedelta(days=30)).date(),
        'date3': (UcatStudent.objects.get(user=request.user).enrolment_date+ timedelta(days=60)).date(),
        'date4': (UcatStudent.objects.get(user=request.user).enrolment_date+ timedelta(days=90)).date(),
        'date5': (UcatStudent.objects.get(user=request.user).enrolment_date+ timedelta(days=120)).date(),
        'sectionId1': UcatSectionInstance.objects.get(student = UcatStudent.objects.get(user = request.user), section = UcatSection.objects.get(id=1)).id,
        'sectionId2': UcatSectionInstance.objects.get(student = UcatStudent.objects.get(user = request.user), section = UcatSection.objects.get(id=2)).id,
        'sectionId3': UcatSectionInstance.objects.get(student = UcatStudent.objects.get(user = request.user), section = UcatSection.objects.get(id=3)).id,
        'sectionId4': UcatSectionInstance.objects.get(student = UcatStudent.objects.get(user = request.user), section = UcatSection.objects.get(id=4)).id,
        'sectionId5': UcatSectionInstance.objects.get(student = UcatStudent.objects.get(user = request.user), section = UcatSection.objects.get(id=5)).id
    }

    if not context['current_section'] == None:
        context['skills_mastered'] = context['current_section'].skills_mastered
        deadline = context['current_section'].start_date + timedelta(days=30)
        current_day = datetime.datetime.now().date()
        context['days_to_master'] = (deadline - current_day).days

    if len(context['tasks']) == 0:
        context['no_tasks'] = True 

    return render(request, 'dashboard.html', context)

def course_page_view(request, sectionInstanceId):
    sectionInstance = UcatSectionInstance.objects.get(id = sectionInstanceId)
    section = sectionInstance.section
    videos_dict = {}
    videos = UcatVideo.objects.filter(section = section, unlocked = True)
    for video in videos:
        videos_dict[str(video.syllabus_point)] = []
    for video in videos:
        videos_dict[str(video.syllabus_point)].append(video)
    context = {
        'tasks': UcatStudent.objects.get(user = request.user).tasks,
        'no_tasks': len(UcatStudent.objects.get(user = request.user).tasks) == 0,
        'videos_dict': videos_dict,
        'section_name': section.name,
        'locked_vids': UcatVideo.objects.filter(section = section, unlocked = False)
        
    }
    return render(request, 'course-page-updated.html', context)

def course_video_view(request, sectionInstanceId, videoId):
    
    
    sectionInstance = UcatSectionInstance.objects.get(id = sectionInstanceId)
    section = sectionInstance.section
    video = UcatVideo.objects.get(id=videoId)
    # thumbnails = UcatVideo.objects.filter(section = section).thumbnail
    
    student = UcatStudent.objects.get(user = request.user) # Assuming the user is logged in
    context = {
        'tasks': UcatStudent.objects.get(user = request.user).tasks,
        'no_tasks': len(UcatStudent.objects.get(user = request.user).tasks) == 0,
        'vid': video,
        'vid_name': video.name,
        'vid_description': video.description,
        'share_code': video.url,
        'comments': Comment.objects.filter(forum = video),
        'section': section,
        'raised': False


    }
    if request.method == 'POST':
        problem_text = request.POST['issue_details']
        if problem_text:
            problem = UcatProblem(student=student, video=video, problem=problem_text)
            problem.save()
            context['raised'] = True
            return redirect(request.path)  # Redirect to the same page to avoid resubmission on refresh


    return render(request, 'course-video.html', context)

@require_POST
def add_comment(request):
    video_id = request.POST.get('video_id')
    user = request.user
    content = request.POST.get('content')

    if not user.is_authenticated:
        return JsonResponse({'error': 'Authentication required.'})

    try:
        video = UcatVideo.objects.get(id=video_id)
    except UcatVideo.DoesNotExist:
        return JsonResponse({'error': 'Video not found.'})

    comment = Comment(forum=video, user=user, content=content, upvotes=0)
    comment.save()

    # Return the new comment as a JSON response
    return JsonResponse({
        'id': comment.id,
        'username': comment.user.username,
        'datetime': comment.datetime.strftime('%Y-%m-%d %H:%M:%S'),
        'content': comment.content,
        'upvotes': comment.upvotes,
    })

def add_reply(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        user = request.user
        content = request.POST.get('reply_content')

        comment = Comment.objects.get(id=comment_id)

        reply = Reply(comment=comment, user=user, content=content, upvotes=0)
        reply.save()

        data = {
            'username': user.username,
            'datetime': reply.datetime.strftime('%Y-%m-%d %H:%M'),
            'content': reply.content,
            'upvotes': reply.upvotes
        }
        return JsonResponse(data)
    else:
        return HttpResponseNotAllowed(['POST'])
    

def upvote_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        comment.upvotes += 1
        comment.save()

        return JsonResponse({'upvotes': comment.upvotes})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def submit_progress_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            # s3_storage = CustomS3Storage()
            user_fullname_dir = request.user.username.upper().replace(" ", "_")
            # upload_directory = 'static/uploads/'+user_fullname_dir+"/"

            # # You can change 'uploads/' to any other directory name you want to save the files in.
            # filename = s3_storage.save(upload_directory + file.name, file)
            file_name = default_storage.save('uploads/'+user_fullname_dir+"/"+file.name, file)
            return redirect('/dashboard/submit-progress/?submitted')
    else:
        form = UploadFileForm()
    context = {
        'form': form,
        'tasks': UcatStudent.objects.get(user = request.user).tasks
    }

    if 'submitted' in request.GET.keys():
        context['submitted'] = True
    return render(request, 'submit-progress.html', context)
    # return redirect("../../under-maintenance/")


def maintenance_view(request):
    return render(request, 'maintenance.html', {})

def sitemap_view(request):
    return render(request, 'sitemap.xml', {})

def back(request):
    # Use request.META.get('HTTP_REFERER') to get the previous page's URL
    # or any other logic to determine the correct URL to redirect to
    url = request.META.get('HTTP_REFERER', '/')
    return redirect(url)