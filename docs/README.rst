README
***********

# EPL-Card-Reader-Interface

The capstone project for Portland State Universities EPL Card Reader project. An interface an admin can interact with to verify or update student's "trained" status for various ECE machines in ECE labs. It will offer portability and flexibility so that it may be used across multiple labs at PSU.

Per the Sponsor's request:
The EPL is seeking a streamlined check in system for students entering the lab. This system would build on the previous ECE capstone RFID badge reader system sponsored by the EPL. At check in, on scanning their student ID, the user interface displays an iconographic grid indicating wether a student is trained to use various equipment categories around the lab. The icons would change color to indicate status. 

This system would also facilitate and track safety waivers and emergency contact status for quick retrieval by an EPL manager in case of emergency. EPL managers will be able to mark a person as trained (per icon) in the system.

This system should be easily reconfigurable in the UI for different shops around campus. 

I would guess that it may make the most sense to host on a local server. I would however, like to make it easy to stand it up on a PC with the UI pointed at the 127.0.0.1:x so that it could have a standalone mode as well. 


Pending hardware specs, currently planning on the following framework:

- Server webdev in Python using the Flask framework.
- An SQL database via SQLAlchemy
- Bootstrap Flask for a front end UI display

# Building

1. First, make sure your enviroment has Python 3 installed with your preferred package manager or download from:

https://www.python.org/downloads/

2. Clone this project down:

```
$ cd your/project/directory/here
$ git clone https://github.com/ZYostSass/EPL-Card-Reader-Interface.git
```

3. Create your virtual enviroment:

```
$ python3 -m venv venv
```

4. And run the application

```
$ ./run.sh
```

# Day to day development

The `run.sh` script is very simple. It:

- Activates your enviroment, so pip doesn't clutter up your $PATH
- Installs all the depencies listed in requirements.txt. This is very fast as pip only checks for new packages.
- Runs flask

This should make it so that this project 'just runs' every time on unix-compatible shells. 
(DM Mikayla if this doesn't work on Windows and we'll try to sort it out. Might need to install the [bash shell](https://superuser.com/a/1059340) that comes with Windows 10)

If you need to add a dependency from pip, add a new line to requirements.txt with the dependency name, exactly as you would write it for a normal `pip install`, as soon as someone else pulls down your changes we'll all have the dependency installed immediately.