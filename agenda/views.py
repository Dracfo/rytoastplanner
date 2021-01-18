import time
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from re import findall
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime, timedelta, time, date
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import random
import string
from django.conf import settings 
from django.core.mail import send_mail, EmailMessage

from .models import User, Meeting, Rolelist, Attendee, BugForm, Buglist, Eventlist
from .functions import update_meeting, meeting_roles_list, update_one_role_in_database, create_default_eventlist, role_recommendation_list, past_role_holders, convert_role_to_shorthand


# View the first upcoming meeting's individual page
def index(request):
    
    # Get the start and end dates for the meeting query
    startdate = date.today()
    enddate = startdate + timedelta(days=365)

    # Get the next meeting
    next_meeting = Meeting.objects.filter(starttime__range=[startdate, enddate]).order_by('starttime').first()

    if next_meeting == None:
        return HttpResponseRedirect(reverse("agenda:meeting_list"))

    # Redirect to views.meeting to load the individual meeting page for the next meeting
    return HttpResponseRedirect(reverse("agenda:meeting", args=(next_meeting.id,)))


# View individual meeting page
def meeting(request, id):

    # Reset the alert notifications
    alert_success = None
    alert_danger = None

    # Get the next meeting information
    meeting = Meeting.objects.filter(id=id).order_by('-starttime')
    
    roles = Rolelist.objects.filter(meeting=meeting[0])
    rolelist = meeting_roles_list(meeting[0])

    # Get the role recommednations for the selected meeting
    role_recommendations = role_recommendation_list(meeting[0])
        
    # Add role recommendations to the rolelist
    # Iterate through all the roles in the rolelist
    for role in rolelist:

        # If no one is assigned to the role, get a list of recommendations. Else skip to next role
        if rolelist[role] == None:

            # Add recommednations to the rolelist
            rolelist[role] = ['No Member Assigned', role_recommendations[role]]

    attendees = Attendee.objects.filter(meeting=meeting[0])
    confirmed_attendees = []
    unknown_attendees = []
    absentees = []
    for attendee in attendees:
        if attendee.status == "U":
            unknown_attendees.append(attendee.user)

            # Check if logged in user has marked their attendance
            if str(attendee.user.username) == str(request.user.username):
                alert_danger = f"You haven't confirmed your attendence for this meeting yet."
        elif attendee.status == "F":
            absentees.append(attendee.user)
        elif attendee.status == "T":
            confirmed_attendees.append(attendee.user)

    # Get the eventlist for the meeting
    eventlist = Eventlist.objects.filter(meeting=meeting[0]).order_by('event_number').values()

    # Update eventlist with role holders
    for event in eventlist:
        if event['role'] != "" and event['role'] != "None" and event['role'] != None:
            event['user'] = rolelist[event['role']]

    # Add start times to each event based on the durations
    f = '%I:%M'
    t = meeting[0].starttime
    printer = t.strftime("%X")
    for event in eventlist:
        # Print event start time to eventlist
        event['start_time'] = t.strftime(f)

        # Update event start time for the next event
        min_to_add = event['duration']
        t = t + timedelta(minutes = min_to_add)
    
    # Remind users to login or register in roder to sign up for roles and speeches
    if request.user.is_authenticated == False:
        alert_danger = f"Login to sign up for a role or speech this meeting."

    # Get the list of all bugs reported
    bugs = Buglist.objects.filter()

    # Render the individual meeting page
    return render(request, "agenda/meeting.html", {
        'id': id,
        "meeting": meeting[0],
        "roles": roles[0],
        'rolelist': rolelist,
        'eventlist': eventlist,
        'confirmed_attendees': confirmed_attendees,
        'unknown_attendees': unknown_attendees,
        'absentees': absentees,
        'username': str(request.user.username),
        'alert_success': alert_success,
        'alert_danger': alert_danger,
        'bugs': bugs,
    })


