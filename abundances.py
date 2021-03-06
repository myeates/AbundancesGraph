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
import urllib2

# open the XML file containing the run parameters
driver = Rappture.library(sys.argv[1])
datafile = driver.get("input.string(datapath).current")
inputtype = driver.get("input.choice(inputtype).current")

# builds empty temporary lists
infozt = []
infoat = []

# first checks if input string is a url or folder path from choice element,
# opens file using the correct method, and then iterates through input file 
# and creates an abundance vs z list and an abundance vs a list without 
# adding abundances of like species
if "web" in inputtype:
  input_file = urllib2.urlopen(datafile)
  for line in input_file:
      z, a, abundance = (item.strip() for item in line.split('\t', 2))
      infozt.append([z, abundance])
      infoat.append([a, abundance])

elif "folder" in inputtype:  
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

# counters/temporary list
z = 1
zsum = 0
infoz = []

# iterates through list of z and abudance, adds abundances of species with
# the same z, and adds them to a new list.
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

# fills final list with only nonzero abundances from infoz
for n in range(len(infoz)):
  if infoz[n][1] != 0:
    infoZ.append(infoz[n])
        
# counters/temporary list
a = 1
asum = 0
infoa = []

# iterates through list of z and abudance, adds abundances of species with
# the same z, and adds them to a new list.
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

# outputs lists to rappture curve elements
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
  
# outputs arrays to rappture string elements
for sp in range(len(infoZ)):
  line = "%s %s\n" % (infoZ[sp][0], infoZ[sp][1])
  driver.put("output.string(dataz).current", line, append=1)
  
for sp in range(len(infoA)):
  line = "%s %s\n" % (infoA[sp][0], infoA[sp][1])
  driver.put("output.string(dataa).current", line, append=1)

# outputs results to Rappture
Rappture.result(driver)

sys.exit()
