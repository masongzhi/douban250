import scrapy
import requests
from douban250.items import Douban250Item


class Douban250Spider(scrapy.Spider):
    name = "douban250"
    allowed_domains = ["douban.com"]

    # 先通过requests拿到评分前250电影的链接
    def get_douban_250_results(self):
        url = "https://movie.douban.com/j/search_subjects"
        payload = {'type': 'movie', 'tag': '豆瓣高分', 'sort': 'rank', 'page_limit': 250, 'page_start': 0}
        r = requests.get(url, params=payload)
        return r.json()

    def start_requests(self):
        results = self.get_douban_250_results()

        for subject in results['subjects']:
            yield scrapy.Request(url=subject['url'], callback=self.parse)

    def parse(self, response):
        item = Douban250Item()
        item['movie_name'] = response.css('#content > h1 > span:nth-child(1)::text').extract_first()
        item['movie_year'] = response.css('#content > h1 > span.year::text').extract_first()
        item['movie_rate_num'] = response.css('#content .rating_num::text').extract_first()
        item['comment'] = self.parse_comment(response)
        yield item

    def parse_comment(self, response):
        result = []
        for comment in response.css('.comment-item'):
            data = {
                'author': comment.css('.comment-info > a::text').extract_first(),
                'author_url': comment.css('.comment-info > a::attr(href)').extract_first(),
                'rating': comment.css('.comment-info .rating::attr(title)').extract_first(),
                'time': comment.css('.comment-info .comment-time::attr(title)').extract_first(),
                'content': comment.css('.short::text').extract_first()
            }
            result.append(data)
        return result


