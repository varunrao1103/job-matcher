from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm,ApplicationForm

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .forms import JobForm
from .models import Job,Application

def index(request):
    return render(request, 'users/index.html') 

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")  # Redirect to dashboard after login
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")  # Redirect to login page after logout


@login_required
def dashboard(request):
    if request.user.user_type == "recruiter":
        return redirect("recruiter_dashboard")
    else:
        return redirect("job_seeker_dashboard")
    
@login_required
def recruiter_dashboard(request):
    if request.user.user_type != "recruiter":
        return redirect("dashboard")

    jobs = Job.objects.filter(recruiter=request.user)  
    return render(request, "users/recruiter_dashboard.html", {"jobs": jobs})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Job

@login_required
def job_seeker_dashboard(request):
    if request.user.user_type != "job_seeker":
        return redirect("dashboard")

    query = request.GET.get("q", "")  # Get search query from URL
    jobs = Job.objects.all()

    if query:
        jobs = jobs.filter(title__icontains=query)  # Case-insensitive search in job title

    return render(request, "users/job_seeker_dashboard.html", {"jobs": jobs, "query": query})


@login_required
def post_job(request):
    if request.user.user_type != "recruiter":
        return redirect("dashboard")  # Prevent job seekers from posting jobs

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user  # Link the job to the recruiter
            job.save()
            return redirect("recruiter_dashboard")
    else:
        form = JobForm()

    return render(request, "users/post_job.html", {"form": form})


@login_required
def job_detail(request, job_id):
    job = Job.objects.get(id=job_id)
    return render(request, "users/job_detail.html", {"job": job})

@login_required
def apply_for_job(request, job_id):
    if request.user.user_type != "job_seeker":
        return redirect("dashboard")

    job = Job.objects.get(id=job_id)

    if Application.objects.filter(job=job, job_seeker=request.user).exists():
        messages.error(request, "You have already applied for this job.")
        return redirect("job_detail", job_id=job.id)

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.job_seeker = request.user
            application.save()
            messages.success(request, "Application submitted successfully!")
            return redirect("job_seeker_dashboard")
    else:
        form = ApplicationForm()

    return render(request, "users/apply_for_job.html", {"form": form, "job": job})


@login_required
def job_applications(request, job_id):
    if request.user.user_type != "recruiter":
        return redirect("dashboard")

    job = Job.objects.get(id=job_id, recruiter=request.user)
    applications = Application.objects.filter(job=job)

    return render(request, "users/job_applications.html", {"job": job, "applications": applications})
