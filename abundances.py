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

driver = Rappture.library(sys.argv[1])

driver.put('output.curve(zvab).about.label','Z vs. Abundance',append=0)
driver.put('output.curve(zvab).xaxis.label','Abundance',append=0)
driver.put('output.curve(zvab).yaxis.label','Z',append=0)

driver.put('output.curve(avab).about.label','A vs. Abundance',append=0)
driver.put('output.curve(avab).xaxis.label','Abundance',append=0)
driver.put('output.curve(avab).yaxis.label','A',append=0)

info = {}
species = 0

with open(driver.get('input.string(data).current') as input_file:
  for line in input_file:
    z, a, abundance = (
      item.strip() for item in line.split('\t', 2))
    line = "%g %g\n" % (z, abundance)
    line2 = "%s %s\n" % (a, abundance)
    driver.put('output.curve(zvab).component.xy', line, append=1)
    driver.put('output.curve(avab).component.xy', line2, append=1)

Rappture.result(driver)
sys.exit()