'''

By ashish Bahuguna 
IIT Roorkee
extracting the data from the odb file using element set 
'''

#
from abaqus import *
from abaqusConstants import *
import __main__
#
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior

def extract_data(odb,fileOutput,paramater,component,elementSets):
    '''
    parameters details
    1- odb is full path of the file 'C:/Users/Administrator/Job-60000.odb'
    2- fileOutput is output file contains xy data of the specifed engineering parameters such shear force (SF)
    3- paramater is desired engineering parameter which needs to be extracted it could be shear force (SF) moment (SM) stress (S) strain (E)
    4- component is compment of engineering parameter in x y and z direction
    5- elementSets is set of element
    '''
    o1 = session.openOdb(name=odb)
    session.viewports['Viewport: 1'].setValues(displayedObject=o1)
    session.linkedViewportCommands.setValues(_highlightLinkedViewports=False)
    odb = session.odbs[odb]
    xyList = xyPlot.xyDataListFromField(odb=odb, outputPosition=ELEMENT_NODAL, 
        variable=((paramater, INTEGRATION_POINT, ((COMPONENT, component), )), ), 
        elementSets=(elementSets, ))  
    #
    string_values = [xy.name for xy in xyList]
    #
    x0 = session.xyDataObjects[string_values[0]]
    x1 = session.xyDataObjects[string_values[1]]
    x2 = session.xyDataObjects[string_values[2]]
    x3 = session.xyDataObjects[string_values[3]]
    session.writeXYReport(fileName=fileOutput, xyData=(x0, x1, x2, x3))
    x0 = session.xyDataObjects[string_values[0]]
    x1 = session.xyDataObjects[string_values[1]]
    x2 = session.xyDataObjects[string_values[2]]
    x3 = session.xyDataObjects[string_values[3]]
    session.writeXYReport(fileName=fileOutput, xyData=(x0, x1, x2, x3))
    o1.close()
#
#
odb = 'C:/Users/Administrator/Job-60000.odb'
fileOutput = 'odb_data2.rpt'
paramater = 'SF'   
component = 'SF1'
elementSets = "mid span s1"
#calling funtion
extract_data(odb, fileOutput, paramater, component, elementSets)
