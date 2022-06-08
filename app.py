from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect
import requests
from remote_scrapper import get_job_data as re_jobs
from we_work_scrapper import get_job_data as we_jobs
from stack_scrapper import get_job_data as st_jobs
from save import save_to_file
"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
}

app = Flask(__name__)

db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/detail")
def detail():
    keyword = request.args.get('job').lower()
    if keyword:
        fromDb = db.get(keyword)
        if fromDb:
            jobs = fromDb
            # print(keyword)
        else:
            re_job = re_jobs(keyword)
            we_job = we_jobs(keyword)
            st_job = st_jobs(keyword)
            jobs = re_job + we_job + st_job
            db[keyword] = jobs
            jobs = db[keyword]
            # print(keyword)
    else:
        return redirect("/")
    return render_template(
        "detail.html",
        searchingWord=keyword,
        searchingResult=len(jobs),
        jobs=jobs)


@app.route('/export')
def export():
    try:
        keyword = request.args.get('job').lower()
        jobs = db.get(keyword)
        if not keyword or not jobs:
            raise Exception()
        save_to_file(jobs)
        send_file(
            "jobs.csv",
            mimetype='application/x-csv',
            attachment_filename='summary_report.csv',
            as_attachment=True)
        return render_template("export.html", keyword=keyword)
    except:
        return render_template("export.html", keyword=keyword)
        # return render_template('export.html',keyword = keyword)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
