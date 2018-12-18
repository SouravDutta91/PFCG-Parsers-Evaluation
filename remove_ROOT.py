# import libraries

import sys

# command line arguments

input_file = sys.argv[1]
output_file = sys.argv[2]

# open a write stream and a read stream to read file, process it
# and write to a new file

try:
    with open(output_file, 'w') as outf, open(input_file, 'r') as inf:

        # we process each line in the input file

        for line in inf:

            # if the sentence starts with (ROOT

            if line.startswith('(ROOT'):

                # remove the ROOT and use the remaining part
            
                line = '(' + line[5:(len(line) - 2)] + ')\n'

                # write to the new file

                outf.write(line)

# exception caught in case thrown

except FileNotFoundError:
    print('Error: Please enter a valid input file.')