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



doc = Revit.ActiveDBDocument

# The inputs to this node will be stored as a list in the IN variables.

##########################################
#Select a layer and convert From polyline in Rhino to lines in Revit

# Select a layer in Rhino

def DetailItems(objectname, famtypename, DetailItemsAllDOC, detailitemtemp):
    #layer = rs.GetLayer(layname)
    #rs.ObjectsByLayer()
    #obj= rs.ObjectsByLayer(layer, True)
    obj = rs.ObjectsByName(objectname)
    
    #selected objects

    profile = []

    rs.SelectObjects(obj)
    ObjId = rs.SelectedObjects(include_lights=False, include_grips=False)
    for obj in ObjId:
        lines = rs.coercecurve(obj)
        profile.append(lines)
        
    #unselect objects
    unselect = rs.UnselectObjects(ObjId)

    explode = rs.ExplodeCurves(profile)

    # coerce

    profcoerce = []

    for prof in explode:
        profco = rs.coercecurve(prof)
        profcoerce.append(profco)

    rvtlines = []

    for ex in profcoerce:
        lines = ri.Revit.Convert.Geometry.GeometryEncoder.ToCurve(ex)
        rvtlines.append(lines)

    ##########################################
    #Create revit family file

    newfam = doc.Application.NewFamilyDocument(detailitemtemp)

    #########Start Transaction
    #t = Transaction(newfam, 'PolyLine')
    #t.Start()
    t1 = TransactionManager.Instance
    t1.EnsureInTransaction(newfam)

    ##########################################
    #Create family type

    #famtypename = "Schueco_ USC-Cust_ Det_ H02_1"
    newtype = newfam.FamilyManager.NewType(famtypename)
    
    parameter = newfam.FamilyManager.get_Parameter("Art. No.")

    setartparam = newfam.FamilyManager.Set(parameter, objectname)

    #Create Curve Array
    #carray = CurveArray()

    bip = BuiltInParameter.VIEW_NAME
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, "Ref. Level", False)
    filter = ElementParameterFilter(rule)
    floorview = FilteredElementCollector(newfam).OfClass(ViewPlan).WherePasses(filter).FirstElement()

    #Creating detail lines

    place = []

    for lines in rvtlines:
        draw = newfam.FamilyCreate.NewDetailCurve(floorview, lines)
        place.append(draw)
    

    TransactionManager.ForceCloseTransaction(t1)

    loadfamily = newfam.LoadFamily(DetailItemsAllDOC)
    # Assign your output to the OUT variable.
    return newfam

def FamilyNew(TemplateFilePath, TypeName):
    doc = Revit.ActiveDBDocument
    newfamily = doc.Application.NewFamilyDocument(TemplateFilePath)

    #########Start Transaction
    t1 = TransactionManager.Instance
    t1.EnsureInTransaction(newfamily)
    #Create family type

    newtype = newfamily.FamilyManager.NewType(TypeName)
    
    #########End Transaction
    TransactionManager.ForceCloseTransaction(t1)
    return newfamily

def ReferenceLine(newfamily, objname, NewreflineName):

    obj = rs.ObjectsByName(objname)

    profile = []

    rs.SelectObjects(obj)
    ObjId = rs.SelectedObjects(include_lights=False, include_grips=False)
    for obj in ObjId:
        lines = rs.coercecurve(obj)
        profile.append(lines)

    puntos = rs.PolylineVertices(obj)
    
    unselect = rs.UnselectObjects(ObjId)
    
    rvtpts = []

    for pp in puntos:
        e = ri.Revit.Convert.Geometry.GeometryEncoder.ToXYZ(pp)
        rvtpts.append(e)

    bip = BuiltInParameter.VIEW_NAME
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, "Ref. Level", False)
    filter = ElementParameterFilter(rule)
    refplan = FilteredElementCollector(newfamily).OfClass(ViewPlan).WherePasses(filter).FirstElement()

    #########Start Transaction
    #t.Start()
    t1 = TransactionManager.Instance
    t1.EnsureInTransaction(newfamily)

    bubblend = rvtpts[0]
    freend = rvtpts [1]
    direc = XYZ(0, 0, 1)

    refp1 = newfamily.FamilyCreate.NewReferencePlane(bubblend, freend, direc, refplan)
    #refPlane = doc.FamilyCreate.NewReferencePlane(bubblend, freend, cutvec, doc.ActiveView)
    refp1.Name = NewreflineName

    #End Transaction
    #t.Commit()
    TransactionManager.ForceCloseTransaction(t1)

    return refp1

