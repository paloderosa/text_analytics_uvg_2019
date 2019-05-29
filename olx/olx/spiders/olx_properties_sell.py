import scrapy


class OlxPropertiesSell(scrapy.Spider):
    name = 'olx_properties_sell'
    start_urls = [
        'https://ciudaddeguatemala.olx.com.gt/piso-casa-en-venta-cat-367'
    ]

    def parse(self, response):
        properties_list = response.css('li.item')
        for prop in properties_list:
            description = prop.css('div.items-info a::text').get()
            price = prop.css('p.items-price a::text')[0].get().strip()
            optionals = {
                optional.xpath('@class')[0].extract().split(' ')[1]: optional.css('::text').get()
                for optional in prop.css('span.optional')
            }
            yield {
                'description': description,
                'price': price,
                'specs': optionals
            }

        next_page = response.css('a.pagination-button.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


# scrapy crawl olx_properties_sell -o olx_props.jl