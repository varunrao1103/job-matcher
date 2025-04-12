from django.urls import path
from .views import signup,login_view, logout_view,dashboard,recruiter_dashboard,job_seeker_dashboard,post_job,job_detail,apply_for_job,job_applications,index

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("recruiter_dashboard/", recruiter_dashboard, name="recruiter_dashboard"),
    path("job_seeker_dashboard/", job_seeker_dashboard, name="job_seeker_dashboard"),
    path("post_job/", post_job, name="post_job"),
    path("job/<int:job_id>/", job_detail, name="job_detail"),
    path("job/<int:job_id>/apply/", apply_for_job, name="apply_for_job"),
    path("job/<int:job_id>/applications/", job_applications, name="job_applications"),
]