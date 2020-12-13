import time
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime, timedelta, time, date
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .models import User, Meeting, Rolelist, Attendee


# View the first upcoming meeting's individual page
def index(request):
    
    # Get the start and end dates for the meeting query
    startdate = date.today()
    enddate = startdate + timedelta(days=365)

    # Get the next meeting
    next_meeting = Meeting.objects.filter(starttime__range=[startdate, enddate]).first()

    if next_meeting == None:
        return HttpResponseRedirect(reverse("agenda:login"))

    # Redirect to views.meeting to load the individual meeting page for the next meeting
    return HttpResponseRedirect(reverse("agenda:meeting", args=(next_meeting.id,)))


# View individual meeting page
def meeting(request, id):

    # Get the next meeting information
    meeting = Meeting.objects.filter(id=id).order_by('-starttime')
    
    roles = Rolelist.objects.filter(meeting=meeting[0])
    rolelist = meeting_roles_list(meeting[0])
    print(rolelist)

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
        elif attendee.status == "F":
            absentees.append(attendee.user)
        elif attendee.status == "T":
            confirmed_attendees.append(attendee.user)


    # Create list of events that will occur during the meeting
    eventlist = {
        'Call meeting to order and cover meeting rules': [1, 0, "Sergeant At Arms", roles[0].saa, "30-45-60 sec"],
        'Welcome guests and introduce Toastmasters': [2, 0, "Chair", rolelist['Chair'], "1-1:30-2 min"],
        'Introduce the Timer, Ah Counter, Quizmaster, and General Evaluator': [5, 0, "Toastmaster", rolelist['Toastmaster'], "3-4-5 min"],
        'Speech 1': [7, 0, "Speaker 1", rolelist['Speaker 1'], "5-6-7 min"],
        'Speech 2': [7, 0, "Speaker 2", rolelist['Speaker 2'], "5-6-7 min"],
        'Speech 3': [7, 0, "Speaker 3", rolelist['Speaker 3'], "5-6-7 min"],
        'Best Speech Voting': [1, 0, "Ballot Counter", rolelist['Facilitator'], "30-45-60 sec"],
        'Evaluation 1': [3, 0, "Evaluator 1", rolelist['Evaluator 1'], "2-2:30-3 min"],
        'Evaluation 2': [3, 0, "Evaluator 2", rolelist['Evaluator 2'], "2-2:30-3 min"],
        'Evaluation 3': [3, 0, "Evaluator 3", rolelist['Evaluator 3'], "2-2:30-3 min"],
        'Table Topics': [19, 0, "Table Topics Master", rolelist['Table Topics Master'], "10-12:30-15 min"],
        'Best Table Topics Speech Voting': [1, 0, "Ballot Counter", rolelist['Facilitator'], "30-45-60 sec"],
        'Table Topics Evaluations': [4, 0, "Table Topics Evaluator", rolelist['Table Topics Evaluator'], "2-3-4 min"],
        "Timer's Report": [3, 0, "Timer", rolelist['Timer'], "1-2-3 min"],
        "Ah Counter's Report": [3, 0, "Ah Counter", rolelist['Ah Counter'], "1-2-3 min"],
        "Quizmaster's Report": [2, 0, "Quizmaster", rolelist['Quizmaster'], "1-1:30-2 min"],
        "General Evaluator's Report": [5, 0, "General Evaluator", rolelist['General Evaluator'], "3-4-5 min"],
        "Next Meeting Role/Speech Sign Ups": [3, 0, "VP Education", "Miguel", "1-2-3 min"],
        "Club Business and Guest Feedback": [5, 0, "President", "Michael", "3-4-5 min"],
        "Membership and Pathways Information": [5, 0, "Director of Membership", "Alex", "3-4-5 min"],
        "Group Photo": [1, 0, "Facilitator", rolelist['Facilitator'], "30-45-60 sec"],
        "Meeting Adjourned": [0, 0, "", "", ""]
    }

    # Add start times to each event based on the durations
    f = '%I:%M'
    t = meeting[0].starttime
    printer = t.strftime("%X")
    for key in eventlist:
        # Print event start time to eventlist
        eventlist[key][1] = t.strftime(f)

        # Update event start time
        min_to_add = eventlist[key][0]
        t = t + timedelta(minutes = min_to_add)

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
        'username': str(request.user.username)

    })


