# E-Sign

---

## Final project by Ilay Tzuberi and Omri Baron

---

## Installation instruction

1. Have python and git (not github) installed on your computer
2. Getting the repository:
    1. Create the folder you wish to have the application on.
    2. Open git bash from within the folder.
    3. Run the following git commands:

        ```bash
        git init
        git remote add origin https://github.com/parzival0152/Final
        git pull origin master
        ```

        you should now see the content of the repository in your designated folder.
3. Setting up the virtual enviroment.
    1. If you dont have virtualenv install install it now using ```pip install virtualenv```.
    2. Create a Venv using ```virtualenv {name}```.
    3. Activate the enviroment using ```.\{name}\Scripts\activate```.
    4. Run ```pip install -r requirements.txt``` to install all the dependent python libraries.
    5. To close the venv use ```deactivate```.
4. To run the app use ```flask run``` and go to ```localhost:5000``` to find the home page.
5. To run the Email Service, in a new terminal use ```python main.py```, do this only after running the flask app.

---

## Template format

A template is a json object that contains a name, a description and a list of stations.
A station is a json object that contains a name, a recipients email (later multiple) and a list of fields.

## Fields

There are a few types of fields:
Text: these fields are rendered as just a block of text on the template
Input: these fields area rendered as and input space and in the template maker they get their prompt
