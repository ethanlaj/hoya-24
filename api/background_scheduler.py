from apscheduler.schedulers.background import BackgroundScheduler
from scrape_sitemap import init_scrape_process
import atexit


def run_scrape_job():
    print("Starting scrape job...")
    init_scrape_process()
    print("Scrape job completed.")


scheduler = BackgroundScheduler()
scheduler.add_job(func=run_scrape_job, trigger="interval", hours=3)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
