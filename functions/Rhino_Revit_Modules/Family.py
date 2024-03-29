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
    
    all = FilteredElementCollector(Document).OfClass(ReferencePlane).ToElements()
    output = []
    for x in all:
        output.append(x.Name)



    listverticalplanes = []# ("A", "A.01", "B", "B.01", "B.02", "C", "C.01", "Center")
    listhorizontalplanes =[]# ("Axis", "Ext. Axis 1", "Ext. Axis 2", "Ext. Axis 3")
    intviewlisthorizontalplanes =[] #("1", "1.01", "2", "2.01","2.02", "3", "3.01")
    
    firstchar = []

    for x in output:
        firstchar.append(x[0])
    
    letras = [] 
    for i,j in enumerate(firstchar):
        if j.isnumeric():
            intviewlisthorizontalplanes.append(output[i])
        else:
            letras.append(output[i])
    for x in letras:
        if "Axis" in x:
            listhorizontalplanes.append(x)
        else:
            listverticalplanes.append(x)


    verticalref = []

    for x in listverticalplanes:
        bip = BuiltInParameter.DATUM_TEXT
        provider = ParameterValueProvider(ElementId(bip))
        evaluator = FilterStringEquals()
        rule = FilterStringRule(provider, evaluator, x, False)
        filter = ElementParameterFilter(rule)
        all = FilteredElementCollector(Document).OfClass(ReferencePlane).WherePasses(filter).FirstElement()
        verticalref.append(all)
    


    

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
    scpoint = XYZ(0, 0 , -1)
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

    bip = BuiltInParameter.MATERIAL_NAME
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEndsWith()
    rule = FilterStringRule(provider, evaluator, "Aluminium (European)", False)
    filter = ElementParameterFilter(rule)
    matids = FilteredElementCollector(Document).OfClass(Material).WherePasses(filter).FirstElementId()
    
    parammat = instance[0].GetParameters("Profile material")
    setwidthmat = parammat[0].Set(matids)

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

    
    all = FilteredElementCollector(Document).OfClass(ReferencePlane).ToElements()
    output = []
    for x in all:
        output.append(x.Name)

    listverticalplanes = []# ("A", "A.01", "B", "B.01", "B.02", "C", "C.01", "Center")
    listhorizontalplanes =[]# ("Axis", "Ext. Axis 1", "Ext. Axis 2", "Ext. Axis 3")
    intviewlisthorizontalplanes =[] #("1", "1.01", "2", "2.01","2.02", "3", "3.01")
    
    firstchar = []

    for x in output:
        firstchar.append(x[0])
    
    letras = [] 
    for i,j in enumerate(firstchar):
        if j.isnumeric():
            intviewlisthorizontalplanes.append(output[i])
        else:
            letras.append(output[i])
    for x in letras:
        if "Axis" in x:
            listhorizontalplanes.append(x)
        else:
            listverticalplanes.append(x)

    
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

    bip = BuiltInParameter.MATERIAL_NAME
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEndsWith()
    rule = FilterStringRule(provider, evaluator, "Aluminium (European)", False)
    filter = ElementParameterFilter(rule)
    matids = FilteredElementCollector(Document).OfClass(Material).WherePasses(filter).FirstElementId()
    
    parammat = instance[0].GetParameters("Profile material")
    setwidthmat = parammat[0].Set(matids)
    
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


    
    all = FilteredElementCollector(Document).OfClass(ReferencePlane).ToElements()
    output = []
    for x in all:
        output.append(x.Name)
    
    test = []
    for x in output:
        test.append(x[0])
    
    listverticalplanes = []
    listhorizontalplanes = []
    intviewlisthorizontalplanes = []
    
    letras = [] 
    for i,j in enumerate(test):
        if j.isnumeric():
            intviewlisthorizontalplanes.append(output[i])
        else:
            letras.append(output[i])
    
    for x in letras:
        if "Axis" in x:
            listhorizontalplanes.append(x)
        else:
            listverticalplanes.append(x)
    
    #First: Dictionaries
    
    verticalref = []
    
    for x in listverticalplanes:
        bip = BuiltInParameter.DATUM_TEXT
        provider = ParameterValueProvider(ElementId(bip))
        evaluator = FilterStringEquals()
        rule = FilterStringRule(provider, evaluator, x, False)
        filter = ElementParameterFilter(rule)
        all = FilteredElementCollector(Document).OfClass(ReferencePlane).WherePasses(filter).FirstElement()
        verticalref.append(all)
    
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
    
    ################ Panel
    
    keysname = ("Glz","Panel","Spandrel")
    lst = ("Glz_40mm", "Panel_2mm", "Spandrel-Panel_100mm")
    
    paneldi = {keysname[i]:lst[i] for i in range(len(keysname))}
    
    panelpicked = paneldi[Typepanel]
    
    bip = BuiltInParameter.SYMBOL_NAME_PARAM
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, panelpicked, False)
    filter = ElementParameterFilter(rule)
    panel = FilteredElementCollector(Document).OfCategory(BuiltInCategory.OST_GenericModel).OfClass(FamilySymbol).WherePasses(filter).FirstElement()

    splitname = paneldi[Typepanel].split("_")
    rename = splitname[0]+ str("_")+str(Thickness)+str("mm")
    
    bip = BuiltInParameter.SYMBOL_NAME_PARAM
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, rename, False)
    filter = ElementParameterFilter(rule)
    panelnew = FilteredElementCollector(Document).OfCategory(BuiltInCategory.OST_GenericModel).OfClass(FamilySymbol).WherePasses(filter).FirstElement()
    
    conditional = []
    if panelnew == None:
        ########################################################
        familyDocument = panel.Family
        edit = Document.EditFamily(familyDocument)
        manager = edit.FamilyManager
        
        tsub = TransactionManager.Instance
        tsub.EnsureInTransaction(edit)
        
        newt = manager.NewType(rename)
        getparam = manager.get_Parameter("Panel thickness")
        
        value = Thickness/304.80
        param = manager.Set(getparam, value)
        
        #End Transaction
        TransactionManager.ForceCloseTransaction(tsub)
        
        class FamilyOption(IFamilyLoadOptions):
    	    def OnFamilyFound(self, familyInUse, overwriteParameterValues):
    		    overwriteParameterValues = True
    		    return True
    
    	    def OnSharedFamilyFound(self, sharedFamily, familyInUse, source, overwriteParameterValues):
    		    return True
        load = edit.LoadFamily(Document, FamilyOption())
        conditional.append(rename)

    else:
        conditional.append(rename)
    ###############################################################
    
    t1 = TransactionManager.Instance
    t1.EnsureInTransaction(Document)
    
    startsloc = ptsdi[LocationKey]
    txt = LocationKey.split(",")

    endsheigthloc = refplanedi[EndHeigthRefPlane]
    endswidthloc = refplanedi[EndWidthRefPlane]
    
    bip = BuiltInParameter.SYMBOL_NAME_PARAM
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, conditional[0], False)
    filter = ElementParameterFilter(rule)
    newpanel = FilteredElementCollector(Document).OfCategory(BuiltInCategory.OST_GenericModel).OfClass(FamilySymbol).WherePasses(filter).FirstElement()
    newpanel.Activate()
    
    newobj = Document.FamilyCreate.NewFamilyInstance(startsloc, newpanel, 0)
    
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
    reflevel = FilteredElementCollector(Document).OfClass(ViewPlan).WherePasses(filter).FirstElement()

    bip = BuiltInParameter.VIEW_NAME
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, "Interior", False)
    filter = ElementParameterFilter(rule)
    interior = FilteredElementCollector(Document).OfClass(ViewSection).WherePasses(filter).FirstElement()

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
    t2.EnsureInTransaction(Document)
    
    align = Document.FamilyCreate.NewAlignment(reflevel, firstref, centerref)
    align2 = Document.FamilyCreate.NewAlignment(reflevel, scnref, hcenterref)
    align3 = Document.FamilyCreate.NewAlignment(interior, thirdref, heightref)
    align4 = Document.FamilyCreate.NewAlignment(interior, fourthref, baseref)
    align5 = Document.FamilyCreate.NewAlignment(reflevel, fifthref, widthref)
    
    #End Transaction
    TransactionManager.ForceCloseTransaction(t2)
    
    return newpanel
    
    all = FilteredElementCollector(doc).OfClass(ReferencePlane).ToElements()
    output = []
    for x in all:
        output.append(x.Name)

    #First: Dictionaries
    
    listverticalplanes = []# ("A", "A.01", "B", "B.01", "B.02", "C", "C.01", "Center")
    listhorizontalplanes =[]# ("Axis", "Ext. Axis 1", "Ext. Axis 2", "Ext. Axis 3")
    intviewlisthorizontalplanes =[] #("1", "1.01", "2", "2.01","2.02", "3", "3.01")
    
    firstchar = []

    for x in output:
        firstchar.append(x[0])
    
    letras = [] 
    for i,j in enumerate(firstchar):
        if j.isnumeric():
            intviewlisthorizontalplanes.append(output[i])
        else:
            letras.append(output[i])
    for x in letras:
        if "Axis" in x:
            listhorizontalplanes.append(x)
        else:
            listverticalplanes.append(x)

    
    verticalref = []
    
    for x in listverticalplanes:
        bip = BuiltInParameter.DATUM_TEXT
        provider = ParameterValueProvider(ElementId(bip))
        evaluator = FilterStringEquals()
        rule = FilterStringRule(provider, evaluator, x, False)
        filter = ElementParameterFilter(rule)
        all = FilteredElementCollector(doc).OfClass(ReferencePlane).WherePasses(filter).FirstElement()
        verticalref.append(all)
         
    # ref = C.GetReference()
    
    
    
    horizontalref = []

    for x in listhorizontalplanes:
        bip = BuiltInParameter.DATUM_TEXT
        provider = ParameterValueProvider(ElementId(bip))
        evaluator = FilterStringEquals()
        rule = FilterStringRule(provider, evaluator, x, False)
        filter = ElementParameterFilter(rule)
        hall = FilteredElementCollector(doc).OfClass(ReferencePlane).WherePasses(filter).FirstElement()
        horizontalref.append(hall)
    
    horizontallines = []
    
    
    
    intviewhorizontalref = []
    
    for x in intviewlisthorizontalplanes:
        bip = BuiltInParameter.DATUM_TEXT
        provider = ParameterValueProvider(ElementId(bip))
        evaluator = FilterStringEquals()
        rule = FilterStringRule(provider, evaluator, x, False)
        filter = ElementParameterFilter(rule)
        intvhall = FilteredElementCollector(doc).OfClass(ReferencePlane).WherePasses(filter).FirstElement()
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
    
    ################ Panel
    
    keysname = ("Glz","Panel","Spandrel")
    lst = ("Glz_40mm", "Panel_2mm", "Spandrel-Panel_100mm")
    
    paneldi = {keysname[i]:lst[i] for i in range(len(keysname))}
    
    panelpicked = paneldi[Typepanel]
    
    bip = BuiltInParameter.SYMBOL_NAME_PARAM
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, panelpicked, False)
    filter = ElementParameterFilter(rule)
    panel = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericModel).OfClass(FamilySymbol).WherePasses(filter).FirstElement()
    
    getparam = panel.GetParameters("Panel thickness")
    
    t1 = TransactionManager.Instance
    t1.EnsureInTransaction(doc)
    
    splitname = paneldi[Typepanel].split("_")
    rename = splitname[0]+ str("_")+str(Thickness)+str("mm")
    #panel.Name = rename

    value = Thickness/304.80
    param = getparam[0].Set(value)
    
    startsloc = ptsdi[LocationKey]
    txt = LocationKey.split(",")

    endsheigthloc = refplanedi[EndHeigthRefPlane]
    endswidthloc = refplanedi[EndWidthRefPlane]
    
    panel.Activate()
    
    newobj = doc.FamilyCreate.NewFamilyInstance(startsloc, panel, 0)
    
    #Change typename
    #name = newobj.GetReferenceType().Name
    #output = name = "test"
    #Autodesk.Revit.DB.FamilyInstance.GetTypeId
    
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
    reflevel = FilteredElementCollector(doc).OfClass(ViewPlan).WherePasses(filter).FirstElement()

    bip = BuiltInParameter.VIEW_NAME
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, "Interior", False)
    filter = ElementParameterFilter(rule)
    interior = FilteredElementCollector(doc).OfClass(ViewSection).WherePasses(filter).FirstElement()

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
    t2.EnsureInTransaction(doc)
    
    align = doc.FamilyCreate.NewAlignment(reflevel, firstref, centerref)
    align2 = doc.FamilyCreate.NewAlignment(reflevel, scnref, hcenterref)
    align3 = doc.FamilyCreate.NewAlignment(interior, thirdref, heightref)
    align4 = doc.FamilyCreate.NewAlignment(interior, fourthref, baseref)
    align5 = doc.FamilyCreate.NewAlignment(reflevel, fifthref, widthref)
    
    #End Transaction
    TransactionManager.ForceCloseTransaction(t2)
    
    return newobj

