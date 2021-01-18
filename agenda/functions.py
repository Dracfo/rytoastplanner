from django.db.models import Q
from datetime import datetime, timedelta, time, date

from .models import User, Meeting, Rolelist, Attendee, BugForm, Buglist, Eventlist


def update_meeting(meeting, new_roles):

    print(f'new_roles: {new_roles}')

    # Update the meeting time
    new_datetime = new_roles['date'] + " " + new_roles['start_time']
    meeting.starttime = new_datetime

    # Update the meeting WoD and Theme
    meeting.wod = new_roles['wod']
    meeting.theme = new_roles['theme']

    meeting.save()

    # Get the meeting information
    roles = Rolelist.objects.get(meeting=meeting)

    # Create a list of all the old roles and who has filled them
    rolelist = {
        'Toastmaster': roles.toastmaster,
        'Chair': roles.chair,
        'Facilitator': roles.facilitator,
        'Zoom Master': roles.zoom,
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
                    elif old_key == 'Zoom Master':
                        roles.zoom = User.objects.filter(username=new_roles[new_key]).first()
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
                    
                    roles.save()  

    # Update the meeting eventlist
    eventlist = Eventlist.objects.filter(meeting=meeting).order_by('event_number').values()  # Get the existing events for the meeting
    print(new_roles)
    index = 1
    for event in eventlist:  # iterate through the existing eventlist and replace the entries
        try:
            event_changes = Eventlist.objects.get(id=event['id'])  # Get the event object to edit
            event_changes.description = new_roles[f'{index} description']
            event_changes.role = new_roles[f'{index} role']
            event_changes.duration = new_roles[f'{index} duration']
            event_changes.green_time = new_roles[f'{index} min_time']
            event_changes.yellow_time = new_roles[f'{index} mid_time']
            event_changes.red_time = new_roles[f'{index} max_time']

            event_changes.save()

            index += 1
        except:
            index += 1

    return


def update_one_role_in_database(role, rolelist, user):
    #Iterate through all the roles in plain text, if you find a match update the database entry
    if role == "Facilitator":
        if user == "None":
            rolelist.facilitator = None
        else:
            rolelist.facilitator = user
        rolelist.save()
        return True
    elif role == "Zoom Master":
        if user == "None":
            rolelist.zoom = None
        else:
            rolelist.zoom = user
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


def meeting_roles_list(meeting):
    
    # Get the meeting information
    roles = Rolelist.objects.filter(meeting=meeting)

    # Create a list of all the roles and who has filled them
    rolelist = {
        'Toastmaster': roles[0].toastmaster,
        'Chair': roles[0].chair,
        'Facilitator': roles[0].facilitator,
        'Zoom Master': roles[0].zoom,
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
        'Ballot Counter': roles[0].zoom,
        'Quizmaster': roles[0].quizmaster,
    } 

    return rolelist


def create_default_eventlist(meeting):

    # List of all the default events
    # Format = [description, role, duration, green_time, yellow_time, red_time]
    default_eventlist = [
        ['Call Meeting to Order, Meeting Rules, Introduce Toastmasters, Welcome Guests', 'Chair', 3, 1, 2, 3],
        ['Introduce the Timer, Ah Counter, Quizmaster, and General Evaluator', 'Toastmaster', 5, 3, 4, 5],
        ['*Speech 1*\nPathway: \nLevel: \nProject: ', "Speaker 1", 7, 5, 6, 7],
        ['*Speech 2*\nPathway: \nLevel: \nProject: ', "Speaker 2", 7, 5, 6, 7],
        ['*Speech 3*\nPathway: \nLevel: \nProject: ', "Speaker 3", 7, 5, 6, 7],
        ['Best Speech Voting', "Zoom Master", 1, 0.5, 0.75, 1],
        ['Evaluation 1', "Evaluator 1", 3, 2, 2.5, 3],
        ['Evaluation 2', "Evaluator 2", 3, 2, 2.5, 3],
        ['Evaluation 3', "Evaluator 3", 3, 2, 2.5, 3],
        ['Table Topics', "Table Topics Master", 25, 15, 20, 25],
        ['Best Table Topics Speech Voting', "Zoom Master", 1, 0.5, 0.75, 1],
        ['Table Topics Evaluations', "Table Topics Evaluator", 4, 2, 3, 4],
        ["Timer's Report", "Timer", 3, 1, 2, 3],
        ["Ah Counter's Report", "Ah Counter", 3, 1, 2, 3],
        ["Quizmaster's Report", "Quizmaster", 3, 1, 2, 3],
        ["Ballot Counter's Report", "Zoom Master", 2, 1, 1, 2],
        ["General Evaluator's Report", "General Evaluator", 5, 3, 4, 5],
        ["Next Meeting Role/Speech Sign Ups", "Toastmaster", 3, 1, 2, 3],
        ["Club Business and Guest Feedback", "", 3, 1, 2, 3],
        ["Membership and Pathways Information", "", 3, 1, 2, 3],
        ["Group Photo", "Zoom Master", 1, 0.5, 0.75, 1],
        ["Meeting Adjourned", "", 0, 0, 0, 0]
    ]

    # Create each of the default events
    # Fill in the meeting properties for each meeting
    event_number = 1
    for event in default_eventlist:
        event = Eventlist(meeting=meeting, event_number=event_number, description=event[0], role=event[1], duration=event[2], green_time=event[3], yellow_time=event[4], red_time=event[5])
        event.save()
        event_number = event_number + 1

    # Get the eventlist for the meeting form the database and return it
    final_eventlist = Eventlist.objects.filter(meeting=meeting).order_by('event_number').values()

    return final_eventlist


def role_recommendation_list(meeting):
    recommendation_list = {'Toastmaster': [], 'Facilitator': [], 'Zoom Master': [],'Chair': [], 'General Evaluator': [], 'Speaker 1': [], 'Speaker 2': [], 'Speaker 3': [], 'Evaluator 1': [], 'Evaluator 2': [], 'Evaluator 3': [], 'Table Topics Master': [], 'Table Topics Evaluator': [], 'Timer': [], 'Ah Counter': [], 'Ballot Counter': [], 'Quizmaster': [], 'Sergeant At Arms': []}
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
            indicator = '#CCCC00'
        else:
            indicator = 'green'
        
        recommendations.append({'user': role_holder, 'time_since': time_since_role, 'indicator': indicator})

    return recommendations


# Function to convert the plain text display versions of roles to the shorthand I use for the database and backend
def convert_role_to_shorthand(role):
    #Iterate through all the roles, if you find a match return the shorthand version of the role
    if role == "Facilitator":
        return "facilitator"
    elif role == "Zoom Master":
        return "zoom"
    elif role == "Toastmaster":
        return "toastmaster"
    elif role == "General Evaluator":
        return "geneval"
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