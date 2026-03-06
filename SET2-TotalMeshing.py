from abaqus import *
from abaqusConstants import *
from caeModules import *
import regionToolset
import math
import numpy

model = mdb.models['Model-1']
assembly = model.rootAssembly


all_edge_lengths = []

for part_name in model.parts.keys():
    part = model.parts[part_name]
    edges = part.edges
    
    for edge in edges:
        edge_length = edge.getSize(printResults=False)
        all_edge_lengths.append(edge_length)
        
min_edge_length = min(all_edge_lengths)
Edge_scaling_factor = 50000 # Edge scale control (Manual, avg, var, std)
Mesh_scaling_factor = 50

# # # # # # # # # # # # # # # # # # # 
# Min. Division Number (Even Number Recommended)
n = 10
# # # # # # # # # # # # # # # # # # # 

for part_name in model.parts.keys():
    part = model.parts[part_name]
    edges = part.edges
    edge_lengths = []
    
    for edge in edges:
        edge_length = edge.getSize(printResults=False)
        edge_lengths.append(edge_length)
        
    for edge, edge_length in zip(edges, edge_lengths):
        num_divisions = math.ceil((edge_length / min_edge_length) * n) 
        # Logarithm Mesh Scaling
        if edge_length / min_edge_length > Edge_scaling_factor:
            # num_divisions = math.ceil(math.log10(num_divisions) * Mesh_scaling_factor)
            num_divisions = math.ceil((edge_length / min_edge_length) * n / 4)
        
        ### Change to even number
        if num_divisions % 2 != 0: 
            num_divisions += 1

        ### If you want to simply give the same division counts to all edges
        # num_divisions = 50
        
        part.seedEdgeByNumber(edges=(edge,), number=num_divisions, constraint=FIXED)
        # print(f"Part {part_name}, Edge {edge.index}: Divided into {num_divisions} sections.")
    
    
    if part.cells:  # Solid Element Meshing
        part.setMeshControls(regions=part.cells, elemShape=HEX, technique=SWEEP, algorithm=MEDIAL_AXIS)
        elem_type = mesh.ElemType(elemCode=C3D20R, elemLibrary=STANDARD)
        part.setElementType(regions=(part.cells,), elemTypes=(elem_type,))
    else:  # Shell Element Meshing
        faces = part.faces
        part.setMeshControls(regions=faces, elemShape=QUAD, technique=FREE, algorithm=MEDIAL_AXIS)
        elem_type = mesh.ElemType(elemCode=S8R, elemLibrary=STANDARD)
        part.setElementType(regions=(faces,), elemTypes=(elem_type,))

# # # # # # # # # # # # # # # # # # # 
# # # # # OPTIONS

# # # # # SHELL
# elemShape= QUAD, QUAD_DOMINATED, TRI
# elemCode = S4R, S8R

# # # # # SOLID
# elemShape= HEX, HEX_DOMINATED, TET, WEDGE
# technique= FREE, STRUCTURED, SWEEP
# algorithm= ADVANCING_FRONT, MEDIAL_AXIS

# Meshing Quadratic
# Shell: Quad >> S8R, TRI >>STRI65
# Solid* HEX >> C3D20R

# # # # # OPTIONS
# # # # # # # # # # # # # # # # # # # 

for part_name in model.parts.keys():
    part = model.parts[part_name]
    part.generateMesh()

print(f"Minimum edge length: {min_edge_length}")
print("SET2!!! Meshing completed with edge-based division.")
