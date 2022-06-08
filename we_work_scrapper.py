from bs4 import BeautifulSoup
import requests
import json

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
MAX_COUNT = 50
def extract_job(data):
    # print("\n",data)
    title = data.find("span",{"class":"title"}).get_text(strip=True)
    company = data.find("span",{"class":"company"}).get_text(strip=True)
    link = data.find("a")["href"]
    link_url = f"https://weworkremotely.com{link}"
        
    try:
        logo = data.find("div", {"class":"flag-logo"})
        if logo:
            logo = logo["style"].replace("background-image:url(","").replace(")","")      
        # print(logo) 
    except:
        logo = "no logo"
    

    return {"title":title,
           "company":company,
           "link":link_url,
           'logo':logo
           }

def get_job_data(keyword):
    jobs = []
    print("we_work job scrapping...")
    url = f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={keyword}"
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, "html.parser")
    li = soup.find("section", {"class":"jobs"})
    if li:
        job_data = soup.find("section", {"class":"jobs"}).find_all("li")
    else:
        print("not found")
        job_data = None
    # print(li)
    if job_data:
        for data in job_data[:-1]:
            job = extract_job(data)
            jobs.append(job)
            length = len(jobs)
            # print(length,"we_work jobs found")
            if length >= MAX_COUNT:
                break
            else:
                continue
    return jobs


# go = get_job_data("c#")

# print(go)

