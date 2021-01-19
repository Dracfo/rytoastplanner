# CHANGELOG
All notable changes to this project will be documented in this file.

The format is adapted from [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]
---
### Added:
-

### Changed:
-

### Removed:
-

### Fixed:
-

### Security
-



## [1.0.1-beta] - 2021-Jan-19
---
### Changed:
- Spreadsheet view can only be accessed by loged in users
- Spreadsheet view only gets role recommendations if the user is an executive



## [1.0.0-beta] - 2021-Jan-19
---
### Added:
- Print button to individual meeting page
- Resources navbar dropdown with links to the club role descriptions and basecamp
- An editable guest list to the individual meeting page
- Ability to mark yourself as absent or attending from the spreadsheet view

### Changed:
- on_delete value of Foreign Keys in the rolelist model to be SET_NULL so that all the meeting rolelists aren't deleted when a user is deleted.

### Removed:
- Ability to create an account, it now has to be done by an executive.



## [0.7.1-alpha] - 2021-Jan-18
---
### Security
- Set CSRF_COOKIE_SECURE = False and SESSION_COOKIE_SECURE = False to try and fix issues with logging in.



## [0.7.0-alpha] - 2021-Jan-18
---
### Added:
- Latest features to the README.md file
- Zoom Master role
- An email confirmation view for every meeting which can be used to send confirmation emails
- Ability for members to confirm their attendance at a meeting through a url sent to their email


### Removed:
- Removed attendance information and bug button from the page when it is printed
- Removed Facilitator and Ballot Counter from displaying in individual meeting and spreadsheet pages



## [0.6.2-alpha] - 2021-Jan-16
---
### Fixed:
- Spreadsheet now displays meetings ordered by date instead of meeting number




## [0.6.1-alpha] - 2021-Jan-16
---
### Added:
- Ability for members to sign up and reject roles in the spreadsheet view using the 'Sign Up' and 'X' buttons

### Fixed:
- 'Sign Up' button not working on the individual meeting page
- Member not being able to remove themselves from a role on individual meeting page



## [0.6.0-alpha] - 2021-Jan-15
---
### Added:
- Meeting themes to the meeting list view
- Bulk Create Meeting button to the navbar in the executive dropdown
- Added the ability to create meetings in bulk with the Bulk_Create_Meetings view

### Changed:
- Edit_meeting view now redirects you to the page for the meeting you just edited instead of the index page

### Fixed:
- Removed 'Edit Meeting' button for non-executives on individual meeting pages
- Removed 'X' button from the Absences and Meeting_id row in the spreadsheet view
- Removed the Meeting_id row from the spreadsheet view



## [0.5.0-alpha] - 2021-Jan-14
---
### Changed:
- Default description for the Chairperson's introduction
- Moved update_one_role_in_database, create_default_eventlist, role_recommendation_list, past_role_holders, and convert_role_to_shorthandfuncions to functions.py from views.py
- Changed redirection when there isn't an upcoming meeting to the meeting list. Used to be the login apge, which was confusing.

### Removed:
- Padding from the description textarea in the edit_meeting view

### Security
- Changed DEBUG setting value to an environment variable so that it is true locally and false in production
- Changed email password to be inputted using an environment variable
- Also changed the gmail password so that past git commits would not compromise future security of the email account
- Changed CSRF_COOKIE_SECURE and SESSION_COOKIE_SECURE to be True



## [0.4.1-alpha] - 2021-Jan-11
---
### Fixed:
- Error with creating a meeting due to a 20 character limit on role names being hit by the Table Topics Evaluator. Changed to 30 character limit.



## [0.4.0-alpha] - 2021-Jan-11
---
### Added:
- Links to role descriptions on the individual page sidebar
- Ability to edit meeting events in the edit_meeting view
- Ability for memebrs to update the speech description in the individual meeting page if they are signed in and signed up for that role

### Changed:
- Individual meeting page to render using the Eventlist database instead of the hardcoded string, sets up the eventlist to become editable in future.
- Schedule view now doesn't show past meetings
- Moved update_meeting function to the new functions.py file for non-view functions
- Speech descriptions to include asterisks at beginning and end to differentiate the title from the description

### Fixed:
- Name appearing twice on individual meeting page
- 'X' button not working in eventlist of individual meeting page
- Homepage not directing to the next meeting from today
- Meeting List View listing meetings in reverse chronological order



## [0.3.1-alpha] - 2021-Jan-07
---
### Added:
- Login page now displays errors if login information is incorrect or entered incorrectly

### Removed:
- Sergeant at arms from meeeting templates

### Fixed:
- Meeting Word of the Day and Theme not updating through the edit meeting form
- Delete button on single meeting page does nto appear if no one can be scheduled to a role now



## [0.3.0-alpha] - 2020-Dec-20
---
### Changed:
- Email support to use the gmail account RyToastPlanner@gmail.com instead of just creating a file



## [0.2.4-alpha] - 2020-Dec-20
---
### Changed:
- Changed email file folder from sent_emails to django-email-dev



## [0.2.3-alpha] - 2020-Dec-19
---
### Added:
- Added note about admins manually emailing password reset instructions to users to password reset forms

### Changed:
- Added white container boxes to login and password reset pages content
- Added white container to meeting page Attendence Information header
- Changed password reset form buttons to blue bootstrap style instead of default HTML gray
- Moved edit meeting button to the top of individual meeting page, in the page header section



## [0.2.2-alpha] - 2020-Dec-17
---
### Fixed:
- Bug where meeting could not be edited due to the @login_required decorator stopping the update_meeting function even when logged in.  




## [0.2.1-alpha] - 2020-Dec-17
---
### Fixed:
- Bug where meetings could not be created because the variable was being improperly referenced



## [0.2.0-alpha] - 2020-Dec-17
---
### Added:
- Word of the Day and Theme form elements to the edit meeting page
- Create user function for executives to create new user accounts with random passwords
- Added bootstrap javascript import code to layout header
- Added ability for the Toastmaster and Facilitator to assign memebrs to roles for the meeting they are serving in the role
- Added ability to reset password (Emails with the link are currently logged in a local folder)
- README.md file with project description

### Changed:
- Changed 'a' element colour to Toastmasters blue (#004165)
- All navbar elements restricted to executives are now in a dropdown menu in the nabar labels "Executive"
- Navbar toggler icon (hamburger menu button on small screens) is now white
- Login and logout functions to use the default django.contrib.auth.urls instead of custom functions

### Removed:
- Requirement that users have a last speech date and time filled in on their accounts

### Fixed:
- Bug where meetings could not be created if no meetings exist



## [0.1.0-alpha] - 2020-Dec-14
---
### Added:
- Created CHANGELOG.md file and began documenting changes
- Added a Buglist model, form, floating button, report page, and list to get bug reports from users and view as administrator
- Added alerts to the top of the layout page
- Added Word of the Day and Meeting Theme fields to the Meeting model
- Added None option to role selector drop downs in meeting and spreadsheet pages
- Added link to the Eventbrite in the meeting page sidebar
- Added Delete Meeting Function
- Added title to edit meeting page


### Changed:
- Made the delete buttons smaller
- Edit Meeting container background colour to white  



## [0.0.0-alpha] - 20YY-MMM-DD (Copiable template for new versions)
---
### Added:
-

### Changed:
-

### Removed:
-

### Fixed:
-

### Security
-