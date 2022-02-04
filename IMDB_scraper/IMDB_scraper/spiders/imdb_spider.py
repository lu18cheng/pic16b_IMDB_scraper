# to run
# scrapy crawl imdb_spider -o movies.csv

import scrapy


class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'

    start_urls = ['https://www.imdb.com/title/tt0096283/']

    def parse(self, response):
        '''
        Assume that you start on a movie page
        then navigate to the Cast & Crew page
        '''

        # since all cast & crew page has the link of fullcredits to
        yield scrapy.Request(response.urljoin("fullcredits/"),
                             callback=self.parse_full_credits)

        # #alternative way of getting the cast & crew website using css
        # elts = response.css("li.ipc-inline-list__item")
        # links = [e.css("a").attrib['href'] for e in elts
        #          if e.css("a::text") and e.css("a::text").get() == "Cast & crew"]
        # yield scrapy.Request(response.urljoin(links[0]), callback=self.parse_full_credits)


    def parse_full_credits(self, response):
        '''
        assume that you start on the Cast & Crew page.
        yield a `scrapy.Request` for the page of each actor listed on the page
        '''

        #get link to all cast members
        cast_links = [a.attrib['href'] for a in response.css("table.cast_list td.primary_photo a")]

        # yield result
        for link in cast_links:
            yield scrapy.Request(response.urljoin(link),
                                 callback=self.parse_actor_page)

    def parse_actor_page(self, response):
        '''
        assume that you start on the page of an actor.
        yield a dictionary with two key-value pairs of the form
        {"actor" : actor_name,
        "movie_or_TV_name" : movie_or_TV_name}.
        '''

        #get name of actor
        actor = response.css("h1.header span.itemprop::text").get()

        #get fields storing information of all films
        rows = response.css("div.filmo-row")
        # filter by `attr(id)` to get only main films and eliminate episodes information
        films = [e.css("a::text").get() for e in rows if e.css("::attr(id)") and e.css("a")]

        # yield result
        for film in films:
            yield {"actor": actor, "movie_or_TV_name": film}

