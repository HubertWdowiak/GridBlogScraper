from utils import get_last_date, scrap_new_urls, scrap_articles_from_urls, \
    update_articles, update_authors, prepare_timeline, read_json_from_file

import matplotlib.pyplot as plt
import pandas as pd
import itertools


def scrape_data():
    """
    Scraps data about articles and their authors from grid dynamics blog.

    If runned for the first time, it creates two files: 'articles.json',
    'authors.json'.

    If 'articles.json' and 'authors.json' already exist, then it finds the
    latest article within it and scraps only articles (and their authors)
    that are more recent.
    """
    last_date = get_last_date()
    new_urls = scrap_new_urls(last_date)
    new_articles = scrap_articles_from_urls(new_urls)
    update_articles(new_articles)
    update_authors(new_articles)


def create_report():
    """
    Creates report containing three plots:

    First bar plot shows 5 most productive authors and how many articles
    they have written by now.

    Second bar plot shows 7 most popular tags and amounts of their occurences
    in the blog.

    Third subplot shows a timeline with 5 most recent articles placed on it.
    """

    authors = read_json_from_file('authors.json')
    articles = read_json_from_file('articles.json')

    articles_df = pd.DataFrame(articles)
    recent_articles = articles_df.sort_values('date', ascending=False)[:5]

    authors_df = pd.DataFrame(authors)
    best_authors = authors_df.nlargest(5, 'articles')

    tags = list(itertools.chain.from_iterable(articles_df.iloc[:]['tags']))
    tags_counted = pd.value_counts(tags, ascending=False)
    best_tags = tags_counted[:7]

    fig, axs = plt.subplots(3, figsize=(25, 10))

    axs[0].set_title('Most productive authors', fontsize=20)
    axs[0].bar(best_authors['name'], best_authors['articles'], color='orange', edgecolor='black')
    axs[0].bar('average', authors_df['articles'].mean())
    axs[0].set_xticks([*best_authors['name'], 'average'])
    axs[0].set_ylabel('Amount of written articles')

    axs[1].set_title('Most common tags', fontsize=20)
    axs[1].barh(best_tags.index, best_tags.values, color='orange', edgecolor='black')
    axs[1].barh('average', tags_counted.mean())
    axs[1].set_xlabel('Number of tag occurrences')

    prepare_timeline(axs[2], names=recent_articles['title'], dates=recent_articles['date'])
    plt.subplots_adjust(hspace=1)
    plt.suptitle("GRID DYNAMICS BLOG REPORT", fontsize=35)

    for ax in axs:
        for spine in ["left", "top", "right"]:
            ax.spines[spine].set_visible(False)

    plt.show()


if __name__ == '__main__':
    scrape_data()
    create_report()