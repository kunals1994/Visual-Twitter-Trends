from twython import Twython
import time
import xmlrpclib
import os
import random

counter = 0
currAccount = -1
twitter = Twython()
failures = 0

def changeAccount():
	acct = currAccount
	global currAccount
	currAccount = acct + 1
	global nextAccount
	nextAccount = accounts[currAccount]
	global twitter
	twitter = Twython (
		app_key = nextAccount[0],
    	app_secret = nextAccount[1],
    	oauth_token = nextAccount[2],
    	oauth_token_secret = nextAccount[3]
	)

def getTrends(ident):
	perform = 0
	if(perform == 0):
		if(counter >15):
			changeAccount()
			global counter
			counter = 0
		global counter
		counter = counter +1
		try:
			return twitter.get_place_trends(id = ident)[0]["trends"]
		except:
			global failures
			failures = failures + 1
			return []
	else:
		return[]

accounts = [
['kqBFSvxPIWruZAgKetyzhQ', 'CoF5NioQgztQRqiqX1jPth63n297FVig3l6ZMc', '1892421098-dRvozyLCEM1QQ4VGtU2oxoLOvdGkmzmJb4wHX71', 'OsJeQT6AacIyhUFB9ffXkIWNLYZtcLQpklQ0TW108Q'],
['lqnqn7EbNJ2bNxkObNoPFg', 'PWJMHZtu4suUZWo0xOS2cP67U2v0HQiS1bpYc6PqUQ', '1881629118-uGEjh1Gwr2zt7Cwnug6KVe4XOgk5fmqUZoJzNhO', 'FSIKjJfkEcKKFNHQl6wgj09pT6W24S0I6yZWDGkhA'],
['Warbf692KOy1NyqvWrgdg', 'vwEi4cRQPOEoioDu3lgwo6NkHtBXz5DCsjQ21XDL6Y', '1892350652-3feaifiTPLGZFth2YZjTOupyxroOb2gZoZrjiKb', 'YkRsGPTLLsZU5wso1ovpuObqfg5Jya8Emy3Fgz8DGE'],
['fXJjQUcNuYAn4tlDh44s3A', '90LQ41LY4XucCOnwb4vZgk28ZCQJ9jUTxITdvv43U84', '1892490416-ZqjdWutSWgCV28pg6Huq6Oes6j4LGu48qbQHVB2', 'yZuuYfaebz7ojdutYoPg3PjOlVgFa20HI203sDCR3sU'],
['K5JJVAUXjKpas4uqzRvLg', 'XQwK3cAel8ZAqOhbScA6RJg8qOOuEQz2dcjjIvwLiOU', '1892532817-siib0x8y53jOKFpHVIrNrRoFH9piNik98nA0p5W', 'aY9KdTaoo7dTVeFvOo17fVGYXdPQqrpfWIOUh6OXJg'],
['ytKwG1grpcvnuBxwaRZQvA', 'hWNNXOnXJNterYG31K73SYZjfQlLkatrBamM4IYo5E', '1892555287-cTU9uvPmvk0Db78xBwlxcPyzQUvKx7FtqoRCZXb', 'vhP2grBnzs8rpT0scza5VUKtXFtJIca6mnoaX54Lo'],
['lDw15Yo7azvp0uHUsOoybQ', 'SBLlwG75ZhkuLQj0nbPkjOIoXCbeF2hJAkje7ifT4', '1892541002-Z2aMDr4gsYv9wkM3E3e7rdCC8YBlKdLSykVK5g8', 'KMcF79WLjlg1gPeTSNhjVQMKCAOMYo4aIctXtIpEs'],
['wDecq4WMAtISD1wBfwvnLA', 'uiWTJbYNWqRhTbBuS60qNQ1B1JlV1wZlVNGy4S2Mo', '1892760554-071Bcvyi9Uqhzt2svY19JtdZAzhjQfTL3aOvMkH', 'jll4Y4QPguYmPCetoOmQMEAMETaTFoC0MBUeaDJJl4'],
['Q6lTBJ1RFIaSsOnfKrug', '74L70LSx1leFwP8En9dfRrZ7PXGfWT904SVROT2tFDA', '1892792875-GSpQge8UXEnO2w7lpeiCMmd8CjKfiXon4CLw6GE', 'AGrLYxW4YKUjYtB2Zniy7F5Ly86LvxeYQnSeg8zA20'], 
['4GEHheM3lOtLuk0mtv1A', 'zPNhwKVjkPAjSM6wpjiwKpO2Ba2ovgw0jueol8gnZk', '1892749626-I0G2T8LOuklifJFNiFyEQToH3KVKTWQtdUlLAGP', 'mdQBGfqnn3sp3DET0rIliDw1lFMocxTD9GtIRatOPXI'], 
['DuU0PLImCxevdkOX8XRFvg','Ye0VqOQTze1zp475dO0bllsrOPQf7KWy8kKvUVvE5rY','1892793883-QReQnIFtM3nOKL8NUsoQyIvFSD6nNhTDz6tuzjs','nUBDAdfMkIRkbkG0cAUIeippxFd9artbNnnm2fVa0'],
['suXuWBxPNHCHDKpgQIMA','8YWVkaWwKnDqZ0jHXhAtpherM7wOdRHTD5GzFaMUI','1892779508-nVeDY0WaLW2a9dxCiv64PAfGgjDmmdpWhJovzVr','nteFRUnD1F45RULXGMTpW2unY13kBYKeTPtnHP6KHQ'],
['w4W45q4o2JwmWqHYuKW3w','ZuO76b6WkQYe4aQUNiroExVqat5xZgOcC4udcLgAvY','1892788328-TTApN7nVupczwDNEDMwnHlZIlyDhZHEyTsa8hZv','QVQHudHDQJEY7LKqWEK7TxI6GPDI02Q5YINRtLkA'],
['FsAUgbmyonaNvVSGFptyHw','Dip2eBrUnwT2Et22o8gqnJCH2zB5esX6Gk21Q6OeC54','1892758320-x9mwSDgiY5evUetvOPRstmBjUzExsRsGTGWkuEj','MVC7eqt25upT5qpM9XPvQYn1UjV4rkkrcqTRNK8rCs'],
['WW5Hk9fAYLYEGp4cLQEVeA','nwi0R7EI0lWHpELIk3VNydSDd8dMoqtNtSji4XghEL8','1892831299-uj7zqyVkwR1Jeyy1E4xGyj1l2KROZ8Xkiarxwa6','F1h2KdT5f6Eo7CwOUeXvm5SabhXEqxz1Zz3ql2xZNA'],
['KFEB9NTn4WJH9IjupnPgg','TLatz8s1Pp5ZvkUBGFHh99MBcPu5H6Q7DNOMfTTE','1892838469-vzFfKew3adiT3mdK8v7W50Afi7qOY4SSu8tvw9E','kVEzSkvPtruaFffAxPnpkrxd4ugYpW2EDj27UUB4z3w'],
['SI00kZTM4MYCysDywHt7uQ','AI5BfFykv3IqguBPWtNcYgemKaPxs4sV64QuyNl6c','1892845015-Wfsfc9fWC0BbHScSkHO0ApWvY3elJLkqus8pyQ','PMs4b3Tf6pAnLkDGP07MveLrfA3bNzLU2MwrGEjQmEs'],
['kvVfpVbDU4KlwXh3oKeTQ','bKnHzFddM0kp92hIC0lkw0Mq06EAjamruVVci7apY','1892797200-VoB955vlvCLBFjYIS73qBbi8NknfyZ74ld6Dmpv','ONWKyXAxmjoHGQtsnML9n7rrgdA9evJdRkx1uLlb4'],
['DmT1r56lPyuwe8nUBx9OFA','YY4iJsUjKflBf3KbfTvPkE3hMyDhR04jkp2HMfzoByI','1892843048-gapDL2KPE5qy62xMlI9aNIpOYqBpFYJCv0xSq6w','oKyTpCdNU5tiFf5Qki72QgzYIX3vmctPRNOHtl5x8']
]

