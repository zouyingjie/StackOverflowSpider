# -*- coding: utf-8 -*-
import scrapy

from StackOverflowScraper.mongo_save import mongoPipeline


class StackOverflowSpider(scrapy.Spider):
    name = "stack_overflow"
    stack_overflow_url = "http://stackoverflow.com"

    def start_requests(self):
        mongoPipeline.open_spider(self)
        tag = getattr(self, "tag", None)
        if tag is not None:
            url = "http://stackoverflow.com/questions/tagged/" + tag + "?page=1&sort=votes&pagesize=50"
            yield scrapy.Request(url=url)
        else:
            print("please input tag")

    def parse(self, response):
        questions = response.css('div.question-summary')
        for question in questions:
            question_votes = question.css('strong::text').extract_first()
            queston_title = question.css("a.question-hyperlink::text").extract_first()
            question_link = StackOverflowSpider.stack_overflow_url + question.css(
                "a.question-hyperlink::attr(href)").extract_first()

            item = {'title': queston_title, 'votes': question_votes, 'url': question_link}
            mongoPipeline.process_item(item, self)
        next_page_url  = StackOverflowSpider.stack_overflow_url + response.css('div.pager a::attr(href)').extract()[-1]
        yield scrapy.Request(next_page_url)


'''
Stackoverflow 爬虫开发流程简记:
1.MongoDB存储
2.标签传入组件base_url
3.爬取base_url分析元素, 存储数据
4.解析next link, 解析下一页
'''
