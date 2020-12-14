from django.urls import path

from . import views

app_name = "agenda"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("accounts/login/", views.login_view, name="accounts/login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("spreadsheet", views.spreadsheet, name="spreadsheet"),
    path("profile/<id>", views.profile, name="profile"),
    path("meeting/<id>", views.meeting, name="meeting"),
    path("edit_meeting/<id>", views.edit_meeting, name="edit_meeting"),
    path("create_meeting", views.create_meeting, name="create_meeting"),
    path("delete_meeting/<id>", views.delete_meeting, name="delete_meeting"),
    path("meeting_list", views.meeting_list, name="meeting_list"),
    path("report_bug", views.report_bug, name="report_bug"),
    path("bug_list", views.bug_list, name="bug_list"),

    # API Routes
    path("attendence", views.attendence, name="attendence"),
    path("sign_up", views.sign_up, name="sign_up"),
]