def meeting_list(request):

    # Get the start and end dates for the next year
    startdate = date.today() - timedelta(days=30)
    enddate = startdate + timedelta(days=396)

    # Get the list of meetings for the next year
    meeting_list_query = Meeting.objects.filter(starttime__range=[startdate, enddate]).order_by('starttime')

    # Setup the meeting list with dates and role holders
    list_of_meetings = []
    for meeting in meeting_list_query:
        print(meeting.theme)

        # Get the toastmaster for the meeting
        role_query = Rolelist.objects.filter(meeting=meeting).values('toastmaster')
        if role_query[0]['toastmaster'] == None:
            toastmaster = None
        else:
            toastmaster = User.objects.get(id=role_query[0]['toastmaster'])

        # Get the general evaluator for the meeting
        role_query =  Rolelist.objects.filter(meeting=meeting).values('geneval')
        if role_query[0]['geneval'] == None:
            geneval = None
        else:
            geneval = User.objects.get(id=role_query[0]['geneval'])

        # Get the table topics master for the meeting
        role_query = Rolelist.objects.filter(meeting=meeting).values('ttmaster')
        if role_query[0]['ttmaster'] == None:
            ttmaster = None
        else:
            ttmaster = User.objects.get(id=role_query[0]['ttmaster'])

        # Get the number of speeches for the meeting
        speech_count = 0
        speech_query = Rolelist.objects.filter(meeting=meeting).values('speaker1', 'speaker2', 'speaker3')
        for speech in speech_query[0]:
            if speech_query[0][speech] != None:
                speech_count += 1

        # Add id's, dates, and role holders to the list
        meeting_entry_for_the_list = {'id': meeting.id, 'date': meeting.starttime.strftime("%d/%b/%Y"), 'theme': meeting.theme,'speech_count': speech_count, 'toastmaster': toastmaster, 'geneval': geneval, 'ttmaster': ttmaster}
        
        # Add dictionary for the individual meeting to the list of all meetings to be passed to the template to display
        list_of_meetings.append(meeting_entry_for_the_list)

    # Render the list of meetings
    return render(request, "agenda/meeting_list.html", {
        'meeting_list': list_of_meetings
    })


@login_required
def profile(request, id):
    
    # Get User information
    user = User.objects.get(id=id)
    print(user)
    
    return render(request, "agenda/profile.html", {
    })


@login_required
def edit_meeting(request, id):

    # If user is submitting the edit meeting form
    if request.method == "POST":
        # Get data from form submission
        form = request.POST
        print(form)

        # Get the existing meeting information
        meeting = Meeting.objects.get(id=id)

        # Update meeting information
        print(meeting, form)
        update_meeting(meeting, form)

        return HttpResponseRedirect(reverse("agenda:meeting", args=(id,)))

    
    # Get meeting details
    meeting = Meeting.objects.filter(id=id)

    # Check if this is a new meeting
    if not meeting:
        
        # Create a new meeting
        new_meeting = Meeting(id=id, starttime=datetime.now())
        new_meeting.save()

        # Create a new rolelist
        new_rolelist = Rolelist(meeting=new_meeting)
        new_rolelist.save()

        # Create a new Eventlist
        create_default_eventlist(new_meeting)

        # Mark all attendees as unknown
        users = User.objects.filter()
        for user in users:
            new_attendence = Attendee(user=user, meeting=new_meeting, status="U")
            new_attendence.save()

        #Reset meeting variable to new meeting
        meeting = Meeting.objects.filter(id=id)
        
    # Get all attending User details
    users = []
    attendees = Attendee.objects.filter(meeting=meeting[0])
    for attendee in attendees:
        if attendee.status != "F":
            users.append(attendee.user)

    meeting = meeting[0]
    roles = meeting_roles_list(meeting)

    # Get the meeting time and date
    start_time = meeting.starttime.time().strftime("%H:%M")
    start_date = meeting.starttime.date().strftime("%Y-%m-%d")

    # Get the eventlist for the meeting
    eventlist = Eventlist.objects.filter(meeting=meeting).order_by('event_number').values()

    return render(request, "agenda/edit_meeting.html", {
        'new_meeting': False,
        'id': id,
        'meeting': meeting,
        'start_date': start_date,
        'start_time': start_time,
        'roles': roles,
        'users': users,
        'eventlist': eventlist,
    })


