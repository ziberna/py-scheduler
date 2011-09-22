import scheduler; datecalc = scheduler.datecalc
import datetime

def algo_test():
    now = datetime.datetime.now()
    for job in jobs:
        print(datecalc.nextjob(job))
    diff = datetime.datetime.now() - now
    print('\nTime:')
    print(diff.microseconds / 1000000)

delay_avg = 0.0
delay_count = 0
delay_max = 0.0
delay_min = 1000000.0

def examplefunc(text):
    now = datetime.datetime.now()
    global delay_avg; global delay_count; global delay_max; global delay_min
    delay = now.microsecond
    delay_sum = delay_avg * delay_count
    delay_sum += delay
    delay_count += 1
    delay_avg = delay_sum / delay_count
    if delay > delay_max: delay_max = delay
    if delay < delay_min: delay_min = delay
    print(text, now)
    if delay_count % 10 == 0:
        print('Measures:',delay_count)
        print('Average:',delay_avg)
        print('Max:',delay_max)
        print('Min:',delay_min)

scheduler.function.examplefunc = examplefunc
jobs = scheduler.jobs(path='example_tab')

def tab_test():
    scheduler.start(jobs, daemon=False)

tab_test()
