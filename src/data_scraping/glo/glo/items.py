import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags

def remove_currency(value):
    #     KES28,000,000
    for char in ['KES', 'KSH', 'ksh', 'kes', 'Ksh','/Sqft']:
      value = value.replace(char, '')

    return value

def furnished_or_not(value):
    value = value.lower()
    #if value contains furnished return True else False
    if 'furnished' in value:
        return True
    else:
        return False

def remove_commas(value):
    value = remove_currency(value)
    return value.replace(',', '')

def try_float(value):
    try:
        return float(value)
    except ValueError:
        return value
    
class GloParentItem(scrapy.Item):
    house_href = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    
    house_price = scrapy.Field(
        input_processor=MapCompose(remove_tags,remove_commas, try_float),
        output_processor=TakeFirst()
    )

    bed_rooms = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, int),
        output_processor=TakeFirst()
    )

    furnished = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, furnished_or_not),
        output_processor=TakeFirst()
    )


class GloChildItem(scrapy.Item):
    house_location = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )

    service_type = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )

    property_type = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )

