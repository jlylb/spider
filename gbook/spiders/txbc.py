# -*- coding: utf-8 -*-
import scrapy
import codecs
import os


class TxbcSpider(scrapy.Spider):
    name = "txbc"
    allowed_domains = ["d8qu.com"]
    start_urls = (
        'http://www.d8qu.com/html/118/118011/index.html',
    )
    title="摸金校尉之九幽将军".decode("utf-8")
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

    def parse(self, response):
        data=[]
        part = response.css('.article li a')
        for x in part:
            href = x.xpath("@href").extract()[0]
            if href:
                url = "/".join([os.path.split(self.start_urls[0])[0],href])
                yield scrapy.Request(url, callback=self.parse_details)
            data.append([x.xpath("text()").extract()[0],href])

        html=self.result_table(data)
        home_title=self.title
        self.add_book("index5.html",html,home_title,self.name)

    def add_book(self,fname,content,title,fdir=None):
        data=self.html.replace('{title}',title)
        data=data.replace('{content}',content)
        if fdir is None:
            root_path='.'
            fpath=fname
        else:
            root_path='..'
            if not os.path.exists(fdir):
                os.mkdir(fdir)
            fpath=os.path.join(fdir,fname)
        data=data.replace('{root_path}',root_path)
        with codecs.open(fpath,"wb",encoding="utf-8") as f:
            f.write(data)

    def format_a(self,attr):
        a_str = "<a href='"+attr[1]+"'>"+attr[0]+"</a>"
        return a_str

    def result_table(self,args):

        arg_len =len(args)
        title ="<h2 class='text-center'>"+self.title+"</h2>"
        t_header = "<div class='container'>"+title+"<table class='table table-hover'>"
        td = ""
        tr ="<tr>"
        for k,x in enumerate(args):
            print x
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
        if os.path.exists(os.path.join(self.name,fname)):
            return
        title=response.css('#cont>h1::text').extract()[0]
        content="<br>".join(response.css('#clickeye_content::text').extract())
        content= "<div class='container'><h1 class='text-center'>"+title+"</h1>"+content+"</div>"
        self.add_book(fname,content,title,self.name)

        yield {'title':title}
