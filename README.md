# RyToast Planner - A Toastmasters Meeting Role Scheduling Webapp
Rytoast Planner is a web app created to schedule club members for roles at the Ryerson Toastmasters. Created using Django 3.1.2, Python 3.9, Bootstrap 4.4.1, and Heroku Postgres.

This app was originally created as the capstone project for [CS50’s Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/2020/) course.

Visit the live website: https://rytoastplanner.herokuapp.com/

![Meeting Page Screenshot](/meeting_page.PNG)



<br>

## Table of contents
---
- [Features](#features)
- [Files](#files)
- [Status](#status)
- [Inspiration](#inspiration)
- [Contact Information](#contact-information)



<br>

## Features
---
#### Meeting Management
- Executives can create, edit, and delete meetings.
- Set and manage the meeting start time, theme, and word of the day
- Manage the events that occur at each meeting (duration, description, role, order, user)
- View the meetings individually, as a list, or as a spreadsheet.
- Bulk create a group of meeting using the 'Bulk Create Meetings' button

#### Individual Meeting View
- View all the events of the meeting, including start times, duration, member assigned, and event description
- A sidebar with meeting information, helpful links, a list of the club executives with links to their LinkedIn, and a list of all the meeting roles with the members who are scheduled for them.
- Ability to confirm or deny attendance at the meeting

#### Meeting List View
- View the date of each meeting with a link to view the full meeting page
- View the number of speeches scheduled for each meeting
- View the theme for the meeting
- View the currently scheduled Toastmaster, General Evaluator, and Topicsmaster for each meeting

#### Spreadsheet View
- View all of the role holders for all of the future meetings in a spreadsheet format
- Members can sign up for any role at any meeting
- Executives can assign any available member to any future meeting

#### Role Scheduling
- Non-logged-in users can view all role holders for each meeting.
- Logged-In users can sign themselves up for roles at any meeting.
- Logged-In users can confirm or deny their attendance at a meeting. Denying it will remove them from the recommendation lists executives get while assigning members to roles.
- Executives can assign any member to any role for any meeting.
- Executives can remove members from their scheduled roles.
- Executives can see an ordered list of recommendations for which members should be scheduled for each role.

#### Authentication and Administration
- Register an account, log in, logout.
- Reset password via email confirmation
- Executives can create new member accounts.
- Executives are assigned using the Django Admin panel.
- Report a bug with the floating "Report a Bug" button.
- Website admin can view a sorted bug list on the Bug List page.



<br>

## Files
---
The following is a list of all the significant files in the web app and a description of their importance.
- The app uses an SQL database. In development, it is SQLite. In production, it is Heroku Postgres.
- **\RolesScheduler** contains the main Django section and settings.
    - **\RolesScheduler\urls.py** contains the redirects for the admin, authentication, and agenda app views.
- **\template\registration** contains all the HTML template files for the login and password reset pages.
- **\agenda** is the folder for the Django app.
    - **\agenda\templates\agenda** contains the HTML templates for the layout and the various meeting views.
    - **\agenda\static\agenda** contains the styles.css file with the custom CSS styles for the entire web app.
    - **\agenda\migrations** contains the migration information to create an SQL database for the web app.
    - **\agenda\templates\admin.py** allows the databases to be viewed from the Django admin panel.
    - **\agenda\templates\models.py** contains the models that the SQL database uses
        - There are models for the users, meetings, role lists, attendees, eventlists, and the bug list.
        - There is a form for the bug list.
        - There is also a function to display 'deleted' where a user used to be if their account is deleted.
    - **\agenda\templates\views.py** contains all the views and many of the functions of the web app.
        - The views are for the index, meeting, meeting list, edit meeting, create a meeting, delete a meeting, spreadsheet, report a bug, see the bug list, register an account, and create a user.
        - The API functions it contains are to update attendance records and sign up for a role.
    - **\agenda\templates\functions.py** contains all the helper functions for the web app. The functions are to:
        - Update a meeting role list
        - Update one role in the database
        - Create a meeting roles list
        - Create a new set of Eventlist models based on default meeting events
        - Make a role recommendation list
        - Sort a list of members
        - Get a list of past role holders for a specific role and meeting
        - Convert a display text role to the backend role shorthand.
    - **\agenda\templates\urls.py** contains all the URL patterns for the agenda app including:
        - spreadsheet, meeting, edit meeting, create a meeting, bulk create meetings, delete a meeting, meeting list, report bug, bug list, update a role description, register, and create a user.
        - It also includes URLs for the API routes to update attendance records, sign up for a role, make a recommendation list for a role, change an event number, and add a new event.



<br>

## Status
---
The web app is currently in a live alpha hosted using Heroku. It is still in active development and many features and bugs are left to add and fix.

If you are interested in attending a club meeting you can check out the [Ryerson Toastmasters Club Website](https://www.ryersontoastmasters.ca/) and sign up to attend a meeting on the [Eventbrite Page](https://www.eventbrite.ca/e/the-ryerson-toastmasters-weekly-membership-meeting-tickets-110513236064).

View the [live website](https://rytoastplanner.herokuapp.com/)

View the [CHANGELOG](CHANGELOG.md)

Future Features:
- Calendar page to see all meetings at a glance and add them to the user's 3rd party calendar.
- A panel for executives to manage members' accounts.
- Printer-friendly individual meeting view
- Printer-friendly spreadsheet view
- Ability to create and manage new Toastmasters Clubs
- Ability for a user to manage their profile (Username, email, password, image, etc)



<br>

## Inspiration
---
This app was created as the capstone project for [CS50’s Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/2020/) course. As such, it draws on the lessons and techniques taught in the course regarding Python, Django, SQL, and Javascript.

The front end of the web app was inspired by the [Toastmasters International Website](https://www.toastmasters.org/), the [Monday.com Dashboard](https://www.monday.com), and the [Dashboard Adobe XD UI kit](https://www.adobe.com/products/xd/features/ui-kits.html).

The [Python Django Tutorial: Deploying Your Application (Option #2) - Deploy using Heroku](https://youtu.be/6DI_7Zja8Zc) tutorial by Corey Schafer helped transfer the web app to Heroku.



<br>

## Contact Information
---
Name: Aidan Dennehy

Website/Portfolio: https://www.aidandennehy.ca

LinkedIn: https://www.linkedin.com/in/adennehy

Github: https://github.com/Dracfo