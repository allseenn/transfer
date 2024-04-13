# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Compose

def input_process_header(header):
    header = header.replace("\xa0", "").replace("\n", " ").replace("\t", " ")\
            .replace("  ", " ").strip()
    return header

def output_process_header(header):
    header = " ".join(header)
    return header.replace("  ", " ").strip()

def input_process_text(text):
    text = text.replace("\xa0", "").replace("\n", " ").replace("\t", " ")\
            .replace("  ", " ").strip()
    return text

def output_process_text(text):
    text = " ".join(text)
    return text.replace("  ", " ").strip()


def output_process_verdict(verdict):
    if verdict[0] == "рекомендует":
        verdict = 1
    else:
        verdict = 0

    return verdict


class YellItem(scrapy.Item):
    link = scrapy.Field()
    header = scrapy.Field(input_processor=MapCompose(input_process_header), output_processor=Compose(output_process_header))
    text = scrapy.Field(input_processor=MapCompose(input_process_text), output_processor=Compose(output_process_text))
    verdict = scrapy.Field(output_processor=Compose(output_process_verdict))

