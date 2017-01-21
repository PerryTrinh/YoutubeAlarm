import time
import webbrowser
import random
import os

def main():
    if valid_path():
        with open("SongList.txt") as reader:
            play_list = reader.readlines()

        print("What time do you want to be notified?")
        print("Ex. \n'>> 03:15 PM' \n'>> 08:40 AM'")
        user_input = input(">> ")
        alarm_time = ""

        #Converts user_input to alarm_time format to compare with current_time later on
        for i in range(len(user_input)):
            substring = user_input[i:i+1]

            #if substring is a part of the numerical time input
            if is_numeric(substring):
                index_last_number = i

            #beginning to read "PM", need to add 12 hours to user_input
            elif substring == "P":
                alarm_time = convertTime(user_input, index_last_number, True)
                break

            elif substring == "A":
                alarm_time = convertTime(user_input, index_last_number, False)
                break

        #If user forgot AM/PM, assume time is same time period as right now
        if alarm_time == "":
            current_hour = int(time.strftime("%H"))
            alarm_time = closest_time(user_input, current_hour, index_last_number)

        current_time = time.strftime("%H:%M")

        while current_time != alarm_time:
            # Every 10 seconds, the current time is displayed
            if int(time.strftime("%S")) % 10 == 0:
                print("Current time: " + current_time)

            #Regardless of whether current time is displayed, current_time will be updated every second
            current_time = time.strftime("%H:%M")
            time.sleep(1)

        webbrowser.open(random.choice(play_list))
    else:
        print("Song List is not found. \nList name should be 'SongList'")

def valid_path():
    return os.path.isfile("SongList.txt")

def is_numeric(t):
    try:
        float(t)
        return True
    except ValueError:
        return False

def convertTime(input, index, PM):
    """Returns input in military time as a String"""
    if PM == True:
        alarm_hours = int(input[0:2]) + 12
        return str(alarm_hours) + input[2:index + 1]
    else:
        return input[:index + 1]

def closest_time(input, current_hour, index):
    """Determines what time is closest to current_time and returns it as a String"""
    """ex. if current_time is 14:40 PM, and user inputs 02:45, closest time is 14:45"""

    AM_time = convertTime(input, index, False)
    PM_time = convertTime(input, index, True)

    #Corrects for single digit hours so they can be compared with later on
    AM_hours = int(AM_time[1:2]) if AM_time[0] == "0" else int(AM_time[:2])
    PM_hours = int(PM_time[1:2]) if PM_time[0] == "0" else int(PM_time[:2])

    if PM_hours == AM_hours and AM_hours == current_hour:
        if int(current_hour) >= 12:
            return PM_time
        else:
            return AM_time

    elif PM_hours >= current_hour and current_hour > AM_hours:
        return PM_time
    else:
        return AM_time


main()
