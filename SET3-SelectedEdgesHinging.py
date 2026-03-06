from abaqus import *
from abaqusConstants import *
from caeModules import *
import regionToolset
import math

# 모델과 어셈블리 참조
model = mdb.models['Model-1']
assembly = model.rootAssembly

# # # # # # # # # # # # RESET (If you want to reset and reconnect connectors, please turn ON this part.)
# 
# # # # # # Clear Function Codes
# 
# def clear_previous_features_and_sets():
#     for set_name in list(assembly.sets.keys()):
#         if 'ConnectorSet' in set_name:
#             del assembly.sets[set_name]
# 
#     for feat_name in list(assembly.features.keys()):
#         if 'Wire' in feat_name:
#             del assembly.features[feat_name]
# 
#     sections_to_delete = [section_name for section_name in model.sections.keys() if 'HingeConnectorSection_' in section_name]
#     for section_name in sections_to_delete:
#         del model.sections[section_name]
# 
#     assignments_to_delete = [i for i, assignment in enumerate(assembly.sectionAssignments) 
#                              if 'HingeConnectorSection' in assignment.sectionName]
# 
#     for index in sorted(assignments_to_delete, reverse=True):
#         del assembly.sectionAssignments[index]
# 
#     print("Previous features, wire lines, connector sets, and connector sections have been cleared.")
# 
# clear_previous_features_and_sets()
# 
# # # # # # # # # # # # RESET

# Round Function
def round_coordinates(node, precision=1):
    """Rounding Node Coordinates"""
    return tuple(round(coord, precision) for coord in node.coordinates)

# Create Connector
# !!!!!!Here you can set the stretching stiffness and rotational stiffness between connected edges.!!!!!!
def create_connector_section(edge_id, num_connected_nodes):
    """Generating Connector Sections, The stiffnesses are automatically considering the node counts"""
    Stretch_value = 1000000 / num_connected_nodes
    Bending_value = 0.001 / num_connected_nodes
    elasticity = connectorBehavior.ConnectorElasticity(behavior=LINEAR, 
                                                       coupling=UNCOUPLED, 
                                                       components=(1, 2, 3, 4, 5, 6),
                                                       table=((Stretch_value, Stretch_value, Stretch_value, Bending_value, Bending_value, Bending_value),))
    section_name = f'HingeConnectorSection_Edge{edge_id}' + '-' + manual_selection
    connector_section = model.ConnectorSection(name=section_name,
                                               assembledType=NONE, 
                                               translationalType=CARTESIAN, 
                                               rotationalType=ROTATION, 
                                               behaviorOptions=[elasticity])
    return section_name


########### ------------------------------------- Manual Edge Selection ---------------------------------------------
######## Please select the edges where you want to connect 
######## and generate the SET with the name of "Selected Edges" (or whatever you want) in the Abaqus Interface

manual_selection = 'SelectedEdges'
selected_edges = assembly.sets[manual_selection].edges
nodes_in_selected_edges = []
########### ------------------------------------- Manual Edge Selection ---------------------------------------------


for edge in selected_edges:
    nodes = edge.getNodes()
    for node in nodes:
        nodes_in_selected_edges.append(node)

node_pairs = set()  # (인스턴스 이름, 노드 라벨) 쌍을 저장할 집합 (중복 방지)

# 모든 노드를 동일한 좌표로 그룹핑
node_coords = {}
for node in nodes_in_selected_edges:
    rounded_coords = round_coordinates(node)
    if rounded_coords not in node_coords:
        node_coords[rounded_coords] = []
    node_coords[rounded_coords].append((node.instanceName, node.label))  # 인스턴스 이름과 노드 라벨 저장


# 동일한 좌표에 있는 모든 노드 쌍 생성
node_pairs = set()  # 중복 방지를 위한 집합

for coords, node_group in node_coords.items():
    if len(node_group) > 1:  # 동일한 위치에 노드가 2개 이상인 경우에만 처리
        for i in range(len(node_group)):
            for j in range(i + 1, len(node_group)):
                nodeA, nodeB = node_group[i], node_group[j]
                # 쌍을 정렬하여 (a, b)와 (b, a)의 중복 방지
                if nodeA != nodeB:
                    if (nodeA, nodeB) not in node_pairs and (nodeB, nodeA) not in node_pairs:
                        node_pairs.add((nodeA, nodeB))


# 사용된 노드 쌍을 추적하는 집합
used_node_pairs = set()
used_edge_list = []