def NewPanel(Document, Typepanel, Thickness, LocationKey, EndHeigthRefPlane, EndWidthRefPlane, materialname):
    
    all = FilteredElementCollector(Document).OfClass(ReferencePlane).ToElements()
    output = []
    for x in all:
        output.append(x.Name)
    
    test = []
    for x in output:
        test.append(x[0])
    
    listverticalplanes = []
    listhorizontalplanes = []
    intviewlisthorizontalplanes = []
    
    letras = [] 
    for i,j in enumerate(test):
        if j.isnumeric():
            intviewlisthorizontalplanes.append(output[i])
        else:
            letras.append(output[i])
    
    for x in letras:
        if "Axis" in x:
            listhorizontalplanes.append(x)
        else:
            listverticalplanes.append(x)
    
    #First: Dictionaries
    
    verticalref = []
    
    for x in listverticalplanes:
        bip = BuiltInParameter.DATUM_TEXT
        provider = ParameterValueProvider(ElementId(bip))
        evaluator = FilterStringEquals()
        rule = FilterStringRule(provider, evaluator, x, False)
        filter = ElementParameterFilter(rule)
        all = FilteredElementCollector(Document).OfClass(ReferencePlane).WherePasses(filter).FirstElement()
        verticalref.append(all)
    
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
    
    ################ Panel
    
    keysname = ("Glz","Panel","Spandrel","IntGlz","IntPanel","IntSpandrel","GlzCust")
    lst = ("Glz_40mm", "Panel_2mm", "Spandrel-Panel_100mm","IntGlz_40mm", "IntPanel_2mm", "IntSpandrel-Panel_100mm","GlzCust_40mm")
    
    paneldi = {keysname[i]:lst[i] for i in range(len(keysname))}
    
    panelpicked = paneldi[Typepanel]
    
    bip = BuiltInParameter.SYMBOL_NAME_PARAM
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, panelpicked, False)
    filter = ElementParameterFilter(rule)
    panel = FilteredElementCollector(Document).OfCategory(BuiltInCategory.OST_GenericModel).OfClass(FamilySymbol).WherePasses(filter).FirstElement()

    splitname = paneldi[Typepanel].split("_")
    rename = splitname[0]+ str("_")+str(Thickness)+str("mm")

        #Opening, closing and reloading of the panel family to make sure it loads all the new types
    familyDocument = panel.Family
    edit = Document.EditFamily(familyDocument)
    manager = edit.FamilyManager
    
    tsub = TransactionManager.Instance
    tsub.EnsureInTransaction(edit)
    
    #End Transaction
    TransactionManager.ForceCloseTransaction(tsub)
    
    class FamilyOption(IFamilyLoadOptions):
	    def OnFamilyFound(self, familyInUse, overwriteParameterValues):
		    overwriteParameterValues = True
		    return True

	    def OnSharedFamilyFound(self, sharedFamily, familyInUse, source, overwriteParameterValues):
		    return True
    load = edit.LoadFamily(Document, FamilyOption())
    ########################

    bip = BuiltInParameter.SYMBOL_NAME_PARAM
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, rename, False)
    filter = ElementParameterFilter(rule)
    panelnew = FilteredElementCollector(Document).OfCategory(BuiltInCategory.OST_GenericModel).OfClass(FamilySymbol).WherePasses(filter).FirstElement()
    
    conditional = []
    
    if panelnew == None:
        ########################################################
        familyDocument = panel.Family
        edit = Document.EditFamily(familyDocument)
        manager = edit.FamilyManager
        
        tsub = TransactionManager.Instance
        tsub.EnsureInTransaction(edit)
        
        newt = manager.NewType(rename)
        getparam = manager.get_Parameter("Panel thickness")
          
        value = Thickness/304.80
        param = manager.Set(getparam, value)
        
        #End Transaction
        TransactionManager.ForceCloseTransaction(tsub)
        
        class FamilyOption(IFamilyLoadOptions):
    	    def OnFamilyFound(self, familyInUse, overwriteParameterValues):
    		    overwriteParameterValues = True
    		    return True
    
    	    def OnSharedFamilyFound(self, sharedFamily, familyInUse, source, overwriteParameterValues):
    		    return True
        load = edit.LoadFamily(Document, FamilyOption())
        
        conditional.append(rename)

    else:
        conditional.append(rename)
    ###############################################################
    
    t1 = TransactionManager.Instance
    t1.EnsureInTransaction(Document)
    
    startsloc = ptsdi[LocationKey]
    txt = LocationKey.split(",")

    endsheigthloc = refplanedi[EndHeigthRefPlane]
    endswidthloc = refplanedi[EndWidthRefPlane]
    
    bip = BuiltInParameter.SYMBOL_NAME_PARAM
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, conditional[0], False)
    filter = ElementParameterFilter(rule)
    newpanel = FilteredElementCollector(Document).OfCategory(BuiltInCategory.OST_GenericModel).OfClass(FamilySymbol).WherePasses(filter).FirstElement()
    newpanel.Activate()
    
    newobj = Document.FamilyCreate.NewFamilyInstance(startsloc, newpanel, 0)
    
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
    
    bip = BuiltInParameter.MATERIAL_NAME
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEndsWith()
    rule = FilterStringRule(provider, evaluator, materialname, False)
    filter = ElementParameterFilter(rule)
    matids = FilteredElementCollector(Document).OfClass(Material).WherePasses(filter).FirstElementId()
    
    parammat = newobj.GetParameters("Panel material")
    setwidthmat = parammat[0].Set(matids)

    #End Transaction
    TransactionManager.ForceCloseTransaction(t1)
    
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
    t2.EnsureInTransaction(Document)
    
    align = Document.FamilyCreate.NewAlignment(reflevel, firstref, centerref)
    align2 = Document.FamilyCreate.NewAlignment(reflevel, scnref, hcenterref)
    align3 = Document.FamilyCreate.NewAlignment(interior, thirdref, heightref)
    align4 = Document.FamilyCreate.NewAlignment(interior, fourthref, baseref)
    align5 = Document.FamilyCreate.NewAlignment(reflevel, fifthref, widthref)
    
    #End Transaction
    TransactionManager.ForceCloseTransaction(t2)
    
    return newpanel

