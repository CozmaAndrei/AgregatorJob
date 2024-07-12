from jobs.models import Jobs
import requests, time, random
from decouple import config
from requests.auth import HTTPProxyAuth
from bs4 import BeautifulSoup
        
def jobs_on_bestjobs():
    page = 1
    while page <= 10:
        print(f'bestjobs page {page}')
        url = 'https://www.bestjobs.eu/ro/locuri-de-munca/' + str(page)
        proxy_ip = config('PROXY_IP')
        proxy_port = config('PROXY_PORT')
        username = config('USERNAME')
        password = config('PASSWORD')
        proxies = {
            'http': f'http://{username}:{password}@{proxy_ip}:{proxy_port}',
            'https': f'http://{username}:{password}@{proxy_ip}:{proxy_port}',
        }
        # auth = HTTPProxyAuth(str(username), str(password))
        source = requests.get(url, proxies=proxies)#, proxies=proxies, auth=auth
        if source.status_code == 200:
            soup = BeautifulSoup(source.content, 'html.parser')
            bestjobs_list = soup.find_all('div', class_='list-card')
            for job in bestjobs_list:
                jobs_title = job.find('h2', class_='h6 truncate-2-line').text.strip()
                if 'python' in jobs_title.lower():
                    jobs_company = job.find('div', class_='h6 text-muted text-truncate py-2').text.strip()
                    url = job.find('a')['href']
                    location = job.find('div', class_='d-flex min-width-3')
                    if location:
                        location = location.text.strip()
                    else:
                        location = 'Necunoscuta'
                    if not Jobs.objects.filter(url=url).exists():
                        Jobs.objects.create(title=jobs_title, company=jobs_company, url=url, location=location)
                        # print(f"Am găsit un job: {jobs_title} - {jobs_company} - {location}")
            time.sleep(random.randint(10, 20))
            page += 1
        elif source.status_code == 429:
            print("Received status code 429, sleeping for 60 seconds")
            time.sleep(60)  # Așteaptă 60 de secunde înainte de a încerca din nou
        else:
            print(f"Failed to retrieve page {page}. Status code: {source.status_code}")
            break
  
# if __name__ == '__main__':
#     jobs_on_bestjobs()
