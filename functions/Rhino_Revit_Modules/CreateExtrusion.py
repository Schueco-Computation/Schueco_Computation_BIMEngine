# Enable Python support and load DesignScript library
import clr

clr.AddReference('RhinoInside.Revit')
clr.AddReference('RevitAPIUI')

import RhinoInside as ri
clr.AddReference('ProtoGeometry')

import rhinoscriptsyntax as rs
import Rhino
from Rhino import Geometry as rg
import RhinoInside as ri
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

#Import RevitAPI
clr.AddReference("RevitAPI")
#import Autodesk.Revit.DB as re
from Autodesk.Revit.DB import*
import Autodesk.Revit.Creation as oCreate
import Autodesk.Revit.ApplicationServices.Application 

# rhino.inside utilities
from RhinoInside.Revit import Revit, Convert
clr.ImportExtensions(Convert.Geometry)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

##########################################
#Get Mullion length

def NewProfile(newfamily, rvtlines, ObjectName, locationref, FrameProfOrVent):
    #CONDITIONAL FRAME OR PROFILE
    dim = []
    if FrameProfOrVent == "Frame":
        bip = BuiltInParameter.DIM_LABEL
        provider = ParameterValueProvider(ElementId(bip))
        evaluator = FilterStringEquals()
        rule = FilterStringRule(provider, evaluator, "Length", False)
        filter = ElementParameterFilter(rule)
        mullionlength = FilteredElementCollector(newfamily).OfClass(Dimension).WherePasses(filter).FirstElement()

        name = mullionlength.get_Parameter(BuiltInParameter.DIM_VALUE_LENGTH)
        paramvalue = name.AsDouble()
        

        object = rs.ObjectsByName(ObjectName)
        pts = rs.BoundingBox(object)

        distanceofinsertion = []
        if pts[0][0] <= -52:
            distanceofinsertion.append(pts[1][0])
        else:
            distanceofinsertion.append(-pts[0][0])
        
        dstinsertion = round(distanceofinsertion[0], 0)

        value = paramvalue+((dstinsertion*2)/304.80)
        t0 = TransactionManager.Instance
        t0.EnsureInTransaction(newfamily)
        
        parametro= newfamily.FamilyManager.get_Parameter("Not visible frame width")
        parametroset= newfamily.FamilyManager.Set(parametro,dstinsertion/304.80)
        
        #End Transaction
        TransactionManager.ForceCloseTransaction(t0)
        dim.append(value)
        
    elif FrameProfOrVent == "Vent":
        bip = BuiltInParameter.DIM_LABEL
        provider = ParameterValueProvider(ElementId(bip))
        evaluator = FilterStringEquals()
        rule = FilterStringRule(provider, evaluator, "Panel height", False)
        filter = ElementParameterFilter(rule)
        mullionlength = FilteredElementCollector(newfamily).OfClass(Dimension).WherePasses(filter).FirstElement()

        name = mullionlength.get_Parameter(BuiltInParameter.DIM_VALUE_LENGTH)
        paramvalue = name.AsDouble()
        dim.append(paramvalue)
    else:
        bip = BuiltInParameter.DIM_LABEL
        provider = ParameterValueProvider(ElementId(bip))
        evaluator = FilterStringEquals()
        rule = FilterStringRule(provider, evaluator, "Mullion length", False)
        filter = ElementParameterFilter(rule)
        mullionlength = FilteredElementCollector(newfamily).OfClass(Dimension).WherePasses(filter).FirstElement()

        name = mullionlength.get_Parameter(BuiltInParameter.DIM_VALUE_LENGTH)
        paramvalue = name.AsDouble()
        dim.append(paramvalue)
        
    #CONDITIONAL FINISH
    
    #Create Curve Array
    carray = CurveArray()
    carrarray = CurveArrArray()
    
    #Loop through lines
    for line in rvtlines:
        carray.Append(line)
    carrarray.Append(carray)

    #Get top and bottom planes
    bip = BuiltInParameter.DATUM_TEXT
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, "top", False)
    filter = ElementParameterFilter(rule)
    planetop = FilteredElementCollector(newfamily).OfClass(ReferencePlane).WherePasses(filter).FirstElement()

    ref2 = planetop.GetReference()

    rule2 = FilterStringRule(provider, evaluator, "bottom", False)
    filter2 = ElementParameterFilter(rule2)
    planebase = FilteredElementCollector(newfamily).OfClass(ReferencePlane).WherePasses(filter2).FirstElement()
    
    t1 = TransactionManager.Instance
    t1.EnsureInTransaction(newfamily)
    
    #Creating SketchPlane
    sketchplane = SketchPlane.Create(newfamily, planebase.Id)
    
    #Creating extrusion
    solid = newfamily.FamilyCreate.NewExtrusion(True, carrarray, sketchplane, dim[0])

    opt = Options()
    opt.ComputeReferences = True

    geometry = solid.get_Geometry(opt)
    for g in geometry:
        try:
            fa = g.Faces[0]
        
        except:
                ""

    #Lock Alignment
    topface = fa.Reference

    #Finding the view
    bip = BuiltInParameter.VIEW_NAME
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, "Front", False)
    filter = ElementParameterFilter(rule)
    frontview = FilteredElementCollector(newfamily).OfClass(ViewSection).WherePasses(filter).FirstElement()

    align = newfamily.FamilyCreate.NewAlignment(frontview, topface, ref2)

    # Add Location reference

    locationreference= newfamily.FamilyManager.get_Parameter("LocationRef")
    locationreferenceset= newfamily.FamilyManager.Set(locationreference,locationref)

    #End Transaction
    TransactionManager.ForceCloseTransaction(t1)
    
    # Assign your output to the OUT variable.
    return solid