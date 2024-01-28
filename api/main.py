from scrape_sitemap import init_scrape_process
from routes import app

if __name__ == '__main__':
    app.run(debug=True, port=8080)
