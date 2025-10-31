from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Candidate,Employer,JobPost,JobApplication,Notification
from django.contrib import messages




def landing_view(request):
    return render(request,'landing.html')
#candidate views;


def candidate_register(request):
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        skills = request.POST.get("skills")
        resume = request.FILES.get("resume")
        image=  request.FILES.get("image")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("candidateregister")

        user = User.objects.create_user(username=username, email=email, password=password)
        Candidate.objects.create(user=user, skills=skills, resume=resume,image=image)

        messages.success(request, "Candidate registered successfully. Please login.")
        return redirect("candidatelogin")




    return render(request, "candidateregister.html")
    
def candidate_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if Candidate.objects.filter(user=user).exists():
                login(request, user)
                return redirect("candidatedashboard")
            else:
                messages.error(request, "This account is not registered as a Candidate.")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "candidatelogin.html")

from django.shortcuts import render
from .models import JobPost, JobApplication, Notification

def candidate_dashboard(request):
    recent_jobs = JobPost.objects.all().order_by('-posted_at')[:5]

    applied_job_ids = []
    applications = []
    notifications = []
    candidate = None

    if request.user.is_authenticated:
        # ✅ get the candidate profile linked to this user
        candidate = get_object_or_404(Candidate, user=request.user)

        # Jobs the candidate has applied to
        applied_job_ids = JobApplication.objects.filter(
            candidate=request.user
        ).values_list("job_id", flat=True)

        # Applications with status
        applications = JobApplication.objects.filter(
            candidate=request.user
        ).select_related("job").order_by("-applied_at")

        # Notifications
        notifications = Notification.objects.filter(
            user=request.user
        ).order_by("-created_at")

    return render(request, 'candidatedashboard.html', {
        'user': request.user,
        'candidate': candidate,           # 👈 now available in template
        'recent_jobs': recent_jobs,
        'applied_job_ids': applied_job_ids,
        'applications': applications,
        'notifications': notifications,
    })






def update_candidatedashboard(request):
    user=request.user
    print(user)
    candidate = get_object_or_404(Candidate, user=request.user)
   

    if request.method == 'POST':
        user.username = request.POST.get('full-name')
        user.email = request.POST.get('email')
        
        user.save()
        return redirect('candidatedashboard')
    

    return render(request,'candidateupdateprofile.html',{'user':user,'candidate':candidate})


from django.contrib.auth import update_session_auth_hash

def settings(request):
    user = request.user

    if request.method == 'POST':
        
        new_password = request.POST.get('new-password')
        

       
        # Update password securely
        user.set_password(new_password)
        user.save()

        # Keep user logged in after password change
        update_session_auth_hash(request, user)

        messages.success(request, "Password updated successfully!")
        return redirect('candidatedashboard')

    return render(request, 'settings.html')




def my_applications(request):
    applications = JobApplication.objects.filter(candidate=request.user).select_related("job")
    return render(request, "myapplication.html", {"applications": applications})

def apply_job(request, job_id):
    if not request.user.is_authenticated:
        messages.error(request, "You must log in to apply for a job.")
        return render(request,"candidatelogin.html")

    job = get_object_or_404(JobPost, id=job_id)

    # check if candidate already applied
    if JobApplication.objects.filter(candidate=request.user, job=job).exists():
        messages.warning(request, "You have already applied for this job.")
    else:
        JobApplication.objects.create(candidate=request.user, job=job)
        messages.success(request, f"You have successfully applied for {job.title}!")

    # ✅ Redirect to applied jobs list
    return redirect("candidatedashboard")



def employer_register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        company_name = request.POST["company-name"]
        industry = request.POST["industry"]
        company_description = request.POST.get("company-description")

        if Employer.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("employerregister")

 
        Employer.objects.create(username=username,email=email,password=password,company_name=company_name, industry=industry, company_description=company_description)

        messages.success(request, "Employer registered successfully. Please login.")
        return redirect("employerlogin")

    return render(request, "employerregister.html")

