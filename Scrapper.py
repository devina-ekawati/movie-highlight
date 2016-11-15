from MovieCriticSite import MovieCriticSite

rt = MovieCriticSite("Rotten Tomatoes")
rt.setCritics("https://www.rottentomatoes.com/m/$film$/reviews/?page=$page$", "//div[@class=\"the_review\"]/text()")
rt.setAudiences("https://www.rottentomatoes.com/m/$film$/reviews/?type=user&page=$page$", '//div[@class="user_review"]/text()[last()]')

mc = MovieCriticSite("Metacritics")
mc.setCritics("http://www.metacritic.com/movie/$film$/critic-reviews?page=$page$", "//div[@class=\"summary\"]/a[@class=\"no_hover\"]/text()")
mc.setAudiences("http://www.metacritic.com/movie/$film$/user-reviews?page=$page$", "//div[@class=\"review_body\"]/span/span[@class=\"blurb blurb_expanded\"]/text()|//div[@class=\"review_body\"]/span/text()")

imdb = MovieCriticSite("IMDB")
#IMDB ga punya page khusus critics :(
imdb.setAudiences("http://www.imdb.com/title/$film$/reviews?start=$page$", "//div[@id=\"tn15content\"]//div/h2/text()|//div[@class=\"review_body\"]/span/text()")

#print('Reviews: ', imdb.getReview('tt1211837', 0, 'audiences'))
print('Reviews: ', mc.getReview('doctor-strange', 1, 'audiences'))