changeAccount()

places = twitter.get_available_trends()

countries= {}

for place in places:
	if(place["country"]=="Worldwide"):
		continue
	if (place["country"] not in countries):
		countries[place["country"]] = {}
	if(place["country"] == place["name"]):
		continue
	countries[place["country"]][place["name"]] = place["woeid"]

os.system("bin/ubigraph_server &")

time.sleep(5)

server_url = 'http://127.0.0.1:20738/RPC2'
server = xmlrpclib.Server(server_url)
G = server.ubigraph

trends = {}
currCountry = 0
world = G.new_vertex()
G.set_vertex_attribute(world, 'shape', 'none')
for country in countries:
	currCountry = G.new_vertex()
	c = G.new_edge(world, currCountry)
	G.set_edge_attribute(c, "oriented", "true")
	G.set_edge_attribute(c, "strength", "0.075")
	G.set_vertex_attribute(currCountry, 'shape', 'sphere')
	G.set_vertex_attribute(currCountry, 'label', country)
	currCity = 0
	for city in countries[country]:
		currCity = G.new_vertex()
		c = G.new_edge(currCountry, currCity)
		G.set_edge_attribute(c, "oriented", "true")
		G.set_edge_attribute(c, "strength", "0.075")
		G.set_vertex_attribute(currCity, 'shape', 'sphere')
		G.set_vertex_attribute(currCity, 'label', city)
		G.set_vertex_attribute(currCity, 'color', '#ff0000')
		#need to make 372 requests to get to all the cities

		trens = getTrends(countries[country][city])
		if (trens == []):
			G.set_vertex_attribute(currCity, 'label', "")
		for trend in trens:
			if (trend["name"] not in trends):
				trends[trend["name"]] = G.new_vertex()
				G.set_vertex_attribute(trends[trend["name"]], 'shape', 'none')
			c = G.new_edge(currCity, trends[trend["name"]])
			G.set_edge_attribute(c, "oriented", "true")
			G.set_edge_attribute(c, "strength", "0.075")
			G.set_vertex_attribute(trends[trend["name"]], 'label', trend["name"])

print failures

