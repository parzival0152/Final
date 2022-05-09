from app import app
from emailschedualer import Email_Schedualer
from threading import Thread

es = Email_Schedualer()

testapp = Thread(target=es.run)
testapp.start()
app.run(debug=True)
