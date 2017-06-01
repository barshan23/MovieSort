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
		if name.find("DvDRip") > -1:
			name = name[:name.find("DvDRip")]
			flag = 1
		if name.find("720p") > -1:
			name = name[:name.find("720p")]
			flag = 1
		if name.find("DVDSCR") > -1:
			name = name[:name.find("DVDSCR")]
			#print movie
			flag = 1
		if name.find("DVDScr") > -1:
			name = name[:name.find("DVDScr")]
			flag = 1
		if name.find("[") > -1:
			name = name[:name.find("[")]
			flag = 1
		if name.find("Hindi") > -1:
			name = name[:name.find("Hindi")]
			flag = 1
		if name.find("XviD") > -1:
			name = name[:name.find("XviD")]
			flag = 1
		if name.find("(") > -1:
			name = name[:name.find("(")]
			flag = 1
		if name.find("BRRip") > -1:
			name = name[:name.find("BRRip")]
			flag = 1
		if name.find("BluRay") > -1:
			name = name[:name.find("BluRay")]
			flag = 1
		if name.find("DesiSCR") > -1:
			name = name[:name.find("DesiSCR")]
			flag = 1
		movie = name
		movie = ''.join([i for i in movie if not i.isdigit()])
		print movie
		movie_search = '+'.join(movie.split())
		url = base_url+movie_search
		response = br.open(url) 
		soup = BeautifulSoup(response.read(),'html.parser')
		if soup.find("td",class_="result_text"):
			links = soup.find("td",class_="result_text").find("a")
			href = "http://www.imdb.com"+links.get("href")
			print href
			page = br.open(href)
			rating = BeautifulSoup(page.read(),'html.parser')
			if rating.find("span",itemprop="ratingValue"):
				ratings = rating.find("span",itemprop="ratingValue").getText()
				movies[movie] = float(ratings) if (ratings) else 0
				print ratings
			else :
				print "rating not found!! check the name"
		else :
			print "movie not found!!"
d_view = [ (v,k) for k,v in movies.iteritems() ]
d_view.sort(reverse=True) # natively sort tuples by first element
for v,k in d_view:
    print "%s: %f" % (k,v)