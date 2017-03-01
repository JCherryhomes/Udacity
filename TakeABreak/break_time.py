import time
import datetime as DT
import webbrowser

# Everything is in seconds for consistency
sleep_time = 600 # Duration in seconds - 10 minutes
total_duration = 1800 # How long to run the program - 30 minutes
current_time = DT.datetime.now() # Current time
end_time = current_time + DT.timedelta(seconds=total_duration) #Current time offset by total duration

print("this program started at " + current_time.strftime("%H:%S, %d %B %Y"))

while(current_time <= end_time):
    time.sleep(sleep_time)
    webbrowser.open("http://www.youtube.com/watch?v=dQw4w9WgXcQ")
    current_time = DT.datetime.now() # Update current time