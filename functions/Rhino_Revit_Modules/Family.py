# Enable Python support and load DesignScript library
import clr
clr.AddReference('RhinoInside.Revit')
clr.AddReference('RevitAPIUI')

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



def NewHorizontalProfileInstace(Document, TypeName, LocationKey, EndRefPlane, MirrorBoolean):
    
    listverticalplanes = ("A", "A.01", "B", "B.01", "B.02", "C", "C.01", "Center")

    verticalref = []

    for x in listverticalplanes:
        bip = BuiltInParameter.DATUM_TEXT
        provider = ParameterValueProvider(ElementId(bip))
        evaluator = FilterStringEquals()
        rule = FilterStringRule(provider, evaluator, x, False)
        filter = ElementParameterFilter(rule)
        all = FilteredElementCollector(Document).OfClass(ReferencePlane).WherePasses(filter).FirstElement()
        verticalref.append(all)
    


    listhorizontalplanes = ("Axis", "Ext. Axis 1", "Ext. Axis 2", "Ext. Axis 3")

    horizontalref = []

    for x in listhorizontalplanes:
        bip = BuiltInParameter.DATUM_TEXT
        provider = ParameterValueProvider(ElementId(bip))
        evaluator = FilterStringEquals()
        rule = FilterStringRule(provider, evaluator, x, False)
        filter = ElementParameterFilter(rule)
        hall = FilteredElementCollector(Document).OfClass(ReferencePlane).WherePasses(filter).FirstElement()
        horizontalref.append(hall)

    horizontallines = []

    intviewlisthorizontalplanes = ("1", "1.01", "2", "2.01","2.02", "3", "3.01")

    intviewhorizontalref = []

    for x in intviewlisthorizontalplanes:
        bip = BuiltInParameter.DATUM_TEXT
        provider = ParameterValueProvider(ElementId(bip))
        evaluator = FilterStringEquals()
        rule = FilterStringRule(provider, evaluator, x, False)
        filter = ElementParameterFilter(rule)
        intvhall = FilteredElementCollector(Document).OfClass(ReferencePlane).WherePasses(filter).FirstElement()
        intviewhorizontalref.append(intvhall)

    pts = []
    for i in verticalref:
        equis = (i.BubbleEnd).X
        for j in horizontalref:
            ye = (j.BubbleEnd).Y
            for k in intviewhorizontalref:
                zeta = (k.BubbleEnd).Z
                pts.append(XYZ(equis,ye,zeta))

    keys = []
    for i in listverticalplanes:
        for j in listhorizontalplanes:
            for k in intviewlisthorizontalplanes:
                keys.append(''.join([i,',',j,',',k]))

    ################ Dictionary ptsdi
    ptsdi = {keys[i]:pts[i] for i in range(len(keys))}
    ################

    keysname = listverticalplanes+listhorizontalplanes+intviewlisthorizontalplanes
    refall = verticalref+horizontalref+intviewhorizontalref

    ################ Dictionary refplanedi
    refplanedi = {keysname[i]:refall[i] for i in range(len(keysname))}
    ################

    bip = BuiltInParameter.SYMBOL_NAME_PARAM
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, TypeName, False)
    filter = ElementParameterFilter(rule)
    collector = FilteredElementCollector(Document).OfCategory(BuiltInCategory.OST_GenericModel).OfClass(FamilySymbol).WherePasses(filter).FirstElement()

    bip = BuiltInParameter.VIEW_NAME
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, "Ref. Level", False)
    filter = ElementParameterFilter(rule)
    reflevel = FilteredElementCollector(Document).OfClass(ViewPlan).WherePasses(filter).FirstElement()

    bip = BuiltInParameter.VIEW_NAME
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, "Interior", False)
    filter = ElementParameterFilter(rule)
    interior = FilteredElementCollector(Document).OfClass(ViewSection).WherePasses(filter).FirstElement()

    ##################New Family Instance
    t1 = TransactionManager.Instance
    t1.EnsureInTransaction(Document)
    
    notVert = collector.Family.get_Parameter(BuiltInParameter.FAMILY_ALWAYS_VERTICAL).Set(0)
    horizontal = collector.Family.get_Parameter(BuiltInParameter.FAMILY_WORK_PLANE_BASED).Set(1)
    
    collector.Activate()

    startsloc = ptsdi[LocationKey]
    txt = LocationKey.split(",")

    endsloc = refplanedi[EndRefPlane]

    ref = refplanedi[txt[0]].GetReference()
    scpoint = XYZ(0, 0 , 0)
    newobj = Document.FamilyCreate.NewFamilyInstance(ref, startsloc, scpoint, collector)

    instance = []
    if MirrorBoolean == True:
        mirror = ElementTransformUtils.MirrorElement(Document, newobj.Id, refplanedi[txt[2]].GetPlane())
        filter = ElementClassFilter(FamilyInstance)
        allins = FilteredElementCollector(Document).WherePasses(filter).ToElements()
        ids = []
        for x in allins:
            ids.append(x.Id)
        obj = Document.GetElement(ids[-1])
        delete = Document.Delete(ids[-2])
        instance.append(obj)
    else:
        instance.append(newobj)

    starts = (refplanedi[txt[0]].BubbleEnd).X
    ends = (endsloc.BubbleEnd).X
    heigthprof = ends - starts

    parameter = instance[0].GetParameters("Mullion length")
    setheight = parameter[0].Set(heigthprof)

    #End Transaction
    TransactionManager.ForceCloseTransaction(t1)

    horref = instance[0].GetReferenceByName("Center (Left/Right)")
    vertref = instance[0].GetReferenceByName("Center (Front/Back)")
    lengthref = instance[0].GetReferenceByName("top")
    baseref = instance[0].GetReferenceByName("bottom")

    firstref = refplanedi[txt[2]].GetReference()
    scnref = refplanedi[txt[1]].GetReference()
    thirdref = endsloc.GetReference()
    fourthref = refplanedi[txt[0]].GetReference()

    t2 = TransactionManager.Instance
    t2.EnsureInTransaction(Document)

    align = Document.FamilyCreate.NewAlignment(interior, firstref, horref)
    align2 = Document.FamilyCreate.NewAlignment(reflevel, scnref, vertref)
    align3 = Document.FamilyCreate.NewAlignment(reflevel, thirdref, lengthref)
    align4 = Document.FamilyCreate.NewAlignment(reflevel, fourthref, baseref)

    #End Transaction
    TransactionManager.ForceCloseTransaction(t2)

    return instance[0]