def meeting_list(request):

    # Get the start and end dates for the next year
    startdate = date.today() - timedelta(days=1)
    enddate = startdate + timedelta(days=366)

    # Get the list of meetings for the next year
    meeting_list_query = Meeting.objects.filter(starttime__range=[startdate, enddate])

    # Setup the meeting list with dates and role holders
    list_of_meetings = []
    for meeting in meeting_list_query:

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
        meeting_entry_for_the_list = {'id': meeting.id, 'date': meeting.starttime.strftime("%d/%b/%Y"), 'speech_count': speech_count, 'toastmaster': toastmaster, 'geneval': geneval, 'ttmaster': ttmaster}
        
        # Add dictionary for the individual meeting to the list of all meetings to be passed to the template to display
        list_of_meetings.append(meeting_entry_for_the_list)

    # Render the list of meetings
    return render(request, "agenda/meeting_list.html", {
        'meeting_list': list_of_meetings
    })


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

        # Get the existing meeting information
        meeting = Meeting.objects.filter(id=id)

        # Update meeting information
        update_meeting(meeting[0], form)

        return HttpResponseRedirect(reverse("agenda:index"))

    
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

    return render(request, "agenda/edit_meeting.html", {
        'new_meeting': False,
        'id': id,
        'meeting': meeting,
        'start_date': start_date,
        'start_time': start_time,
        'roles': roles,
        'users': users,
    })


@login_required
def create_meeting(request):

    # Get the list of meetings ordered highest id first
    meeting = Meeting.objects.filter().order_by('-id')

    # If no meetings exist yet set id to 1
    if meeting == None:
        id = 1
    
    # Else add 1 to the highest id
    else:
        id = meeting[0].id + 1

    print(meeting[0].id)

    return HttpResponseRedirect(reverse("agenda:edit_meeting", args=(id,)))


def spreadsheet(request):

    # Find meetings in next 4 months
    startdate = date.today() - timedelta(days=31)
    enddate = date.today() + timedelta(days=62)
    meeting_list = Meeting.objects.filter(starttime__range=[startdate, enddate])

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
        'Ballot Counter': [],
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


def meeting_roles_list(meeting):
    
    # Get the meeting information
    roles = Rolelist.objects.filter(meeting=meeting)

    # Create a list of all the roles and who has filled them
    rolelist = {
        'Toastmaster': roles[0].toastmaster,
        'Chair': roles[0].chair,
        'Facilitator': roles[0].facilitator,
        'General Evaluator': roles[0].geneval,
        'Speaker 1': roles[0].speaker1,
        'Speaker 2': roles[0].speaker2,
        'Speaker 3': roles[0].speaker3,
        'Evaluator 1': roles[0].eval1,
        'Evaluator 2': roles[0].eval2,
        'Evaluator 3': roles[0].eval3,
        'Table Topics Master': roles[0].ttmaster,
        'Table Topics Evaluator': roles[0].tteval,
        'Timer': roles[0].timer,
        'Ah Counter': roles[0].ah_counter,
        'Ballot Counter': roles[0].facilitator,
        'Quizmaster': roles[0].quizmaster,
        'Sergeant At Arms': roles[0].saa
    } 

    return rolelist


def update_meeting(meeting, new_roles):

    # Update the meeting time
    new_datetime = new_roles['date'] + " " + new_roles['start_time']
    meeting.starttime = new_datetime
    meeting.save()

    # Get the meeting information
    roles = Rolelist.objects.filter(meeting=meeting)
    roles = roles[0]

    # Create a list of all the old roles and who has filled them
    rolelist = {
        'Toastmaster': roles.toastmaster,
        'Chair': roles.chair,
        'Facilitator': roles.facilitator,
        'General Evaluator': roles.geneval,
        'Speaker 1': roles.speaker1,
        'Speaker 2': roles.speaker2,
        'Speaker 3': roles.speaker3,
        'Evaluator 1': roles.eval1,
        'Evaluator 2': roles.eval1,
        'Evaluator 3': roles.eval1,
        'Table Topics Master': roles.ttmaster,
        'Table Topics Evaluator': roles.tteval,
        'Timer': roles.timer,
        'Ah Counter': roles.ah_counter,
        'Ballot Counter': roles.facilitator,
        'Quizmaster': roles.quizmaster,
        'Sergeant At Arms': roles.saa,
    }

    for old_key in rolelist:  # Iterate through the old rolelist
        for new_key in new_roles:  # Iterate through the new roles user has submitted
            if old_key == new_key:  # If the roles in both lists match (ex: Toastmaster and Toastmaster)
                if str(rolelist[old_key]) != str(new_roles[new_key]):  # If the new role assignment is different than the old role assignment
                    if old_key == 'Toastmaster':
                        roles.toastmaster = User.objects.filter(username=new_roles[new_key]).first()
                    elif old_key == 'Chair':
                        roles.chair = User.objects.filter(username=new_roles[new_key]).first()
                    elif old_key == 'Facilitator':
                        roles.facilitator = User.objects.filter(username=new_roles[new_key]).first()
                    elif old_key == 'General Evaluator':
                        roles.geneval = User.objects.filter(username=new_roles[new_key]).first()
                    elif old_key == 'Speaker 1':
                        roles.speaker1 = User.objects.filter(username=new_roles[new_key]).first()
                    elif old_key == 'Speaker 2':
                        roles.speaker2 = User.objects.filter(username=new_roles[new_key]).first()
                    elif old_key == 'Speaker 3':
                        roles.speaker3 = User.objects.filter(username=new_roles[new_key]).first()
                    elif old_key == 'Evaluator 1':
                        roles.eval1 = User.objects.filter(username=new_roles[new_key]).first()
                    elif old_key == 'Evaluator 2':
                        roles.eval2 = User.objects.filter(username=new_roles[new_key]).first()
                    elif old_key == 'Evaluator 3':
                        roles.eval3 = User.objects.filter(username=new_roles[new_key]).first()
                    elif old_key == 'Table Topics Master':
                        roles.ttmaster = User.objects.filter(username=new_roles[new_key]).first()
                    elif old_key == 'Table Topics Evaluator':
                        roles.tteval = User.objects.filter(username=new_roles[new_key]).first()
                    elif old_key == 'Timer':
                        roles.timer = User.objects.filter(username=new_roles[new_key]).first()
                    elif old_key == 'Ah Counter':
                        roles.ah_counter = User.objects.filter(username=new_roles[new_key]).first()
                    elif old_key == 'Ballot Counter':
                        roles.facilitator = User.objects.filter(username=new_roles[new_key]).first()
                    elif old_key == 'Quizmaster':
                        roles.quizmaster = User.objects.filter(username=new_roles[new_key]).first()
                    elif old_key == 'Sergeant At Arms':
                        roles.saa = User.objects.filter(username=new_roles[new_key]).first()
                    
                    roles.save()
                    

    return


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


