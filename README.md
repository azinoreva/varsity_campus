## WELCOME:
**You are gladly welcome** for deciding to contribute in this project. Your idears and creativity are highly welcome.

## PROJECT OVERVIEW:
MiniCampus is a social and educational website meant for university students and the school community. The aim of the website is to provide a platform where students can learn and socialize all in one place. It comes with features like: 
Posts - where you can post content related to academics and your fellow students can comment like and repost.
Communities - here you can join a community and post messages related to it.
Courses - this is where you can find all your courses and assignments.
Messages - whereby you can add friends and message them.
Library - in here, lecturers and students can upload resources that pertain to academics.

## INSTALLATION:

The following are the step by step guides to actiively work on this project.
### Installing Python

To run a python script you need to install python. Let's [download](https://www.python.org/) python.
If you are a windows user. Click the link below.

![installing on Windows](./images/installing_on_windows.png) (https://www.python.org/)

If you are a macOS user. Click the link below.

![installing on Windows](./images/installing_on_macOS.png) (https://www.python.org/)

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
Then run the *flask* using this command.
```shell
$ python3 -m flask run
or
$ flask run
or
$ flask run --debug
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
* Create a new branch.
* make your changes and submit a pull request
```

## CONTENTS OF THE VARSITY_CAMPUS APP

|# NO.  |  Folder's name           |
|-------| :------------------------|
|  01  | [app](./app)
|  02  | [instance](./instance)
|  03  | [migrarations](./migrations)
|  04  | [tests](./tests)
|  05  | [venv](./venv)


## Usage
**Register page**
        *Purpose:* This create a new user account to access the website.
      This will allow you enter your registered email and password on the login page.
      ![Register.jpg](https://github.com/azinoreva/varsity_campus/raw/main/register.jpg)

**Login paage**
        *purpose:* This allows you to access your personal account

