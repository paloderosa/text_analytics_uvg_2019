import scrapy
from scrapy.loader import ItemLoader
from hotel_sentiment.items import BookingReviewItem

#crawl up to 6 pages of review per hotel
max_pages_per_hotel = 100

class BookingSpider(scrapy.Spider):
    name = "booking"
    start_urls = [
        "https://www.booking.com/searchresults.en-us.html?label=gen173nr-1DCAEoggI46AdIM1gEaF6IAQGYATG4AQfIAQzYAQPoAQH4AQKIAgGoAgO4AvzOk-cFwAIB&sid=c6849bc753756b94c36fcc2129eb73a4&sb=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.html%3Flabel%3Dgen173nr-1DCAEoggI46AdIM1gEaF6IAQGYATG4AQfIAQzYAQPoAQH4AQKIAgGoAgO4AvzOk-cFwAIB%3Bsid%3Dc6849bc753756b94c36fcc2129eb73a4%3Bsb_price_type%3Dtotal%26%3B&ss=Antigua+Guatemala&is_ski_area=0&ssne=Antigua+Guatemala&ssne_untouched=Antigua+Guatemala&dest_id=-1131627&dest_type=city&checkin_year=2019&checkin_month=5&checkin_monthday=27&checkout_year=2019&checkout_month=5&checkout_monthday=31&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1"
        # "https://www.booking.com/searchresults.html?aid=356980&label=gog235jc-1BCAMoXkIJZ3VhdGVtYWxhSDNYA2heiAEBmAEJuAEHyAEN2AEB6AEBiAIBqAIDuAKFtJjnBcACAQ&sid=45b1e237a6ab60fb706edf93f12765d1&dest_id=-1133206&dest_type=city"
        # "http://www.booking.com/searchresults.html?aid=357026&label=gog235jc-city-XX-us-newNyork-unspec-uy-com-L%3Axu-O%3AosSx-B%3Achrome-N%3Ayes-S%3Abo-U%3Ac&sid=b9f9f1f142a364f6c36f275cfe47ee55&dcid=4&city=20088325&class_interval=1&dtdisc=0&from_popular_filter=1&hlrd=0&hyb_red=0&inac=0&label_click=undef&nflt=di%3D929%3Bdistrict%3D929%3B&nha_red=0&postcard=0&redirected_from_city=0&redirected_from_landmark=0&redirected_from_region=0&review_score_group=empty&room1=A%2CA&sb_price_type=total&score_min=0&ss_all=0&ssb=empty&sshis=0&rows=15",
        #add your city url here
    ]

    pageNumber = 1

    # for every hotel
    def parse(self, response):
        for hotelurl in response.css('a.hotel_name_link.url::attr(href)'):
            url = response.urljoin(hotelurl.extract()[1:])
            yield scrapy.Request(url, callback=self.parse_hotel)

        next_page = response.css('a.paging-next::attr(href)')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)

    # get its reviews page
    def parse_hotel(self, response):
        reviewsurl = response.css('a.show_all_reviews_btn::attr(href)')
        try:
            url = response.urljoin(reviewsurl[0].extract())
            self.pageNumber = 1
            return scrapy.Request(url, callback=self.parse_reviews)
        except IndexError:
            pass

    # and parse the reviews
    def parse_reviews(self, response):
        if self.pageNumber > max_pages_per_hotel:
            return
        for rev in response.css('li.review_item'):
            item = BookingReviewItem()
            #sometimes the title is empty because of some reason, not sure when it happens but this works
            title = rev.css("div.review_item_header_content span[itemprop='name']::text")
            if title:
                item['title'] = title[0].extract()
                positive_content = rev.css("p.review_pos span::text")
                if positive_content:
                    item['positive_content'] = positive_content[0].extract()
                negative_content = rev.css("p.review_neg span::text")
                if negative_content:
                    item['negative_content'] = negative_content[0].extract()
                item['score'] = rev.xpath('.//span[@itemprop="reviewRating"]/meta[@itemprop="ratingValue"]/@content')[0].extract()
                # tags are separated by ;
                item['tags'] = [tag.strip() for tag in rev.css('li.review_info_tag::text').extract() if len(tag.strip())>0]
                yield item

        next_page = response.css('a.review_next_page_link::attr(href)')
        if next_page:
            self.pageNumber += 1
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse_reviews)
