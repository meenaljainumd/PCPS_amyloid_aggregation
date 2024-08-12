# Amyloid aggregation in mixed PC/PS lipid bilayers: Dual role of anionic lipids 
This directory contains all files and protocol for the self-assembly of amyloid peptides under mixed PC/PS lipid bilayers.

# Contents

(1) ITP_files/ 


Directory with all the topology files required to set the simulations. 

    (a) ff_r.itp : nonbonded interaction parameters 
    (b) popc.itp : topology file for POPC lipids in the     
                   upper leaflet
    (c) pc_l.itp : topology file for POPC lipids in the 
                   lower leaflet. These lipids have repulsive interactions with the peptide backbones. 
    (d) pops.itp : topology file for POPS lipids in the     
                   upper leaflet
    (e) pc_l.itp : topology file for POPS lipids in the 
                   lower leaflet. These lipids have repulsive interactions with the peptide backbones.
    (f) abeta.itp : topology file for amyloid-beta fragment, Aβ16-22 (K16LVFFAE22).
    (g) water.em.itp : topology file for EM of MARTINI    
                       polarizable water. 
    (h) water.md.itp : topology file for equilibration/     
                       production run of MARTINI polarizable water. 

(2) Initial_molecular_structures/
This directory contains the initial configurations of the lipid bilayer system with and without peptides for the different percentages of PS.

(3) Position_restraint_files/
This directory contains the position restraint files for POPC, POPS and Aβ16-22 molecules.

(4) TOP files/
This directory contains the topology of the entire simulation system for the production run of 3000 ns for different percentages of PS.

(5) Simulation_MDPS
This directory contains the MDP options for energy minimization, equilibration and production run for different percentages of PS. Different PS percentages were simulated at different values of surface tension to model an APL of 95 Å².