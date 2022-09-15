import schedule
from time import sleep
from requests import get
from requests.exceptions import ConnectionError
from EmailSubsystem.EmailSender import send_email


class user:
    # user class for the managment of reminder emails
    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.name = kwargs["name"]
        self.email = kwargs["email"]
        self.prefered_time = kwargs["preferances"]["alert_time"] # save info from user list
        self.set_timer()

    def set_timer(self, time=None):
        # function to set a time for a reminder email
        if time:
            # if a new timer was given cancel the last job and update the user prefered time
            schedule.cancel_job(self.emailer)
            self.prefered_time = time
        self.emailer = schedule.every().day.at(self.prefered_time).do(self.send_email)
        # create a new job every day at the prefered time to send an email 

    def send_email(self):
        # function to send an email
        try:
            # attempt to get the pending document count of the user and if its non-zero, send an email
            r = get(f"http://127.0.0.1:5000/api/docs_count/{self.id}")
            if r.status_code == 200:
                count = r.json()["count"]
                msg = ""
                if count > 0:
                    msg = f"Hello {self.name} \nYou have {count} pending document{'s' if count>1 else ''}"
                    send_email(self.email,msg)
        except ConnectionError:
            # dont fail if the server fails to respond
            pass


class Email_Schedualer:
    def get_users(self):
        try:
            r = get("http://127.0.0.1:5000/api/users")  # make request to the server
            if r.status_code == 200:
                return r.json()
            else:
                print(r.status_code)
        except ConnectionError:  # if there was a connection error just give up and try again
            return []
    
    def update_users(self):
        print("updating info")
        updated_info = self.get_users() #get updated user info
        for new_user_info in updated_info: # run over the new data
            specified_user = self.userlist[new_user_info['id']] # grab the specific user using his id
            if not new_user_info["preferances"]["alert_time"] == specified_user.prefered_time: # if the prefered time has been changed
                specified_user.set_timer(new_user_info["preferances"]["alert_time"]) # update the timer

    def run(self):
        print("Starting EmailSchedualer system")
        userlist = self.get_users()  # get list of user information from the server
        self.userlist = {u["id"]:user(**u) for u in userlist} # create user handler dict with the keys being the user id
        schedule.every().minute.at(":00").do(self.update_users) # set update time for checking updated information
        while 1:
            schedule.run_pending() # keep excecuting email updates
            print("Excecuting tasks")
            sleep(60)


if __name__ == "__main__":
    Es = Email_Schedualer()
    Es.run()
