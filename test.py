from sending import send
from verification import previous_decision
import time
name=input("Name:")
uuid=input("UUID:")
decision=input("Decision:")
send(name,uuid,decision)

time.sleep(120)

prev_dec=previous_decision(name,uuid)
print(prev_dec)