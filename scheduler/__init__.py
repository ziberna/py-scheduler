# Py 2/3 compatibility:
try:
    # Py 2
    from scheduler import Job, jobs, start, parse, interval, threads, func_repo\
         as function
    import datecalc
except ImportError:
    # Py 3
    from scheduler.scheduler import Job, jobs, start, parse, interval, threads,\
         func_repo as function
    import scheduler.datecalc
