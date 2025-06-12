# OrigamiABAQUS
Origami crease(hinge) modeling for Abaqus simulation
This code connects nodes to nodes, which are located at the same location
In SET3, this code basically involves the linear stiffness setting for translation and rotation stiffness between nodes.
Also, you can add any other complex connector settings in the ABAQUS interface (connector section) or code editor, such as damping, plastic, rotation limits, etc.
The basic concept[1] and further detailed explanation[2,3] are included in the reference papers.

SET1: 

SET2:

SET3:

SUP1: 

**REFERENCES**

[1] Munkyun Lee and Tomohiro Tachi, “Design and Evaluation of Compliant Hinges for Deployable Thick Origami Structures”, Journal of the International Association for Shell and Spatial Structures (IASS), No. 65(4), pp.238-247. 2024.12
DOI: https://doi.org/10.20898/j.iass.2024.015
  
[2] Munkyun Lee, Joseph M. Gattas, and Tomohiro Tachi, “Multistable Curved-crease Origami Blocks for Reconfigurable Modular Building System”, Proceedings of International Association for Shell and Spatial Structures (IASS) Annual Symposia, Mexico City, Mexico, 2025.10

[3] Felix Dellinger, Martin Kilian, Munkyun Lee, Christian Muller, Georg Nawratil, Tomohiro Tachi, and Kiumars Sharifmoghaddam, “Snapping Deployable Toroids for Modular Gridshells”, Proceedings of the 2025 ACM SIGGRAPH Asia, Hong Kong, China, 2025.12
