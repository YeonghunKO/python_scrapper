import requests
from bs4 import BeautifulSoup


# url = 'https://weworkremotely.com/remote-jobs/search?term=python';
MAX_COUNT = 50

def extract_jobs(url):
  print(f"Scrapping WeWorkRemotely ...")

  jobs = []
  result = requests.get(url)
  soup = BeautifulSoup(result.text, 'html.parser')

  category = soup.find("section", {"id":"category-2"})

  if not category:
    return jobs

  job_items = category.findAll("li")

  for item in job_items:
    try:
      if item.get("class") and "view-all" in item["class"]:
        continue

      logo = item.find("div",{"class":"flag-logo"})
      if logo :
        logo = logo["style"].replace("background-image:url", "")
        logo = logo.replace("(", "").replace(")", "")
      else :
        logo = None

      job_link = item.find("a", recursive=False)

      if job_link :
        title = job_link.find("span", {"class":"title"}).get_text()
        company = job_link.find("span", {"class":"company"}, recursive=False).get_text()
        
        location = job_link.find("span", {"class":"region"})
        if location:
          location = location.get_text()

        link = job_link["href"]
        job = {
          "logo": logo,
          "title": title,
          "company": company,
          "location": location,
          "link": f"https://weworkremotely.com{link}"
        }
        jobs.append(job)

        if len(jobs) >= MAX_COUNT:
          break

      else :
        continue

    except Exception as e:
      print(item)
      print("WeWorkRemotely, Error Message : ", e)

  return jobs


def get_job_data(word):
  url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
  jobs = extract_jobs(url)

  return jobs