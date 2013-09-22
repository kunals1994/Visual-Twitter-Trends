import ubigraph

U = ubigraph.Ubigraph()
U.clear()

for i in range(0,100):
  U.newVertex(i, color="#ff0000")

