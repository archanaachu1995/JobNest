from django.db import models
from django.contrib.auth.models import User






# Candidate model
class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="profile_pics/")

    def __str__(self):
        return self.user.username


# Employer model
class Employer(models.Model):
    username=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=50)
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100)
    company_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.company_name
    
#model for posting jobs for employe    
class JobPost(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    
    vacancies = models.PositiveIntegerField(default=1)  # 🔹 number of open positions
    
    is_active = models.BooleanField(default=True)  # 🔹 auto-updated

    job_type = models.CharField(
        max_length=50,
        choices=[
            ("full-time", "Full Time"),
            ("part-time", "Part Time"),
            ("contract", "Contract"),
            ("internship", "Internship"),
            ("remote", "Remote"),
        ],
        default="full-time"
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # 🔹 Automatically set is_active based on vacancies
        if self.vacancies <= 0:
            self.is_active = False
        else:
            self.is_active = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} at {self.employer.company_name}"
    
#models for applying job for candidate   
class JobApplication(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.candidate.username} applied for {self.job.title}"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}"