import os
from bs4 import BeautifulSoup, SoupStrainer
import urllib2, jsonld
import mechanize

base_url = "http://www.imdb.com/find?ref_=nv_sr_fn&q="# base url for searching the movie
br = mechanize.Browser()
br.addheaders = [('User-agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0')]
movies = {}
br.set_handle_robots(False)
js = jsonld.JsonLdExtractor()

for name in os.listdir("."):
	movie = ''
	if os.path.isdir(name):
		movie = name
		name = name.lower()
		rules = ("dvdrip","720p","dvdscr","[","hindi","xvid","(","brrip","bluray","desiscr") # names part that are in the downloaded movie names but is not the part of the real movie name
		for rule in rules:
			if name.find(rule) > -1:
				name = name[:name.find(rule)]
		movie = name
		movie = ''.join([i if (i != '.') else ' ' for i in movie ])# getting rid of the dots in the title
		print movie
		movie = movie.lower()
		movie_search = '+'.join(movie.split())# exchanging the spaces with '+' sign
		url = base_url+movie_search# constructing the search url
		try:
			response = br.open(url)
		except Exception as e:
			print e
		else:
			only_td_tags = SoupStrainer(class_="result_text")
			soup = BeautifulSoup(response.read(),'lxml', parse_only=only_td_tags)
			link = soup.find("td",class_="result_text")
			if link:#finding the first table row with class 'result_text' that holds the first search reslult which is in most cases the desired movie
				links = link.find("a")# now getting the link to the searched movie to get the rating
				href = "http://www.imdb.com"+links.get("href")+"&s=tt&ttype=ft&ref_=fn_ft"
				print href
				try:
					page = br.open(href)
				except Exception as e:
					print e
				else:
					page = page.read()
					jsonld = js.extract(page)[0] if len(js.extract(page)) > 0 else None # extract the jsonld part that contains all the data about the movie
					# print jsonld
					if 'aggregateRating' in jsonld:
						if 'ratingValue' in jsonld['aggregateRating']:
							ratings = jsonld['aggregateRating']['ratingValue']
							movies[movie] = float(ratings) if (ratings) else 0
							print ratings
						else:
							print "rating not found!! check the name"
					else:
						"rating not found!! check the name"
			else :
				print "movie not found!!"
d_view = [ (v,k) for k,v in movies.iteritems() ] # entering all the values from the dict to a list of tuples
d_view.sort(reverse=True) # natively sort tuples by first element
for v,k in d_view:
    print "%s: %f" % (k,v)