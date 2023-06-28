"""
-------------------------------------------------------------------------------

Created on Thu Jun  1 14:27:01 2023

@author: Ashish Bahuguna
         Dept. of Earthquake Engineering IIT Roorkee

this function can be used to post-processing of ABAQUS ODB file
-------------------------------------------------------------------------------
"""
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


def extract_data(job_name, fileOutput, parameter, component, elementSets):
    odb_path = 'C:/Temp/Job-' + str(job_name) + '.odb'
    o1 = session.openOdb(name=odb_path)
    session.viewports['Viewport: 1'].setValues(displayedObject=o1)
    session.linkedViewportCommands.setValues(_highlightLinkedViewports=False)
    odb = session.odbs[odb_path]
    xyList = xyPlot.xyDataListFromField(odb=odb, outputPosition=ELEMENT_NODAL, 
        variable=((parameter, INTEGRATION_POINT, ((COMPONENT, component), )), ), 
        elementSets=(elementSets, ))  
    #
    string_values = [xy.name for xy in xyList]
    #
    x0 = session.xyDataObjects[string_values[0]]
    session.writeXYReport(fileName=fileOutput, xyData=(x0))
    o1.close()

job_names = [1100, 55000, 112200, 83600, 16500, 36300, 129800, 128699, 27500]
fileOutput = 'odb_data2.rpt'
parameter_a = ['SF', 'SF', 'SF', 'SF', 'SM', 'SM', 'SM', 'SM', 'SM']
component_a = ['SF4', 'SF4', 'SF4', 'SF2', 'SM1', 'SM1', 'SM1', 'SM2', 'SM1']
elementSets_a = ["left corner s1", "right corner s1", "left corner s2", "mid wall", "left corner s1", "right corner s1", "left corner s2", "mid wall", "mid span s1"]

# Iterate over each job name and extract data
for job_name, parameter, component, elementSets in zip(job_names, parameter_a, component_a, elementSets_a):
    extract_data(job_name, fileOutput, parameter, component, elementSets)


import pandas as pd
data = pd.read_csv('C:/Temp/odb_data2.rpt', sep='\s+')
appended_data = pd.DataFrame()
for i in range(0, len(data), 12):
    subset = data.iloc[i:i+12].reset_index(drop=True)
    appended_data = pd.concat([appended_data, subset], axis=1)
print(appended_data)