def update_one_role_in_database(role, rolelist, user):
    #Iterate through all the roles in plain text, if you find a match update the database entry
    if role == "Facilitator":
        if user == "None":
            rolelist.facilitator = None
        else:
            rolelist.facilitator = user
        rolelist.save()
        return True
    elif role == "Toastmaster":
        if user == "None":
            rolelist.toastmaster = None
        else:
            rolelist.toastmaster = user
        rolelist.save()
        return True
    elif role == "General Evaluator":
        if user == "None":
            rolelist.geneval = None
        else:
            rolelist.geneval = user
        rolelist.save()
        return True
    elif role == "Sergeant At Arms":
        if user == "None":
            rolelist.saa = None
        else:
            rolelist.saa = user
        rolelist.save()
        return True
    elif role == "Chair":
        if user == "None":
            rolelist.chair = None
        else:
            rolelist.chair = user
        rolelist.save()
        return True
    
    elif role == "Speaker 1":
        if user == "None":
            rolelist.speaker1 = None
        else:
            rolelist.speaker1 = user
        rolelist.save()
        return True
    elif role == "Speaker 2":
        if user == "None":
            rolelist.speaker2 = None
        else:
            rolelist.speaker2 = user
        rolelist.save()
        return True
    elif role == "Speaker 3":
        if user == "None":
            rolelist.speaker3 = None
        else:
            rolelist.speaker3 = user
        rolelist.save()
        return True
    elif role == "Evaluator 1":
        if user == "None":
            rolelist.eval1 = None
        else:
            rolelist.eval1 = user
        rolelist.save()
        return True
    elif role == "Evaluator 2":
        if user == "None":
            rolelist.eval2 = None
        else:
            rolelist.eval2 = user
        rolelist.save()
        return True
    elif role == "Evaluator 3":
        if user == "None":
            rolelist.eval3 = None
        else:
            rolelist.eval3 = user
        rolelist.save()
        return True
    
    elif role == "Table Topics Master":
        if user == "None":
            rolelist.ttmaster = None
        else:
            rolelist.ttmaster = user
        rolelist.save()
        return True
    elif role == "Table Topics Evaluator":
        if user == "None":
            rolelist.tteval = None
        else:
            rolelist.tteval = user
        rolelist.save()
        return True
    
    elif role == "Timer":
        if user == "None":
            rolelist.timer = None
        else:
            rolelist.timer = user
        rolelist.save()
        return True
    elif role == "Ah Counter":
        if user == "None":
            rolelist.ah_counter = None
        else:
            rolelist.ah_counter = user
        rolelist.save()
        return True
    elif role == "Quizmaster":
        if user == "None":
            rolelist.quizmaster = None
        else:
            rolelist.quizmaster = user
        rolelist.save()
        return True

    return false


