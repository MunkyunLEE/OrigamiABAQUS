from abaqus import *
from abaqusConstants import *
from caeModules import *
import regionToolset
import math

# 모델과 어셈블리 참조
model = mdb.models['Model-1']
assembly = model.rootAssembly

# 기존 피쳐, 와이어, 커넥터 세트, 커넥터 섹션 삭제 함수
def clear_previous_features_and_sets():
    # 기존 커넥터 세트 삭제
    for set_name in list(assembly.sets.keys()):
        if 'ConnectorSet' in set_name:
            del assembly.sets[set_name]
            
    for set_name in list(assembly.sets.keys()):
        if 'EdgeSet' in set_name:
            del assembly.sets[set_name]
    
    # 기존 피쳐 삭제
    for feat_name in list(assembly.features.keys()):
        if 'Wire' in feat_name:
            del assembly.features[feat_name]
    
    # 기존 커넥터 섹션 삭제
    sections_to_delete = [section_name for section_name in model.sections.keys() if 'ConnectorSection' in section_name]
    for section_name in sections_to_delete:
        del model.sections[section_name]
        
    # 기존 Section Assignment 삭제 (이름으로 삭제)
    assignments_to_delete = [i for i, assignment in enumerate(assembly.sectionAssignments) 
                             if 'HingeConnectorSection' in assignment.sectionName]
    
    # 이름 조건에 맞는 Section Assignment 삭제
    for index in sorted(assignments_to_delete, reverse=True):
        del assembly.sectionAssignments[index]
    
    print("Previous features, wire lines, connector sets, and connector sections have been cleared.")

# 피처, 와이어, 커넥터 세트, 커넥터 섹션 삭제
clear_previous_features_and_sets()