@login_required
def create_meeting(request):

    # Get the list of meetings ordered highest id first
    meeting = Meeting.objects.filter().order_by('-id').first()

    # If no meetings exist yet set id to 1
    if meeting == None:
        id = 1
    
    # Else add 1 to the highest id
    elif meeting != None:
        id = meeting.id + 1

    return HttpResponseRedirect(reverse("agenda:edit_meeting", args=(id,)))


def bulk_create_meeting(request):

    # Check if the user is submitting the bulk meeting creation form
    if request.method == 'POST':
        # Get data from form submission
        form = request.POST

        # Organize the date information (Date and time of week, start date, end date)
        start_date = form['start_date']
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = form['end_date']
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        form_day_of_week = form['day_of_the_week']
        start_time = form['start_time']

        # Check if the end date is after the start date
        if end_date < start_date:
            return HttpResponseRedirect(reverse("agenda:meeting_list"))

        # Get the first time a day of the week selected occurs in the date range
        while int(start_date.weekday()) != int(form_day_of_week):
            start_date = start_date + timedelta(days=1)

        i = start_date
        while i < end_date:
            # Create a new meeting at the date
            new_meeting = Meeting(starttime=datetime.combine(i, datetime.strptime(start_time, "%H:%M").time()))
            new_meeting.save()

            # Create an eventlist and rolelist for the meeting
            new_rolelist = Rolelist(meeting=new_meeting)
            new_rolelist.save()
            create_default_eventlist(new_meeting)

            # Mark all attendees as unknown for the meeting
            users = User.objects.filter()
            for user in users:
                new_attendence = Attendee(user=user, meeting=new_meeting, status="U")
                new_attendence.save()

            # Update the meeting date for the next iteration
            i = i + timedelta(days=7)

        # Redirect to the meeting list page so user can see that all the meetings have been created
        return HttpResponseRedirect(reverse("agenda:meeting_list"))

    # Else the user is trying to access the bulk create meetings form
    return render(request, "agenda/bulk_create_meetings.html", {
        'date_today': date.today().strftime("%Y-%m-%d")
    })




def delete_meeting(request, id):

    # Check if user is an executive
    if request.user.executive == False:
        return HttpResponseRedirect(reverse("agenda:index"))

    # Get meeting information
    meeting = Meeting.objects.get(id=id)

    # Check if user is submitting via a POST request, delete the meeting
    if request.method == "POST":
        
        # Delete the meeting
        meeting.delete()

        #Redirect to index page
        return HttpResponseRedirect(reverse("agenda:index"))
    
    # If user is not submitting via a post request then redirect to confirmation page
    return render(request, "agenda/delete_meeting_confirmation.html", {
        'meeting': meeting,
    })


