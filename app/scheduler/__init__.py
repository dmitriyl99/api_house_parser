from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.combining import OrTrigger

from .jobs import parse_uybor, parse_olx


_scheduler = BackgroundScheduler()


def start():
    trigger = OrTrigger([CronTrigger(hour=12, minute=0), CronTrigger(hour=24, minute=0)])
    # _scheduler.add_job(parse_uybor, trigger=trigger, id='parse_uybor', replace_existing=True)
    _scheduler.add_job(parse_olx, trigger=trigger, id='parse_olx', replace_existing=True)
    _scheduler.start()


def stop():
    _scheduler.remove_all_jobs()
    _scheduler.shutdown()
