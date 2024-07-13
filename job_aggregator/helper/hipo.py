from jobs.models import Jobs
import requests, time, random
from decouple import config
# from requests.auth import HTTPProxyAuth
from bs4 import BeautifulSoup

def jobs_on_hipo():
    page = 1
    while page <= 10:
        print(f'hipo page {page}')
        url = f'https://www.hipo.ro/locuri-de-munca/cautajob/{page}'
        proxy_ip = config('PROXY_IP')
        proxy_port = config('PROXY_PORT')
        username = config('USERNAME')
        password = config('PASSWORD')
        proxies = {
            'http': f'http://{username}:{password}@{proxy_ip}:{proxy_port}',
            'https': f'http://{username}:{password}@{proxy_ip}:{proxy_port}',
        }
        source = requests.get(url, proxies=proxies)
        if source.status_code == 200:
            soup = BeautifulSoup(source.content, 'html.parser')
            hipo_list = soup.find_all('div', {'itemtype': 'http://schema.org/JobPosting'})
            for job in hipo_list:
                job_title = job.find('h5', class_='mb-3').text.strip()
                if 'python' in job_title.lower():
                    job_company = job.find('span', {'itemprop': 'name'}).text.strip()
                    job_url = job.find('a', {'itemprop': 'url'})['href']
                    job_url = f'https://www.hipo.ro{job_url}'
                    location = job.find('span', {'itemprop': 'jobLocation'}).text.strip()
                    if not Jobs.objects.filter(url=job_url).exists():
                        Jobs.objects.create(title=job_title, company=job_company, url=job_url, location=location)
            time.sleep(random.randint(10, 20))
            page += 1
        elif source.status_code == 429:
            print("Received status code 429, sleeping for 60 seconds")
            time.sleep(60)
        else:
            print(f"Failed to retrieve page {page}. Status code: {source.status_code}")
            break

# if __name__ == '__main__':
#     jobs_on_hipo()
    