def ReferenceLines(newfamily, FrameOrProf):

    object = rs.ObjectsByName("a_simp-prof")
    pts = rs.BoundingBox(object)
    
    subtract = []
    if FrameOrProf == "Frame":
        subtract.append(0)
    else:
        subtract.append(pts[0][0] * pts[1][0])
    
    lst = []
    if -1 <= subtract[0] <= 1:
        refone = ["a_ref-line1"]
        lst.append(refone)
    else:
        reftwo = ["a_ref-line1","a_ref-line2"]
        lst.append(reftwo)
    
    objnames =lst[0]
    reflines = []
    for i,j in enumerate(objnames, 1):
        obj = rs.ObjectsByName(j)

        profile = []

        rs.SelectObjects(obj)
        ObjId = rs.SelectedObjects(include_lights=False, include_grips=False)
        for obj in ObjId:
            lines = rs.coercecurve(obj)
            profile.append(lines)

        puntos = rs.PolylineVertices(obj)
    
        unselect = rs.UnselectObjects(ObjId)
    
        rvtpts = []

        for pp in puntos:
            e = ri.Revit.Convert.Geometry.GeometryEncoder.ToXYZ(pp)
            rvtpts.append(e)

        bip = BuiltInParameter.VIEW_NAME
        provider = ParameterValueProvider(ElementId(bip))
        evaluator = FilterStringEquals()
        rule = FilterStringRule(provider, evaluator, "Ref. Level", False)
        filter = ElementParameterFilter(rule)
        refplan = FilteredElementCollector(newfamily).OfClass(ViewPlan).WherePasses(filter).FirstElement()

        #########Start Transaction
        #t.Start()
        t1 = TransactionManager.Instance
        t1.EnsureInTransaction(newfamily)

        bubblend = rvtpts[0]
        freend = rvtpts [1]
        direc = XYZ(0, 0, 1)

        refp1 = newfamily.FamilyCreate.NewReferencePlane(bubblend, freend, direc, refplan)
    
        refp1.Name = "Reference line "+ str(i)

        #End Transaction
        #t.Commit()
        TransactionManager.ForceCloseTransaction(t1)
        reflines.append(refp1)

    return refp1

def NewAlignment(newfamily, refPlane, solid):
    
    ref1 = refPlane.GetReference()
    refplane = refPlane.GetPlane()

    n0 = refPlane.Normal
    bubblend = refPlane.BubbleEnd
    free = refPlane.FreeEnd
    
    opt = Options()
    opt.ComputeReferences = True

    geometry = solid.get_Geometry(opt)
    fac = []

    for g in geometry:
    	fac = g.Faces

    allfaces = []
    for i in fac:
        allfaces.append(i)

    normal = []

    for i in fac:
        fc = i.FaceNormal
        normal.append(fc)

    indexesOne = []
    for i,j in enumerate(normal,0):
        if j.DotProduct(n0)==1:
            indexesOne.append(i)
    indexesTwo = []
    for i,j in enumerate(normal,0):
        if j.DotProduct(n0)==-1:
            indexesTwo.append(i)
    indexes = indexesOne+indexesTwo

    pfaces = [fac[x] for x in sorted(indexes)]
    
    edgeloops = []
    for i in pfaces:
        loops = i.EdgeLoops
        edgearr = []
        for j in loops:
            edgearr.append(j)
            edge = []
            for k in edgearr:
                new = []
                for l in k:
                   new.append(l)
                   points = []
                   for m in new:
                       points.append(m.Evaluate(0.5))
        edgeloops.append(points)

    ppt = [el[0] for el in edgeloops]
    
    sameplane = []
    for i,j in enumerate(ppt,0):
        if round(n0.DotProduct(j-bubblend),4)==0:
            sameplane.append(i)
    
    idx = indexes[sameplane[0]]
    theface = allfaces[idx]
    facere = theface.Reference
    
    #Finding the view
    
    bip = BuiltInParameter.VIEW_NAME
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, "Ref. Level", False)
    filter = ElementParameterFilter(rule)
    refplan = FilteredElementCollector(newfamily).OfClass(ViewPlan).WherePasses(filter).FirstElement()
    
    #########Start Transaction
    #t = Transaction(newfam, 'PolyLine')
    #t.Start()
    t2 = TransactionManager.Instance
    t2.EnsureInTransaction(newfamily)
    
    align = newfamily.FamilyCreate.NewAlignment(refplan, facere, ref1)
    
    #End Transaction
    #t.Commit()
    TransactionManager.ForceCloseTransaction(t2)
    
    return align

