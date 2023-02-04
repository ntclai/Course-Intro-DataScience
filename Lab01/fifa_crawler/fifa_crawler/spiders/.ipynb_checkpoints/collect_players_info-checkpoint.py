import scrapy
import json

class collect_player_info(scrapy.Spider):
    name='players_info'
    def __init__(self):
        try:
            with open('dataset/players_urls.json') as f:
                self.players = json.load(f)
            self.player_count = 1
        except IOError:
            print("File not found")

    def start_requests(self):
        urls = ['https://sofifa.com/player/231747?units=mks']
        # YOUR CODE HERE
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
  
    def parse(self, response):
      # YOUR CODE HERE
        def extract_with_css(query, getall=False):
            if getall:
                return response.css(query).getall()
            return response.css(query).get(default='').strip()
        
        def extract_with_xpath(query, extract_all=False):
            if extract_all:
                return response.xpath(query).extract()
            return response.xpath(query).extract_first(default='').strip()
        str1=extract_with_css("div.info div::text", getall=True)[-1]# lưu age, birth_date, height, weight
        birth_date=str1[17:21]+'/'+str1[9:12]+'/'+str1[13:15]
        teams={}
        temp1=response.xpath('//div[@class="center"][1]//div[@class="grid"]//div[@class="col col-12"]//div[@class="block-quarter"]').xpath('@class').getall()
        index_team=[]
        if len(temp1)>7:
            index_team=[3,4]
        else:
            index_team=[3]
        for i in index_team:
            n=response.xpath(f'//div[@class="center"][1]//div[@class="grid"]//div[@class="col col-12"]//div[@class="block-quarter"][{i}]//div[@class="card"]//h5/a/text()').get()
            v=response.xpath(f'//div[@class="center"][1]//div[@class="grid"]//div[@class="col col-12"]//div[@class="block-quarter"][{i}]//div[@class="card"]//ul[@class="ellipsis pl"]//li/span/text()').get()
            teams[' '+n]=int(v)
            
        #Get Release Clause
        temp2=response.xpath('//div[@class="block-quarter"]//div[@class="card"]//ul[@class="pl"]//li[@class="ellipsis"]/span/text()')
        release_clause=None
        if len(temp2)>3:
            release_clause=temp2[3]
        if release_clause!=None:
            yield{
                "id":self.players[self.player_count-1]['player_url'][8:],
                "name": extract_with_xpath("//div[@class='info']/h1/text()"), #ok
                "primary_position": extract_with_xpath("//div[@class='meta ellipsis']/span[1]/text()"), #ok
                "positions":extract_with_xpath("//div[@class='meta ellipsis']/span/text()", extract_all=True), #ok
                "age": str1[:3],#ok
                "birth_date": birth_date,#ok
                "height": str1[23:26],#ok
                "weight": str1[29:31], #ok
            
                "Overall Rating": extract_with_xpath("//div[@class='block-quarter'][1]/div/span/text()"),#ok
                "Potential": extract_with_xpath("//div[@class='block-quarter'][2]/div/span/text()"), #ok
                "Value": extract_with_xpath("//div[@class='block-quarter'][3]/div/text()"),#ok
                "Wage": extract_with_xpath("//div[@class='block-quarter'][4]/div/text()"),#ok
            
                "Preferred Foot": extract_with_xpath("//div[@class='card'][1]/ul/li[1]/text()"),#ok
                "Weak Foot": extract_with_xpath("//div[@class='card'][1]/ul/li[2]/text()"),#ok
                "Skill Moves": extract_with_xpath("//div[@class='card'][1]/ul/li[3]/text()"),#ok
                "International Reputation": extract_with_xpath("//div[@class='card'][1]/ul/li[4]/text()"), #ok
                "Work Rate": extract_with_xpath("//div[@class='card'][1]/ul/li[5]/span/text()"), #ok
                "Body Type": extract_with_xpath("//div[@class='card'][1]/ul/li[6]/span/text()"), #ok
                "Real Face": extract_with_xpath("//div[@class='card'][1]/ul/li[7]/span/text()"), #ok
                "Release Clause": extract_with_xpath("//div[@class='card'][1]/ul/li[8]/span/text()"), #ok
                "teams":teams, #ok
                "attacking": {"Crossing": extract_with_xpath("//div[@class='col col-12']/div[3]//ul/li[1]/span/text()"),"Finishing": extract_with_xpath("//div[@class='col col-12']/div[3]//ul/li[2]/span/text()"), "HeadingAccuracy": extract_with_xpath("//div[@class='col col-12']/div[3]//ul/li[3]/span/text()"), "ShortPassing":extract_with_xpath("//div[@class='col col-12']/div[3]//ul/li[4]/span/text()"), "Volleys": extract_with_xpath("//div[@class='col col-12']/div[3]//ul/li[5]/span/text()")}, #ok
            
                "skill":{"Dribbling":extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[4]//ul/li[1]/span[1]/text()"), "Curve": extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[4]//ul/li[2]/span[1]/text()"), "FKAccuracy":extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[4]//ul/li[3]/span[1]/text()"), "LongPassing": extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[4]//ul/li[4]/span[1]/text()") , "BallControl":extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[4]//ul/li[5]/span[1]/text()")}, #ok
            
                "movement":{"Acceleration": extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[5]//ul/li[1]/span[1]/text()"), "SprintSpeed":extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[5]//ul/li[2]/span[1]/text()"), "Agility": extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[5]//ul/li[3]/span[1]/text()"), "Reactions": extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[5]//ul/li[4]/span[1]/text()"), "Balance": extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[5]//ul/li[5]/span[1]/text()")}, #ok
            
                "power":{"ShotPower":extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[6]//ul/li[1]/span[1]/text()"), "Jumping": extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[6]//ul/li[2]/span[1]/text()"), "Stamina":extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[6]//ul/li[3]/span[1]/text()"), "Strength":extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[6]//ul/li[4]/span[1]/text()"), "LongShots":extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[6]//ul/li[5]/span[1]/text()")}, #ok
            
                "mentality":{'Aggression':extract_with_xpath("//div[@class='block-quarter'][5]/div/ul/li/span/text()"),'Interceptions':extract_with_xpath("//div[@class='block-quarter'][5]/div/ul/li[2]/span/text()"),'Positioning':extract_with_xpath("//div[@class='block-quarter'][5]/div/ul/li[3]/span/text()"),'Vision':extract_with_xpath("//div[@class='block-quarter'][5]/div/ul/li[4]/span/text()"),'Penalties':extract_with_xpath("//div[@class='block-quarter'][5]/div/ul/li[5]/span/text()"),'Composure':extract_with_xpath("//div[@class='block-quarter'][5]/div/ul/li[6]/span/text()")}, #ok 
            
                "defending": {'DefensiveAwareness':extract_with_xpath("//div[@class='block-quarter'][6]/div/ul/li/span/text()"),'StandingTackle':extract_with_xpath("//div[@class='block-quarter'][6]/div/ul/li[2]/span/text()"),'SlidingTackle':extract_with_xpath("//div[@class='block-quarter'][6]/div/ul/li[3]/span/text()")}, #ok
            
                "goalkeeping": {"GKDiving": extract_with_xpath("//div[@class='block-quarter'][7]/div/ul/li[1]/span/text()"), "GKHandling": extract_with_xpath("//div[@class='block-quarter'][7]/div/ul/li[2]/span/text()"), "GKKicking": extract_with_xpath("//div[@class='block-quarter'][7]/div/ul/li[3]/span/text()"), "GKPositioning":extract_with_xpath("//div[@class='block-quarter'][7]/div/ul/li[4]/span/text()") , "GKReflexes": extract_with_xpath("//div[@class='block-quarter'][7]/div/ul/li[5]/span/text()")}, #ok
            
                "player_traits":extract_with_xpath("//div[@class='block-quarter'][8]/div/ul/li/span/text()", extract_all=True), #ok
                "player_specialities": extract_with_xpath("//div[@class='block-quarter'][2]/div/ul/li/a/text()", extract_all=True) #ok
            }
        else:
            yield{
                "id":self.players[self.player_count-1]['player_url'][8:],
                "name": extract_with_xpath("//div[@class='info']/h1/text()"), #ok
                "primary_position": extract_with_xpath("//div[@class='meta ellipsis']/span[1]/text()"), #ok
                "positions":extract_with_xpath("//div[@class='meta ellipsis']/span/text()", extract_all=True), #ok
                "age": str1[:3],#ok
                "birth_date": birth_date,#ok
                "height": str1[23:26],#ok
                "weight": str1[29:31], #ok
            
                "Overall Rating": extract_with_xpath("//div[@class='block-quarter'][1]/div/span/text()"),#ok
                "Potential": extract_with_xpath("//div[@class='block-quarter'][2]/div/span/text()"), #ok
                "Value": extract_with_xpath("//div[@class='block-quarter'][3]/div/text()"),#ok
                "Wage": extract_with_xpath("//div[@class='block-quarter'][4]/div/text()"),#ok
            
                "Preferred Foot": extract_with_xpath("//div[@class='card'][1]/ul/li[1]/text()"),#ok
                "Weak Foot": extract_with_xpath("//div[@class='card'][1]/ul/li[2]/text()"),#ok
                "Skill Moves": extract_with_xpath("//div[@class='card'][1]/ul/li[3]/text()"),#ok
                "International Reputation": extract_with_xpath("//div[@class='card'][1]/ul/li[4]/text()"), #ok
                "Work Rate": extract_with_xpath("//div[@class='card'][1]/ul/li[5]/span/text()"), #ok
                "Body Type": extract_with_xpath("//div[@class='card'][1]/ul/li[6]/span/text()"), #ok
                "Real Face": extract_with_xpath("//div[@class='card'][1]/ul/li[7]/span/text()"), #ok
                "teams":teams, #ok
                "attacking": {"Crossing": extract_with_xpath("//div[@class='col col-12']/div[3]//ul/li[1]/span/text()"),"Finishing": extract_with_xpath("//div[@class='col col-12']/div[3]//ul/li[2]/span/text()"), "HeadingAccuracy": extract_with_xpath("//div[@class='col col-12']/div[3]//ul/li[3]/span/text()"), "ShortPassing":extract_with_xpath("//div[@class='col col-12']/div[3]//ul/li[4]/span/text()"), "Volleys": extract_with_xpath("//div[@class='col col-12']/div[3]//ul/li[5]/span/text()")}, #ok
            
                "skill":{"Dribbling":extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[4]//ul/li[1]/span[1]/text()"), "Curve": extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[4]//ul/li[2]/span[1]/text()"), "FKAccuracy":extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[4]//ul/li[3]/span[1]/text()"), "LongPassing": extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[4]//ul/li[4]/span[1]/text()") , "BallControl":extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[4]//ul/li[5]/span[1]/text()")}, #ok
            
                "movement":{"Acceleration": extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[5]//ul/li[1]/span[1]/text()"), "SprintSpeed":extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[5]//ul/li[2]/span[1]/text()"), "Agility": extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[5]//ul/li[3]/span[1]/text()"), "Reactions": extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[5]//ul/li[4]/span[1]/text()"), "Balance": extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[5]//ul/li[5]/span[1]/text()")}, #ok
            
                "power":{"ShotPower":extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[6]//ul/li[1]/span[1]/text()"), "Jumping": extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[6]//ul/li[2]/span[1]/text()"), "Stamina":extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[6]//ul/li[3]/span[1]/text()"), "Strength":extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[6]//ul/li[4]/span[1]/text()"), "LongShots":extract_with_xpath("//div[@class='center'][2]/div/div[2]/div[6]//ul/li[5]/span[1]/text()")}, #ok
            
                "mentality":{'Aggression':extract_with_xpath("//div[@class='block-quarter'][5]/div/ul/li/span/text()"),'Interceptions':extract_with_xpath("//div[@class='block-quarter'][5]/div/ul/li[2]/span/text()"),'Positioning':extract_with_xpath("//div[@class='block-quarter'][5]/div/ul/li[3]/span/text()"),'Vision':extract_with_xpath("//div[@class='block-quarter'][5]/div/ul/li[4]/span/text()"),'Penalties':extract_with_xpath("//div[@class='block-quarter'][5]/div/ul/li[5]/span/text()"),'Composure':extract_with_xpath("//div[@class='block-quarter'][5]/div/ul/li[6]/span/text()")}, #ok 
            
                "defending": {'DefensiveAwareness':extract_with_xpath("//div[@class='block-quarter'][6]/div/ul/li/span/text()"),'StandingTackle':extract_with_xpath("//div[@class='block-quarter'][6]/div/ul/li[2]/span/text()"),'SlidingTackle':extract_with_xpath("//div[@class='block-quarter'][6]/div/ul/li[3]/span/text()")}, #ok
            
                "goalkeeping": {"GKDiving": extract_with_xpath("//div[@class='block-quarter'][7]/div/ul/li[1]/span/text()"), "GKHandling": extract_with_xpath("//div[@class='block-quarter'][7]/div/ul/li[2]/span/text()"), "GKKicking": extract_with_xpath("//div[@class='block-quarter'][7]/div/ul/li[3]/span/text()"), "GKPositioning":extract_with_xpath("//div[@class='block-quarter'][7]/div/ul/li[4]/span/text()") , "GKReflexes": extract_with_xpath("//div[@class='block-quarter'][7]/div/ul/li[5]/span/text()")}, #ok
            
                "player_traits":extract_with_xpath("//div[@class='block-quarter'][8]/div/ul/li/span/text()", extract_all=True), #ok
                "player_specialities": extract_with_xpath("//div[@class='block-quarter'][2]/div/ul/li/a/text()", extract_all=True)
            }
        if self.player_count < len(self.players):
            next_page_url = 'https://sofifa.com' + self.players[self.player_count]['player_url'] + '?units=mks'
            self.player_count += 1
            yield scrapy.Request(url=next_page_url, callback=self.parse) 