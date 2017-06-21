# Web Scraping with Python

## 第一章：背景调查
 1. [The Web Robots Pages](http://www.robotstxt.org)
 2. [Sitemap Protocol](https://www.sitemaps.org/protocol.html)
 3. 识别网站所用的技术
  - `pip install builtwith`
  - `builtwith.parse('http://new.packhub.com.au')`
 4. 寻找网站所有者
  - `pip install python-whois`
  - `print whois.whois('packhub.com.au')`
