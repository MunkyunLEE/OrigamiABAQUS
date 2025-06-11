from abaqus import *
from abaqusConstants import *
from caeModules import *
import regionToolset
import math
import numpy

# 모델 참조
model = mdb.models['Model-1']
assembly = model.rootAssembly

# 모든 파트의 엣지를 찾고, 엣지 길이 계산 및 분할 수 설정

all_edge_lengths = []

for part_name in model.parts.keys():
    part = model.parts[part_name]
    edges = part.edges
    
    for edge in edges:
        # 각 엣지의 길이 계산
        edge_length = edge.getSize(printResults=False)
        all_edge_lengths.append(edge_length)
        
min_edge_length = min(all_edge_lengths)
Edge_scaling_factor = 50000 # Edge scale control (Manual, avg, var, std)
# print("Average:", numpy.mean(all_edge_lengths))
# print("Variance:", numpy.var(all_edge_lengths))
# print("Standard:", numpy.std(all_edge_lengths))
Mesh_scaling_factor = 50
n = 10  # 최소 엣지에 대한 분할 수 (Even Number Recommended)


for part_name in model.parts.keys():
    part = model.parts[part_name]
    edges = part.edges
    edge_lengths = []
    
    for edge in edges:
        # 각 엣지의 길이 계산
        edge_length = edge.getSize(printResults=False)
        edge_lengths.append(edge_length)
        
        # 각 엣지에 대해 비율에 따라 분할 수 설정
    for edge, edge_length in zip(edges, edge_lengths):
        num_divisions = math.ceil((edge_length / min_edge_length) * n)  # 소수점 올림
        # Logarithm Mesh Scaling
        if edge_length / min_edge_length > Edge_scaling_factor:
            # num_divisions = math.ceil(math.log10(num_divisions) * Mesh_scaling_factor)
            num_divisions = math.ceil((edge_length / min_edge_length) * n / 4)  # 소수점 올림

        # Bi-Linear Mesh Scaling
        # if edge_length / min_edge_length > Edge_scaling_factor:
        #     num_divisions = math.ceil(num_divisions / Mesh_scaling_factor)
        
        if num_divisions % 2 != 0:  # 홀수일 경우
            num_divisions += 1  # 1을 더해 짝수로 만듦
        
        part.seedEdgeByNumber(edges=(edge,), number=num_divisions, constraint=FIXED)
        # print(f"Part {part_name}, Edge {edge.index}: Divided into {num_divisions} sections.")
    
    
    if part.cells:  # 셀이 존재하는 경우 Solid Element Meshing
        part.setMeshControls(regions=part.cells, elemShape=HEX, technique=SWEEP, algorithm=MEDIAL_AXIS)
        elem_type = mesh.ElemType(elemCode=C3D20R, elemLibrary=STANDARD)  # TET 2차 요소
        part.setElementType(regions=(part.cells,), elemTypes=(elem_type,))
    else:  # Face 존재하는 경우 Shell Element Meshing
        faces = part.faces
        part.setMeshControls(regions=faces, elemShape=QUAD, technique=FREE, algorithm=MEDIAL_AXIS)
        elem_type = mesh.ElemType(elemCode=S8R, elemLibrary=STANDARD)  # QUAD 2차 요소
        part.setElementType(regions=(faces,), elemTypes=(elem_type,))

# SHELL
# elemShape= QUAD, QUAD_DOMINATED, TRI
# SOLID
# elemShape= HEX, HEX_DOMINATED, TET, WEDGE
# technique= FREE, STRUCTURED, SWEEP
# algorithm= ADVANCING_FRONT, MEDIAL_AXIS
# Meshing Quadratic
# Shell: Quad >> S8R, TRI >>STRI65
# Solid* HEX >> C3D20R


# 메쉬 생성
for part_name in model.parts.keys():
    part = model.parts[part_name]
    part.generateMesh()

print(f"Minimum edge length: {min_edge_length}")
print("SET2!!! Meshing completed with edge-based division.")