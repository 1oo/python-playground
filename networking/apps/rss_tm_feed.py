#!/usr/bin/env python3

import feedparser


def pretty_print(title, link, published):
    template = "{0} \n {1} \n {2} \n\n"
    print(template.format(title, link, published))


def select_titles(feed):
    for item in feed["items"]:
        pretty_print(item["title"], item["link"], item["published"])


def main():
    sites = ("https://habrahabr.ru/rss/interesting/",
             "https://megamozg.ru/rss/interesting/",
             "https://geektimes.ru/rss/interesting/")

    for rss in sites:
        feed = feedparser.parse(rss)
        select_titles(feed)

if __name__ == '__main__':
    main()
