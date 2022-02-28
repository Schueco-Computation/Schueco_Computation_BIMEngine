# Enable Python support and load DesignScript library
import clr

clr.AddReference('RhinoInside.Revit')
clr.AddReference('RevitAPIUI')

import RhinoInside as ri
clr.AddReference('ProtoGeometry')

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

def NewProfile(newfamily, rvtlines, locationref, FrameOrProf):
    #CONDITIONAL FRAME OR PROFILE
    dim = []
    if FrameOrProf == "Frame":
        bip = BuiltInParameter.DIM_LABEL
        provider = ParameterValueProvider(ElementId(bip))
        evaluator = FilterStringEquals()
        rule = FilterStringRule(provider, evaluator, "Length", False)
        filter = ElementParameterFilter(rule)
        mullionlength = FilteredElementCollector(newfamily).OfClass(Dimension).WherePasses(filter).FirstElement()

        name = mullionlength.get_Parameter(BuiltInParameter.DIM_VALUE_LENGTH)
        paramvalue = name.AsDouble()
    
        value = paramvalue+(24/304.80)
        dim.append(value)
        
    if FrameProfOrVent == "Vent":
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