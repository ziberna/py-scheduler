#    py-scheduler
#    Copyright (C) 2011 Kantist
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.
#    If not, see http://www.gnu.org/licenses/gpl-3.0.html

import re

import time
import datetime

# Py 2/3 compatibility:
try:
    import datecalc # Py 2
except ImportError:
    import scheduler.datecalc as datecalc # Py 3

import threading
import traceback

interval = 300.0

class Job(object):    
    def __init__(self, string='', seconds=[], minutes=[], hours=[], \
                 weekdays=[], days=[], months=[], function=None, args=(), \
                 kwargs={}, enabled=True, cancel=False):
        # Parse string
        if string:
            self.seconds, self.minutes, self.hours, self.weekdays, self.days, \
            self.months, self.function, self.args, self.kwargs = Job.parse(string)
        # Extend time fields with supplied lists
        self.seconds += seconds
        self.minutes += minutes
        self.hours += hours
        self.weekdays += weekdays
        self.days += days
        self.months += months
        # Overwrite function fields if supplied
        if function: self.function = function
        if args: self.args = args
        if kwargs: self.kwargs = kwargs
        # Set enabled and cancel flag
        self.enabled = enabled
        self.cancel = cancel
    
    def start(self):
        # Calculate the datetime of first occurrence
        now = datetime.datetime.now()
        self.next = datecalc.nextjob(self, now)
        
        while self.next:
            # Calculate float number of seconds until next occurrence
            until = datecalc.delta(now, self.next)
            # Sleep for inteval-seconds if until is longer than interval
            if until > interval:
                time.sleep(interval)
            # Else sleep for until-seconds, then do the job
            else:
                time.sleep(until)
                self.do()
            # Calculate the datetime of next occurrence
            now = datetime.datetime.now()
            self.next = datecalc.nextjob(self, now)
    
    def do(self):
        # Return if disabled
        if not self.enabled: return
        # Return and reset cancel flag if canceled
        if self.cancel:
            cancel = False
            return
        # Try to do the job
        try: self.function(*self.args, **self.kwargs)
        except: traceback.print_exc()
    
    @staticmethod
    def parse_pattern(string, bottom, top):
        # Range between two numbers
        if '-' in string:
            start, end = [int(s) for s in string.split('-')]
            if end > top: end = top
            elif end < bottom: end = bottom
            if start > top: start = top
            elif start < bottom: start = bottom
            if start < end:
                times = range(start, end)
            elif start > end:
                times = list(range(start, top+1)) + list(range(bottom, end))
        # Match asterisk
        elif '*' in string:
            # Turn string into regular expression
            string = '^'+string.replace('*','\d+')+'$'
            # Do regex search for whole range
            times = [num for num in range(bottom,top+1) if re.search(string, '0'+str(num))]
        # Parse string as int
        elif string:
            times = [int(string)]
        # Else generate whole range
        else:
            times = list(range(bottom,top+1))
        return times
    
    @staticmethod
    def parse_increment(nums, increment):
        increment = int(increment)
        # Return first element and every increment-element after first one
        return [nums[i] for i in range(len(nums)) if i % increment == 0]
    
    @staticmethod
    def parse_list(string, bottom, top):
        # Split list of patterns
        strings = [s for s in string.split(',') if s != '']
        times = []
        for s in strings:
            # Split by increment-sign ('/')
            s = s.split('/')
            # Parse pattern before increment-sign
            time = Job.parse_pattern(s[0], bottom, top)
            # Apply increments
            if len(s) > 1: time = Job.parse_increment(time, s[1])
            times.extend(time)
        return times
    
    @staticmethod
    def parse(string):
        # Split into fields and filter unneeded characters
        fields = [field.strip() for field in string.split(' ') if field != '']
        # Add missing fields
        if len(fields) < 9:
            if len(fields) < 6:
                fields.extend('*' for n in range(6-len(fields)))
            fields.extend('/' for n in range(9-len(fields)))
        # Replace non-defined function characters with empty strings
        for n in range(6,9):
            if fields[n] == '/': fields[n] = ''
        
        # Parse each time field as list of patterns
        seconds = Job.parse_list(fields[0], 0, 59)
        minutes = Job.parse_list(fields[1], 0, 59)
        hours = Job.parse_list(fields[2], 0, 23)
        weekdays = Job.parse_list(fields[3], 1, 7)
        days = Job.parse_list(fields[4], 1, 31)
        months = Job.parse_list(fields[5], 1, 12)
        
        # Parse function field
        function = fields[6] if fields[6] else None
        # Parse args field
        try:
            args = tuple(eval(arg) for arg in fields[7].split(','))
        except:
            args = ()
        # Parse kwargs field
        kwargs = {}
        try:
            for kwarg in fields[8].split(','):
                if '=' in kwarg:
                    kwarg = kwarg.split('=')
                    kwargs[kwarg[0]] = eval(kwarg[1])
        except: pass
        
        return seconds, minutes, hours, weekdays, days, months, function, args, kwargs

def jobs(path='', text='', jobs=[]):
    if path:
        try:
            with open(path) as file:
                jobs += parse(file.read())
        except IOError: pass
    if text: jobs += parse(text)
    return jobs

def parse(text):
    strings = [string.strip() for string in text.split('\n')]
    strings = [string for string in strings if string != '' and not string.startswith('#')]
    jobs = [Job(string) for string in strings]
    return jobs

threads = []
def start(jobs = [], daemon=True):
    global threads
    for job in jobs:
        thread = threading.Thread(target=job.start)
        thread.daemon = True
        thread.start()
        threads.append(thread)
