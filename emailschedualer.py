from threading import Timer
from time import sleep
from requests import get

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

class Email_Schedualer:
    def __init__(self) -> None:
        sleep(10) # give the flask aplication time to boot up before making a request to the api of the aplication
        self.get_users() # get list of user information from the server


    def get_users(self) ->None:
        try:
            r = get("http://127.0.0.1:5000/api/users") # make request to the server
            if r.status_code == 200:
                users = r.json()
        except ConnectionError: # if there was a connection error just give up and try again
            pass

    def send_email(self,user) -> None:
        try:
            r = get(f"http://127.0.0.1:5000/api/docs_count/{user.id}")
            if r.status_code == 200:
                count = r.json()["count"]
                msg = ""
                if count == 0:
                    msg = f"Hello {user.name} \nYou currently have no pending documents"
                else:
                    msg = f"Hello {user.name} \nYou have {count} pending document{'s' if count>1 else ''}"
                
                #TODO: send the msg to user.email

        except ConnectionError:
            pass



    