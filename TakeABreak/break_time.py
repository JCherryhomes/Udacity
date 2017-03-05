import time
import datetime as DT
import webbrowser

# Everything is in seconds for consistency
sleep_time = 3600 # Duration in seconds before a break
number_of_breaks = 3 # The number of breaks that will be taken
total_duration = sleep_time * number_of_breaks # Total time the program will run

current_time = DT.datetime.now() # Current time
end_time = current_time + DT.timedelta(seconds=total_duration) # Current time offset by total duration

print("this program started at " + time.strftime("%H:%S, %d %B %Y"))

while(current_time <= end_time):
    time.sleep(sleep_time)
    webbrowser.open("http://www.youtube.com/watch?v=dQw4w9WgXcQ")
    current_time = DT.datetime.now() # Update current time