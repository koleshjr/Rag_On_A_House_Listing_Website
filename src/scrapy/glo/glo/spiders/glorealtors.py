import scrapy
from glo.glo.items import GloParentItem, GloChildItem
from scrapy.loader import ItemLoader



class GlorealtorsSpider(scrapy.Spider):
    name = "glorealtors"
    allowed_domains = ["glorealtors.com"]
    start_urls = ["https://glorealtors.com/search-results/?status%5B0%5D&areas%5B0%5D&keyword"]
    page_number = 1  # Initialize the page number

    def parse(self, response):
        for house in response.css('div.item-listing-wrap'):
            parent_item = ItemLoader(item=GloParentItem(), selector=house)
            
            parent_item.add_css("house_href", "div.item-body h2 > a::attr(href)")
            parent_item.add_css("house_price", "div.item-body ul li.item-price::text")
            parent_item.add_css("bed_rooms", "ul.item-amenities li.h-beds > span.hz-figure::text")
            parent_item.add_css("furnished", "div.item-body h2 > a::attr(href)")
            
            # Extract the child page URL
            child_page_url = house.css('div.item-body h2 > a::attr(href)').extract_first()
            if child_page_url:
                yield scrapy.Request(url=child_page_url, callback=self.parse_child_page, meta={'parent_item': parent_item.load_item()})

        # Check for the "Next" button
        next_page = response.css('ul.pagination li.page-item.active + li.page-item a.page-link::attr(href)').extract_first()
        if next_page:
            self.page_number += 1
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_child_page(self, response):
        parent_item = response.meta['parent_item']
        child_item = ItemLoader(item=GloChildItem(), response=response)
        
        # Use your actual CSS selectors for "house_location," "service_type," and "property_type"
        child_item.add_css("house_location", "li.detail-area > span::text")
        child_item.add_css("service_type", "li.prop_status > span::text")
        child_item.add_css("property_type", "li.prop_type > span::text")
        
        # Merge parent and child items into one
        merged_item = {**parent_item, **child_item.load_item()}
        yield merged_item