def NewWidthDimension(newfamily, FrameOrProf):
    obj = rs.ObjectsByName("a_ref-line1")

    profile1 = []

    rs.SelectObjects(obj)
    ObjId = rs.SelectedObjects(include_lights=False, include_grips=False)
    for obj in ObjId:
        lines = rs.coercecurve(obj)
        profile1.append(lines)

    puntos = rs.PolylineVertices(obj)
    unselect = rs.UnselectObjects(ObjId)

    rvtpts1 = []

    for pp in puntos:
        e = ri.Revit.Convert.Geometry.GeometryEncoder.ToXYZ(pp)
        rvtpts1.append(e)

    obj2 = rs.ObjectsByName("a_ref-line2")

    profile2 = []

    rs.SelectObjects(obj2)
    ObjId2 = rs.SelectedObjects(include_lights=False, include_grips=False)
    for obj2 in ObjId2:
        lines2 = rs.coercecurve(obj2)
        profile2.append(lines2)

    puntos2 = rs.PolylineVertices(obj2)
    unselect2 = rs.UnselectObjects(ObjId2)

    rvtpts2 = []

    for i in puntos2:
        e2 = ri.Revit.Convert.Geometry.GeometryEncoder.ToXYZ(i)
        rvtpts2.append(e2)
    
    newrvtpt = XYZ(rvtpts2[0].X, rvtpts1[0].Y, rvtpts2[0].Z)
    line = Line.CreateBound(rvtpts1[0], newrvtpt)
    
    #########Start Transaction
    #t = Transaction(newfam, 'PolyLine')
    #t.Start()
    t2 = TransactionManager.Instance
    t2.EnsureInTransaction(newfamily)

    bip = BuiltInParameter.VIEW_NAME
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, "Ref. Level", False)
    filter = ElementParameterFilter(rule)
    plane = FilteredElementCollector(newfamily).OfClass(ViewPlan).WherePasses(filter).FirstElement()

    lst = ["Reference line 2","Center (Left/Right)"]
    firstref = []
    for x in lst:
        bip = BuiltInParameter.DATUM_TEXT
        provider = ParameterValueProvider(ElementId(bip))
        evaluator = FilterStringEquals()
        rule = FilterStringRule(provider, evaluator, x, False)
        filter = ElementParameterFilter(rule)
        refplancenter = FilteredElementCollector(newfamily).OfClass(ReferencePlane).WherePasses(filter).FirstElement()
        firstref.append(refplancenter)
    firstrefclean = [i for i in firstref if i]
    ref1 = firstrefclean[0].GetReference()

    bip = BuiltInParameter.DATUM_TEXT
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, "Reference line 1", False)
    filter = ElementParameterFilter(rule)
    refplancenter = FilteredElementCollector(newfamily).OfClass(ReferencePlane).WherePasses(filter).FirstElement()
    ref2 = refplancenter.GetReference()

    refarray = ReferenceArray()

    refarray.Append(ref1)
    refarray.Append(ref2)
    
    dimension = newfamily.FamilyCreate.NewLinearDimension(plane, line, refarray)
    parameter = []
    if FrameOrProf == "Frame":
        widthparameter = newfamily.FamilyManager.get_Parameter("Visible frame width")
        parameter.append(widthparameter)
    else:
        widthparam = newfamily.FamilyManager.get_Parameter("Profile width")
        parameter.append(widthparam)

    dimension.FamilyLabel = parameter[0]

    #End Transaction
    #t.Commit()
    TransactionManager.ForceCloseTransaction(t2)

    return dimension
