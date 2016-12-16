# -*- coding: gb2312 -*-

'''
Created on 2016-12-15

@author: Sawatari
'''

import string
import sys
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from FindGoods.items import FindgoodsItem

class FindGoods(Spider):
    name = "FindGoods"
    download_delay = 4
    allowed_domains = ["tmall.com"]
    start_urls = [
        "https://www.tmall.com/"
    ]

    def parse(self, response):
        # 反复确认是否搜索成功
        if response.url == "https://www.tmall.com/":
            # 读取临时文件
            temp = open('tempgoods.temp', 'r')
            good = temp.read()
            temp.close()
            # 天猫搜索该商品第一页
            url = "https://list.tmall.com/search_product.htm?q=" + good + "&type=p&vmarket=&spm=875.7931836%2FA.a2227oh.d100&from=mallfp..pc_1_searchbutton"
            # 递归
            yield Request(url, callback=self.parse)

        else:
            # 搜索成功
            item = FindgoodsItem()
            sel = Selector(response)
            gifts = sel.xpath('//*[@id="J_ItemList"]/div[@class="product  "]')
            for gift in gifts:
                name = gift.xpath('div/p[@class="productTitle"]/a/@title').extract()
                # 天猫电器城HTML结构不同
                if not name:
                    name = gift.xpath('div/div[@class="productTitle productTitle-spu"]/a[1]/text()').extract()

                shop = gift.xpath('div/div[@class="productShop"]/a[@class="productShop-name"]/text()').extract()
                price = gift.xpath('div/p[@class="productPrice"]/em/@title').extract()
                trading = gift.xpath('div/p[@class="productStatus"]/span[1]/em/text()').extract()
                review = gift.xpath('div/p[@class="productStatus"]/span[2]/a/text()').extract()
                url = gift.xpath('div/p[@class="productTitle"]/a/@href').extract()
                if not url:
                    url = gift.xpath('div/div[@class="productTitle productTitle-spu"]/a[1]/@href').extract()

                # sys.getfilesystemencoding()获得本地编码（mbcs编码）
                item['name'] = [na.encode(sys.getfilesystemencoding()) for na in name]

                # 去掉商店名末尾的\n换行符（有两个\n）
                tempshop = str(shop[0].encode(sys.getfilesystemencoding()))
                item['shop'] = tempshop.strip('\n')

                item['price'] = price
                item['url'] = 'https:' + url[0]

                # 天猫电器城少数商品无交易量信息
                tradnum = 0
                if trading:
                    # 在搜索页无法获取交易量详细数字，需转化
                    tradstr = str(trading[0].encode(sys.getfilesystemencoding()))
                    item['trading'] = tradstr
                    # “笔”字在字符串中的下标
                    biindex = tradstr.index('\xb1\xca')
                    # 除去“笔”
                    tradstr = tradstr[:biindex]
                    # 判断是否有“万”字
                    if '\xcd\xf2' in tradstr:
                        # “万”字在字符串中的下标
                        wanindex = tradstr.index('\xcd\xf2')
                        # 除去“万”字
                        tradstr = tradstr[:wanindex]
                        tradnum = tradnum + string.atof(tradstr) * 10000
                    else:
                        # 没有“万”字
                        tradnum = tradnum + string.atof(tradstr)

                # 天猫电器城无评论数信息
                revinum = 0
                if review:
                    # 在搜索页无法获取评论数详细数字，需转化
                    revistr = str(review[0].encode(sys.getfilesystemencoding()))
                    item['review'] = revistr
                    # 判断是否有“万”字
                    if '\xcd\xf2' in revistr:
                        # “万”字在字符串中的下标
                        wanindex2 = revistr.index('\xcd\xf2')
                        # 除去“万”字
                        revistr = revistr[:wanindex2]
                        revinum = revinum + string.atof(revistr) * 10000
                    else:
                        # 没有“万”字
                        revinum = revinum + string.atof(revistr)

                # 计算评分
                score = revinum + (tradnum * 2)
                item['score'] = round(score)
                yield(item)
            # 提取商品名
            good = response.url[(response.url.index("q=") + 2):response.url.index("&type=p&v")]
            next_page_urls = [
                "https://list.tmall.com/search_product.htm?spm=a220m.1000858.0.0.0HVJLN&s=60&q=" + good + "&sort=s&style=g&from=mallfp..pc_1_searchbutton&type=pc#J_Filter",
                "https://list.tmall.com/search_product.htm?spm=a220m.1000858.0.0.Zt2HlG&s=120&q=" + good + "&sort=s&style=g&from=mallfp..pc_1_searchbutton&type=pc#J_Filter"
            ]
            # 递归获取后两页
            for next_page_url in next_page_urls:
                yield Request(next_page_url, callback=self.parse)