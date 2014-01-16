from twython import Twython
import time
import xmlrpclib
import sys
import random
import os

twitter = Twython (
	app_key = 'kqBFSvxPIWruZAgKetyzhQ',
	app_secret = 'CoF5NioQgztQRqiqX1jPth63n297FVig3l6ZMc',
	oauth_token = '1892421098-dRvozyLCEM1QQ4VGtU2oxoLOvdGkmzmJb4wHX71',
	oauth_token_secret = 'OsJeQT6AacIyhUFB9ffXkIWNLYZtcLQpklQ0TW108Q'
)

class Node():
	def __init__(self, node_type):
		self.children = {}
		self.type = node_type

def main(args):
	world = Node (node_type = "world")
	#Pickle/Save to disk in future to save time?
	cities = twitter.get_available_trends()

	for curr_city in cities:
		country = curr_city["country"]
		name = curr_city["name"]

		if( (name+","+country) in args):
			if(country not in world.children):
				world.children[country] = Node (node_type = "country")

			add_to_graph(curr_city, world.children[country])


	os.system("bin/ubigraph_server &")

	time.sleep(5)

	server_url = 'http://127.0.0.1:20738/RPC2'
	server = xmlrpclib.Server(server_url)
	G = server.ubigraph

	display(world, G, None, "world")

def display(node, ubi, parent, name):

	curr_vertex = ubi.new_vertex()
	ubi.set_vertex_attribute(curr_vertex, 'shape', 'sphere')
	ubi.set_vertex_attribute(curr_vertex, 'label', name)

	if (node.type == "world" or node.type == "trend"):
		ubi.set_vertex_attribute(curr_vertex, 'shape', 'none')

	if (parent != None):
		curr_edge = ubi.new_edge(curr_vertex, parent)
		curr_vertex
		ubi.set_edge_attribute(curr_edge, 'oriented', "true")
		ubi.set_edge_attribute(curr_edge, 'strength', "0.075")

	for child in node.children:
		display (node.children[child], ubi, curr_vertex, child)

def add_to_graph(city, country):
	name = city ["name"]
	city_node = Node (node_type = "city")
	country.children[name] = city_node
	for trend in get_trends(city):
		city_node.children[trend["name"]] = Node(node_type = "trend")

def get_trends(place):
	return twitter.get_place_trends(id = place["woeid"])[0]["trends"]
	


main(sys.argv)


