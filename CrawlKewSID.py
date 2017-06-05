from bs4 import BeautifulSoup
import requests
import sys
import codecs

def main():
  """Usage: <exe> <TAXA> <Search>"""
  if len(sys.argv) != 3:
    print main.__doc__
    sys.exit(1)

  TAXA, behave = sys.argv[1], sys.argv[2]
  url = "http://data.kew.org/sid/SidServlet?Clade=" + TAXA + "&Order=&Family=&APG=off&Genus=&Species=&StorBehav=0&" + behave + "=on"
  r = requests.get(url)
  data = r.text
  soup = BeautifulSoup(data)
  species = soup.find_all('a')
  species = [link.contents[0] for link in species]
  species = species[species.index("Seed Information Database")+1:species.index("Back to search")]

  raw_grams = soup.findAll('span', attrs={'style':'COLOR: navy'})
  grams = [returnGrams(e) for e in raw_grams if returnGrams(e) != '']
  final = zip(species, grams)
  out = codecs.open(TAXA+"_"+behave+".csv", 'w','utf-8')
  for s,g in final:
    out.write("%s,%s\n" % (s,g))

def returnGrams(li):
  for e in li:
    if e[len(e)-1] == 'g':
      return str(e)
  else:
    return ''

def findSpeciesStart(li):
  count = 0
  for e in li:
    if e == u"Seed Information Database":
      return count + 1
    else:
      count = count + 1

main()
