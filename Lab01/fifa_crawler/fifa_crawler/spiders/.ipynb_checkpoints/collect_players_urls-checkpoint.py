import scrapy

class collect_player_url(scrapy.Spider):
    name='players_urls' 
    def start_requests(self):
        urls = ['https://sofifa.com/players?col=oa&sort=desc&offset=0']
        # YOUR CODE HERE
        self.pages=0
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
  
    def parse(self, response):
    # YOUR CODE HERE
        for player in response.css('.col-name'):
            player_link = player.xpath('a/@href').re(r'/player/\w+')
            if len(player_link)> 0:
                yield {'player_url': player_link[0]}
                
        next_page=response.xpath('.//a[@class="bp3-button bp3-intent-primary pjax"]/@href').extract()
        if next_page and self.pages <11:
            if len(next_page)==1: # previous, next
                next_href=next_page[0]
            else:
                next_href=next_page[1]
            next_page_url='https://sofifa.com'+next_href
            self.pages+=1
            request=scrapy.Request(url=next_page_url)
            yield request
