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