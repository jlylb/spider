# -*- coding: utf-8 -*-
"""
#from gbook.items import GbookItem

  Last Modified: 2016/1/14 9:58:52
  Last Modified: 2016/1/14 10:29:16
  Last Modified: 2016/1/14 9:58:28









"""
import scrapy
import codecs
class GuichuidengSpider(scrapy.Spider):
    name = "guichuideng"
    allowed_domains = ["guichuideng.org"]
    start_urls = (
        'http://www.guichuideng.org/',
    )
    html = """
    <html>
        <head>
            <title>
                {title}
            </title>
            <meta charset="UTF-8">
            <script src="static/jquery-1.11.1.js"></script>
            <script src="static/bootstrap.min.js"></script>
            <link rel="stylesheet" href="static/bootstrap.min.css">
            <link type="image/x-icon" href="/pig.ico" rel="shortcut icon">
        </head>
        <body>
            {content}
        </body>
    </html>
    """
    def parse(self, response):
        data=[]
        part = response.css('h2+ul')
        title = response.css('h2::text').extract()
        for k,sel in enumerate(part):
            subdata = [(xx.xpath("@href").extract()[0],xx.xpath("text()").extract()[0]) for xx in sel.css("li>a")]
            subdata.insert(0,title[k])
            data.append(subdata)
        html=''
        for book in data:
            html+=self.result_table(book)
        self.add_book("index.html",html,'list')
            #with codecs.open('gcd1.html','wb',encoding="utf-8") as f:
            #    json.dump(data,f,ensure_ascii=False,indent=2)

    def add_book(self,fname,content,title):
        data=self.html.replace('{title}',title)
        data=data.replace('{content}',content)
        with codecs.open(fname,"wb",encoding="utf-8") as f:
            f.write(data)
    def format_a(self,attr):
        a_str = "<a href='"+attr[0]+"'>"+attr[1]+"</a>"
        return a_str
    def result_table(self,args):
        s_title = args.pop(0)
        title ="<h2 class='text-center'>"+s_title+"</h2>"
        t_header = "<div class='container'>"+title+"<table class='table table-hover'>"
        td = ""
        tr ="<tr>"
        arg_len =len(args)
        for k,x in enumerate(args):
            td = "<td>"+self.format_a(x)+"</td>"
            tr+=td
            if (k+1) % 3 == 0:
                tr+='</tr>'
                if  arg_len  != k+1:
                    tr+='<tr>'
        if  arg_len % 3 != 0:
            tr+='</tr>'
        return t_header+tr+"</table></div>"

