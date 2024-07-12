from jobs.models import Jobs
import requests, time, random
from decouple import config
from requests.auth import HTTPProxyAuth
from bs4 import BeautifulSoup
import requests


def jobs_on_ejobs():
    
    page = 1
    while page <= 10:
        print(f'ejobs page {page}')
        url = f'https://www.ejobs.ro/locuri-de-munca/pagina{page}'
        proxy_ip = config('PROXY_IP')
        proxy_port = config('PROXY_PORT')
        username = config('USERNAME')
        password = config('PASSWORD')
        proxies = {
            'http': f'http://{username}:{password}@{proxy_ip}:{proxy_port}',
            'https': f'http://{username}:{password}@{proxy_ip}:{proxy_port}',
        }
        try:
            source = requests.get(url, proxies=proxies)#, proxies=proxies, auth=auth
            if source.status_code == 200:
                soup = BeautifulSoup(source.content, 'html.parser')
                ejobs_list = soup.find_all('ul', class_='JobList__List')
                for job in ejobs_list:
                    jobs_title = job.find('h2', class_='JCContentMiddle__Title').text.strip()
                    if 'python' in jobs_title.lower():
                        jobs_company = job.find('h3', class_='JCContentMiddle__Info').text.strip()
                        job_url = job.find('a')['href']
                        location = job.find('div', class_='JCContentMiddle__Info')
                        if location:
                            location = location.text.strip()
                        else:
                            location = 'Necunoscuta'
                        if not Jobs.objects.filter(url=job_url).exists():
                            Jobs.objects.create(title=jobs_title, company=jobs_company, url=job_url, location=location)
                            # print(f"Am găsit un job: {jobs_title} - {jobs_company} - {location}")
                time.sleep(random.randint(10, 20))
                page += 1
            elif source.status_code == 429:
                print("Received status code 429, sleeping for 60 seconds")
                time.sleep(60)  # Așteaptă 60 de secunde înainte de a încerca din nou
            else:
                print(f"Failed to retrieve page {page}. Status code: {source.status_code}")
                break
        except requests.exceptions.RequestException as e:
            print(f"RequestException: {e}")
            break

# if __name__ == '__main__':
#     jobs_on_ejobs()