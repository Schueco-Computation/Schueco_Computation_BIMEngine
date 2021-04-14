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
from Autodesk.Revit.UI import *
from Autodesk.Revit.Creation import*
#as oCreate
import Autodesk.Revit.ApplicationServices.Application 

# rhino.inside utilities
from RhinoInside.Revit import Revit, Convert
clr.ImportExtensions(Convert.Geometry)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

def FrameCornerVoids(Document, ObjectName):

    object = rs.ObjectsByName(ObjectName)
    pts = rs.BoundingBox(object)
    
    selectedpts = []
    if pts[0][0] <= -35:
        points = [pts[0], pts[1], pts[2]]
        selectedpts.append(points)
    else:
        points = [pts[1], pts[0], pts[3]]
        selectedpts.append(points)
    
    rvtpts = []
    for pp in selectedpts[0]:
        e = ri.Revit.Convert.Geometry.GeometryEncoder.ToXYZ(pp)
        rvtpts.append(e)
        
    fixrvtpts= []
    for i in rvtpts:
        fixrvtpts.append(XYZ(i.X, i.Y, ((i.Z)-(12/304.80))))

    firstp = fixrvtpts[0]
    scndp = fixrvtpts[1]

    distance = firstp.DistanceTo(scndp)

    thirdp = XYZ(firstp.X,firstp.Y, (distance-(12/304.80)))

    lineOne= Line.CreateBound(firstp,scndp)
    lineTwo = Line.CreateBound(scndp, thirdp)
    lineThree = Line.CreateBound(thirdp, firstp)

    rvtlines =lineOne, lineTwo, lineThree

    #Create Curve Array
    carray = CurveArray()
    carrarray = CurveArrArray()
    
    #Loop through lines
    for line in rvtlines:
        carray.Append(line)
    carrarray.Append(carray)

    depth = scndp.DistanceTo(fixrvtpts[2])

    plane = Plane.CreateByThreePoints(firstp, scndp, thirdp)

    t1 = TransactionManager.Instance
    t1.EnsureInTransaction(Document)

    sketchp = SketchPlane.Create(Document, plane)
    
    extrusionvoid = []
    if pts[0][0] <= -35:
        extrusionvoid.append(Document.FamilyCreate.NewExtrusion(False, carrarray, sketchp, -depth))
    else:
        extrusionvoid.append(Document.FamilyCreate.NewExtrusion(False, carrarray, sketchp, depth))
    void = extrusionvoid[0]
    
    bip = BuiltInParameter.DIM_LABEL
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, "Length", False)
    filter = ElementParameterFilter(rule)
    mullionlength = FilteredElementCollector(Document).OfClass(Dimension).WherePasses(filter).FirstElement()

    name = mullionlength.get_Parameter(BuiltInParameter.DIM_VALUE_LENGTH)
    paramvalue = name.AsDouble()
    value = (paramvalue/2)

    planemirror = Plane.CreateByNormalAndOrigin(XYZ(0,0,1), XYZ(0,0,value))
    mirror = ElementTransformUtils.MirrorElement(Document, void.Id, planemirror)

    filter = ElementClassFilter(Extrusion)
    allins = FilteredElementCollector(Document).WherePasses(filter).ToElements()

    ids = []
    for x in allins:
        ids.append(x.Id)
    obj = Document.GetElement(ids[-1])
    delete = Document.Delete(ids[-2])

    mirrorscnd = ElementTransformUtils.MirrorElement(Document, obj.Id, planemirror)

    #End Transaction
    TransactionManager.ForceCloseTransaction(t1)

    return depth

