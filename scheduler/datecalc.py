#    py-scheduler
#    Copyright (C) 2011 Jure Žiberna
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

import datetime
import calendar

MONTHS = list(range(1,13))
DAYS = list(range(1,32))
WEEKDAYS = list(range(1,8))
HOURS = list(range(0,24))
MINUTES = list(range(0,60))
SECONDS = list(MINUTES)

def dayfilter_month(year, month, days):
    last = calendar.monthrange(year, month)[1]
    return [day for day in days if day <= last]

def dayfilter_weekdays(year, month, weekdays, days):
    return [day for day in days if calendar.weekday(year, month, day)+1 in weekdays]

def next(now=None, Months=MONTHS, Days=DAYS, WeekDays=WEEKDAYS, Hours=HOURS, Minutes=MINUTES, Seconds=SECONDS):
    # I know this seems very inefficient (6 loops deep?!), but if you do some
    # testing (uncomment print lines), you'll see that the only loops that
    # iterate more than once are the first two. First one is needed because of
    # the one-year-span search and second one because the number of days is
    # different between months (28,29,30,31).
    
    if now == None: now = datetime.datetime.now()
    #print();print(now)
    
    year1 = now.year
    year2 = now.year + 1
    
    months1 = [mon for mon in Months if mon >= now.month and mon in MONTHS]
    months2 = [mon for mon in Months if mon <= now.month and mon in MONTHS]
    
    for months, y in [(months1, year1), (months2, year2)]:
        #print('year:'+str(y))
        skip = (y == now.year)
        
        for mon in months:
            #print('month:'+str(mon))
            days = Days
            days = dayfilter_month(y, mon, days)
            days = dayfilter_weekdays(y, mon, WeekDays, days)
            if days == []: continue
            
            skip = (skip and mon == now.month)
            if skip:
                days = [d for d in days if d >= now.day]
            
            for d in days:
                #print('day:'+str(d))
                hours = Hours
                
                skip = (skip and d == now.day)
                if skip:
                    hours = [h for h in hours if h >= now.hour]
                
                for h in hours:
                    #print('hour:'+str(h))
                    minutes = Minutes
                    
                    skip = (skip and h == now.hour)
                    if skip:
                        minutes = [min for min in minutes if min >= now.minute]
                    
                    for min in minutes:
                        #print('minute:'+str(min))
                        seconds = Seconds
                        
                        skip = (skip and min == now.minute)
                        if skip:
                            seconds = [s for s in seconds if s > now.second]
                        
                        for s in seconds:
                            #print('second:'+str(s))
                            next = datetime.datetime(y, mon, d, h, min, s)
                            if next >= now:
                                #print(next)
                                return next

def nextjob(job, now=None):
    return next(now, job.months, job.days, job.weekdays, job.hours, job.minutes, job.seconds)

def delta(start, goal):
    delta = goal - start
    return delta.days * 86400 + delta.seconds + float(delta.microseconds) / 1000000
