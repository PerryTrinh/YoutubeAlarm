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
            current_hour = time.strftime("%H")

            if int(current_hour) >= 12:
                alarm_time = convertTime(user_input, index_last_number, True)
            else:
                alarm_time = convertTime(user_input, index_last_number, False)

        current_time = time.strftime("%H:%M")
        print("alarm time is" + alarm_time)

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
    print(input)
    print(index)
    if PM == True:
        alarm_hours = int(input[0:2]) + 12
        return str(alarm_hours) + input[2:index + 1]
    else:
        return input[:index + 1]

main()
