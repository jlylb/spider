# -*- coding: utf-8 -*-
"""
#from gbook.items import GbookItem

  Last Modified: 2016/1/14 9:58:52
  Last Modified: 2016/1/14 16:49:03
  Last Modified: 2016/1/14 9:58:28









"""
import scrapy
import codecs
import os
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
            <script src="{root_path}/static/jquery-1.11.1.js"></script>
            <script src="{root_path}/static/bootstrap.min.js"></script>
            <link rel="stylesheet" href="{root_path}/static/bootstrap.min.css">
            <link type="image/x-icon" href="/pig.ico" rel="shortcut icon">
        </head>
        <body>
            {content}
        </body>
    </html>
    """
    def __init__(self, category=None, *args, **kwargs):
        super(GuichuidengSpider, self).__init__(*args, **kwargs)
        self.category=category

    def parse(self, response):
        data=[]
        part = response.css('h2+ul')
        title = response.css('h2::text').extract()
        #self.logger.info(title)
        for k,sel in enumerate(part):
            subdata=[]
            for xx in sel.css("li>a"):
                href = xx.xpath("@href").extract()[0]
                yield scrapy.Request(href, callback=self.parse_details)
                subdata.append((os.path.join(self.category,href.rsplit('/',1)[-1]),xx.xpath("text()").extract()[0]))
            subdata.insert(0,title[k])
            data.append(subdata)
        html=''
        for book in data:
            html+=self.result_table(book)
        self.add_book("index.html",html,'list')

    def add_book(self,fname,content,title,fdir=None):
        data=self.html.replace('{title}',title)
        data=data.replace('{content}',content)
        if fdir is None:
            root_path='.'
            fpath=fname
        else:
            root_path='..'
            fdir=self.category
            if not os.path.exists(fdir):
                os.mkdir(fdir)
            fpath=os.path.join(fdir,fname)
        data=data.replace('{root_path}',root_path)
        with codecs.open(fpath,"wb",encoding="utf-8") as f:
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

    def parse_details(self,response):
        fname=response.url.rsplit('/',1)[-1]
        if os.path.exists(os.path.join(self.category,fname)):
            return
        title=response.css('h1[class*="entry-title"]>span::text').extract()[0]
        content="\n".join(response.css('div[class*="entry-content"]>p:not([style])').extract())
        content= "<div class='container'><h1 class='text-center'>"+title+"</h1>"+content+"</div>"
        self.add_book(fname,content,title,'guichuideng')
