import sys
import timeit

import requests
from requests_html import HTMLSession


class Crawler(object):
    def __init__(self):
        self.extracted_data = {}
        self.selectors = {}

    def crawl(self):
        self.session = HTMLSession()
        self.request = self.session.get(self.url)
        self.crawl_execution()

    def crawl_execution(self):
        tree = self.request.html

        for name, selectors in self.selectors.items():

            for selector in selectors:
                content = tree.xpath(selector)

                if content:
                    if not self.extracted_data.get(name):
                        self.extracted_data[name] = []

                    for element in content:
                        self.extracted_data[name].append(element.full_text)

    def parse(self, unparsed_data):
        data = unparsed_data.split("\n")[:-1]

        for line in data:
            name, *selector = line.split(",")
            self.selectors[name] = selector

    def read_input(self, url=None, file_name=None):
        self.url = url or sys.argv[2]

        with open(file_name or sys.argv[1]) as infile:
            self.data = self.parse(infile.read())


def main(url=None, file_name=None):
    crawler = Crawler()
    crawler.read_input(url=url, file_name=file_name)
    crawler.crawl()

    print(crawler.extracted_data)


def how_long():
    example_url = "https://www.jetpens.com/Pilot-Metropolitan-Fountain-Pen-Black-Plain-Medium-Italic-Nib/pd/19271"
    example_file = "jetpens.txt"
    t = timeit.Timer(lambda: main(url=example_url, file_name=example_file))
    print(t.timeit(number=20)/20)


if __name__ == "__main__":
    main()