def spreadsheet(request):

    # Find meetings in next 4 months
    startdate = date.today()
    enddate = date.today() + timedelta(days=62)
    meeting_list = Meeting.objects.filter(starttime__range=[startdate, enddate]).order_by('starttime')

    # Get the next meeting information
    roles = {}
    initial_rolelist = []
    role_recommendations = {}
    id_list =[]
    meeting_absentee_list = []
    all_meetings_absentee_list = []
    for meeting in meeting_list:
        roles = meeting_roles_list(meeting)
        initial_rolelist.append(roles)
        role_recommendations[meeting.id] = role_recommendation_list(meeting)
        id_list.append(meeting.id)

        # Get list of absences for the rolelist dictionary
        absences = Attendee.objects.filter(meeting=meeting, status="F").values('user_id')
        meeting_absentee_list = []
        for absentee in absences:
            user = User.objects.get(id=absentee['user_id']).username
            meeting_absentee_list.append(user)
        all_meetings_absentee_list.append(meeting_absentee_list)


    # Sort the rolelist into groups by role
    rolelist = {
        'Meeting_id': id_list,
        'Toastmaster': [],
        'Chair': [],
        'Facilitator': [],
        'Zoom Master': [],
        'General Evaluator': [],
        'Speaker 1': [],
        'Speaker 2': [],
        'Speaker 3': [],
        'Evaluator 1': [],
        'Evaluator 2': [],
        'Evaluator 3': [],
        'Table Topics Master': [],
        'Table Topics Evaluator': [],
        'Timer': [],
        'Ah Counter': [],
        'Ballot Counter':[],
        'Quizmaster': [],
        'Absences': all_meetings_absentee_list,
    } 

    # Fill the rolelist with all the signed up role holders
    for i in range(len(initial_rolelist)):  # Iterate through the meetings
        for init_role in initial_rolelist[i]:  # Iterate through the rolelist for each meeting
            
            # Get list of absences for the meeting
            if init_role == 'Absences':
                # Get the list of user ids who will be absent
                absences = Attendee.objects.filter(meeting=meeting_list[i]).filter(status="F").values('user_id')
                absentees = []

                # Get the names of the absent users
                for absent in absences:
                    absentees.append(User.objects.get(id=absent['user_id']).username)

                rolelist[role_key].append(absentees)

            # Else fill the role
            else:
                for role_key in rolelist:  # Iterate through all the roles
                    if role_key == init_role:  # If the role matches, then add it to the rolelist dictionary
                        rolelist[role_key].append(initial_rolelist[i][role_key])
    
    
    # Add role recommendations to the rolelist
    # Iterate through all the roles in the rolelist
    for role in rolelist:

        # Iterate through the holder holders for the role and track the index number (To compare with meeting index number and find the meeting id)
        for role_index, role_holder in enumerate(rolelist[role]):

            # If no one is assigned to the role, get a list of recommendations. Else skip to next role
            if role_holder == None:

                for recommendation_index, meeting_id in enumerate(id_list):

                    if recommendation_index == role_index:

                        rolelist[role][role_index] = ['No Member Assigned', role_recommendations[meeting_id][role]]

    return render(request, "agenda/spreadsheet.html", {
        'rolelist': rolelist,
        'meeting_list': meeting_list,
        'meeting_count': range(len(meeting_list)),
        'role_recommendations': role_recommendations,
    })


@login_required
def attendence(request):
    # Updating attendence must be via POST request
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get fetch request data
    data = json.loads(request.body.decode("utf-8"))
    username = data.get("user", "")
    meeting_id = data.get("meeting_id", "")
    status = data.get("status", "")

    # Update user's attendence in the database
    user = User.objects.get(username=username)
    meeting = Meeting.objects.get(id=meeting_id)
    attendee = Attendee.objects.filter(user=user, meeting=meeting)
    attendee = attendee[0]
    attendee.status = status
    attendee.save()

    action = [{'action': status}]
    return JsonResponse(action, safe=False)


@login_required
def sign_up(request):
    # Updating role holder must be via POST request
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get fetch request data
    data = json.loads(request.body.decode("utf-8"))
    username = data.get("user", "")
    meeting_id = data.get("meeting_id", "")
    role = data.get("role", "")

    # Get meeting, rolelist, and user info from database
    meeting = Meeting.objects.get(id=meeting_id)
    rolelist = Rolelist.objects.get(meeting=meeting)
    if username == "None":
        user = "None"
    else:
        user = User.objects.get(username=username)

    # Update rolelist in database
    update_one_role_in_database(role, rolelist, user)
    
    return JsonResponse({"message": "Role Updated successfully."}, status=201)


# How members update the descriptions for their speeches
@login_required
def update_role_description(request, id):

     # If user is submitting the update description form
    if request.method == "POST":
        
        # Get data from form submission
        form = request.POST

        # Get the existing meeting information
        meeting = Meeting.objects.get(id=id)

        # Update meeting event information
        event = Eventlist.objects.get(meeting=meeting, role=form['role'])
        event.description = form['description']
        event.save()
        
    # Return to the index page
    return HttpResponseRedirect(reverse("agenda:index"))


