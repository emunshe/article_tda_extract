from tdaExtract.dtExtractor import get_date
from tdaExtract.dtExtractor import get_title
from tdaExtract.dtExtractor import build_doc
from tdaExtract.auExtractor import get_author
from tdaExtract.cleaners import html_cleaner
import re
import time

reg_location = [r'\s', r'<head>.*?</head>', r'<script.*?</script>',
                r'<a[^>]*?href[^>]*?>.*?</a>', r'style=".*?"',
                r'<img.*?>', r'<!--[^>]*?-->']


class Document():
    def __init__(self, html, url=None, header_time=None):
        self.response_url = url
        self.htime = header_time
        self._parse(html)
        self._html()

    def together(self):
        """
        Also extract title, time, author information
        :return:dict
        """
        title_d = get_title(self.doc, self.decoded_page)
        date_d = get_date(self.clean_html, self.decoded_page, self.response_url, title=title_d['title'])
        author_d = get_author(self.decoded_page)
        return dict(dict(title_d, **date_d), **author_d)

    def date(self):
        return get_date(self.clean_html, self.decoded_page, self.response_url, self.doc, self.htime)

    def title(self):
        return get_title(self.doc, self.decoded_page)

    def author(self):
        return get_author(self.decoded_page)

    def _html(self,):
        """
        Clear html: space,head,img,script,a,style...
        """
        self.clean_html = self.decoded_page
        for reg in reg_location:
            pattern_location = re.compile(reg)
            self.clean_html = pattern_location.sub('', self.clean_html)

    def _parse(self, html):
        intact_doc, self.decoded_page, self.encoding = build_doc(html)
        self.doc = html_cleaner.clean_html(intact_doc)

