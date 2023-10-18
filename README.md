# HC-TTIExp
HC-TTIExp is an extension of Deal.II (Arndt et al, 2023), a finite element method (FEM) library written in the C++ programming language. It has the purpose of providing tools to compute the Time Temperature Index (TTI) for any given 2D geological section based on the Arrhenius equation proposed by Wood in 1988 (An application for type II kerogens, which are major oil generators in the world, can be found in Hunt et al, 1991: https://pubs.geoscienceworld.org/aapgbull/article-abstract/75/4/795/38677/Modeling-Oil-Generation-with-Time-Temperature?redirectedFrom=fulltext).

Still this code is based on object oriented programming (OOP) standards and it permits to easily adapt input ASCII files to user needs and specific basin parameters, the general application is to make preliminary evaluations of the depth of the oil window in exploration areas of interest without need for temperature boundary conditions. Preliminary knowledge of burial history and source hydrocarbon kinetics is stricly necessary, in any other scenario a similar test case e.g. SPE Comparative Solution Project can be used (spe.org).

HC-TTIExp also allows for simulation of multi-phase fluid flow in the meshed domain without consideration of geomechanical effects, stratigraphic and tectonic disposition suffer no evolution, a geometric simplification helps keeping focus only on oil/gas dynamics. For this purpose the program employs discretization of the goberning equations for this phenomena such as accumulation and flow terms based on Darcy's law with pressure and saturation expressions that consider the relative velocity of mobilizing phase; temporal and spatial discretizations are adapted for this problem and context.

A test case for the Atrato basin of northwestern Colombia is found.

<b>For any required information please contact<b>:
* Juan Sebastián Osorno Bolívar (juansebosornob@gmail.com)