def fetch_call_recommend_one_role(request):
    # Updating role holder must be via POST request
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get JSON data from request
    data = json.loads(request.body.decode("utf-8"))
    meeting_id = data.get("meeting_id", "")
    role = data.get("role", "")

    # Get the list for this meeting and role
    meeting = Meeting.objects.get(id=meeting_id)
    recommendations = role_recommendation_list(meeting)
    recommend_role = recommendations[role]

    # Return json response with new recommendation list
    recommendation_list = [{'recommendation_list': recommend_role}]
    return JsonResponse(recommendation_list, safe=False)


def add_new_event(request):
    # Updating role holder must be via POST request
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get JSON data from request
    data = json.loads(request.body.decode("utf-8"))
    meeting_id = data.get("meeting_id", "")
    event_number = data.get("event_number", "")

    # Get the list for this meeting and role
    meeting = Meeting.objects.get(id=meeting_id)
    new_event = Eventlist(meeting=meeting, event_number=event_number)
    new_event.save()

    # Return json response with success message
    return JsonResponse(f'Successfully added new event {event_number} to meeting {meeting_id}', safe=False)


def report_bug(request):
    # If request is via post, process the data and submit the bug report
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BugForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            bug_type = form.cleaned_data['bug_type']
            bug_location = form.cleaned_data['bug_location']
            bug_description = form.cleaned_data['bug_description']
            contact_info = form.cleaned_data['contact_info']
            user = request.user

            # Create and save a new entry in the bug list
            new_bug = Buglist(user=user, bug_type=bug_type, bug_location=bug_location, bug_description=bug_description, contact_info=contact_info)
            new_bug.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('agenda:index'))

    # If request is via GET load the bug report page
    return render(request, "agenda/bug_report.html", {
        'bug_report_form': BugForm(),
    })


# View the list of bugs users have reported
@login_required
def bug_list(request):

    # load the buglist entries
    list_of_bugs = Buglist.objects.filter().order_by('bug_type')

    return render(request, "agenda/bug_list.html", {
        'bug_list': list_of_bugs,
    })


def change_event_number(request):
    # Updating attendence must be via POST request
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get fetch request data
    data = json.loads(request.body.decode("utf-8"))
    event_number = data.get("event_id", "")
    action = data.get('action', "")
    meeting_id = data.get("meeting_id", "")

    # Check if the event is being deleted
    if action == 'delete':
        meeting = Meeting.objects.get(id=meeting_id)  # Get the meeting
        event = Eventlist.objects.get(meeting=meeting, event_number=event_number)  # Get the event to be deleted
        event.delete()  # Delete the event

        # Update the event number of all the following events
        eventlist = Eventlist.objects.filter(meeting=meeting).order_by('event_number')
        for event in eventlist:
            if int(event.event_number) > int(event_number):
                event.event_number = int(event.event_number) - int(1)
                event.save()

        return JsonResponse(f'Event {event_number} successfully deleted', safe=False)  # Return success message

    # Check if event is being increased or decreased
    elif action == 'increase':
        event_number2 = int(event_number) - 1
    elif action == 'decrease':
        event_number2 = int(event_number) + 1

    if event_number2 == 0:
        return JsonResponse("Can't increase the first entry", safe=False)

    # Get the meeting info
    meeting = Meeting.objects.get(id=meeting_id)

    # Update eventlist order in the database
    event1 = Eventlist.objects.get(meeting=meeting, event_number=event_number)
    event2 = Eventlist.objects.get(meeting=meeting, event_number=event_number2)

    event1.event_number = event_number2
    event1.save()
    event2.event_number = event_number
    event2.save()

    action = [{'action': 'status'}]
    return JsonResponse(action, safe=False)