# 각 엣지 k에 대해 엣지 위에 있는 노드들과 nodeA.label의 노드 위치를 비교
connector_id = 0
edge_id = 0  # 각 엣지별로 섹션 이름을 다르게 하기 위해 사용

for edge_id, edge in enumerate(selected_edges):
    edge_nodes = edge.getNodes()  # 엣지 k에 있는 모든 노드들
    num_connected_nodes = 0  # 동일한 위치에 있는 노드 개수를 저장할 변수

    edge_connected_pairs = set()  # 현재 엣지에서 연결된 노드 쌍

   # 엣지 위의 모든 노드들과 node_pairs에 있는 노드들 비교 (좌표를 반올림하여 비교)
    for node in edge_nodes:
        node_rounded_coords = round_coordinates(node)  # 노드 좌표 반올림
        for nodeA, nodeB in list(node_pairs):  # node_pairs는 (nodeA, nodeB) 쌍을 포함
            nodeA_rounded_coords = round_coordinates(assembly.instances[nodeA[0]].nodes.sequenceFromLabels([nodeA[1]])[0])
            if node_rounded_coords == nodeA_rounded_coords:  # 노드 A와 좌표가 동일한 경우
                # 중복되지 않은 쌍만 처리
                if (nodeA, nodeB) not in used_node_pairs:
                    # 동일한 위치에 있는 노드임을 확인
                    num_connected_nodes += 1
                    edge_connected_pairs.add((nodeA, nodeB))  # 현재 엣지에서 사용된 쌍 기록
                    
    # 커넥터 쌍의 총 개수가 4개 이상인 경우에만 커넥터 섹션 생성 (즉 그 밑에는 커넥터 섹션으로 보지 않음)
    if num_connected_nodes > 3:
        # 커넥터 섹션 생성
        section_name = create_connector_section(edge_id, num_connected_nodes)

        # 각 노드 쌍에 대해 커넥터 할당
        for nodeA, nodeB in edge_connected_pairs:
            point1 = assembly.instances[nodeA[0]].nodes.sequenceFromLabels([nodeA[1]])[0]
            point2 = assembly.instances[nodeB[0]].nodes.sequenceFromLabels([nodeB[1]])[0]

            # 커넥터 와이어 생성
            connector_wires = assembly.WirePolyLine(points=((point1, point2),), mergeType=SEPARATE, meshable=OFF)
            wire_name = 'Wire-1'
            feature_name = 'Wire' + manual_selection + '_' + str(connector_id)
            assembly.features.changeKey(fromName=wire_name, toName=feature_name)

            # 커넥터 세트 생성
            wire_set = assembly.Set(name='ConnectorSet' + '_' +  manual_selection + str(connector_id), edges=assembly.getFeatureEdges(connector_wires.name))

            # 커넥터 섹션 할당
            assembly.SectionAssignment(region=wire_set, sectionName=section_name)
          
            connector_id += 1
            
        used_edge_list.append(edge_id)
        
        # 사용된 노드 쌍을 node_pairs에서 제거
        used_node_pairs.update(edge_connected_pairs)


# 사용된 엣지들에 대해 엣지 세트 생성
for edge_id in used_edge_list:
    edge = selected_edges[edge_id]
    edge_nodes = edge.getNodes()
    edge_node_labels = [node.label for node in edge_nodes]
    edge_node_coords = [round_coordinates(node) for node in edge_nodes]  # 엣지 노드의 좌표 사용

    instance_name = None
    for instance in assembly.instances.values():
        # 각 인스턴스의 엣지와 현재 사용된 엣지의 노드 좌표를 비교
        for inst_edge in instance.edges:
            inst_edge_nodes = inst_edge.getNodes()
            inst_edge_node_coords = [round_coordinates(node) for node in inst_edge_nodes]

            # 노드 좌표가 동일하면 해당 인스턴스가 일치한다고 판단
            if edge_node_coords == inst_edge_node_coords:
                instance_name = instance.name
                break  # 인스턴스 확인되면 종료
        if instance_name:
            break
    
    # 인스턴스가 확인되었으면 노드 세트 생성
    if instance_name:
        edge_set_name = f"EdgeSet_{edge_id}" + '_' + manual_selection
        
        # 노드 세트 생성
        assembly.Set(name=edge_set_name, nodes=assembly.instances[instance_name].nodes.sequenceFromLabels(edge_node_labels))



print("Hinge connectors have been successfully created for nodes at the same locations.")
