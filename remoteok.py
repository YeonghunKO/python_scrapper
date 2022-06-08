import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

MAX_COUNT = 50

def extract_jobs(url):
  print(f"Scrapping RemoteOk ...")

  jobs = []
  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, 'html.parser')
  job_board = soup.find("table", {"id":"jobsboard"})
  if job_board:
    job_data_rows = job_board.findAll("tr", {"class":"job"})
  else:
    print("not found result :", url)
    job_data_rows = None

  if job_data_rows :

    for data_rows in job_data_rows:
      try:
        logo = data_rows.find("img", {"class":"logo"})
        if logo and logo.get("data-src"):
          logo = logo["data-src"]
        elif logo and logo.get("src"):
          logo = logo["src"]
        else:
          logo = None

        company_position = data_rows.find("td", {"class":"company_and_position"})
        title = company_position.find("h2",{"itemprop":"title"}).string
        company = company_position.find("h3",{"itemprop":"name"}).string
        link = company_position.find("a" ,{"class":"preventLink"})["href"]
        
        location = company_position.find("div", {"class":"location"})
        if location :
          location = location.string
        else :
          location = None
        
        job = {
          "logo": logo,
          "title": title,
          "company": company,
          "location": location,
          "link": f"https://remoteok.io{link}"
        }
        jobs.append(job)
        length = len(jobs)
        print(length, "jobs found")
        if length >= MAX_COUNT:
          break

      except Exception as e:
        # print(data_rows)
        print("RemoteOk, Error Message : ", e)

  return jobs

def get_job_data(word):
  # remoteok was not supplying '#' or '+' character
  word = word.replace("+", " plus").replace("#"," sharp")
  url = f"https://remoteok.io/remote-dev+{word}-jobs"
  jobs = extract_jobs(url)
  return jobs

go = get_job_data("python")
print(go)