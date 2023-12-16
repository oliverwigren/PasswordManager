# Password Manager

This is my final project to HarvardX's CS50 course on the foundations of computer science. I have choosen to create a simple password manager. Its features are listed below.

### Video
[Link to my video](https://youtu.be/yY4USK412Ys)


## :warning: DISCLAIMER: CREATED PASSWORDS ARE NOT ENCRYPTED AND ARE STORED AS PLAIN TEXT. NEVER USE YOUR OWN REAL PASSWORD OR CREDENTIALS!!

## Features

<!--- Generate passwords by three difficulties.-->
- View all passwords in a table
- Create, Change and Save passwords to a database.
- Log-in with password and username
- Register as a new user with name, username and password
- Stay logged in with sessions
- Log-in-password is hashed
<!-- - Entered passwords are encrypted--->

## Technologies used

- Python
- SQLite3
- HTML
- CSS
- Bootstrap
- Flask
- Jinja
- werkzeug.security

## Usage and installation instructions
This project is in very early development and is not meant to be installed or used. In this stage is the point to show the source code.

## Deep dive

### app.py
This the main functionality to the manager. This is where everything is powered. Every function in more detail below.

### Log-in
The user enters a password and a username. The app checks for invalid input and if invalid input is detected, then a error message is returned and displayed. Otherwise, the app continues and checks the users-database for an account with that username and password. If more then one account or none is found then once again a error message is displayed. If everything is correct then a session is started with the unique user-id and the user is redirected to the first-page (index.html).
### Log-out
The session is set None and the user is redirected to the login-page.
### Register
The register function takes a username, password and a password confirmation as input. The app checks input and returns an error message if the input is incorrect. The app then checks with the database if the username is unique. If the username is not unique then an error message is displayed to the user. If the username is unique then the user credentials are inserted into the users-database. (The password is hashed with werkzeug.security to make it secure to store passwords in a database). Then the app gets the user-id to start a session and the user is afterwards redirected to first-page (index.html).
### Create
The create function takes a website name, a username and a password and makes sure that everything has been inputed correctly. If so the app checks if there already exists an passwords saved to database with the same website name. If either of this fails then a error is sent back and a text is shown to the user what went wrong. On the other hand, if everything went fine then the credentials are inserted into the passwords database and the user is redirected to the first-page. There is also an option to click on the back button, if pressed will the user be redirected to the first-page and the credentials will not be inserted into the database.
### Index
The app searches for any passwords in the specific user's part of the password-database, if none are found will nothing be shown. Otherwise, the passwords, websites, and usernames be shown in a table. In each row is there a button to change password and/ or username. If clicked will the "change" function be called. (Described below.) There is also a additional button: "New Password", if clicked will the "create" function be called. (Described above)
### Change
The change function takes a website name, username and password. The website name is set not by user through text input but depending on which password that the "change" button is pressed. The function checks that correct input has been submitted and if not will an error be sent back. If the input is correct then the app will check that there is a (only one) password that corresponds with that user id and that website name. If not will an error be sent back to the user. Otherwise, will the username and password be updated in the database. Afterwards will the user be redirected to the first-page.

<!--Using:
werkzeug.security
cryptography.fernet
-->


© 2023 Oliver Wigren
