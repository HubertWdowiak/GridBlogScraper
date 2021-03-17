from utils import get_last_date, scrap_new_urls, scrap_articles_from_urls, update_articles


def scrape_data():
    last_date = get_last_date()
    new_urls = scrap_new_urls(last_date)
    new_articles = scrap_articles_from_urls(new_urls)
    update_articles(new_articles)


def create_report():
    scrape_data()


if __name__ == '__main__':
    create_report()
