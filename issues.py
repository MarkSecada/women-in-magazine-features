from bs4 import BeautifulSoup
import requests

class Issue(object):
    def __init__(self, html, url, date):
        self.soup = BeautifulSoup(html, features='html.parser')
        self.url = url
        self.date = date

class NYMagIssue(Issue):

    @property
    def cover_author(self):
        try:
            return self.soup.find('span',
                class_='magazine-toc-cover-author').text
        except AttributeError:  
            article = self.soup.find('div',
                class_='magazine-toc-cover-text').a['href']
            return self._get_author_from_article(article)

    @property
    def feature_authors(self):
        authors = []
        features = self._find_features()
        for feature in features:
            try:
                authors.append(feature.find('a', 
                    class_='author-link').span.text)
            except AttributeError:
                article = feature.find('a', 
                    class_='article-link')['href']
                author = self._get_author_from_article(article)
                authors.append(author)
        return authors

    def _find_features(self):
        features = self.soup.find_all('li', 
            class_='magazine-features-article')
        return features

    def _get_author_from_article(self, article):
        r = requests.get(article)
        soup = BeautifulSoup(r.text, features='html.parser')
        try:
            return soup.find('a', class_='article-author').span.text
        except:
            return None

class AtlanticIssue(Issue):

    @property
    def cover_authors(self):
        authors = []
        cover_section = self.soup.find('ul', id='section-Cover Story')
        if cover_section:
            byline = cover_section.find('li', class_='byline')
            links = byline.find_all('a')
            for link in links:
                authors.append(link['title'])
        return authors

    @property
    def feature_authors(self):
        authors = []
        features = self.soup.find('ul', id='section-Features')
        articles = features.find_all('li', class_='article')
        for article in articles:
            byline = article.find('li', class_='byline')
            links = byline.find_all('a')
            for link in links:
                authors.append(link['title'])
        return authors

class NYTMagIssue(Issue):

    @property
    def feature_authors(self):
        authors = []
        features = self.soup.find('div', 
            class_='rank-template featured-rank-template template-1')
        if features:
            articles = features.find_all('li')
            for article in articles:
                byline = article.find('span', class_='author').text
                try:
                    if byline != '' and 'and' not in byline:
                        authors.append(byline.split('By ')[1])
                    elif byline != '' and 'and' in byline:
                        article_authors = byline.split('By ')[1:][0].split(' and ')
                        for author in article_authors:
                            authors.append(author)
                    else:
                        authors.append(byline)
                except:
                    authors.append(byline)
        return authors

class HarpersIssue(Issue):
    pass

class VanityFairIssue(Issue):
    pass