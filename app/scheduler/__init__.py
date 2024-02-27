from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from .jobs import parse_uybor


_scheduler = BackgroundScheduler()

def start():
    _scheduler.add_job(parse_uybor, trigger=IntervalTrigger(hours=12), id='parse_uybor', replace_existing=True)
    _scheduler.start()


def stop():
    _scheduler.remove_all_jobs()
    _scheduler.shutdown()
