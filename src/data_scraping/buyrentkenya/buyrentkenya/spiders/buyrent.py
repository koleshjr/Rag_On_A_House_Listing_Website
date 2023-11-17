import os
import sys

# Get the parent directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')

# Add the parent directory to sys.path
sys.path.append(parent_dir)


import scrapy
from items import BrParentItem, BrChildItem
from scrapy.loader import ItemLoader
from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess



class BuyrentSpider(scrapy.Spider):
    name = "buyrent"
    allowed_domains = ["buyrentkenya.com"]
    start_urls = ["https://www.buyrentkenya.com/estate-agent/glo-realtors"]
    page_number = 1
    max_pages = 15

    def parse(self, response):
        # follow links to property pages
        for house in response.css('div.listing-card'):
            parent_item = ItemLoader(item=BrParentItem(), selector=house)

        #get the css selector of href and join it with www.buyrentkenya.com
            house_href = house.css('div.block h3> a::attr(href)').extract_first()
            house_href = response.urljoin(house_href)
            parent_item.add_value('house_href', house_href)
            parent_item.add_css('house_price', 'div.hidden p a::text')
            parent_item.add_css('house_location', 'div.flex p::text')
            parent_item.add_css('furnished', 'div.block h3> a::attr(href)')
            


            child_page_url = house_href
            if child_page_url:
                yield response.follow(child_page_url, callback=self.parse_child_page, meta={'parent_item': parent_item})

        next_page = response.css('a.justify-center:nth-child(3)::attr(href)').extract_first()
        if next_page:
            if self.page_number <= self.max_pages:
                self.page_number += 1
                yield scrapy.Request(url = next_page, callback=self.parse)

    def parse_child_page(self, response):
        parent_item = response.meta['parent_item']
        child_item = ItemLoader(item=BrChildItem(), response=response)

        child_item.add_css('service_type', 'a.text-grey-550:nth-child(1)')
        child_item.add_css('property_type', 'li.items-center:nth-child(3) > a:nth-child(2)')

        texts = response.css('span[aria-label="bedrooms"]::text').extract()
        num_beds = ''.join([text.strip() for text in texts if text.strip()])
        child_item.add_value('bed_rooms', num_beds)
        
        
        merged_item = {**parent_item.load_item(), **child_item.load_item()}
        yield merged_item            


def main():

    home_path = os.path.expanduser("~")
    output_file_path = f"{home_path}/Desktop/personal_projects/Rag_On_A_House_Listing_Website/src/data/buyrent.csv"

    # Set up Scrapy settings
    settings = Settings()
    settings.set('FEEDS', {output_file_path: {'format': 'csv'}})

    # Create a CrawlerProcess with project settings
    process = CrawlerProcess(settings)

    # Run the spider
    process.crawl(BuyrentSpider)
    process.start()       


if __name__ == "__main__":
    main() 
