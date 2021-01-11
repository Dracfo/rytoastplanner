

from .models import User, Meeting, Rolelist, Attendee, BugForm, Buglist, Eventlist


def update_meeting(meeting, new_roles):

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
        event_changes = Eventlist.objects.get(id=event['id'])  # Get the event object to edit
        event_changes.description = new_roles[f'{index} description']
        event_changes.role = new_roles[f'{index} role']
        event_changes.duration = new_roles[f'{index} duration']
        event_changes.green_time = new_roles[f'{index} min_time']
        event_changes.yellow_time = new_roles[f'{index} mid_time']
        event_changes.red_time = new_roles[f'{index} max_time']

        event_changes.save()

        index += 1


    return


def create_default_eventlist(meeting):

    # List of all the default events
    # Format = [description, role, duration, green_time, yellow_time, red_time]
    default_eventlist = [
        ['Welcome guests, introduce Toastmasters, cover meeting rules', 'Chair', 3, 1, 2, 3],
        ['Introduce the Timer, Ah Counter, Quizmaster, and General Evaluator', 'Toastmaster', 5, 3, 4, 5],
        ['*Speech 1*\nPathway: \nLevel: \nProject: ', "Speaker 1", 7, 5, 6, 7],
        ['*Speech 2*\nPathway: \nLevel: \nProject: ', "Speaker 2", 7, 5, 6, 7],
        ['*Speech 3*\nPathway: \nLevel: \nProject: ', "Speaker 3", 7, 5, 6, 7],
        ['Best Speech Voting', "Ballot Counter", 1, 0.5, 0.75, 1],
        ['Evaluation 1', "Evaluator 1", 3, 2, 2.5, 3],
        ['Evaluation 2', "Evaluator 2", 3, 2, 2.5, 3],
        ['Evaluation 3', "Evaluator 3", 3, 2, 2.5, 3],
        ['Table Topics', "Table Topics Master", 15, 10, 12.5, 15],
        ['Best Table Topics Speech Voting', "Ballot Counter", 1, 0.5, 0.75, 1],
        ['Table Topics Evaluations', "Table Topics Evaluator", 4, 2, 3, 4],
        ["Timer's Report", "Timer", 3, 1, 2, 3],
        ["Ah Counter's Report", "Ah Counter", 3, 1, 2, 3],
        ["Quizmaster's Report", "Quizmaster", 3, 1, 2, 3],
        ["General Evaluator's Report", "General Evaluator", 5, 3, 4, 5],
        ["Next Meeting Role/Speech Sign Ups", "Toastmaster", 3, 1, 2, 3],
        ["Club Business and Guest Feedback", "", 4, 2, 3, 4],
        ["Membership and Pathways Information", "", 4, 2, 3, 4],
        ["Group Photo", "Facilitator", 1, 0.5, 0.75, 1],
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