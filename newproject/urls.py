"""
URL configuration for newproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from JobNest import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('',views.landing_view,name='Landing'),
    path('candidateregister/',views.candidate_register,name='candidateregister'),
    path('employerregister/',views.employer_register,name='employerregister'),
    path('candidatelogin/',views.candidate_login,name='candidatelogin'),
    path('candidatedashboard/',views.candidate_dashboard,name='candidatedashboard'),
    path('updatecandidatedashboard/',views.update_candidatedashboard,name='updatedashboard'),
    path('employerlogin/',views.employer_login,name='employerlogin'),
    path('employerdashboard/<int:user_id>/',views.employer_dashboard,name='employerdashboard'),
    path('dashboardlogout/',views.dashboard_logout,name='Logout'),
    path('jobpost/<int:employer_id>/',views.post_a_job,name='Jobpost'),
    path("jobs/apply/<int:job_id>/", views.apply_job, name="apply_job"),
    path("applications/", views.my_applications, name="my_applications"),
    path("settings/",views.settings,name="settings"),
    path("findjob/",views.find_job,name='findjob'),
    path("application/<int:app_id>/approve/", views.approve_application, name="ApproveApplication"),
    path("application/<int:app_id>/reject/", views.reject_application, name="RejectApplication"),
    path("employer/<int:employer_id>/profile/", views.employer_profile, name="employer_profile"),

  

    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)