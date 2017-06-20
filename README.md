This tool uses rappture to create two graphs, one of Abundance versus Atomic Number and one of Abundance versus Atomic Mass. 
It takes a text file with 3 columns separated by tabs; the first atomic numbers, the second atomic masses, and the third
abundances. It can take either a file from an internet address or a folder location on the local device.

For each graph, the tool iterates through the input file, and then adds the abundances with the same atomic number or mass,
depending on the graph. The final data is output as various rappture elements; a scatter plot curve, a solid line curve, and a 
string. This allows for both quick visualization of the data and data processing in one tool.
