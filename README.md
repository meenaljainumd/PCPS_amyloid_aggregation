# Amyloid Aggregation in Mixed PC/PS Lipid Bilayers: Dual Role of Anionic Lipids

This repository contains all files and protocols for simulating the self-assembly of amyloid peptides under mixed PC/PS lipid bilayers.

## Contents

1. **ITP_files/**: Directory with all topology files required for simulations.
   - `ff_r.itp`: Nonbonded interaction parameters
   - `popc.itp`: Topology file for POPC lipids in the upper leaflet
   - `pc_l.itp`: Topology file for POPC lipids in the lower leaflet (with repulsive interactions with peptide backbones)
   - `pops.itp`: Topology file for POPS lipids in the upper leaflet
   - `ps_l.itp`: Topology file for POPS lipids in the lower leaflet (with repulsive interactions with peptide backbones)
   - `abeta.itp`: Topology file for amyloid-beta fragment, Aβ16-22 (K16LVFFAE22)
   - `water.em.itp`: Topology file for EM of MARTINI polarizable water
   - `water.md.itp`: Topology file for equilibration/production run of MARTINI polarizable water

2. **Initial_molecular_structures**: Initial configurations of the lipid bilayer system with and without peptides for different percentages of PS.

3. **Position_restraint_files**: Position restraint files for POPC, POPS, and Aβ16-22 molecules.

4. **TOP_files**: Topology of the entire simulation system for the production run of 3000 ns for different percentages of PS.

5. **Simulation_MDPS**: MDP options for energy minimization, equilibration, and production run for different percentages of PS. Different PS percentages were simulated at different values of surface tension to model an APL of 95 Å².

6. **scripts**: Contains `insane_genBL.py`, `add_pep.py`, and `abeta.gro`. See the tutorial below on how to use these scripts to generate a mixed lipid bilayer and add peptides.

## Tutorial: Setting Up a Mixed Lipid Bilayer with 16 Peptides

This tutorial guides you through the process of creating a mixed lipid bilayer and inserting peptides for simulation.

### 1. Prepare a mixed lipid bilayer (10% POPS: 90% POPC)

Use the `insane_genBL.py` script (a modified version of insane[1]) to prepare the lipid bilayer for WEPMEM[2] lipids. This creates a box of dimensions 12 x 12 x 13 nm with polarizable water.

```bash
python3 insane_genBL.py -u POPC:154 -u POPS:15 -l PC_L:154 -l PS_L:15 -sol PW -x 12 -y 12 -z 13 -o pcps_10.gro -p topol.top
```

This command generates:
- `pcps_10.gro`: A GRO file containing the mixed bilayer and polarizable water
- `topol.top`: The topology file

Next, edit `topol.top` to include the ITP files for the force-field, POPC, POPS, water, and Aβ16-22 molecules. 

### 2. Insert 16 peptides into the simulation box

Use the `add_pep.py` script, which requires the initial structure of the Aβ16-22 peptide (`abeta.gro`).

```bash
python add_pep.py -c pcps_10.gro -f pcps_10_pep.gro -conf ./abeta.gro -n 16
```

This creates `pcps_10_pep.gro` with:
- 8 peptides near the upper leaflet (at 0.85 of the z-dimension)
- 8 peptides near the lower leaflet (at 0.15 of the z-dimension)

### 3. Proceed with simulation

After creating the mixed bilayer with peptides, you can begin the Energy Minimization, Equilibration, and Production MD using the GROMACS simulation package. All necessary files are provided in this repository, and the detailed protocol is available in our publication [citation needed].

For specific queries or further assistance, please email mjain123@umd.edu.

---

### References

[1] Wassenaar, T. A. et al. Computational lipidomics with insane: a versatile tool for generating custom membranes for molecular simulations. J. Chem. Theory Comput. 2015, 11, 2144–2155.

[2] Ganesan, S. J. et al. Effect of lipid head group interactions on membrane properties and membrane-induced cationic β-hairpin folding. Phys. Chem. Chem. Phys. 2016, 18, 17836–17850.
