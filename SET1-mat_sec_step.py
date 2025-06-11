from abaqus import *
from abaqusConstants import *
from caeModules import *
import regionToolset

# 모델과 파트 참조
model = mdb.models['Model-1']

# 재료 생성
# Aluminium
# material = model.Material(name='AL')
# material.Density(table=((2.7e-9, ), ))
# material.Elastic(table=((73100, 0.35), ))
# # material.Plastic(table=((160,0),(340,0.3)))

# # Plywood
# material = model.Material(name='Ply')
# material.Density(table=((5.52e-10, ), ))
# material.Elastic(table=((7700, 0.25), ))

# PDPPZ-100 Isotropic
material = model.Material(name='PDPPZ-100')
material.Density(table=((2e-10, ), ))
material.Elastic(table=((316.5, 0.42), ))

# PDPPZ-100 Orthotropic
material = model.Material(name='PDPPZ-100_Ortho')
material.Density(table=((2e-10, ), ))
material.Elastic(type=ENGINEERING_CONSTANTS,table=((105.5, 105.5, 316.5, 0.42, 0.12, 0.12, 37.148, 74.615, 74.615), ))
# material.Plastic(table=((3.1,0),(4.4,0.0269),(3.5,0.06)))

mat_thick = 5


# 섹션 생성(Shell, Thickness control)
shell_section = model.HomogeneousShellSection(name='ShellSection',
                                              preIntegrate=OFF,
                                              material='PDPPZ-100_Ortho',
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

# 섹션 생성(Solid)
solid_section = model.HomogeneousSolidSection(name='SolidSection',
                                              material='Ply',
                                              thickness=None)

# 어셈블리 생성
assembly = model.rootAssembly
    
for part_name in model.parts.keys():
    part = model.parts[part_name]
    
    if part.cells:  # 셀이 존재하는 경우 솔리드 섹션 할당
        region = part.Set(cells=part.cells, name=part_name + '_SolidSet')  # 셀 사용
        part.SectionAssignment(region=region, sectionName='SolidSection')  # 솔리드 섹션 할당
    else:
        region = part.Set(faces=part.faces, name=part_name + '_ShellSet')  # 면 사용
        part.SectionAssignment(region=region, sectionName='ShellSection')  # 쉘 섹션 할당
    
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
model.steps['Quasi-static'].setValues(initialInc=1e-5, minInc=1e-8)


# ############ Amplitude Setting
model.TabularAmplitude(name='Load', timeSpan=STEP, data=((0,0), (10,1)))
model.TabularAmplitude(name='Bias', timeSpan=STEP, data=((0,0), (0.1,1), (0.2,0)))

print("SET1!!! Material, Section, Instance, and Step are completed")