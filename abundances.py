#------------------------------------------------------------------------------
# 
# Generates a graph of Z or A vs abundances from an input .txt file
#
#==============================================================================
#
# AUTHOR: Matt Yeates
#
#==============================================================================
import Rappture
import sys
from lxml import etree
from collections import defaultdict

# open the XML file containing the run parameters
driver = Rappture.library(sys.argv[1])

datafile = driver.get("input.string(datapath).current")
  
# Label the output graph with a title, x-axis label,
# y-axis label, and y-axis units
driver.put("output.curve(zvab).about.label","Z vs. Abundance",append=0)
driver.put("output.curve(zvab).xaxis.label","Abundance",append=0)
driver.put("output.curve(zvab).yaxis.label","Z",append=0)

driver.put("output.curve(avab).about.label","A vs. Abundance",append=0)
driver.put("output.curve(avab).xaxis.label","Abundance",append=0)
driver.put("output.curve(avab).yaxis.label","A",append=0)

#builds empty list of lists of width w and height h
w = 2
h = 1000
infozt = [[0 for x in range(w)] for y in range(h)]
infoat = [[0 for x in range(w)] for y in range(h)]
s = 0

#iterates through input file and creates a z vs abundance array 
#and an a vs abundance array without adding abundances of like species
with open(datafile) as input_file:
  for line in input_file:
    z, a, abundance = (item.strip() for item in line.split('\t', 2))
    infozt[s][0] = z
    infozt[s][1] = abundance
    infoat[s][0] = a
    infoat[s][1] = abundance
    s = s + 1

#converts strings in arrays to float vars
infozt = [list(map(float, x)) for x in infozt]
infoat = [list(map(float, x)) for x in infoat]

#creates a z vs abundance array that adds abundances for like z values
infoz = [[0 for x in range(w)] for y in range(h)]
sp = 0
s = 0

for s in range(len(infozt)-1):
  if infozt[s][0] == infozt[s+1][0]:
    infoz[sp][0] = infozt[s][0]
    infoz[sp][1] = infoz[sp][1] + infozt[s+1][1]
  else:
    infoz[sp][0] = infozt[s][0]
    infoz[sp][1] = infozt[s][1]
  sp = sp + 1

#creates an a vs abundance array that adds abundances for like a values
infoa = [[0 for x in range(w)] for y in range(h)]
sp = 0

for s in range(len(infoat)-1):
  if infoat[s][0] == infoat[s+1][0]:
    infoa[sp][0] = infoat[s][0]
    infoa[sp][1] = infoa[sp][1] + infoat[s+1][1]
  else:
    infoa[sp][0] = infoat[s][0]
    infoa[sp][1] = infoat[s][1]
  sp = sp + 1

#outputs arrays to rappture curve element
for sp in range(len(infoz)):
  line = "%s %s\n" % (infoz[sp][0], infoz[sp][1])
  driver.put("output.curve(zvab).component.xy", line, append=1)
  
for sp in range(len(infoz)):
  line = "%s %s\n" % (infoa[sp][0], infoa[sp][1])
  driver.put("output.curve(avab).component.xy", line, append=1)

Rappture.result(driver)

sys.exit()
