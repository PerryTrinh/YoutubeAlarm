import time
import webbrowser
import random
import os

# Checks if SongList is in the same folder
if os.path.isfile("SongList.txt") == False:
    print("Song List is not found. \nList name should be 'SongList'")
else:
    with open("SongList.txt") as reader:
        play_list = reader.readlines()

    print("What time do you want to be notified?")
    print("Ex. '>> 03:15 PM' or '>> 08:40 AM'")
    user_input = input(">> ")
    alarm_time = ""

    #Converts user_input to alarm_time format to compare with current_time
    for i in range(len(user_input)):
        substring = user_input[i:i+1]

        if substring == "P": #beginning to read "PM", need to add 12 hours to user_input
            alarm_hours = int(user_input[0:2]) + 12
            alarm_time = str(alarm_hours) + user_input[2:i-1] #-1 accounts for space between time and period
            break
        elif substring == "A":
            alarm_time = user_input[:i-1]
            break


    current_time = time.strftime("%H:%M")

    while current_time != alarm_time:
        # Every 10 seconds, the current time is displayed
        if int(time.strftime("%S")) % 10 == 0:
            print("Current time: " + current_time)

        #Regardless of whether current time is displayed, current_time will be updated every second
        current_time = time.strftime("%H:%M")
        time.sleep(1)

    webbrowser.open(random.choice(play_list))
