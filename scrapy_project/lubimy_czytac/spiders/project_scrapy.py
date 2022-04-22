# Necessary imports
import scrapy
import re
import pandas as pd
from scrapy import Request

#creating results class to store results in
class results(scrapy.Item):
    month = scrapy.Field()
    position = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    rating = scrapy.Field()
    readers = scrapy.Field()
    opinions = scrapy.Field()
    no_of_ratings = scrapy.Field()



class scrapy_Spider(scrapy.Spider):
    name = 'scrapy_books'
    allowed_domains = ['lubimyczytac.pl']
    start_urls = ['https://lubimyczytac.pl/top100']

    def parse(self, response):

        #list with pages numbers we want to scrap. For every month there are around 137 books,
        #however we will only take first 100. There are 20 books a page
        #so we need to scrap first 5 pages for each month
        pages = [1, 2, 3, 4, 5]

        ##I'm getting list of all available months for which there is a record (April 2021 - May 2020)
        name_xpath = '//div[@class = "filtr__itemTitle"]/text()'
        months_list = response.xpath(name_xpath).getall()

        #creating a list of urls we want to scrap. We will be scraping the same information from every url. We are receiveing
        #urls by looping over every month and page. So for example we will receive urls for first 5 pages in April 2021,
        #then for the first 5 pages in March 2021 and so on
        urls_list = ["https://lubimyczytac.pl/top100?page=" + str(page) + "&listId=listTop100&month=" + str(x) + "&year=" + str(y).split()[-1] + "&paginatorType=Standard"
                     for x, y in enumerate(months_list, 1) for page in pages]

        #go to the url from the list above
        return (Request(url, callback=self.parse_books_list) for url in urls_list)


    def parse_books_list(self, response):
        #instance of results class where the data will be stored
        m = results()

        #extracting currently selected month
        current_month = response.xpath('//input[@checked="checked"]/@value').extract()
        current_month = current_month*20

        #extracting book's position in ranking and cleaning the output
        position = response.xpath('//span[@class="authorAllBooks__singleImgInfoBottom"]/text()').getall()
        position = [pos.strip() for pos in position]
        position = list(filter(None, position))

        #extracting it's title
        title = response.xpath('//a[@class="authorAllBooks__singleTextTitle float-left"]/text()').getall()
        title = [x.strip() for x in title]

        #it's author
        author = response.xpath('//div[@class="authorAllBooks__singleTextAuthor authorAllBooks__singleTextAuthor--bottomMore"]/a/text()').getall()

        #rating
        rating = response.xpath('//span[@class="listLibrary__ratingStarsNumber"]/text()').getall()
        rating = [x.strip() for x in rating]

        #number of readers
        readers = response.xpath('//span[@class="small grey mr-2 mb-3"]/text()').getall()
        readers = [x.strip() for x in readers]
        readers = [x.replace('Czytelnicy: ', '') for x in readers]

        #number opinions
        opinions = response.xpath('//span[@class="ml-2 small grey"]/text()').getall()
        opinions = [x.strip() for x in opinions]
        opinions= [x.replace('Opinie: ', '') for x in opinions]

        #number of ratings
        no_of_ratings = response.xpath('//div[@class="listLibrary__ratingAll"]/text()').getall()
        no_of_ratings = [x.strip() for x in no_of_ratings]
        no_of_ratings = [x.replace(' ocen', '') for x in no_of_ratings]

        #since above we received lists with results, now I will take in a loop every n-th element of the list and
        #assign it to m. If we assigned a whole list, then results for the whole page (20 books) would be stored as a single row in csv
        for i in range(0, len(position)):
            m["month"] = current_month[i]
            m["position"] = position[i]
            m["title"] = title[i]
            m["author"] = author[i]
            m["rating"] = rating[i]
            m["readers"] = readers[i]
            m["opinions"] = opinions[i]
            m["no_of_ratings"] = no_of_ratings[i]

            #outputting results
            yield m





