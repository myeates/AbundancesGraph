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

# open the XML file containing the run parameters
driver = Rappture.library(sys.argv[1])
datafile = driver.get("input.string(datapath).current")

# Label the output graph with a title, x-axis label,
# y-axis label, and y-axis units
driver.put('output.curve(zvab).about.label','Abundance vs. Z',append=0)
driver.put('output.curve(zvab).xaxis.label','Z',append=0)
driver.put('output.curve(zvab).yaxis.label','Abundance',append=0)

driver.put('output.curve(avab).about.label','Abundance vs. A',append=0)
driver.put('output.curve(avab).xaxis.label','A',append=0)
driver.put('output.curve(avab).yaxis.label','Abundance',append=0)

# builds empty temporary lists
infozt = []
infoat = []

# iterates through input file and creates an abundance vs z list
# and an abundance vs a list without adding abundances of like species
with open(datafile) as input_file:
  for line in input_file:
    z, a, abundance = (item.strip() for item in line.split('\t', 2))
    infozt.append([z, abundance])
    infoat.append([a, abundance])

#converts strings in lists to float vars
for line in range(len(infozt)):
  for sub in range(len(infozt[line])):
    infozt[line][sub] = float(infozt[line][sub])
    
for line2 in range(len(infoat)):
  for sub2 in range(len(infoat[line2])):
    infoat[line2][sub2] = float(infoat[line2][sub2])

# constants/counters
tlength = len(infozt)
tcounter = 0
ncounter = 0
zsum = float(infozt[0][1])
# final list
infoz = []

# loop for iterative sorting of abundance vs z
while ncounter < (tlength - 1):
  ncounter += 1
  tline = infozt[tcounter]
  nline = infozt[ncounter]
  # if they are equal, get simple sum and continue
  if tline[0] == nline[0]:
    zsum += float(nline[1])
  # if not equal, print out sums and restart at new values
  elif tline[0] != nline[0]:
    infoz.append([int(tline[0]),zsum])
    zsum = float(nline[1])
    tcounter = ncounter
  # for end of list
  if tcounter == (tlength - 2):
    infoz.append([int(tline[0]),zsum])
        
# constants/counters
tlength = len(infoat)
asum = 0
# final list
infoa = []

# loop for iterative sorting of abundance vs a
for ncounter in range(tlength):
  nline = infoat[ncounter]
  for tcounter in range(tlength):
    tline = infoat[tcounter+1]
    # if they are equal, get sum and continue
    if tline[0] == nline[0]:
      asum += float(nline[1])
    # if not equal, print out sums and restart at new values
    elif tline[0] != nline[0]:
      infoa.append([(int(nline[0])-1),asum])
      asum = float(nline[1])
      tcounter = ncounter
      break

# this (along with subtracting one from int(nline[0])) fixes a small error 
# in the above code; there's definitely a more elegant solution, but this 
# works for now
del infoa[0]
infoa.append([int(infoat[-1][0]), infoat[-1][1]])

#outputs arrays to rappture string element
for sp in range(len(infoz)):
  line = "%s %s\n" % (infoz[sp][0], infoz[sp][1])
  driver.put("output.curve(zvab).component.xy", line, append=1)
  
for sp in range(len(infoa)):
  line = "%s %s\n" % (infoa[sp][0], infoa[sp][1])
  driver.put("output.curve(avab).component.xy", line, append=1)

Rappture.result(driver)

sys.exit()
