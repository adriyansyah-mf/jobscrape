import requests
import re
from bs4 import BeautifulSoup
import xlsxwriter

class JobScrape:
    user_agents = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/36.0.1941.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/37.0.2062.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
    ]

    def get_id_company(self, url: str):
        req = requests.get(url, headers={
            "User-Agent": self.user_agents[0]
        })

        data = req.text

        soup = BeautifulSoup(data, 'html.parser')

        meta_tag = soup.findAll('meta')

        for tag in meta_tag:
            try:
                if 'https://siva' in tag.get('content'):
                    url = tag.get('content')
                    get_id = re.findall(r'(?<=/)\d+', url)
                    return get_id[0]
            except:
                pass

    def get_job(self, url):
        id = self.get_id_company(url)
        url = f"https://api-js.prod.companyreview.co/jobs/{id}?page=1&language=en&country=id"
        req = requests.get(url, headers={
            "User-Agent": self.user_agents[0],
            "referer": "https://www.jobstreet.co.id/",
            "Origin": "https://www.jobstreet.co.id",
            "x-api-key": "77GsVyxVDN5HQN1eUOZ4t3R6zx0awW3Y5eZHzFr6"
        })
        job = req.json()

        return job

    def get_page(self, url):
        data = self.get_job(url)
        paging = data['paging']
        total = paging['total']
        per_page = paging['per_page']
        page = total // per_page
        return page + 1

    def get_job_detail(self, url):
        workbook = xlsxwriter.Workbook('job.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write('A1', 'Job Title')
        worksheet.write('B1', 'Job Url')

        row = 1
        id_company = self.get_id_company(url)
        for page in range(1, self.get_page(url) + 1):
            url = f"https://api-js.prod.companyreview.co/jobs/{id_company}?page={page}&language=en&country=id"
            req = requests.get(url, headers={
                "User-Agent": self.user_agents[0],
                "referer": "https://www.jobstreet.co.id/",
                "Origin": "https://www.jobstreet.co.id",
                "x-api-key": "77GsVyxVDN5HQN1eUOZ4t3R6zx0awW3Y5eZHzFr6"
            })
            job = req.json()
            data = job['data']
            for i in data:
                job_title = i['position_title']
                job_url = i['url']
                worksheet.write(row, 0, job_title)
                worksheet.write(row, 1, job_url)
                row += 1
                print(job_title, job_url)

        workbook.close()



if __name__ == '__main__':
    url = input("Masukkan url: ")
    JobScrape().get_job_detail(url)
