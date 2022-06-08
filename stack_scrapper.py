import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
MAX_COUNT = 50

def so_last_page(url):
    try:
        result = requests.get(url, headers = headers)
        soup = BeautifulSoup(result.text, "html.parser")
        pagi = soup.find("div", {"class":"s-pagination"}).find_all("a")           
        last = pagi[-2].get_text(strip=True) #pagi 안에 텍스트(페이지넘버)를 불러들이고 strip 해서 정리해줌.(이런식으로 strip=true를 인자로 사용가능)
        return int(last)
        # indeed 서 처럼 link에서 span을 다 뽑아서 리스트에 넣은다음 리스트 마지막 숫자만 뽑아내도 좋고
        # 여기서 처럼 아예 링크 마지막 부분을 애초부터 뽑아내도 괜찮다.
    except:
        return int(1)

def extract_job(html):       
    title = html.find("h2", {"class": "mb4"}).find("a")["title"]
    company = html.find("h3", {"class":"fc-black-700"}).find("span").get_text(strip=True)
    location = html.find("span", {"class": "fc-black-500"}).get_text(strip=True)
    job_id = html["data-jobid"]    
    link = f"https://stackoverflow.com/jobs/{job_id}" # 어떻게 하면 간편하게 링크를 만들수 있을까 이것저것 시험해봐라
    try:
        logo = html.find("div", {"class":"grid--cell"}).find("img")["src"]
    except:
        logo = "no logo"

    return {'title': title , 
            'company': company ,             
            'link':link,
            'logo':logo
            }


def extract_data(last_page, url):   
    jobs = [] 
    is_full_array = False
    print("stack jobs scrapping...")
    for page in range(last_page):
        
        # print(f"Scrapping SO Page:{page}")
        result = requests.get(f"{url}&pg={page + 1}", headers = headers)
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class":"-job"} )
        if results:
            job_data = soup.find_all("div", {"class":"-job"} )
        else:
            print("not found")
            job_data = None
        if job_data:
            for result in job_data:
                job = extract_job(result)
                jobs.append(job)
                length = len(jobs)
                # print(length,"stack jobs found")
                if length >= MAX_COUNT:
                    is_full_array = True
                    break
                else:
                    continue     
            if is_full_array:
                break

    return jobs


def get_job_data(word):
    url =f"https://stackoverflow.com/jobs?q={word}&sort=i"
    last_page = so_last_page(url)
    so_jobs = extract_data(last_page, url) # 인자를 2개 넣을 수 있다.
    return so_jobs

# get = get_job_data("python")
# print(get)

# lets_go = get_jobs('react')
# print(lets_go) # 함수안에 저장된 리스트를 볼려면 print 해줘야함.


# <난 사용안했지만, 니코는 사용한것>

# tuple unpacking(mutiple assignment)--알아보자!(밑에 계속)

# 장소와 회사변수를 각각 지정안해주고 한번에 지정할 수 있음
# company,location = html.find("div", {"class": "-company"}).find_all("span",recursive=False)
# 라고 하면 
# // recursive = false --안에 속해있는 모든 자손을 불러오지 말고 직계자손만, first level 만 불러옴!
# 예를 들어 아래와 같은 html 코드가 있다고 치고. 위에 코드를 쳤다고 치자.
# <div class = -company >
#   <span class = a>
#     KIA
#     <span class = b>LOL</span>
#   </span> 
#   <span class = a1>
#     KOREA
#   </span>
# </div>
# 그럼 직계자손 span 만 불러오므로 결과값은 company = KIA, location = KOREA 가 된다.