def NewVerticalProfileInstace(Document, TypeName, LocationKey, EndRefPlane, MirrorBoolean):
   
    listverticalplanes = ("A", "A.01", "B", "B.01", "B.02", "C", "C.01", "Center")
    
    verticalref = []
    
    for x in listverticalplanes:
        bip = BuiltInParameter.DATUM_TEXT
        provider = ParameterValueProvider(ElementId(bip))
        evaluator = FilterStringEquals()
        rule = FilterStringRule(provider, evaluator, x, False)
        filter = ElementParameterFilter(rule)
        all = FilteredElementCollector(Document).OfClass(ReferencePlane).WherePasses(filter).FirstElement()
        verticalref.append(all)
         
    # ref = C.GetReference()
    
    listhorizontalplanes = ("Axis", "Ext. Axis 1", "Ext. Axis 2", "Ext. Axis 3")
    
    horizontalref = []

    for x in listhorizontalplanes:
        bip = BuiltInParameter.DATUM_TEXT
        provider = ParameterValueProvider(ElementId(bip))
        evaluator = FilterStringEquals()
        rule = FilterStringRule(provider, evaluator, x, False)
        filter = ElementParameterFilter(rule)
        hall = FilteredElementCollector(Document).OfClass(ReferencePlane).WherePasses(filter).FirstElement()
        horizontalref.append(hall)
    
    horizontallines = []
    
    intviewlisthorizontalplanes = ("1", "1.01", "2", "2.01","2.02", "3", "3.01")
    
    intviewhorizontalref = []
    
    for x in intviewlisthorizontalplanes:
        bip = BuiltInParameter.DATUM_TEXT
        provider = ParameterValueProvider(ElementId(bip))
        evaluator = FilterStringEquals()
        rule = FilterStringRule(provider, evaluator, x, False)
        filter = ElementParameterFilter(rule)
        intvhall = FilteredElementCollector(Document).OfClass(ReferencePlane).WherePasses(filter).FirstElement()
        intviewhorizontalref.append(intvhall)
    
    pts = []
    for i in verticalref:
        equis = (i.BubbleEnd).X
        for j in horizontalref:
            ye = (j.BubbleEnd).Y
            for k in intviewhorizontalref:
                zeta = (k.BubbleEnd).Z
                pts.append(XYZ(equis,ye,zeta))
    
    keys = []
    for i in listverticalplanes:
        for j in listhorizontalplanes:
            for k in intviewlisthorizontalplanes:
                keys.append(''.join([i,',',j,',',k]))
    
    ################ Dictionary ptsdi
    ptsdi = {keys[i]:pts[i] for i in range(len(keys))}
    ################
    
    keysname = listverticalplanes+listhorizontalplanes+intviewlisthorizontalplanes
    refall = verticalref+horizontalref+intviewhorizontalref
    
    ################ Dictionary refplanedi
    refplanedi = {keysname[i]:refall[i] for i in range(len(keysname))}
    ################
    
    bip = BuiltInParameter.SYMBOL_NAME_PARAM
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, TypeName, False)
    filter = ElementParameterFilter(rule)
    collector = FilteredElementCollector(Document).OfCategory(BuiltInCategory.OST_GenericModel).OfClass(FamilySymbol).WherePasses(filter).FirstElement()
    
    bip = BuiltInParameter.VIEW_NAME
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, "Ref. Level", False)
    filter = ElementParameterFilter(rule)
    reflevel = FilteredElementCollector(Document).OfClass(ViewPlan).WherePasses(filter).FirstElement()
    
    bip = BuiltInParameter.VIEW_NAME
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, "Interior", False)
    filter = ElementParameterFilter(rule)
    interior = FilteredElementCollector(Document).OfClass(ViewSection).WherePasses(filter).FirstElement()
    
    ##################New Family Instance
    t1 = TransactionManager.Instance
    t1.EnsureInTransaction(Document)
    
    collector.Activate()
    
    #LocationKey = "F,1b,3"
    startsloc = ptsdi[LocationKey]
    txt = LocationKey.split(",")
    #EndRefPlane = "D"
    endsloc = refplanedi[EndRefPlane]
    
    newobj = Document.FamilyCreate.NewFamilyInstance(startsloc, collector, 0)
    
    #MirrorBoolean = False
    
    instance = []
    if MirrorBoolean == True:
        mirror = ElementTransformUtils.MirrorElement(Document, newobj.Id, refplanedi[txt[0]].GetPlane())
        filter = ElementClassFilter(FamilyInstance)
        allins = FilteredElementCollector(Document).WherePasses(filter).ToElements()
        ids = []
        for x in allins:
            ids.append(x.Id)
        obj = Document.GetElement(ids[-1])
        delete = Document.Delete(ids[-2])
        instance.append(obj)
    else:
        instance.append(newobj)
    
    starts = (refplanedi[txt[2]].BubbleEnd).Z
    ends = (endsloc.BubbleEnd).Z
    heigthprof = ends - starts
    
    parameter = instance[0].GetParameters("Mullion length")
    setheight = parameter[0].Set(heigthprof)
    
    #End Transaction
    TransactionManager.ForceCloseTransaction(t1)
    
    centerref = instance[0].GetReferenceByName("Center (Left/Right)")
    hcenterref = instance[0].GetReferenceByName("Center (Front/Back)")
    heightref = instance[0].GetReferenceByName("top")
    baseref = instance[0].GetReferenceByName("bottom")
    
    firstref = refplanedi[txt[0]].GetReference()
    scnref = refplanedi[txt[1]].GetReference()
    thirdref = endsloc.GetReference()
    fourthref = refplanedi[txt[2]].GetReference()
    
    t2 = TransactionManager.Instance
    t2.EnsureInTransaction(Document)
    
    align = Document.FamilyCreate.NewAlignment(reflevel, firstref, centerref)
    align2 = Document.FamilyCreate.NewAlignment(reflevel, scnref, hcenterref)
    align3 = Document.FamilyCreate.NewAlignment(interior, thirdref, heightref)
    align4 = Document.FamilyCreate.NewAlignment(interior, fourthref, baseref)
    
    #End Transaction
    TransactionManager.ForceCloseTransaction(t2)
    
    return instance[0]
