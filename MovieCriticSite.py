from lxml import html
import requests

class MovieCriticSite:
	def __init__(self, name):
		self.name = name
		self.critics = {}
		self.audiences = {}
		self.search = {}

	def setCritics(self, link, xpath):
		self.critics['link'] = link
		self.critics['xpath'] = xpath

	def setAudiences(self, link, xpath):
		self.audiences['link'] = link
		self.audiences['xpath'] = xpath

	def setSearch(self, link, xpath):
		self.search['link'] = link
		self.search['xpath'] = xpath

	def getReview(self, film, page_num, utype):
		if ( hasattr(self, utype) ):
			if ( utype == 'critics' ):
				data = self.critics
			else:
				data = self.audiences

			film = self.getFilmID(film)
			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
			page = requests.get(data['link'].replace("$page$", str(page_num)).replace("$film$", film), headers=headers)
			tree = html.fromstring((page.content).decode('cp1252').encode('utf-8'))

			reviews = tree.xpath(data['xpath'])
			reviews = list(map(str.rstrip, reviews))
			reviews = list(filter(None, reviews))
			return reviews

	def getFilmID(self, film):
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
		page = requests.get(self.search['link'].replace("$film$", film), headers=headers)
		tree = html.fromstring(page.content)

		filmID = tree.xpath(self.search['xpath'])
		return filmID

