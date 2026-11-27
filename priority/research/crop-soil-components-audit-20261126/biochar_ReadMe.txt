Title:
------
Geospatial raster files of global biochar potential from crop-residues


Related publication:
--------------------
Potential for biochar carbon sequestration from crop residues: a global spatially explicit assessment
Global Change Biology - Bioenergy (2023)

Shivesh Kishore Karan(1,2†), Dominic Woolf(3,4,5*†), Elias Sebastian Azzi(1), Cecilia Sundberg(1), and Stephen A. Wood(6,7)
† These authors contributed equally to this work.

1 Department of Energy and Technology, Swedish University of Agricultural Sciences, Uppsala, Sweden
2 Department of Geomatics, Norwegian Institute of Bioeconomy Research, Ås, Norway
3 School of Integrative Plant Sciences, Cornell University, Ithaca, NY, USA
4 Atkinson Center for Sustainability, Cornell University, Ithaca, NY, USA
5 Institute of Digital Agriculture, Cornell University, Ithaca, NY, USA
6 The Nature Conservancy, Arlington, VA, USA
7 Yale School of the Environment, New Haven, CT, USA

* Address correspondence to: d.woolf@cornell.edu


Description:
------------
Raster files for crop-residue feedstock availability and biochar production from residues


Units:
------
All files except FPerm.tif are in Mg carbon per year per pixel (Mg C / yr)
FPerm.tif is a dimensionless fraction.


Geographic extent:
------------------
Global


Coordinate system:
------------------
WGS84 lat-long geographic coordinate systems


Resolution:
-----------
5×5 minutes of arc


File names:
-----------
res_prod.tif             = Annual production of crop residues from 42 crops
res_harv.tif             = Annual quantity of crop residues that can be sustainably harvested
res_avail.tif            = Annual quantity of harvestable crop residues available as a
                           bio-resource after allowing for competing uses in livestock production

bc_prod_tech.tif         = Annual potential for biochar production if 100% of generated residues
                           were utilized (i.e. technical potential)
bc_prod_constrained.tif  = Annual potential for biochar production if available residues (i.e.
                           after accounting for sustainably harvestable amounts and livestock use)
                           are utilized ("constrained potential")

bc_100_tech.tif          = Net carbon sequestration in technical potential, after accounting for
                           biochar decomposition over 100 years
bc_100_constrained.tif   = Net carbon sequestration in constrained potential, after accounting for
                           biochar decomposition over 100 years
Fperm.tif                = Fraction of biochar carbon that would remain sequestered after 100 years
