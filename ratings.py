import os
from bs4 import BeautifulSoup
import urllib2
import mechanize

base_url = "http://www.imdb.com/find?ref_=nv_sr_fn&q="
br = mechanize.Browser()
br.addheaders = [('User-agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:53.0) Gecko/20100101 Firefox/53.0')]
movies = {}

for name in os.listdir("."):
	flag = 0
	movie = ''
	if os.path.isdir(name):
		movie = name
		name = name.lower()
		rules = ("dvdrip","720p","dvdscr","[","hindi","xvid","(","brrip","bluray","desiscr")
		for rule in rules:
			if name.find(rule) > -1:
				name = name[:name.find(rule)]
		movie = name
		movie = ''.join([i if (i != '.') else ' ' for i in movie ])# getting rid of the dots in the title
		print movie
		movie = movie.lower()
		movie_search = '+'.join(movie.split())# exchanging the spaces with '+' sign
		url = base_url+movie_search# constructing the search url
		response = br.open(url) 
		soup = BeautifulSoup(response.read(),'html.parser')
		if soup.find("td",class_="result_text"):#finding the first table row with class 'result_text' that holds the first search reslult which is in most cases the desired movie
			links = soup.find("td",class_="result_text").find("a")# now getting the link to the searched movie to get the rating
			href = "http://www.imdb.com"+links.get("href")+"&s=tt&ttype=ft&ref_=fn_ft"
			print href
			page = br.open(href)
			rating = BeautifulSoup(page.read(),'html.parser')
			if rating.find("span",itemprop="ratingValue"):#selecting the span that contains the rating of the movie
				ratings = rating.find("span",itemprop="ratingValue").getText()# retrieving the rating value
				movies[movie] = float(ratings) if (ratings) else 0
				print ratings
			else :
				print "rating not found!! check the name"
		else :
			print "movie not found!!"
d_view = [ (v,k) for k,v in movies.iteritems() ] # entering all the values from the dict to a list of tuples
d_view.sort(reverse=True) # natively sort tuples by first element
for v,k in d_view:
    print "%s: %f" % (k,v)