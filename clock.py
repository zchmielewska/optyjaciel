from game.tasks import send_something_to_me

import apscheduler.schedulers.blocking

sched = apscheduler.schedulers.blocking.BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)
def timed_job():
    send_something_to_me.delay()


sched.start()
