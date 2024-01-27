# background_scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from scrape_sitemap import init_scrape_process
import time


def my_job():
    print("Job is running")
    init_scrape_process()


scheduler = BackgroundScheduler()
scheduler.add_job(my_job, 'interval', hours=3)
scheduler.start()

try:
    # This is used to keep the main thread alive.
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
