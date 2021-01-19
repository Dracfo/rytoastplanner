document.onload = function(){
    alert('hello world');
}


// Function to parse string of user and their roles this meeting to return just the user as a string
function convert_user_and_roles_string_to_just_user(input) {
    record = [];

    for (var i = 0; i < input.length; i++) {
        if (input[i] != ' ') {
            record[i] = input[i];
        }
        else {
            record = record.join("");
            return record;
        }
    }
    // If there is only one word in the string, exit
    record = record.join("");
    return record;
}

// Navbar dropdown functionality
$('.dropdown-toggle').dropdown();



//Function to sign user up for a role when they click the sign up button
function sign_up(username, role, meeting_id, button) {

    console.log(username, role, meeting_id, button);

    // Check if this is coming form the spreadsheet and I still need to find the meeting id
    if (meeting_id == 'spreadsheet_exception') {
        // Get the column id
        const column = button.parentElement.id;
        console.log(column);

        // Get the meeting id from the top of the spreadsheet
        meeting_id = document.querySelector("thead").children[0].children[column].id;
        console.log(meeting_id);


    }

    fetch('/sign_up', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'user': username,
            'role': role,
            'meeting_id': meeting_id
        })
    })
        .then(response => response.json())
        .then(result => {
            // Print result
            console.log(result);
            return result;
        })
        .catch(function (err) {
            console.log(err);
        });

    // If the function call was to remove the user, update innerHTML with a role recommendation list
    if (username == 'None') {
        console.log("We're in the username == 'None' condition");
        console.log(role, meeting_id);

        //If the user is an executive, create a dropdown recommendation list
        if ('{{ request.user.executive }}' == 'True') {
            fetch('/fetch_call_recommend_one_role', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    'role': role,
                    'meeting_id': meeting_id
                })
            })
                .then(response => response.json())
                .then(result => {
                    // Print result
                    console.log(result);
                    console.log(result[0]['recommendation_list']);

                    // Get the recommendation list from the fetch call result
                    recommendation_list = result[0]['recommendation_list'];

                    // Make the recommendation list into a printable string
                    recommendation_str = "";
                    for (index in recommendation_list) {
                        if (typeof yourVariable === 'Object') {
                            recommendation_str = recommendation_str + `<option>${recommendation_list[index]['user']} - ${recommendation_list[index]['time_since']}  days ago</option>`;
                        }
                        else {
                            recommendation_str = recommendation_str + `<option>${recommendation_list[index]}</option>`;
                        }
                    }

                    // Update the innerHTML
                    console.log(`Role being deleted: ${role}`);
                    console.log(button.parentElement);
                    button.parentElement.innerHTML = `<select id="{{ value.2 }}" class="form-control" onchange='OnChange(this);'>
                    <option>None</option>
                    ${recommendation_str}
                </select>`;


                    return result;
                })
                .catch(function (err) {
                    console.log(err);
                });
        }



        // Else user is just a member, so just throw up a sign up button
        else {
            console.log("Addinng a sign up button to replace role holder");
            console.log(button);
            button.parentElement.innerHTML = `<button onclick="sign_up('{{ request.user.username }}', '${role}', '${meeting_id}', this);" class="btn btn-sm btn-primary" style="white-space: nowrap;">Sign Up</button>`;
        }

    }




    // if the function was to sign someone up for a role
    else {
        button.parentElement.innerHTML = `${username} <button class="btn btn-outline-danger btn-sm" onclick="sign_up('None', '${role}', '${meeting_id}', this);" id="${role}" style="margin: auto!important">X</button>`;
    }

    return false;
}


function confirm_attendence() {
    // Get username
    const username = document.querySelector('#confirm_attendence_btn').value;
    const meeting_id = {}, { meeting, id };
};

// Pass input to API
fetch('/attendence', {
    method: 'POST',
    credentials: 'same-origin',
    headers: {
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({
        'user': username,
        'meeting_id': meeting_id,
        'status': 'T'
    })
})
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        const action = result[0]['action'];

        // Update the attendence list buttons
        document.querySelector('#confirm_attendence_btn').style.display = 'none';
        document.querySelector('#decline_attendence_btn').style.display = 'block';

        // Update the attendence lists
        document.querySelector(`#${username}_attendence`).style.display = 'none';
        document.querySelector(`#${username}_decline_attendence`).style.display = 'none';
        document.querySelector(`#${username}_confirm_attendence`).style.display = 'block';
        document.querySelector(`#${username}_confirm_attendence`).innerHTML = username;
    })
    .catch(function (err) {
        console.log(err);
    });



return false;
}


function decline_attendence(id, username, page, button){
    // Get username
    const username = username;
    const meeting_id = id;
    
    // Pass input to API
    fetch('/attendence', {
        method: 'POST',
        credentials: 'same-origin',
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'user': username,
            'meeting_id': meeting_id,
            'status': 'F'
        })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        const action = result[0]['action'];

        // Update the attendence list buttons
        document.querySelector('#confirm_attendence_btn').style.display = 'block';
        document.querySelector('#decline_attendence_btn').style.display = 'none';

        // Update the attendence lists
        document.querySelector(`#${username}_attendence`).style.display = 'none';
        document.querySelector(`#${username}_confirm_attendence`).style.display = 'none';
        document.querySelector(`#${username}_decline_attendence`).style.display = 'block';
        document.querySelector(`#${username}_decline_attendence`).innerHTML = username;
    });

    return false;
}