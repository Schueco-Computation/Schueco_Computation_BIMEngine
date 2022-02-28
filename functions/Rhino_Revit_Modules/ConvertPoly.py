# Enable Python support and load DesignScript library
import clr

clr.AddReference('RhinoInside.Revit')

import rhinoscriptsyntax as rs
import Rhino
from Rhino import Geometry as rg
import RhinoInside as ri
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# rhino.inside utilities
from RhinoInside.Revit import Revit, Convert
clr.ImportExtensions(Convert.Geometry)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# The inputs to this node will be stored as a list in the IN variables.

##########################################
#Select a layer and convert From polyline in Rhino to lines in Revit

# Select a layer in Rhino
def ToRvtline(objectname):
    obj = rs.ObjectsByName(objectname)
    
    #selected objects
    
    profile = []

    rs.SelectObjects(obj)
    ObjId = rs.SelectedObjects(include_lights=False, include_grips=False)
    for obj in ObjId:
        lines = rs.coercecurve(obj)
        profile.append(lines)

    explode = rs.ExplodeCurves(profile)
    unselect = rs.UnselectObjects(ObjId)
    # coerce

    profcoerce = []

    for prof in explode:
        profco = rs.coercecurve(prof)
        profcoerce.append(profco)

    rvtlines = []

    for ex in profcoerce:
        lines = ri.Revit.Convert.Geometry.GeometryEncoder.ToCurve(ex)
        rvtlines.append(lines)
    # Assign your output to the OUT variable.
    return rvtlines


