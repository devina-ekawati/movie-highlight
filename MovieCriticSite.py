from lxml import html
import requests

class MovieCriticSite:
	def __init__(self, name):
		self.name = name
		self.critics = {}
		self.audiences = {}

	def setCritics(self, link, xpath):
		self.critics['link'] = link
		self.critics['xpath'] = xpath

	def setAudiences(self, link, xpath):
		self.audiences['link'] = link
		self.audiences['xpath'] = xpath

	def getReview(self, film, page_num, utype):
		if ( hasattr(self, utype) ):
			if ( utype == 'critics' ):
				data = self.critics
			else:
				data = self.audiences

			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
			page = requests.get(data['link'].replace("$page$", str(page_num)).replace("$film$", film), headers=headers)
			tree = html.fromstring(page.content)

			reviews = tree.xpath(data['xpath'])
			reviews = list(map(str.rstrip, reviews))
			reviews = list(filter(None, reviews))
			return reviews