def NewVerticalFrameInstance(Document, TypeName, Position, MirrorBoolean):
    
    listverticalplanes = ["A", "B", "C", "D", "Center"]

    verticalref = []

    for x in listverticalplanes:
        bip = BuiltInParameter.DATUM_TEXT
        provider = ParameterValueProvider(ElementId(bip))
        evaluator = FilterStringEquals()
        rule = FilterStringRule(provider, evaluator, x, False)
        filter = ElementParameterFilter(rule)
        all = FilteredElementCollector(Document).OfClass(ReferencePlane).WherePasses(filter).FirstElement()
        verticalref.append(all)
    
    listhorizontalplanes = ["Axis"]

    bip = BuiltInParameter.DATUM_TEXT
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, "Axis", False)
    filter = ElementParameterFilter(rule)
    horizontalref = FilteredElementCollector(Document).OfClass(ReferencePlane).WherePasses(filter).FirstElement()

    intviewlisthorizontalplanes = ["1.01", "1", "2", "3", "4", "4.01"]

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
        for k in intviewhorizontalref:
            zeta = (k.BubbleEnd).Z
            pts.append(XYZ(equis,((horizontalref.BubbleEnd).Y),zeta))
    keys = []
    for i in listverticalplanes:
        for j in listhorizontalplanes:
            for k in intviewlisthorizontalplanes:
                keys.append(''.join([i,',',j,',',k]))
    
    ################ Dictionary ptsdi
    ptsdi = {keys[i]:pts[i] for i in range(len(keys))}
    ################
    
    keysname = listverticalplanes+listhorizontalplanes+intviewlisthorizontalplanes
    refall = verticalref+[horizontalref]+intviewhorizontalref
    
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
    rule = FilterStringRule(provider, evaluator, "Front", False)
    filter = ElementParameterFilter(rule)
    interior = FilteredElementCollector(Document).OfClass(ViewSection).WherePasses(filter).FirstElement()
    
    ############### NewFamily Instance
    t1 = TransactionManager.Instance
    t1.EnsureInTransaction(Document)
    
    collector.Activate()
    
    position=[]
    if Position == "Left":
        Loc = "A,Axis,1"
        position.append(Loc)
    else:
        Loc = "D,Axis,1"
        position.append(Loc)
    
    LocationKey = position[0]
    startsloc = ptsdi[LocationKey]
    txt = LocationKey.split(",")
    EndRefPlane = "4"
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
    
    parameter = instance[0].GetParameters("Length")
    setheight = parameter[0].Set(heigthprof)
    
    #End Transaction
    TransactionManager.ForceCloseTransaction(t1)
    
    centerref = instance[0].GetReferenceByName("Center (Left/Right)")
    hcenterref = instance[0].GetReferenceByName("Center (Front/Back)")
    heightref = instance[0].GetReferenceByName("Lock top")
    baseref = instance[0].GetReferenceByName("Lock bottom")
    
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

def NewHorizontalFrameInstance(Document, TypeName, Position, MirrorBoolean):
    
    listverticalplanes = ["A", "B", "C", "D", "Center"]

    verticalref = []

    for x in listverticalplanes:
        bip = BuiltInParameter.DATUM_TEXT
        provider = ParameterValueProvider(ElementId(bip))
        evaluator = FilterStringEquals()
        rule = FilterStringRule(provider, evaluator, x, False)
        filter = ElementParameterFilter(rule)
        all = FilteredElementCollector(Document).OfClass(ReferencePlane).WherePasses(filter).FirstElement()
        verticalref.append(all)
    
    listhorizontalplanes = ["Axis"]

    bip = BuiltInParameter.DATUM_TEXT
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, "Axis", False)
    filter = ElementParameterFilter(rule)
    horizontalref = FilteredElementCollector(Document).OfClass(ReferencePlane).WherePasses(filter).FirstElement()

    intviewlisthorizontalplanes = ["1.01", "1", "2", "3", "4", "4.01"]

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
        for k in intviewhorizontalref:
            zeta = (k.BubbleEnd).Z
            pts.append(XYZ(equis,((horizontalref.BubbleEnd).Y),zeta))
    keys = []
    for i in listverticalplanes:
        for j in listhorizontalplanes:
            for k in intviewlisthorizontalplanes:
                keys.append(''.join([i,',',j,',',k]))
    
    ################ Dictionary ptsdi
    ptsdi = {keys[i]:pts[i] for i in range(len(keys))}
    ################
    
    keysname = listverticalplanes+listhorizontalplanes+intviewlisthorizontalplanes
    refall = verticalref+[horizontalref]+intviewhorizontalref
    
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
    rule = FilterStringRule(provider, evaluator, "Front", False)
    filter = ElementParameterFilter(rule)
    interior = FilteredElementCollector(Document).OfClass(ViewSection).WherePasses(filter).FirstElement()
    
    ############### NewFamily Instance
    t1 = TransactionManager.Instance
    t1.EnsureInTransaction(Document)
    
    notVert = collector.Family.get_Parameter(BuiltInParameter.FAMILY_ALWAYS_VERTICAL).Set(0)
    horizontal = collector.Family.get_Parameter(BuiltInParameter.FAMILY_WORK_PLANE_BASED).Set(1)
    
    collector.Activate()
    
    position=[]
    if Position == "Top":
        Loc = "A,Axis,4"
        position.append(Loc)
    else:
        Loc = "A,Axis,1"
        position.append(Loc)
    
    LocationKey = position[0]
    startsloc = ptsdi[LocationKey]
    txt = LocationKey.split(",")
    EndRefPlane = "D"
    endsloc = refplanedi[EndRefPlane]
    
    ref = refplanedi[txt[0]].GetReference()
    scpoint = XYZ(0, 0 , -1)
    newobj = Document.FamilyCreate.NewFamilyInstance(ref, startsloc, scpoint, collector)
    
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
    
    starts = (refplanedi[txt[0]].BubbleEnd).X
    ends = (endsloc.BubbleEnd).X
    heigthprof = ends - starts
    
    parameter = instance[0].GetParameters("Length")
    setheight = parameter[0].Set(heigthprof)
    
    #End Transaction
    TransactionManager.ForceCloseTransaction(t1)
    
    horref = instance[0].GetReferenceByName("Center (Left/Right)")
    vertref = instance[0].GetReferenceByName("Center (Front/Back)")
    lengthref = instance[0].GetReferenceByName("Lock top")
    baseref = instance[0].GetReferenceByName("Lock bottom")

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
    
    return newobj

