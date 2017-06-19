#==============================================================================
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
import urllib2

# open the XML file containing the run parameters
driver = Rappture.library(sys.argv[1])
datafile = driver.get("input.string(datapath).current")

# Label the output graph with a title, x-axis label,
# y-axis label, and y-axis units
driver.put('output.curve(zvabs).about.label','Abundance vs. Z (Scatter)',append=0)
driver.put('output.curve(zvabs).xaxis.label','Z',append=0)
driver.put('output.curve(zvabs).yaxis.label','Abundance',append=0)

driver.put('output.curve(avabs).about.label','Abundance vs. A (Scatter)',append=0)
driver.put('output.curve(avabs).xaxis.label','A',append=0)
driver.put('output.curve(avabs).yaxis.label','Abundance',append=0)

driver.put('output.curve(zvabl).about.label','Abundance vs. Z (Line)',append=0)
driver.put('output.curve(zvabl).xaxis.label','Z',append=0)
driver.put('output.curve(zvabl).yaxis.label','Abundance',append=0)

driver.put('output.curve(avabl).about.label','Abundance vs. A (Line)',append=0)
driver.put('output.curve(avabl).xaxis.label','A',append=0)
driver.put('output.curve(avabl).yaxis.label','Abundance',append=0)

# builds empty temporary lists
infozt = []
infoat = []

# first checks if input string is a url or folder path, then
# iterates through input file and creates an abundance vs z list
# and an abundance vs a list without adding abundances of like species
if "://" in datafile:
  input_file = urllib2.urlopen(datafile)
  for line in input_file:
      z, a, abundance = (item.strip() for item in line.split('\t', 2))
      infozt.append([z, abundance])
      infoat.append([a, abundance])
else:  
  with open(datafile) as input_file:
    for line in input_file:
      z, a, abundance = (item.strip() for item in line.split('\t', 2))
      infozt.append([z, abundance])
      infoat.append([a, abundance])

# converts strings in lists to float vars
for line in range(len(infozt)):
  for sub in range(len(infozt[line])):
    infozt[line][sub] = float(infozt[line][sub])
    
for line2 in range(len(infoat)):
  for sub2 in range(len(infoat[line2])):
    infoat[line2][sub2] = float(infoat[line2][sub2])

# counters
z = 1
zsum = 0
infoz = []
    
while z <= 92:
  for n in range(len(infozt)):
    nline = infozt[n]
    if nline[0] == z:
      zsum += nline[1]
  infoz.append([z,zsum])
  z += 1
  zsum = 0
  
# final list
infoZ = []

#fills final list with only nonzero abundances from infoz
for n in range(len(infoz)):
  if infoz[n][1] != 0:
    infoZ.append(infoz[n])
        
# counters
a = 1
asum = 0
infoa = []

# adds like abundances and creates a new list
while a <= 238:
  for n in range(len(infoat)):
    nline = infoat[n]
    if nline[0] == a:
      asum += nline[1]
  infoa.append([a,asum])
  a += 1
  asum = 0
  
# final list
infoA = []

# fills the final list with only nonzero abundances from infoa
for n in range(len(infoa)):
  if infoa[n][1] != 0:
    infoA.append(infoa[n])

#outputs lists to rappture curve elements
for sp in range(len(infoZ)):
  line = "%s %s\n" % (infoZ[sp][0], infoZ[sp][1])
  driver.put("output.curve(zvabs).component.xy", line, append=1)
  
for sp in range(len(infoA)):
  line = "%s %s\n" % (infoA[sp][0], infoA[sp][1])
  driver.put("output.curve(avabs).component.xy", line, append=1)

for sp in range(len(infoZ)):
  line = "%s %s\n" % (infoZ[sp][0], infoZ[sp][1])
  driver.put("output.curve(zvabl).component.xy", line, append=1)
  
for sp in range(len(infoA)):
  line = "%s %s\n" % (infoA[sp][0], infoA[sp][1])
  driver.put("output.curve(avabl).component.xy", line, append=1)
  
#outputs arrays to rappture string elements
for sp in range(len(infoZ)):
  line = "%s %s\n" % (infoZ[sp][0], infoZ[sp][1])
  driver.put("output.string(dataz).current", line, append=1)
  
for sp in range(len(infoA)):
  line = "%s %s\n" % (infoA[sp][0], infoA[sp][1])
  driver.put("output.string(dataa).current", line, append=1)

Rappture.result(driver)

sys.exit()
