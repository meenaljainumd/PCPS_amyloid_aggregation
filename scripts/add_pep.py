import scipy.spatial
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns
from MDAnalysis import *
import MDAnalysis as mda
import argparse
import math

# Set up argument parser
parser = argparse.ArgumentParser(description='GRO, Final, and peptidegro files.')
parser.add_argument('-c', '--gro', required=True, help='GRO file for adding peptides')
parser.add_argument('-f', '--Final', required=True, help='file with peptides')
parser.add_argument('-conf', '--peptidegro', required=True, help='GRO file for Abeta')
parser.add_argument('-n', '--num_peptides', type=int, required=True, help='Total number of peptides to insert')
args = vars(parser.parse_args())

GRO = args['gro']
Final = args['Final']
peptidegro = args['peptidegro']
total_peptides = args['num_peptides']

print(GRO, Final, peptidegro, total_peptides)

u = Universe(GRO)
boxz = u.dimensions[2]
boxx = u.dimensions[0]
boxy = u.dimensions[1]

def calculate_grid(num_peptides):
    side = math.ceil(math.sqrt(num_peptides))
    return side, side

def insert_peptides(num_peptides, z_fraction):
    nx, ny = calculate_grid(num_peptides)
    x = np.linspace(0.2*boxx/10, 0.8*(boxx)/10.0, nx)
    y = np.linspace(0.2*boxy/10, 0.8*(boxy)/10.0, ny)
    xv, yv = np.meshgrid(x, y)
    
    it_len = min(np.shape(xv))
    Peploc = np.array([list(zip(xv[i], yv[i])) for i in range(it_len)])
    PROT = []
    
    count = 0
    for i, row in enumerate(Peploc):
        for j, coord in enumerate(row):
            if count >= num_peptides:
                break
            count += 1
            os.system(f"gmx editconf -f {peptidegro} -o Nsvs_mod_{i+1}{j+1}.gro -center {coord[0]} {coord[1]} {z_fraction*boxz/10.0} -box {boxx/10.0} {boxy/10.0} {boxz/10.0}")
            newgro = f"Nsvs_mod_{i+1}{j+1}.gro"
            PROT.append(Universe(newgro).atoms)
        if count >= num_peptides:
            break
    
    return PROT

# Calculate peptides for upper and lower leaflets
upper_peptides = total_peptides // 2
lower_peptides = total_peptides - upper_peptides

# Insert peptides in upper leaflet
PROT_upper = insert_peptides(upper_peptides, 0.85)

# Insert peptides in lower leaflet
PROT_lower = insert_peptides(lower_peptides, 0.15)

# Combine all peptides
PROT = PROT_upper + PROT_lower

proteins = mda.Merge(PROT[0])
for p in PROT[1:]:    
    proteins = mda.Merge(proteins.atoms, p)

wat = u.select_atoms("resname PW")
not_water = u.select_atoms("not resname PW")
combined_water = mda.Merge(proteins.atoms, wat.atoms)
no_overlap_water = combined_water.select_atoms("same resid as (not around 6 name BB BBp BBm S1 S2)")
combined = mda.Merge(not_water.atoms, no_overlap_water.atoms)
no_overlap = combined.select_atoms("all") 
no_overlap.write("overlap_fix.gro")

with open("overlap_fix.gro") as f:
    content = f.readlines()
content[-1] = f'   {boxx/10.0:.6f}   {boxy/10.0:.6f}   {boxz/10.0:.6f}\n'

with open("pepappend.gro", "w") as f:
    f.writelines(content)

os.system(f"gmx genconf -f pepappend.gro -o {Final}")
os.system("rm -rf overlap_fix.gro N*.gro \#*")
