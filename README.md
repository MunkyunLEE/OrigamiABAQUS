# OrigamiABAQUS
Pin Joints Array (PJA)[1]-based Origami crease(hinge) modeling for Abaqus simulation.
This code connects nodes to nodes, which are located at the same location.
All details are included in Chapter 2 of reference [2]. 
The examples of linear creases are included in reference [3], and curved creases are included in reference [4].
The codes are written in Python by referring to the Abaqus API [5].

SET1: Material, Section assignment, Step, and Amplitude Setting 

SET2: Meshing >> 

SET3:

SUP1: 


**REFERENCES**

[1] Munkyun Lee and Tomohiro Tachi, “Design and Evaluation of Compliant Hinges for Deployable Thick Origami Structures”, Journal of the International Association for Shell and Spatial Structures (IASS), No. 65(4), pp.238-247. 2024.12
DOI: https://doi.org/10.20898/j.iass.2024.015

[2] Munkyun Lee, "Geometry and Mechanics of Multistable Origami Blocks", Doctoral Thesis, Department of Architecture, Graduate School of Engineering, The University of Tokyo, 2026.03 
  
[3] Felix Dellinger, Martin Kilian, Munkyun Lee, Christian Muller, Georg Nawratil, Tomohiro Tachi, and Kiumars Sharifmoghaddam, “Snapping Deployable Toroids for Modular Gridshells”, ACM Trans. Graph., Vol.44, No.6, pp.235:1-21, ACM SIGGRAPH Asia 2025, Hong Kong, China, 2025.12
DOI: https://doi.org/10.1145/3763808

[4] Munkyun Lee, Joseph M. Gattas, and Tomohiro Tachi, “Multistable Curved-crease Origami Blocks for Reconfigurable Modular Building System”, Proceedings of International Association for Shell and Spatial Structures (IASS) Annual Symposia, Mexico City, Mexico, 2025.10
DOI: https://doi.org/10.48550/arXiv.2509.07337

[5] "ABAQUS Scripting Reference", http://130.149.89.49:2080/v2016/books/ker/default.htm?startat=pt01ch44pyo01.html



**!!! PLEASE READ !!!**

All the code appears to work, but I am aware that it is neither very efficient nor particularly clear 😭. This is mainly because I am not very familiar with Python and Abaqus. The code was written primarily for my own use, so if you find it inefficient, please feel free to rewrite and improve it as needed.
I believe the key improvement is that many tasks can be done more efficiently and automatically by integrating Rhino/Grasshopper modeling—for example, performing meshing and defining boundary conditions during the modeling stage using STEP file data.
(It will be one of the future works)
If you would like to add features or modify aspects beyond the current code, please take a look at the Abaqus API documentation at [5].

**!!! PLEASE READ !!!**
