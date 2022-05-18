import schedule
from time import sleep
from requests import get
from requests.exceptions import ConnectionError
from EmailSubsystem.EmailSender import send_email


class user:
    def __init__(self, **kwargs) -> None:
        self.id = kwargs["id"]
        self.name = kwargs["name"]
        self.email = kwargs["email"]
        self.prefered_time = kwargs["preferances"]["alert_time"] # save info from user list
        self.set_timer()

    def set_timer(self, time=None) -> None:
        if time:
            schedule.cancel_job(self.emailer)
            self.prefered_time = time
        self.emailer = schedule.every().day.at(self.prefered_time).do(self.send_email)

    def send_email(self) -> None:
        try:
            r = get(f"http://127.0.0.1:5000/api/docs_count/{self.id}")
            if r.status_code == 200:
                count = r.json()["count"]
                msg = ""
                if count > 0:
                    msg = f"Hello {self.name} \nYou have {count} pending document{'s' if count>1 else ''}"
                    send_email(self.email,msg)
        except ConnectionError:
            pass


class Email_Schedualer:
    def get_users(self):
        try:
            r = get("http://127.0.0.1:5000/api/users")  # make request to the server
            if r.status_code == 200:
                print(r.json())
                return r.json()
        except ConnectionError:  # if there was a connection error just give up and try again
            return []
    
    def update_users(self):
        print("updating info")
        updated_info = self.get_users() #get updated user info
        for n,o in zip(updated_info,self.userlist): # run over the pairs of users
            assert n["id"] == o.id # users should be alligned, if not this will raise an error
            if not n["preferances"]["alert_time"] == o.prefered_time: # if the prefered time has been changed
                o.set_timer(n["preferances"]["alert_time"]) # update the timer

    def run(self) -> None:
        sleep(5)  # give the flask aplication time to boot up before making a request to the api of the aplication
        print("here we go bois")
        userlist = self.get_users()  # get list of user information from the server
        self.userlist = [user(**u) for u in userlist] # create user handler list
        schedule.every(1).minutes.do(self.update_users) # set update time for checking updated information
        while 1:
            schedule.run_pending() # keep excecuting email updates
            print("sending emails if they exist")
            sleep(60)


if __name__ == "__main__":
    Es = Email_Schedualer()
    Es.run()