def employer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Employer.objects.get(username=username)
        except Employer.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return render(request,'employerlogin.html')

        if user is not None:
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('employerdashboard',user.id)
        else:   
            messages.error(request, "Invalid email or password.")
            return redirect('employerlogin')

    return render(request, 'employerlogin.html')



def employer_dashboard(request, user_id):
    employer = Employer.objects.get(id=user_id)
    jobs = JobPost.objects.filter(employer=employer).order_by("-posted_at")
    job_count = JobPost.objects.filter(employer=employer).count()
    applicants_count = JobApplication.objects.filter(job__employer=employer).count()

    # Get job applications for this employer's jobs
    recent_applicants = JobApplication.objects.filter(
        job__employer=employer
    ).select_related("candidate", "job").order_by("-applied_at")[:5]

    return render(request, 'employerdashboard.html', {
        'employer': employer,
        'jobs': jobs,
        'recent_applicants': recent_applicants,
        'job_count': job_count,
        'applicants_count': applicants_count
    })



def post_a_job(request,employer_id):
    if request.method == "POST":
     
        

        employer = get_object_or_404(Employer, id=employer_id)

        title = request.POST.get("title")
        description = request.POST.get("description")
        location = request.POST.get("location")
        job_type = request.POST.get("job_type")
        salary = request.POST.get("salary")
        vacancies=request.POST.get("vacancies")

        try:
            vacancies = int(vacancies)
        except (TypeError, ValueError):
            vacancies = 1

        JobPost.objects.create(
            employer=employer,  # ✅ FIX: add employer
            title=title,
            description=description,
            location=location,
            job_type=job_type,
            vacancies=vacancies,
            salary=salary if salary else None,
        )

        return redirect("employerdashboard", employer.id)  # ✅ pass employer id

    return render(request, "jobpost.html")




def find_job(request):
    """
    Display all active job posts with search filters.
    """
    jobs = JobPost.objects.filter(is_active=True).select_related("employer")

    # ✅ Filtering by GET parameters
    job_title = request.GET.get("job-title", "")
    location = request.GET.get("location", "")

    if job_title:
        jobs = jobs.filter(title__icontains=job_title)

    if location:
        jobs = jobs.filter(location__icontains=location)

    # ✅ Check which jobs the logged-in user already applied for
    applied_job_ids = []
    if request.user.is_authenticated:
        applied_job_ids = JobApplication.objects.filter(
            candidate=request.user
        ).values_list("job_id", flat=True)

    context = {
        "jobs": jobs,
        "total_results": jobs.count(),
        "applied_job_ids": applied_job_ids,   # 👈 send to template
    }
    return render(request, "findjob.html", context)


def approve_application(request, app_id):
    application = get_object_or_404(JobApplication, id=app_id)

    if application.status != "pending":
        messages.warning(request, "This application has already been processed.")
        return redirect("employerdashboard", user_id=application.job.employer.id)

    application.status = "approved"
    application.save()

    # Create notification for candidate
    Notification.objects.create(
        user=application.candidate,
        message=f"🎉 Your application for {application.job.title} has been approved!"
    )

    messages.success(request, "Application approved successfully.")
    return redirect("employerdashboard", user_id=application.job.employer.id)


def reject_application(request, app_id):
    application = get_object_or_404(JobApplication, id=app_id)

    if application.status != "pending":
        messages.warning(request, "This application has already been processed.")
        return redirect("employerdashboard", user_id=application.job.employer.id)

    application.status = "rejected"
    application.save()

    # Create notification for candidate
    Notification.objects.create(
        user=application.candidate,
        message=f"❌ Your application for {application.job.title} has been rejected."
    )

    messages.success(request, "Application rejected successfully.")
    return redirect("employerdashboard", user_id=application.job.employer.id)



def job_listing(request):
    return render(request,)

def employer_profile(request, employer_id):
    employer = get_object_or_404(Employer, id=employer_id)
    jobs = JobPost.objects.filter(employer=employer, is_active=True).order_by("-posted_at")

    return render(request, "employerprofile.html", {
        "employer": employer,
        "jobs": jobs,
    })

def dashboard_logout(request):
    logout(request)
    return redirect('Landing')


