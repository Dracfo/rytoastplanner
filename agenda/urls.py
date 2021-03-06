from django.urls import path

from . import views

app_name = "agenda"

urlpatterns = [
    path("", views.index, name="index"),
    path("spreadsheet", views.spreadsheet, name="spreadsheet"),
    path("profile/<id>", views.profile, name="profile"),
    path("meeting/<id>", views.meeting, name="meeting"),
    path("edit_meeting/<id>", views.edit_meeting, name="edit_meeting"),
    path("create_meeting", views.create_meeting, name="create_meeting"),
    path("bulk_create_meeting", views.bulk_create_meeting, name="bulk_create_meeting"),
    path("delete_meeting/<id>", views.delete_meeting, name="delete_meeting"),
    path("meeting_list", views.meeting_list, name="meeting_list"),
    path("report_bug", views.report_bug, name="report_bug"),
    path("bug_list", views.bug_list, name="bug_list"),
    path("update_role_description/<id>", views.update_role_description, name="update_role_description"),
    path("confirmation_emails/<id>", views.confirmation_emails, name="confirmation_emails"),
    path("update_guest_list/<id>", views.update_guest_list, name="update_guest_list"),

    # Meeting Confirmation from email routes
    path("confirm_attendance/<id>/<username>/<status>", views.confirm_attendance, name="confirm_attendance"),

    # Authentication routes
    path("register/", views.register, name="register"),
    path("create_user/", views.create_user, name="create_user"),

    # API Routes
    path("attendence", views.attendence, name="attendence"),
    path("sign_up", views.sign_up, name="sign_up"),
    path("fetch_call_recommend_one_role", views.fetch_call_recommend_one_role, name="fetch_call_recommend_one_role"),
    path("change_event_number", views.change_event_number, name="change_event_number"),
    path("add_new_event", views.add_new_event, name="add_new_event"),
]