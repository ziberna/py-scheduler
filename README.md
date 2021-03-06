py-scheduler
============

py-scheduler is a cron-like scheduler written in Python with some advanced
features.


Format of schedule table (the tab)
----------------------------------

	sec    min    hour    weekday    day    month    function    args    kwargs
	*      *      *       *          *      *        myfunc      5.6     y=[],z=3

The above example would execute this every second:

	myfunc(5.6, y=[], z=3)

Format for time fields is very similar to crontab. It supports list of patterns
(<pattern1>,<pattern2>; e.g. *5,*0), ranges (<start>-<end>; e.g. 5-49) and
increments (<pattern>/<increment> or just /<increment> for whole range; e.g.
5-49/11,*7/5,/3). Weekdays and days can be set for same job (unlike cron).

Functions
---------

There are two ways to set functions. One way is add whichever functions may
be written in schedule table to the function repository. Example:

	import scheduler
	# Add my_function to scheduler's function repository as 'myfunc'
	scheduler.function.myfunc = my_function

This is recommended. py-schedule will look for functions in function repository
by function name written in schedule table. If it doesn't find one, which brings
us to the second way of setting function, it will set the name (string) to
function itself. That way you can set function of a job by checking the name
yourself.

You may want to set default function for schedule entries that have no function
defined. To do this, simply write:

	scheduler.function.default = my_default_function

NOTE: You should add functions to function repository before parsing any tables,
i.e. before calling scheduler.jobs with path or text or scheduler.Job.parse. You
can still add a function later, but be aware that functions for a certaing job
are retrieved from repository only at the time of the parsing of that certain
job. If you want to change function of already parsed job later, you have to
change function attribute of a job (e.g. myjob1.function = some_other_function).


See camscheduler (https://github.com/jzib/camscheduler) for an example of a
program using py-scheduler.

Python version
--------------

I've tested py-scheduler with Python 2.7.2 and Python 3.2.2; these are the
latest stable versions of Python. py-scheduler is thus Python 2/3 compatible.
