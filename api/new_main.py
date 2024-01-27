import schedule
import multiprocessing
import time
from scrape_sitemap import init_scrape_process
from routes import app


def run_multiprocessed(job_func):
    job_process = multiprocessing.Process(target=job_func)
    job_process.start()


schedule.every(3).hours.do(run_multiprocessed, init_scrape_process)


if __name__ == '__main__':
    app.run(debug=True, port=8080)

while True:
    schedule.run_pending()
    time.sleep(1)
