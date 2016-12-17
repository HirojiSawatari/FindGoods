FindGoods
=========
This is a web crawler which can get most popular goods in Tmall. This web crawler based on Scrapy. 

<img src='mdimage/image01.png' height='300px'/>

Users can input key words of goods, and after several minutes later a CSV file named "goods.csv" can be generated in the root of this project. In this file, users can get about 170 informations of related goods, they come from the first five pages of Tmall. And they can be sorted based on their scores (sales * 2 + comments).

<img src='mdimage/image03.png' height='300px'/>

Of course, this table also be shown in TreeView of the form. The goods are arranged in descending order of scores. When users click any of the items, browser will automatically start and open the purchase page.

<img src='mdimage/image02.png' height='300px'/>

