import time
import webbrowser
import random
import os

def main():
    if valid_path():
        with open("SongList.txt") as reader:
            play_list = reader.readlines()

        print("What time do you want to be notified?")
        print("Ex. \n'>>> 03:15 PM' \n'>>> 08:40 AM'")
        user_input = input(">>> ")
        alarm_time = ""

        #Converts user_input to alarm_time format to compare with current_time later on
        for i in range(len(user_input)):
            substring = user_input[i:i+1]

            #if substring is a part of the numerical time input
            if is_numeric(substring):
                index_last_number = i

            #beginning to read "PM", need to add 12 hours to user_input
            elif substring == "P":
                alarm_time = convert_time(user_input, index_last_number, True)
                break

            elif substring == "A":
                alarm_time = convert_time(user_input, index_last_number, False)
                break

        current_time = time.strftime("%H:%M")

        #If user forgot AM/PM, assume time is same time period as right now
        if alarm_time == "":
            alarm_time = closest_time(user_input, current_time, index_last_number)
            
        while current_time != alarm_time:
            # Every 20 seconds, the current time is displayed
            if int(time.strftime("%S")) % 20 == 0:
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

def convert_time(input, index, PM):
    """Returns input in military time as a String

    >>> convert_time("2:12", 3, True)
    "14:12"
    >>> convert_time("12:47", 4, True)
    "12:47"
    >>> convert_time("12:47", 4, False)
    "00:47"
    """
    if input[1:2] == ":":
        input = "0" + input
        index += 1

    input_hours = int(input[0:2])

    if PM == True:
        if input_hours == 12:
            return input[:index + 1]

        alarm_hours = str(input_hours + 12)
        return alarm_hours + input[2:index + 1]
    else:
        if input_hours == 12:
            input = "00" + input[2:index + 1]
        return input[:index + 1]

def cut_zeros(time, time_period):
    """Returns time (hours or minutes) as an int with no leading zeros

    >>> cut_zeros("02:01", "Minutes")
    1
    >>> cut_zeros("04:10", "Hours")
    4
    """
    if time_period == "Minutes":
        return int(time[4:5]) if time[3] == "0" else int(time[3:])
    else:
        return int(time[1:2]) if time[0] == "0" else int(time[:2])

def closest_time(input, current_time, index):
    """Determines what time is closest to current_time and returns it as a String

    >>> closest_time("2:20", "12:24", 3)
    "14:20"
    >>> closest_time("12:10", "12:24", 4)
    "00:10"
    """

    AM_time = convert_time(input, index, False)
    PM_time = convert_time(input, index, True)

    #Corrects for single digit time stamps so they can be compared with later on
    AM_hours = cut_zeros(AM_time, "Hours")
    PM_hours = cut_zeros(PM_time, "Hours")
    current_hour = cut_zeros(current_time, "Hours")
    AM_min = cut_zeros(AM_time, "Minutes")
    PM_min = cut_zeros(PM_time, "Minutes")
    current_minute = cut_zeros(current_time, "Minutes")

    if current_hour == AM_hours:
        if AM_min - current_minute < 0:
            return PM_time
        else:
            return AM_time
    elif current_hour == PM_hours:
        if PM_min - current_minute < 0:
            return AM_time
        else:
            return PM_time
    elif PM_hours >= current_hour and current_hour > AM_hours:
        return PM_time
    else:
        return AM_time

main()
