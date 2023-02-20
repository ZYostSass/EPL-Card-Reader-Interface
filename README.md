Description: The purpose of this project is a learning environment for Python Flask and associated modules, with the intent of implementing the demonstrated features in the Winter/Spring Capstone EPL Card Reader project.

Requirements:

Python3 [(https://www.python.org/downloads/)] Flask [(https://pypi.org/project/Flask/)] SQLAlchemy [(https://www.sqlalchemy.org/)] Flask-SQLAlchemy [(https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)] ngrok [(https://ngrok.com/docs]

Setup: Install the required software Clone this repo, then cd into the root directory and run-

Linux: flask --app app run Windows: python -m flask run

The app will serve the file ./templates/home.html at http://127.0.0.1:5000. This is a minimal app for demonstration of the use of ngrok as a hosting service for the EPL card reader project.

To start the ngrok service:

Initial Setup: Install the ngrok agent-

Linux:
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc |
sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null &&
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" |
sudo tee /etc/apt/sources.list.d/ngrok.list &&
sudo apt update && sudo apt install ngrok

Windows: choco install ngrok

Mac: brew install ngrok/ngrok/ngrok

Additional install assistance: [(https://ngrok.com/download)]

Once ngrok is installed, it will need to be connected to your ngrok account via an Auth token. (Sign up for free account here: [(https://dashboard.ngrok.com/signup)]

Once you have your Auth token, run:

ngrok config add-authtoken TOKEN

replacing TOKEN with the value copied from the ngrok Dashboard.

Start the Flask app on your local machine. Run: ngrok http 5000 (See ngrok documentation for setup instructions - you will need to create a free account)

When the ngrok service starts, it will provide a link ending in .ngrok.io - this link can be used to access the Flask application from devices other than the host.

Additional Files: ./createdb.py is a script that can be run to create a sample SQLite database. This can be run as a standard Python script and will create a file named 'sample.db' at the project root. The file schema.sql contains the SQL commands that create the table.