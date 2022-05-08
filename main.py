from app import app
from time import sleep
from threading import Thread

def runtest():
    while True:
        sleep(5)
        print("i have awoken\ni will now go back to sleep")


testapp = Thread(target=runtest)
testapp.start()
app.run(debug=True)
