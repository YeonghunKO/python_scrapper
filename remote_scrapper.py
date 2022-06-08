from bs4 import BeautifulSoup
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
MAX_COUNT = 50

def extract_job(ele):    
    company = ele['data-company']
    link = ele['data-href']
    link_url = f"https://remoteok.io/{link}"
    title = ele.find("h2", {"itemprop": "title"}).get_text(strip=True)
    try:
        logo = ele.find("img",{"class":"logo"})
        if logo and logo.get("data-src"):
            logo = logo["data-src"]
        elif logo and logo.get("src"):
            logo = logo["src"]
        else:
            logo = "no logo"
    except:
        pass

    return {"title": title,
            "company": company, 
            "link": link_url, 
            "logo": logo
            }        


def get_job_data(keyword):
    print("remote job scrapping...")
    jobs = []
    # remote website doesn't support # and + character
    keyword = keyword.replace("+","plus").replace("#","sharp")
    url = f"https://remoteok.io/remote-{keyword}-jobs"
    result = requests.get(url, headers = headers)
    soup = BeautifulSoup(result.text, "html.parser")
    element = soup.find("table", {"id":"jobsboard"})
    if element:
        job_data = element.findAll("tr", {"class":"job"})
    else:
        print("not found")
        job_data = None
    if job_data:
        for ele in job_data:
            data = extract_job(ele)
            jobs.append(data)
            length = len(jobs)
            # print(length, "remote job found")
            if length >= MAX_COUNT:
                break
            else:
                continue
    return jobs


# job = get_job_data("python")
# print(job)