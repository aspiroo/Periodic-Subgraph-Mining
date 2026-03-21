import os
from pathlib import Path

# Delete existing files to avoid append mode accumulation
out_dir = Path('data/processed/timesteps_with_edge_number')
out_dir.mkdir(parents=True, exist_ok=True)
for f in out_dir.glob('t*.txt'):
    f.unlink()
print(f"Cleared {out_dir}")

i = 1
while i <= 30:
    # read in your reference and the file
    reference = open("data/processed/keller_networks/drosophila_subset_t"+str(i)+".txt").read().strip()
    filetext = open("data/processed/outputWithEdgeNum.txt").read().strip()

    # split the reference file into a list of strings, splitting each time you encounter a new line
    splitReference = reference.split("\n")

    # do the same for the file
    splitFile = filetext.split("\n")

    # then, for each line in the reference,
    for referenceLine in splitReference:

        # split that line into a list of strings, splitting each time you encouter a stretch of whitespace
        referenceCells = referenceLine.split()

        # then, for each line in your 'file',
        for fileLine in splitFile:

            # split that line into a list of strings, splitting each time you encouter a stretch of whitespace
            lineCells = fileLine.split()

            # now, for each line in 'reference' check to see if the first value is equal to the first value of the current line in 'file'
            if referenceCells[0] == lineCells[1]:

                # if those are equal, then check to see if the current rows of the reference and the file both have a length of more than one
                if len(referenceCells) > 1:
                    if len(lineCells) > 1:

                        # if both have a length of more than one, compare the values in their second columns. If they are equal, print the file line
                        if referenceCells[1] == lineCells[2]:
                            out = open('data/processed/timesteps_with_edge_number/t'+str(i)+'.txt', 'a')
                            out.write(fileLine + '\n')
                            out.close()
    print("file " + str(i) + " complete")
    i += 1