def Dimensions(WindowDocument):
    
    bip = BuiltInParameter.SYMBOL_NAME_PARAM
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringBeginsWith()
    rule = FilterStringRule(provider, evaluator, "Schueco", False)
    filter = ElementParameterFilter(rule)
    collector = FilteredElementCollector(WindowDocument).OfCategory(BuiltInCategory.OST_GenericModel).OfClass(FamilySymbol).WherePasses(filter).FirstElement()
    
    parameter = collector.GetParameters("Visible frame width")
    value = parameter[0].AsDouble()
    
    winparameter = WindowDocument.FamilyManager.get_Parameter("Visible frame width")
    
    #Axis to glass distance
    lineone = rs.ObjectsByName("a_AxisToGlass")
    linetwo = rs.ObjectsByName("a_ref-line2")
    
    intersection = rs.LineLineIntersection(lineone, linetwo)
    distance = intersection[0][1]
    
    axistog = WindowDocument.FamilyManager.get_Parameter("AxisToGlass")
    
    t1 = TransactionManager.Instance
    t1.EnsureInTransaction(WindowDocument)
    
    set = WindowDocument.FamilyManager.Set(winparameter, value)
    setaxistog = WindowDocument.FamilyManager.Set(axistog, (-distance/304.80))
    
    #End Transaction
    
    TransactionManager.ForceCloseTransaction(t1)
    return distance

