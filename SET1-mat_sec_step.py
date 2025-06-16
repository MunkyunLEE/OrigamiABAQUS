from abaqus import *
from abaqusConstants import *
from caeModules import *
import regionToolset

# Referencing Model and Parts
model = mdb.models['Model-1']

# Aluminium
# material = model.Material(name='AL')
# material.Density(table=((2.7e-9, ), ))
# material.Elastic(table=((73100, 0.35), ))
# material.Plastic(table=((160,0),(340,0.3)))

# Plywood
# material = model.Material(name='Ply')
# material.Density(table=((5.52e-10, ), ))
# material.Elastic(table=((7700, 0.25), ))

# Polypropylene-Elastic
material = model.Material(name='PP-Elastic')
material.Density(table=((9.05e-10, ), ))
material.Elastic(table=((1134, 0.38), ))

# Polypropylene-Plastic
material = model.Material(name='PP-Plastic')
material.Density(table=((9.05e-10, ), ))
material.Elastic(table=((1134, 0.38), ))
material.Plastic(table=((10.64,0),(14.82,0.01),(23.38,0.04),(26.97,0.08),(28.06,0.24),(28.06,0.34),(49.76,0.94)))

mat_thick = 5


# Section Generation (Shell elements)
shell_section = model.HomogeneousShellSection(name='ShellSection',
                                              preIntegrate=OFF,
                                              material='PP-Elastic',
                                              thicknessType=UNIFORM,
                                              thickness=mat_thick,
                                              thicknessField='',
                                              nodalThicknessField='',
                                              idealization=NO_IDEALIZATION,
                                              poissonDefinition=DEFAULT,
                                              thicknessModulus=None,
                                              temperature=GRADIENT,
                                              useDensity=OFF,
                                              integrationRule=SIMPSON,
                                              numIntPts=5)

# Section Generation (Solid)
solid_section = model.HomogeneousSolidSection(name='SolidSection',
                                              material='Ply',
                                              thickness=None)

# Assembly Generation and Assignment
assembly = model.rootAssembly
    
for part_name in model.parts.keys():
    part = model.parts[part_name]
    
    if part.cells:  # Assignment
        region = part.Set(cells=part.cells, name=part_name + '_SolidSet')  # if Cell case
        part.SectionAssignment(region=region, sectionName='SolidSection')  # Assigning Solid Sections
    else:
        region = part.Set(faces=part.faces, name=part_name + '_ShellSet')  # if Face case
        part.SectionAssignment(region=region, sectionName='ShellSection')  # Assigning Shell Sections
    
    assembly.Instance(name=part_name + '_Inst', part=part, dependent=ON)
   
# ############ Static, General Step
# model.StaticStep(name='StaticStep', previous='Initial', nlgeom=ON, maxNumInc=250)
# model.steps['StaticStep'].setValues(initialInc=1e-3, minInc=1e-15, maxInc=1)

# ############ Static, Riks Step
# model.StaticRiksStep(name='RiksStep', previous='Initial', nlgeom=ON, maxNumInc=100)
# model.steps['RiksStep'].setValues(initialArcInc=0.01, minArcInc=1e-20, maxArcInc=1, totalArcLength=1.0)

# ############ EigenValue, Frequency Step
model.FrequencyStep(name='Frequency', previous='Initial', numEigen=10)

# ############ Dynamic Implicit, Quasi-static
model.ImplicitDynamicsStep(name='Quasi-static', previous='Frequency', timePeriod=10, nlgeom=ON, application=QUASI_STATIC, maxNumInc=1000)
model.steps['Quasi-static'].setValues(initialInc=1e-3, minInc=1e-8)


# ############ Amplitude Setting
model.TabularAmplitude(name='Load', timeSpan=STEP, data=((0,0), (10,1)))
model.TabularAmplitude(name='Bias', timeSpan=STEP, data=((0,0), (0.1,1), (0.2,0)))

print("SET1!!! Material, Section, Instance, and Step are completed")
