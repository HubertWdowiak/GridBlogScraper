import json
from subprocess import call
import os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import logging

utils_logger = logging.getLogger('utils')


def read_json_from_file(filename: str) -> list or dict:
    """Reads data from json file."""
    try:
        with open(filename) as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_json_to_file(data: list or dict, filename: str):
    """Saves data to json file."""
    with open(filename, 'w') as file:
        json.dump(data, file)


def get_last_date() -> datetime:
    """
    Reads data from 'articles.json' and returns date of most recent article
    within it, as a datetime. If the file does not exist, returns '2000-01-01'.
    """
    try:
        articles = read_json_from_file('articles.json')
        dates = sorted([article['date'] for article in articles], reverse=True)
        last_date = dates[0]
        utils_logger.info(f'Found date of last article: {last_date}')
        return last_date
    except (json.decoder.JSONDecodeError, KeyError, FileNotFoundError, IndexError):
        utils_logger.info(f'Could not find date of last article')
        return datetime.strptime('2000-01-01', '%Y-%m-%d')


def scrap_new_urls(last_date: datetime) -> list[str]:
    """
    Takes date, scraps and returns urls for articles from https://blog.griddynamics.com,
    that were created after the date, passed as an argument.
    """
    return_code = call(["scrapy", "crawl", "urls",
                        "-a", f"last_date={last_date}",
                        "-O", "../url.json"], cwd='tutorial')

    if return_code == 0:

        all_scraped_urls = read_json_from_file('url.json')
        try:
            os.remove('url.json')
        except FileNotFoundError:
            pass
        new_urls = []
        for urls in all_scraped_urls:
            new_urls.extend(next(iter((urls.values()))))

        new_urls = ['http://blog.griddynamics.com' + url for url in new_urls]

        return new_urls


def scrap_articles_from_urls(new_urls: list[str]) -> list:
    """
    Takes list of urls and scrapes data from them. Returned data are:
    article title, article url(repeated), authors, first 160 symbols of text,
    publication date, tags placed inside article.
    """
    if not new_urls:
        return []

    if not call(['scrapy', 'crawl', 'articles',
                 '-a', f'start_urls={new_urls}',
                 '-O', '../new_articles.json'],
                cwd='tutorial'):
        new_articles = read_json_from_file('new_articles.json')
        try:
            os.remove('new_articles.json')
        except FileNotFoundError:
            pass
        return new_articles
    return []


def update_articles(new_articles: list):
    """
    Takes list of new articles and appends them to articles.json file.
    """
    if new_articles:
        try:
            all_articles = read_json_from_file('articles.json') + new_articles
        except (json.JSONDecodeError, FileNotFoundError, TypeError):
            all_articles = new_articles

        save_json_to_file(all_articles, 'articles.json')
        return all_articles


def get_urls_of_new_authors(new_articles: list) -> list:
    """
    Takes a list of new articles and compares the names of authors within it,
    to names already saved in authors.json. Returns a list of urls of pages
    which describe authors, who are missing in authors.json file.
    """
    authors = read_json_from_file('authors.json')
    authors_names = [author['name'] for author in authors]
    new_authors_urls = []
    for article in new_articles:
        for author in article['authors']:
            name, url = author
            if name not in authors_names:
                new_authors_urls.append(url)
                authors_names.append(name)

    return ['https://blog.griddynamics.com' + sufix for sufix in new_authors_urls]


def update_old_authors(new_articles: list):
    """
    Takes a list of new articles and compares the names of authors within it,
    to names already saved in authors.json. Updates article-counters for authors
    that are in authors.json.
    """
    authors = read_json_from_file('authors.json')
    authors_names = [author['name'] for author in authors]

    for article in new_articles:
        for author in article['authors']:
            name, url = author
            if name in authors_names:
                for author in authors:
                    if author['name'] == name:
                        author['articles'] += 1

    save_json_to_file(authors, 'authors.json')
    return authors


def update_authors(new_articles: list):
    """
    Takes a list of new articles and updates article-counters for
    the authors who are stored in authors.json file. Also crawls
    all the new authors that do not occur in authors.json file.
    The functions results are dumped to authors.json file.
    """
    urls_of_new_authors = get_urls_of_new_authors(new_articles)
    update_old_authors(new_articles)
    if not call(['scrapy', 'crawl', 'authors',
                 '-a', f'start_urls={urls_of_new_authors}',
                 '-O', '../new_authors.json'],
                cwd='tutorial'):

        authors = read_json_from_file('authors.json')
        new_authors = read_json_from_file('new_authors.json')
        if new_authors:
            authors += new_authors
        try:
            os.remove('new_authors.json')
        except FileNotFoundError:
            pass
        save_json_to_file(authors, 'authors.json')


def prepare_timeline(ax, names, dates):
    """
    Creates plot of timeline, with names placed on it according
    to dates.
    """

    levels = [-0.1, 0.1, -0.1, 0.1, -0.1]
    dates = [datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d in dates]

    ax.set_title("5 most recent articles", fontsize=20)
    ax.vlines(dates, 0, levels, color="tab:red")
    ax.plot(dates, np.zeros_like(dates), "-o",
            color="k", markerfacecolor="w")

    for d, l, r in zip(dates, levels, names):
        ax.annotate(r, xy=(d, l),
                    xytext=(-3, np.sign(l) * 3), textcoords="offset points",
                    horizontalalignment="center",
                    verticalalignment="bottom" if l > 0 else "top")

    ax.get_xaxis().set_major_locator(mdates.DayLocator(interval=1))
    ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%d %b %Y"))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    ax.get_yaxis().set_visible(False)

    ax.margins(y=0.5)