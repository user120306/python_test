import re
from datetime import datetime, timedelta

def get_meeting_duration(meeting_entry):
    if(meeting_entry == '12:00PM Lunch'):
       return 60; 
    else:
        match = re.findall('(\d+)(min)', meeting_entry);
        return int(match[0][0]);

def get_next_timeslot(meeting_room, next_meeting_duration):
    #Assumption is that the rooms are sorted by meeting start time
    next_time_slot = datetime.strptime('09:00AM', '%H:%M%p')
    
    for r in meeting_room:

        meeting_duration = get_meeting_duration(r);
        if(next_time_slot + timedelta(minutes=next_meeting_duration)) <=datetime.strptime(r[:7], '%H:%M%p') :
            return next_time_slot;
        else:
            next_time_slot = datetime.strptime(r[:7], '%H:%M%p') + timedelta(minutes=meeting_duration);
    return next_time_slot;

def load_meeting_list(file_name, meetings):
    with open(file_name, 'r') as f:
        for l in f:
            meetings.append(l);
        f.closed;

def main():
    meetings=[];
    
    room1_schedule=['12:00PM Lunch'];
    room2_schedule=['12:00PM Lunch'];
    
    load_meeting_list('meetings.txt', meetings);
    
    #Sort meetings by smallest duration. This is a simple way to distribute the bookings
    meetings = sorted(meetings, key=lambda meeting:get_meeting_duration(meeting)); 
    
    # Allocate meetings to rooms
    for m in meetings:
        meeting_duration = get_meeting_duration(m);
        next_time = get_next_timeslot(room1_schedule, meeting_duration);
        
        if(next_time + timedelta(minutes=meeting_duration) <= datetime.strptime('17:00PM', '%H:%M%p')):
            room1_schedule.append(next_time.strftime('%H:%M%p')+' '+m);
            room1_schedule.sort();
        else:
            next_time = get_next_timeslot(room2_schedule, meeting_duration);
            room2_schedule.append( next_time.strftime('%H:%M%p')+' '+m);
            room2_schedule.sort();
    
    #Print room allocations
    print 'Room1:'
    for booking in room1_schedule:
        print booking;
    
    print '\nRoom2:';    
    for booking in room2_schedule:
        print booking;