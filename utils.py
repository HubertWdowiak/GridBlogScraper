import json
from datetime import datetime
from subprocess import call
import subprocess

def execute(cmd):
    popen = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE,
                             universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
         yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

def get_last_date():
    try:
        with open('articles.json', 'r') as file:
            articles = json.load(file)

            dates = [article['date'] for article in articles]
            dates.sort()
            return dates[-1]

    except (json.decoder.JSONDecodeError, KeyError, FileNotFoundError) as e:
        return datetime.strptime('2000-02-22', '%Y-%m-%d')



def scrap_new_urls(last_date):
    return_code = call(["scrapy", "crawl", "urls", "-a", f"last_date={last_date}", "-O", "../url.json"], cwd='tutorial')
    if return_code == 0:
        with open('url.json', 'r') as file:
            all_scraped_urls = json.load(file)

        new_urls = []
        for i in all_scraped_urls:
            new_urls.extend(next(iter((i.values()))))

        for i in range(len(new_urls)):
            new_urls[i] = 'http://blog.griddynamics.com' + new_urls[i]

        return new_urls


def scrap_articles_from_urls(new_urls):
    if new_urls:
        call(['scrapy', 'crawl', 'articles', '-a', f'start_urls={new_urls}', '-O', '../new_articles.json'],
             cwd='tutorial')

        with open('new_articles.json', 'r') as file:
            return json.load(file)


def update_articles(new_articles):
    try:
        with open('articles.json', 'r') as file:
            all_articles = json.load(file) + new_articles
    except (json.JSONDecodeError, FileNotFoundError) as e:
        all_articles = new_articles

    with open('articles.json', 'w') as file:
        json.dump(all_articles, file)

    open('new_articles.json', 'w').close()
    open('url.json', 'w').close()