def NewWindowInstance(Document, TypeName, LocationKey, EndHeigthRefPlane, EndWidthRefPlane):
    
    all = FilteredElementCollector(Document).OfClass(ReferencePlane).ToElements()
    output = []
    for x in all:
        output.append(x.Name)
    #First: Dictionaries
    
    listverticalplanes = []# ("A", "A.01", "B", "B.01", "B.02", "C", "C.01", "Center")
    listhorizontalplanes =[]# ("Axis", "Ext. Axis 1", "Ext. Axis 2", "Ext. Axis 3")
    intviewlisthorizontalplanes =[] #("1", "1.01", "2", "2.01","2.02", "3", "3.01")
    
    firstchar = []

    for x in output:
        firstchar.append(x[0])
    
    letras = [] 
    for i,j in enumerate(firstchar):
        if j.isnumeric():
            intviewlisthorizontalplanes.append(output[i])
        else:
            letras.append(output[i])
    for x in letras:
        if "Axis" in x:
            listhorizontalplanes.append(x)
        else:
            listverticalplanes.append(x)

    
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
    
    ################ window
    
    
    bip = BuiltInParameter.SYMBOL_NAME_PARAM
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, TypeName, False)
    filter = ElementParameterFilter(rule)
    window = FilteredElementCollector(Document).OfCategory(BuiltInCategory.OST_Windows).OfClass(FamilySymbol).WherePasses(filter).FirstElement()
    
    
    t1 = TransactionManager.Instance
    t1.EnsureInTransaction(Document)
    
    startsloc = ptsdi[LocationKey]
    txt = LocationKey.split(",")

    endsheigthloc = refplanedi[EndHeigthRefPlane]
    endswidthloc = refplanedi[EndWidthRefPlane]
    
    window.Activate()
    
    newobj = Document.FamilyCreate.NewFamilyInstance(startsloc, window, 0)
    
    starts = (refplanedi[txt[2]].BubbleEnd).Z
    ends = (endsheigthloc.BubbleEnd).Z
    heigthwindow = ends - starts
    
    parameter = newobj.get_Parameter(BuiltInParameter.FAMILY_HEIGHT_PARAM)
    setheight = parameter.Set(heigthwindow)
    
    start = (refplanedi[txt[0]].BubbleEnd).X
    end = (endswidthloc.BubbleEnd).X
    widthwindow = end - start
    
    param = newobj.get_Parameter(BuiltInParameter.FURNITURE_WIDTH)
    setwidth = param.Set(widthwindow)
    
    #End Transaction
    TransactionManager.ForceCloseTransaction(t1)
    
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

    centerref = newobj.GetReferenceByName("A")
    hcenterref = newobj.GetReferenceByName("Axis")
    heightref = newobj.GetReferenceByName("4")
    baseref = newobj.GetReferenceByName("1")
    widthref = newobj.GetReferenceByName("D")
    
    firstref = refplanedi[txt[0]].GetReference()
    scnref = refplanedi[txt[1]].GetReference()
    thirdref = endsheigthloc.GetReference()
    fourthref = refplanedi[txt[2]].GetReference()
    fifthref = endswidthloc.GetReference()
    
    t2 = TransactionManager.Instance
    t2.EnsureInTransaction(Document)
    
    align = Document.FamilyCreate.NewAlignment(reflevel, firstref, centerref)
    align2 = Document.FamilyCreate.NewAlignment(reflevel, scnref, hcenterref)
    align3 = Document.FamilyCreate.NewAlignment(interior, thirdref, heightref)
    align4 = Document.FamilyCreate.NewAlignment(interior, fourthref, baseref)
    align5 = Document.FamilyCreate.NewAlignment(reflevel, fifthref, widthref)
    
    #End Transaction
    TransactionManager.ForceCloseTransaction(t1)
    
    return newobj