from jobs.models import Jobs
import requests
from bs4 import BeautifulSoup
        
def jobs_on_bestjobs():
    page = 1
    while page <= 50:
        url = 'https://www.bestjobs.eu/ro/locuri-de-munca/' + str(page)
        source = requests.get(url)
        if source.status_code == 200:
            soup = BeautifulSoup(source.content, 'html.parser')
            jobs_list = soup.find_all('div', class_='list-card')
            for job in jobs_list:
                jobs_title = job.find('h2', class_='h6 truncate-2-line').text.strip()
                jobs_company = job.find('div', class_='h6 text-muted text-truncate py-2').text.strip()
                url = job.find('a')['href']
                location = job.find('div', class_='d-flex min-width-3')
                if location:
                    location = location.text.strip()
                else:
                    location = 'Necunoscuta'
                
                if 'python' in jobs_title.lower():
                    # if not Jobs.objects.filter(url=url).exists():
                    Jobs.objects.create(title=jobs_title, company=jobs_company, url=url, location=location)
                else:
                    pass
            
            page += 1
        else:
            pass
        
if __name__ == '__main__':
    jobs_on_bestjobs()