from jobs.models import Jobs
import requests
from bs4 import BeautifulSoup
        
def jobs_on_bestjobs():
    print("bestjobs ruleaza")
    page = 1
    while page <= 50:
        print(f'pagina {page}')
        url = 'https://www.bestjobs.eu/ro/locuri-de-munca/' + str(page)
        print("se citeste url")
        source = requests.get(url)
        print(source)
        if source.status_code == 200:
            print("statusul este 200!")
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
            print("statusul nu este 200!")
        
if __name__ == '__main__':
    print("__name__==__main__ ruleaza in bestjobs")
    jobs_on_bestjobs()
