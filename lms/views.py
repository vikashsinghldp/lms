from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import razorpay
from . import settings
from app.models import Enrollment, Course, Lesson, Doubt, StudentProfile, Resource, Course


def BASE(request):
    return render(request,'base.html')

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')
def courses(request):
    return render(request, 'courses.html')

@csrf_exempt
def ajax_login(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'msg': 'Invalid credentials'})


@csrf_exempt
def ajax_signup(request):
    if request.method == "POST":
        if User.objects.filter(username=request.POST['email']).exists() or User.objects.filter(username=request.POST['username']).exists():
            return JsonResponse({'status': 'error', 'msg': 'Already registered'})
        user = User.objects.create_user(
            first_name = request.POST['name'],
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password']
        )
        login(request, user)   # ✅ auto login
        #return redirect('dashboard')  # /dashboard/
        return JsonResponse({'status': 'success'})


@csrf_exempt
def ajax_forgot_password(request):
    return JsonResponse({'status': 'success', 'msg': 'Password reset link sent'})


@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(
        user=request.user,
        paid=True
    ).select_related("course")
    courses = Course.objects.all()
    return render(request, 'dashboard.html', {
        "enrollments": enrollments,
        "courses": courses
    })


def logout_view(request):
    logout(request)
    return redirect('/')

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

def create_order(request):
    course_id = request.POST.get("course_id")
    course = Course.objects.get(id=course_id)
    if Enrollment.objects.filter(
        user=request.user,
        course=course,
        paid=True
    ).exists():
        return JsonResponse({
            "error": "You are already enrolled in this course"
        }, status=400)

    request.session["course_id"] = course.id

    order = client.order.create({
        "amount": course.price * 100,  # paisa
        "currency": "INR",
        "payment_capture": 1
    })

    return JsonResponse({
        "order_id": order["id"],
        "amount": course.price,
        "course": course.title,
        "key": settings.RAZORPAY_KEY_ID
    })

def course1(request):
    return render(request,'course1.html')

@login_required
def payment_success(request):
    
    course_id = request.session.get("course_id")
    course = get_object_or_404(Course, pk=course_id)
    Enrollment.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={"paid": True}
    )

    del request.session["course_id"]
    return render(request, "success.html")

@login_required
def course_lessons(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    # check enrollment
    is_enrolled = Enrollment.objects.filter(
        user=request.user,
        course=course,
        paid=True
    ).exists()

    lessons = Lesson.objects.filter(course=course)

    return render(request, "course_lessons.html", {
        "course": course,
        "lessons": lessons,
        "is_enrolled": is_enrolled
    })

@login_required
def ask_doubt(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    # allow only enrolled students
    if not Enrollment.objects.filter(user=request.user, course=course, paid=True).exists():
        return redirect("dashboard")

    if request.method == "POST":
        question = request.POST.get("question")

        Doubt.objects.create(
            course=course,
            student=request.user,
            question=question
        )

    return redirect("course_doubts", course_id=course.id)


@login_required
def course_doubts(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    doubts = Doubt.objects.filter(
        course=course,
        student=request.user
    ).order_by("-created_at")

    return render(request, "course_doubts.html", {
        "course": course,
        "doubts": doubts
    })


@login_required
def profile_settings(request):
    user = request.user
    profile = user.studentprofile

    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        profile.phone = request.POST.get("phone")
        profile.bio = request.POST.get("bio")

        if "profile_image" in request.FILES:
            profile.profile_image = request.FILES["profile_image"]

        user.save()
        profile.save()

        messages.success(request, "Profile updated successfully")

    return render(request, "profile_settings.html", {
        "profile": profile
    })

@login_required
def view_profile(request):
    # Ensure profile exists (for old users)
    profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    return render(request, "view_profile.html", {
        "profile": profile
    })


@login_required
def course_resources(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    # 🔐 Allow only enrolled students
    if not Enrollment.objects.filter(
        user=request.user,
        course=course,
        paid=True
    ).exists():
        return redirect("dashboard")

    notes = Resource.objects.filter(course=course, resource_type="note")
    assignments = Resource.objects.filter(course=course, resource_type="assignment")
    enrollments = Enrollment.objects.filter(user=request.user)

    return render(request, "course_resources.html", {
        "course": course,
        "notes": notes,
        "assignments": assignments
    })

