from jobs.models import Jobs
import requests, time, random
from decouple import config
# from requests.auth import HTTPProxyAuth
from bs4 import BeautifulSoup

def jobs_on_juniors():
    page = 1
    while page <= 10:
        print(f'juniors page {page}')
        url = f'https://www.juniors.ro/jobs?page={page}'
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
            juniors_list = soup.find_all('li', class_='job')
            for job in juniors_list:
                job_title = job.find('div', class_='job_header_title').find('h3').text.strip()
                job_tags = job.find('div', class_='job_header_title').find('ul', class_='job_tags').find_all('a')
                job_tags = [tag.text.strip().lower() for tag in job_tags]
                if 'python' in job_title.lower() or 'python' in job_tags:
                    job_company = job.find('div', class_="job_content").find('ul').find('li').text.strip().replace('Companie:', '').strip('"').strip()
                    job_url = job.find('div', class_='job_header_buttons').find('form')['action']
                    location = job.find('div', class_='job_header_title').find('strong').text.strip()
                    location = location.strip()
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
#     jobs_on_juniors()