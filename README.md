## WELCOME:
**You are gladly welcome** for deciding to contribute in this project. Your idears and creativity are highly welcome.

## PROJECT OVERVIEW:
MiniCampus application is an innovative academic application designed to enhance the experience of students, lectureres and administrators within an academic environment. It provides various features including events, course materials, access to the library, assigning a role to a lecturer(s) and also a platform for communication within the campus community.

## FEATURES AND FUCNTIONS

1. **The students(Users) can have:-**

  * Access to courses
  * Access to library (Digital learning materials shared by the instructors/lecturers)
* Receives important notifications posted by the instructors/lectureres
* The students/Users can easily communicate with each other and other members using the *in-app messaging*. You can chat in real-time and get feedback instanly, and this is applied to all users that can log-in. The message is encrypted, even the developers can not read the ongoing communication.
* Ability to add friend(s)

2. **The lecturers(instructors) can:-**
* Add courses.
* View courses when added
* Upload lecture (either in DOC, PDF, MP3, as well as MP4)
* Ability to view the uploaded/posted courses.
* Add reading materials in the library
* Ability to view the library.

3. **Administrator can:-**

* Add assign a user to be lecturer
* Grant a lecturer permission to do those in no.2
* Ability to view campus activities

## INSTALLATION:

The following are the step by step guides to actiively work on this project.
### Installing Python

To run a python script you need to install python. Let's [download](https://www.python.org/) python.
If you are a windows user. Click the link below.

[![installing on Windows](./images/installing_on_windows.png)](https://www.python.org/)

If you are a macOS user. Click the link below.

[![installing on Windows](./images/installing_on_macOS.png)](https://www.python.org/)

To check if python is installed write the following command on your device terminal.

```shell
python --version
```

![Python Version](./images/python_versio.png)

**Note**: After installing the latest version of the python, then;
```shell
* **clone the repository**:$ git clone https://{*YOUR_ACCESS_TOKEN*}/{*YOUR_USERNAME}/varsity_campus.git.
$ cd varsity_campus
```
### Create an environment
```shell
$ cd varsity_campus
$ python3 -m venv/bin/activate for (macOS/Linux) users.
$ source venv/bin/activate for window users.
```

### Installing flask

Within the activated environment, use the following command to install Flask:
```shell
$ pip install Flask
```
### Dependencies:
These distributions will be installed automatically when installing Flask.

* [Werkzeug](https://palletsprojects.com/p/werkzeug/) implements WSGI, the standard Python interface between applications and servers.

* [Jinja](https://palletsprojects.com/p/jinja/) is a template language that renders the pages your application serves.

* [MarkupSafe](https://palletsprojects.com/p/markupsafe/) comes with Jinja. It escapes untrusted input when rendering templates to avoid injection attacks.

* [ItsDangerous](https://palletsprojects.com/p/itsdangerous/) securely signs data to ensure its integrity. This is used to protect Flask’s session cookie.

* [Click](https://palletsprojects.com/p/click/) is a framework for writing command line applications. It provides the *flask* command and allows adding custom management commands.

* [Blinker](https://blinker.readthedocs.io/) provides support for [Signals.](https://flask.palletsprojects.com/en/stable/signals/)

### Optional dependencies
These distributions will not be installed automatically. Flask will detect and use them if you install them.

* [python-dotenv](https://github.com/theskumar/python-dotenv#readme) enables support for Environment Variables From dotenv when running flask commands.

* [Watchdog](https://pythonhosted.org/watchdog/) provides a faster, more efficient reloader for the development server.

## REQUIREMENT
To make the software requirements available on you machine, type the following commands in your terminal
```shell
$ pip install -r requirements.txt
```

## CONTRIBUTION GUIDES:
We welcome contributions from you to enhance the **MiniCampus** if you wish to contribute; Just:---
```shell
* fork the repository.