@login_required
def confirmation_emails(request, id):
    # If the user is not an executive reroute them to the main page
    if request.user.executive == False:
        return HttpResponseRedirect(reverse('agenda:index'))

    # Check if an email form is being submitted
    if request.method =="POST":
        # Get data from form submission
        form = request.POST
        recipients = findall('\S+@\S+', form['recipients']) # Get the recipients list

        # Create and send the email for each recipient
        for member_email in recipients:
            try:  # Try to send a user the email, except if the user doesn't exist.
                username = User.objects.filter(email=member_email).first().username # Get the recipient's name
                body = form['body'] # Get the email body
                body = body.replace("$/Name/$", username)  # Replace the variables in the body with the user's name
                email = EmailMessage(form['subject'], body, to=[member_email])  # Create the email message
                email.send()  # Send the email
            except:
                pass
        
        # Redirect the user to the meeting page
        return HttpResponseRedirect(reverse("agenda:meeting", args=(id,)))


    # Else user is trying to access the email confirmation dashboard page

    # Get all necesarry information from database
    meeting = Meeting.objects.get(id=id)  # Get the meeting user wants to make confirmation emails for
    attendees = Attendee.objects.filter(meeting=meeting).values()  # Get the users in attendence at the meeting

    for attendee in attendees:  # Add contact information to each attendee
        # Get the User information
        user = User.objects.get(id=attendee['user_id'])

        # Append user contact info to attendees list
        attendee['username'] = user.username
        attendee['email'] = user.email
        attendee['role'] = []

    # Add roles to all attendee information
    rolelist = meeting_roles_list(meeting)
    for role in rolelist:  # Iterate through the rolelist
        if rolelist[role] != None:  # Exclude any roles without a user holding them
            for attendee in attendees:  # Iterate through the attendee list to find a match for the role holder
                if str(rolelist[role]) == str(attendee['username']):
                    attendee['role'].append(str(role))
    
    # Make a list of the roles that still have to be filled
    unfilled_roles = []
    for role in rolelist:
        if rolelist[role] == None:
            unfilled_roles.append(role)

    # Make a list of all members with unknown attendance
    unknown_attendees = []
    for attendee in attendees:
        if attendee['status'] == 'U':
            unknown_attendees.append(attendee)

    return render(request, "agenda/confirmation_emails.html", {
                "meeting": meeting,
                'unknown_attendees': unknown_attendees,
            })
    

def confirm_attendance(request, id, username, status):
    # Update user's attendence in the database
    user = User.objects.get(username=username)
    meeting = Meeting.objects.get(id=id)
    attendee = Attendee.objects.filter(user=user, meeting=meeting)
    attendee = attendee[0]
    attendee.status = status
    attendee.save()
    # Redirect the user to the meeting page
    return HttpResponseRedirect(reverse("agenda:meeting", args=(id,)))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)

            return HttpResponseRedirect(reverse('agenda:index'))
        else:
            return render(request, "agenda/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "agenda/login.html", {})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("agenda:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "agenda/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "agenda/register.html", {
                "message": "Username already taken."
            })
        login(request, user)

        # Add user attendence to all meetings
        meetings = Meeting.objects.filter()
        for meeting in meetings:
            new_attendence = Attendee(user=user, meeting=meeting, status="U")
            new_attendence.save()

        return HttpResponseRedirect(reverse("agenda:index"))
    else:
        return render(request, "agenda/register.html")


# Function for executives to create a new user
@login_required
def create_user(request):

    # Check for a POST request
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Generate a random password
        # Random password generator from https://medium.com/analytics-vidhya/create-a-random-password-generator-using-python-2fea485e9da9
        length = 20

        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        num = string.digits
        symbols = string.punctuation

        all_characters = lower + upper + num + symbols

        temp = random.sample(all_characters,length)
        password = "".join(temp)

        all_characters = string.ascii_letters + string.digits + string.punctuation
        password = "".join(random.sample(all_characters,length))

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "agenda/create_user.html", {
                "message": "Username already taken."
            })
        
        # Add user attendence to all meetings
        meetings = Meeting.objects.filter()
        for meeting in meetings:
            new_attendence = Attendee(user=user, meeting=meeting, status="U")
            new_attendence.save()

        return HttpResponseRedirect(reverse("agenda:index"))
    
    return render(request, "agenda/create_user.html")