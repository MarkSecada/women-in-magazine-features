from bs4 import BeautifulSoup
import requests
import sqlite3

def create_tables():
    conn = sqlite3.connect('./magazine_features.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE issue_html (
        magazine VARCHAR(32),
        issue_date DATE,
        url TEXT,
        html TEXT);""")
    cur.execute("""CREATE TABLE authors (
        magazine VARCHAR(32),
        issue_date DATE,
        title TEXT,
        url TEXT,
        is_cover BOOLEAN,
        author TEXT);""")
    conn.close()

def get_new_yorker_reports(end_year=2010):
    base_url = 'https://www.newyorker.com/magazine/reporting/page/'
    page_num = 1
    conn = sqlite3.connect('./magazine_features.db')
    cur = conn.cursor()
    url = f'{base_url}{page_num}'
    while True:
        r = requests.get(url)
        page = BeautifulSoup(r.text, features='html.parser')
        articles = page.findall('li', class_='River__riverItem___3huWr')
        for article in articles:
            issue_date = article.find('div', class_='River__issueDate___2DPuc')
            issue_link = issue_date.find('a', class_='Link__link___3dWao')['href']
            
            if int(issue_link.split('/')[2]) < end_year:
                break

            date = '-'.join(issue_link.split('/')[2:])

            byline_div = article.find('div', class_='Byline__by___37lv8')
            authors = byline_div.findall('a')
            for author in authors:
                row = ('new_yorker', date, author.text.a)
                cur.execute('INSERT INTO authors VALUES (?,?,?)', row)
                conn.commit()
                print(f'Inserted for issue {date}')
        page_num += 1
    conn.close()
    return 'success!'

def get_nymag_issues(start_year=2010, end_year=2019):
    base_url = 'http://nymag.com/magazine/'
    issue_pages = []
    for year in range(start_year, end_year + 1):
        url = f'{base_url}{year}.html'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, features='html.parser')
        issues = soup.find_all('li', class_='issue-wrapper list-item')
        for issue in issues:
            if 'wedding' in issue:
                pass
            else:
                issue_pages.append(issue.a['href'])
    conn = sqlite3.connect('./magazine_features.db')
    cur = conn.cursor()
    for issue in issue_pages:
        r = requests.get(issue)
        date = issue.split('/')[-1].split('.')[0]
        row = ('nymag',
            date,
            issue,
            r.text)
        cur.execute('INSERT INTO issue_html VALUES (?,?,?,?)', row)
        conn.commit()
        print(f'Inserted issue {date}')
    conn.close()
    return 'success!'

def get_atlantic_issues(start_year=2010, end_year=2019):
    base_url = 'https://www.theatlantic.com/magazine/backissues/year/'
    conn = sqlite3.connect('./magazine_features.db')
    cur = conn.cursor()
    for year in range(start_year, end_year + 1):
        url = f'{base_url}{year}'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, features='html.parser')
        issues = soup.find_all('li', class_='article')
        for issue in issues:
            href = issue.a['href']
            issue_url = f'https://www.theatlantic.com{href}'
            html = requests.get(issue_url).text
            date = issue_url.split('/')[-3:-1]
            row = ('the_atlantic',
                f'{date[0]}-{date[1]}-01',
                issue_url,
                html)
            cur.execute('INSERT INTO issue_html VALUES (?,?,?,?)', row)
            conn.commit()
            print(f'Inserted issue {date[0]}-{date[1]}-01')
    conn.close()
    return 'success!'

def get_harpers_issues(start_year=2010, end_year=2019):
    pass

def get_nyt_mag_issues():
    url = ('https://www.nytimes.com/'
        'interactive/2017/magazine/'
        'past-issues-sunday-mag.html')
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features='html.parser')
    issues = soup.find_all('a', class_='issue')
    conn = sqlite3.connect('./magazine_features.db')
    cur = conn.cursor()
    for issue in issues:
        href = issue['href']
        html = requests.get(href).text
        date = '-'.join(href.split('/')[5:8])
        row = ('nyt_mag', date, href, html)
        cur.execute('INSERT INTO issue_html VALUES (?,?,?,?)', row)
        conn.commit()
        print(f'Inserted issue {date}')
    conn.close()
    return 'success!'

def get_vanity_fair_issues(start_year=2010, end_year=2019):
    pass