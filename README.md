# E-Sign
---
## Final project by Ilay Tzuberi and Omri Baron
---
# Installation instruction

1. Have python and git (not github) installed on your computer
2. Getting the repository:
2.1. Create the folder you wish to have the application on.
2.2. Open git bash from within the folder.
2.3. Run the following git commands:
    ```
    git init
    git remote add origin https://github.com/parzival0152/Final
    git pull origin
    ```
    you should now see the content of the repository in your designated folder.
3. Setting up the virtual enviroment.
3.1. If you dont have virtualenv install install it now using ```pip install virtualenv```.
3.2. Create a Venv using ```virtualenv {name}```.
3.3. Activate the enviroment using ```.\{name}\Scripts\activate```.
3.4. Run ```pip install -r requirements.txt``` to install all the dependent python libraries.
3.5. To close the venv use ```deactivate```.
4. To run the app use ```python app.py``` and go to ```localhost:5000``` to find the home page.