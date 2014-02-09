from twython import Twython
import time
import xmlrpclib
import sys
import random
import os

twitter = Twython (
	#Twitter Credentials
)

class Node():
	def __init__(self, node_type):
		self.children = {}
		self.type = node_type
		self.id = 0

def main(args):
	world = Node (node_type = "world")

	all_trends = {}
	
	cities = twitter.get_available_trends()

	#Look up by city,country instead of woeid?
	for curr_city in cities:
		country = curr_city["country"]
		name = curr_city["name"]

		args_name = (name+","+country).replace(" ", "_")

		if(args_name in args):
			if(country not in world.children):
				world.children[country] = Node (node_type = "country")

			add_to_graph(curr_city, world.children[country], all_trends)

	os.system("bin/ubigraph_server &")

	time.sleep(5)

	server_url = 'http://127.0.0.1:20738/RPC2'
	server = xmlrpclib.Server(server_url)
	G = server.ubigraph
	display(world, G, None, "world")

def display(node, ubi, parent, name):

	curr_vertex = 0

	if(node.id == 0):
		curr_vertex = ubi.new_vertex()
		ubi.set_vertex_attribute(curr_vertex, 'shape', 'sphere')
		ubi.set_vertex_attribute(curr_vertex, 'label', name)
		node.id = curr_vertex

	else:
		curr_vertex = node.id

	if (node.type == "world" or node.type == "trend"):
		ubi.set_vertex_attribute(curr_vertex, 'shape', 'none')

	if (parent != None):
		curr_edge = ubi.new_edge(curr_vertex, parent)
		curr_vertex
		ubi.set_edge_attribute(curr_edge, 'oriented', "true")
		ubi.set_edge_attribute(curr_edge, 'strength', "0.075")

	for child in node.children:
		display (node.children[child], ubi, curr_vertex, child)

def add_to_graph(city, country, all_displayed_trends):
	name = city ["name"]
	city_node = Node (node_type = "city")
	country.children[name] = city_node
	for trend in get_trends(city):
		trend_name = (trend["name"].lower()).replace(" ", "")
		if(trend_name not in all_displayed_trends):
			all_displayed_trends [trend_name] = Node(node_type = "trend")			

		city_node.children[trend_name] = all_displayed_trends[trend_name]

def get_trends(place):
	try:
		return twitter.get_place_trends(id = place["woeid"])[0]["trends"]
	except:
		print "problem with twitter..."
		return []

main(sys.argv)
