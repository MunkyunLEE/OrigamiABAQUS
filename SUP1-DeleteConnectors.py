from abaqus import *
from abaqusConstants import *
from caeModules import *
import regionToolset
import math

# Referencing Model Parts and Assembly
model = mdb.models['Model-1']
assembly = model.rootAssembly

# Function: Clear Connectors, Connector Sections, Features, Section Assignments
def clear_previous_features_and_sets():
    # Clear Connector Set
    for set_name in list(assembly.sets.keys()):
        if 'ConnectorSet' in set_name:
            del assembly.sets[set_name]
            
    for set_name in list(assembly.sets.keys()):
        if 'EdgeSet' in set_name:
            del assembly.sets[set_name]
    
    # Clear Feature Set
    for feat_name in list(assembly.features.keys()):
        if 'Wire' in feat_name:
            del assembly.features[feat_name]
    
    # Clear Connector Section Set
    sections_to_delete = [section_name for section_name in model.sections.keys() if 'ConnectorSection' in section_name]
    for section_name in sections_to_delete:
        del model.sections[section_name]
        
    # Clear Connector Section Assignments (Naming base)
    assignments_to_delete = [i for i, assignment in enumerate(assembly.sectionAssignments) 
                             if 'HingeConnectorSection' in assignment.sectionName]
    
    for index in sorted(assignments_to_delete, reverse=True):
        del assembly.sectionAssignments[index]
    
    print("Previous features, wire lines, connector sets, and connector sections have been cleared.")

# Operate Clear Function
clear_previous_features_and_sets()
