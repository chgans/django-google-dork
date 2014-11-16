#
# Heavily based on parsing.py from https://github.com/NikolaiT/GoogleScraper/
#

import sys, re, logging, random
import lxml.html, urllib
from collections import namedtuple
from cssselect import HTMLTranslator, SelectorError
from bs4 import UnicodeDammit

logger = logging.getLogger(__name__)

# Named tuple type for the search results
ParserResult = namedtuple('ParserResult', 'link_title link_snippet link_url link_position')

class Parser():
    """Parses data from Google SERP pages."""

    # short alias because we use it so extensively
    _xp = HTMLTranslator().css_to_xpath

    # Valid URL (taken from django)
    _REGEX_VALID_URL = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    _REGEX_VALID_URL_SIMPLE = re.compile(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    def __init__(self, html, searchtype='normal'):
        self.html = html
        self.searchtype = searchtype
        self.dom = None

        self.search_results = {'num_results_for_kw': ''}
        self.page_links = []

        # Try to parse the google HTML result using lxml
        try:
            doc = UnicodeDammit(self.html, is_html=True)
            parser = lxml.html.HTMLParser(encoding=doc.declared_html_encoding)
            self.dom = lxml.html.document_fromstring(self.html, parser=parser)
            self.dom.resolve_base_href()
        except Exception as e:
            print('Some error occurred while lxml tried to parse: {}'.format(e))

        # Very redundant by now, but might change in the soon future
        if self.searchtype == 'normal':
            self.search_results.update({
                'results': [],  # List of Result, list of named tuples
                'ads_main': [],  # The google ads in the main result set.
                'ads_aside': [],  # The google ads on the right aside.
            })
        elif self.searchtype == 'video':
            self.search_results.update({
                'results': [],  # Video search results
                'ads_main': [],  # The google ads in the main result set.
                'ads_aside': [],  # The google ads on the right aside.
            })
        elif self.searchtype == 'image':
            self.search_results.update({
                'results': [],  # Images links
            })
        elif self.searchtype == 'news':
            self.search_results.update({
                'results': [],  # Links from news search
                'ads_main': [],  # The google ads in the main result set.
                'ads_aside': [],  # The google ads on the right aside.
            })

        ### the actual PARSING happens here
        parsing_actions = {
            'normal': self._parse_normal_search,
            'image': self._parse_image_search,
            'video': self._parse_video_search,
            'news': self._parse_news_search,
        }
        # Call the correct parsing method
        parsing_actions.get(self.searchtype)(self.dom)

        # Clean the results
        self._clean_results()

    def __iter__(self):
        """Simple magic method to iterate quickly over found non ad results"""
        for link_title, link_snippet, link_url in self.result['results']:
            yield (link_title, link_snippet, link_url)

    def num_results(self):
        """Returns the number of pages found by keyword as shown in top of SERP page."""
        return self.search_results['num_results_for_kw']

    @property
    def results(self):
        """Returns all results including sidebar and main result advertisements"""
        return {k: v for k, v in self.search_results.items() if k not in
                                                                ('num_results_for_kw', )}

    @property
    def pages(self):
        """Returns all results including sidebar and main result advertisements"""
        return self.page_links

    @property
    def all_results(self):
        return self.search_results

    @property
    def links(self):
        """Only returns non ad results"""
        return self.search_results['results']

    def _clean_results(self):
        """Cleans/extracts the found href or data-href attributes."""

        # Now try to create ParseResult objects from the URL
        for key in ('results', 'ads_aside', 'ads_main'):
            for i, e in enumerate(self.search_results[key]):
                # First try to extract the url from the strange relative /url?sa= format
                matcher = re.search(r'/url\?q=(?P<url>.*?)&sa=U&ei=', e.link_url)
                if matcher:
                    url = matcher.group(1)
                else:
                    url = e.link_url

                self.search_results[key][i] = \
                    ParserResult(link_title=e.link_title, link_url=urllib.parse.urlparse(url),
                                 link_snippet=e.link_snippet, link_position=e.link_position)

    def _parse_num_results(self):
        # try to get the number of results for our search query
        try:
            self.search_results['num_results_for_kw'] = \
                self.dom.xpath(self._xp('div#resultStats'))[0].text_content()
        except Exception as e:
            logger.debug('Cannot parse number of results for keyword from SERP page: {}'.format(e))

    def _parse_normal_search(self, dom):
        """Specifies the CSS selectors to extract links/snippets for a normal search.

        @param dom The page source to parse.
        """

        # There might be several list of different css selectors to handle different SERP formats
        css_selectors = {
            # to extract all links of non-ad results, including their snippets(descriptions) and titles.
            'results': (['li.g', 'h3.r > a:first-child', 'div.s span.st'], ),
            # to parse the centered ads
            'ads_main': (['div#center_col li.ads-ad', 'h3.r > a', 'div.ads-creative'],
                         ['div#tads li', 'h3 > a:first-child', 'span:last-child']),
            # the ads on on the right
            'ads_aside': (['#rhs_block li.ads-ad', 'h3.r > a', 'div.ads-creative'], ),
        }
        self._parse(dom, css_selectors)

    def _parse_image_search(self, dom):
        """Specifies the CSS selectors to extract links/snippets for a image search."""
        css_selectors = {
            'results': (['div.rg_di', 'a:first-child', 'span.rg_ilmn'], )
        }
        self._parse(dom, css_selectors)

    def _parse_video_search(self, dom):
        """Specifies the CSS selectors to extract links/snippets for a video search.

        Very similar to a normal search. Basically the same. But this is a unique method
        because the parsing logic may change over time.
        """
        css_selectors = {
            # to extract all links of non-ad results, including their snippets(descriptions) and titles.
            'results': (['li.g', 'h3.r > a:first-child', 'div.s > span.st'], ),
            # to parse the centered ads
            'ads_main': (['div#center_col li.ads-ad', 'h3.r > a', 'div.ads-creative'],
                         ['div#tads li', 'h3 > a:first-child', 'span:last-child']),
            # the ads on on the right
            'ads_aside': (['#rhs_block li.ads-ad', 'h3.r > a', 'div.ads-creative'], ),
        }
        self._parse(dom, css_selectors)

    def _parse_news_search(self, dom):
        """Specifies the CSS selectors to extract links/snippets for a news search.

        Is also similar to a normal search. But must be a separate function since
        https://news.google.com/nwshp? needs own parsing code...
        """
        css_selectors = {
            # to extract all links of non-ad results, including their snippets(descriptions) and titles.
            # The first CSS selector is the wrapper element where the search results are situated
            # the second CSS selector selects the link and the title. If there are 4 elements in the list, then
            # the second and the third element are for the link and the title.
            # the 4th selector is for the snippet.
            'results': (['li.g', 'h3.r > a:first-child', 'div.s span.st'], ),
            # to parse the centered ads
            'ads_main': (['div#center_col li.ads-ad', 'h3.r > a', 'div.ads-creative'],
                         ['div#tads li', 'h3 > a:first-child', 'span:last-child']),
            # the ads on on the right
            'ads_aside': (['#rhs_block li.ads-ad', 'h3.r > a', 'div.ads-creative'], ),
        }
        self._parse(dom, css_selectors)

    def _parse(self, dom, css_selectors):
        """Generic parse method"""
        for key, slist in css_selectors.items():
            for selectors in slist:
                self.search_results[key].extend(self._parse_links(dom, *selectors))
        self._parse_num_results()
        self._parse_page_links(dom, 'table#nav a.fl')

    def _parse_page_links(self, dom, selector):
        a_fl_results = dom.xpath(self._xp(selector))
        for i, e in enumerate(a_fl_results):
            link = e.get('href')
            title = e.text_content()
            self.page_links += [(link, title)]

    def _parse_links(self, dom, container_selector, link_selector, snippet_selector):
        links = []
        # Try to extract all links of non-ad results, including their snippets(descriptions) and titles.
        # The parsing should be as robust as possible. Sometimes we can't extract all data, but as much as humanly
        # possible.
        rank = 0
        try:
            li_g_results = dom.xpath(self._xp(container_selector))
            for i, e in enumerate(li_g_results):
                snippet = link = title = ''
                try:
                    link_element = e.xpath(self._xp(link_selector))
                    link = link_element[0].get('href')
                    title = link_element[0].text_content()
                    # For every result where we can parse the link and title, increase the rank
                    rank += 1
                except IndexError as err:
                    logger.debug(
                        'Error while parsing link/title element with selector={}: {}'.format(link_selector, err))
                try:
                    for r in e.xpath(self._xp(snippet_selector)):
                        snippet += r.text_content()
                except Exception as err:
                    logger.debug('Error in parsing snippet with selector={}.Error: {}'.format(
                                            snippet_selector, repr(e), err))            

                links.append(ParserResult(link_title=title, link_url=link, link_snippet=snippet, link_position=rank))

        # Catch further errors besides parsing errors that take shape as IndexErrors
        except Exception as err:
            logger.error('Error in parsing result links with selector={}: {}'.format(container_selector, err))
        return links or []