def role_recommendation_list(meeting):
    recommendation_list = {'Toastmaster': [], 'Facilitator': [], 'Chair': [], 'General Evaluator': [], 'Speaker 1': [], 'Speaker 2': [], 'Speaker 3': [], 'Evaluator 1': [], 'Evaluator 2': [], 'Evaluator 3': [], 'Table Topics Master': [], 'Table Topics Evaluator': [], 'Timer': [], 'Ah Counter': [], 'Ballot Counter': [], 'Quizmaster': [], 'Sergeant At Arms': []}
    temp_rec = []

    # Get list of users with confirmed or unknown attendence
    attendees = Attendee.objects.filter(meeting=meeting).filter(Q(status="T") | Q(status="U"))

    # Get all user information
    users = []
    for attendee in attendees:
        user = {'user': attendee.user.username, 'speech_count': attendee.user.speech_count, 'meeting_count': attendee.user.meeting_count, 'other_role': "", 'days_since_last_time': ""}
        users.append(user)

    # Sort users by experience level
    users.sort(key=sortByMeetingCountFunc)

    # Iterate through each of the meeting roles and get a recommendation list for each
    for role in recommendation_list:

        # Add all the users who will be attending
        for user in users:
            recommendation_list[role].append(user['user'])

        # Use the past role holders function to get the list of people who have held the role in the past time period
        past_holders = past_role_holders(meeting, role)

        for index, recommendation in enumerate(recommendation_list[role]):
            if past_holders == False:
                continue

            for user_info in past_holders:
                if recommendation == user_info['user']:
                    del recommendation_list[role][index]
                    recommendation_list[role].append(user_info)

        # Figure out and label the users who already have a role this meeting
        rolelist = meeting_roles_list(meeting)

        # Iterate through the existing list of recommendations for the role
        for index, recommendation in enumerate(recommendation_list[role]):

            # Iterate throguh the rolelist for the selected meeting
            for meeting_role in rolelist:

                # Check if the user being recommended already holds a role this meeting
                if str(recommendation) == str(rolelist[meeting_role]):

                    # Add the role to the user string to display in the dropdown role selector menu
                    recommendation_list[role][index] = " ".join((recommendation_list[role][index], "[" + str(meeting_role) + "]"))
                
                # Check if the user is a past role holder, they have to be treated differently because they use a dictionary instead of a plain string
                for key in recommendation:
                    if key == 'user':

                        # Check if the user being recommended already holds a role this meeting
                        if str(recommendation[key]) == str(rolelist[meeting_role]):

                            # Add the role to the user string to display in the dropdown role selector menu
                            recommendation_list[role][index]['user'] = " ".join((recommendation_list[role][index]['user'], "[" + str(meeting_role) + "]"))

    return recommendation_list


def sortByMeetingCountFunc(e):
    return e['meeting_count']

def sortByTimeSinceFunc(e):
    return e['time_since']


def past_role_holders(meeting, role):

    # Get the past 2 months of meetings
    startdate = meeting.starttime - timedelta(days=62)
    enddate = meeting.starttime - timedelta(days=1)
    meeting_list_query = Meeting.objects.filter(starttime__range=[startdate, enddate])

    # Check if there are past meetings
    if not meeting_list_query:
        return False

    # Get the role holder for each meeting
    recommendations = []
    for past_meeting in meeting_list_query:
        
        # Get who held the role at the meeting
        role_holder = ""
        role_list = Rolelist.objects.get(meeting=past_meeting)
        for field in role_list._meta.fields:
            if field.name == convert_role_to_shorthand(role):
                role_holder = str(getattr(role_list, field.name))

        # Get the time since the meeting
        time_since_role = meeting.starttime - past_meeting.starttime
        time_since_role = time_since_role.days

        # Assign a color to indicate how long it has been
        if time_since_role < 14:
            indicator = 'red'
        elif time_since_role < 31:
            indicator = 'yellow'
        else:
            indicator = 'green'
        
        recommendations.append({'user': role_holder, 'time_since': time_since_role, 'indicator': indicator})

    return recommendations


# Function to convert the plain text display versions of roles to the shorthand I use for the database and backend
def convert_role_to_shorthand(role):
    #Iterate through all the roles, if you find a match return the shorthand version of the role
    if role == "Facilitator":
        return "facilitator"
    elif role == "Toastmaster":
        return "toastmaster"
    elif role == "General Evaluator":
        return "geneval"
    elif role == "Sergeant At Arms":
        return "saa"
    elif role == "Chair":
        return "chair"
    
    elif role == "Speaker 1":
        return "speaker1"
    elif role == "Speaker 2":
        return "speaker2"
    elif role == "Speaker 3":
        return "speaker3"
    elif role == "Evaluator 1":
        return "eval1"
    elif role == "Evaluator 2":
        return "eval2"
    elif role == "Evaluator 3":
        return "eval3"
    
    elif role == "Table Topics Master":
        return "ttmaster"
    elif role == "Table Topics Evaluator":
        return "tteval"
    
    elif role == "Timer":
        return "timer"
    elif role == "Ah Counter":
        return "ah_counter"
    elif role == "Quizmaster":
        return "quizmaster"
    elif role == "Ballot Counter":
        return "facilitator"

    return "Invalid Role"


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