def NewPanel(WindowDocument, Typepanel, Thickness):

    #First: Dictionaries
    
    listverticalplanes = ["B","C","Center"]
    
    verticalref = []
    
    for x in listverticalplanes:
        bip = BuiltInParameter.DATUM_TEXT
        provider = ParameterValueProvider(ElementId(bip))
        evaluator = FilterStringEquals()
        rule = FilterStringRule(provider, evaluator, x, False)
        filter = ElementParameterFilter(rule)
        all = FilteredElementCollector(WindowDocument).OfClass(ReferencePlane).WherePasses(filter).FirstElement()
        verticalref.append(all)
         
    # ref = C.GetReference()
    
    listhorizontalplanes = ["Ext. Axis 1"]

    bip = BuiltInParameter.DATUM_TEXT
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, "Ext. Axis 1", False)
    filter = ElementParameterFilter(rule)
    horizontalref = FilteredElementCollector(WindowDocument).OfClass(ReferencePlane).WherePasses(filter).FirstElement()
    
    horizontallines = []
    
    intviewlisthorizontalplanes = ["2", "3"]
    
    intviewhorizontalref = []
    
    for x in intviewlisthorizontalplanes:
        bip = BuiltInParameter.DATUM_TEXT
        provider = ParameterValueProvider(ElementId(bip))
        evaluator = FilterStringEquals()
        rule = FilterStringRule(provider, evaluator, x, False)
        filter = ElementParameterFilter(rule)
        intvhall = FilteredElementCollector(WindowDocument).OfClass(ReferencePlane).WherePasses(filter).FirstElement()
        intviewhorizontalref.append(intvhall)
    
    pts = []
    for i in verticalref:
        equis = (i.BubbleEnd).X
        for k in intviewhorizontalref:
            zeta = (k.BubbleEnd).Z
            pts.append(XYZ(equis,((horizontalref.BubbleEnd).Y),zeta))
    
    keys = []
    for i in listverticalplanes:
        for j in listhorizontalplanes:
            for k in intviewlisthorizontalplanes:
                keys.append(''.join([i,',',j,',',k]))
    
    ################ Dictionary ptsdi
    ptsdi = {keys[i]:pts[i] for i in range(len(keys))}
    ################
    
    keysname = listverticalplanes+listhorizontalplanes+intviewlisthorizontalplanes
    refall = verticalref+[horizontalref]+intviewhorizontalref
    
    ################ Dictionary refplanedi
    refplanedi = {keysname[i]:refall[i] for i in range(len(keysname))}
    
    ################ Panel
    
    keysname = ["Glz","Panel"]
    lst = ["Glz_40mm", "Panel_2mm"]
    
    paneldi = {keysname[i]:lst[i] for i in range(len(keysname))}
    
    panelpicked = paneldi[Typepanel]
    
    bip = BuiltInParameter.SYMBOL_NAME_PARAM
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, panelpicked, False)
    filter = ElementParameterFilter(rule)
    panel = FilteredElementCollector(WindowDocument).OfCategory(BuiltInCategory.OST_GenericModel).OfClass(FamilySymbol).WherePasses(filter).FirstElement()
    
    getparam = panel.GetParameters("Panel thickness")
    
    t1 = TransactionManager.Instance
    t1.EnsureInTransaction(WindowDocument)
    
    splitname = paneldi[Typepanel].split("_")
    rename = splitname[0]+ str("_")+str(Thickness)+str("mm")
    panel.Name = rename

    value = Thickness/304.80
    param = getparam[0].Set(value)
    
    LocationKey = "B,Ext. Axis 1,2"
    startsloc = ptsdi[LocationKey]
    txt = LocationKey.split(",")

    endsheigthloc = refplanedi["3"]
    endswidthloc = refplanedi["C"]
    
    panel.Activate()
    
    newobj = WindowDocument.FamilyCreate.NewFamilyInstance(startsloc, panel, 0)
    
    starts = (refplanedi[txt[2]].BubbleEnd).Z
    ends = (endsheigthloc.BubbleEnd).Z
    heigthpanel = ends - starts
    
    parameter = newobj.GetParameters("Panel height")
    setheight = parameter[0].Set(heigthpanel)
    
    start = (refplanedi[txt[0]].BubbleEnd).X
    end = (endswidthloc.BubbleEnd).X
    widthpanel = end - start
    
    param = newobj.GetParameters("Panel width")
    setwidth = param[0].Set(widthpanel)
    
    #End Transaction
    TransactionManager.ForceCloseTransaction(t1)
    
    bip = BuiltInParameter.VIEW_NAME
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, "Ref. Level", False)
    filter = ElementParameterFilter(rule)
    reflevel = FilteredElementCollector(WindowDocument).OfClass(ViewPlan).WherePasses(filter).FirstElement()

    bip = BuiltInParameter.VIEW_NAME
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, "Front", False)
    filter = ElementParameterFilter(rule)
    interior = FilteredElementCollector(WindowDocument).OfClass(ViewSection).WherePasses(filter).FirstElement()

    centerref = newobj.GetReferenceByName("Center (Left/Right)")
    hcenterref = newobj.GetReferenceByName("Center (Front/Back)")
    heightref = newobj.GetReferenceByName("top")
    baseref = newobj.GetReferenceByName("bottom")
    widthref = newobj.GetReferenceByName("right")
    
    firstref = refplanedi[txt[0]].GetReference()
    scnref = refplanedi[txt[1]].GetReference()
    thirdref = endsheigthloc.GetReference()
    fourthref = refplanedi[txt[2]].GetReference()
    fifthref = endswidthloc.GetReference()
    
    t2 = TransactionManager.Instance
    t2.EnsureInTransaction(WindowDocument)
    
    align = WindowDocument.FamilyCreate.NewAlignment(reflevel, firstref, centerref)
    align2 = WindowDocument.FamilyCreate.NewAlignment(reflevel, scnref, hcenterref)
    align3 = WindowDocument.FamilyCreate.NewAlignment(interior, thirdref, heightref)
    align4 = WindowDocument.FamilyCreate.NewAlignment(interior, fourthref, baseref)
    align5 = WindowDocument.FamilyCreate.NewAlignment(reflevel, fifthref, widthref)
    
    #End Transaction
    TransactionManager.ForceCloseTransaction(t2)
    
    return newobj