import requests
from bs4 import BeautifulSoup

MAX_COUNT = 50

def extract_job(soup_result):
  logo = soup_result.find("img")
  if logo :
    logo = logo["src"]
  else :
    logo = None

  title = soup_result.find("h2").find("a")["title"]
  company, location = soup_result.find("h3").find_all("span", recursive=False)
  company = company.get_text(strip=True).strip("/n")
  location = location.get_text(strip=True)
  job_id = soup_result["data-jobid"]

  return {
    "logo":logo,
    "title": title,
    "company": company,
    "location": location,
    "link": f"https://stackoverflow.com/jobs/{job_id}"
  }


def extract_jobs(last_page, url):
  jobs = []
  is_full_array = False

  for page in range(last_page):

    try:
      pageIdx = page +1
      print(f"Scrapping Stack-over-flow page {pageIdx}")
      result = requests.get(f"{url}&pg={pageIdx}")
      soup = BeautifulSoup(result.text, 'html.parser')
      soup_results = soup.find_all("div", {"class": "-job"})
      for soup_result in soup_results:
        job = extract_job(soup_result)
        jobs.append(job)
        
        if len(jobs) >= MAX_COUNT:
          is_full_array =True
          break

      if is_full_array:
        break

    except Exception as e:
      # print(page)
      print("Stack-over-flow, Error Message : ", e)

  return jobs


def get_last_page(url):
  try:
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    page_links = soup.find("div", {"class": "s-pagination"}).find_all("a")
    lastPage = int(page_links[-2].get_text(strip=True))
    return lastPage

  except Exception as e:
    # print(data_rows)
    print("Stack-over-flow, Error Message : ", e)
    return None


def get_job_data(word):
  url = f"https://stackoverflow.com/jobs?q={word}&r=true"
  last_page = get_last_page(url)

  if last_page :
    jobs = extract_jobs(last_page, url)
    return jobs
  else :
    return []


get = get_job_data("python")
print(get)