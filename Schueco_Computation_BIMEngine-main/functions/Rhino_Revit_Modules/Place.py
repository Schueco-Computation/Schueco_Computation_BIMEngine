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

def DetailItems(DetailItemsAllDOC):
    bip = BuiltInParameter.SYMBOL_NAME_PARAM
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringBeginsWith()
    rule = FilterStringRule(provider, evaluator, "S", False)
    filter = ElementParameterFilter(rule)
    collector = FilteredElementCollector(DetailItemsAllDOC).OfCategory(BuiltInCategory.OST_DetailComponents).OfClass(FamilySymbol).WherePasses(filter).ToElements()

    #########Start Transaction
    t2 = TransactionManager.Instance
    t2.EnsureInTransaction(DetailItemsAllDOC)

    #Activating FamilySYmbol
    all = []
    for elements in collector:
        allelements = elements.Activate()
        all.append(allelements)

    #Placing new family

    bip = BuiltInParameter.VIEW_NAME
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringEquals()
    rule = FilterStringRule(provider, evaluator, "Ref. Level", False)
    filter = ElementParameterFilter(rule)
    refplan = FilteredElementCollector(DetailItemsAllDOC).OfClass(ViewPlan).WherePasses(filter).FirstElement()

    loc = XYZ(0, 0,0)
    output = []

    newobjs = []

    for symball in collector:
        newobj = DetailItemsAllDOC.FamilyCreate.NewFamilyInstance(loc, symball, refplan)
        newobjs.append(newobj)

    TransactionManager.ForceCloseTransaction(t2)
    return newobjs

def DetailItemInprof(DetailItemsAllDOC):
    bip = BuiltInParameter.SYMBOL_NAME_PARAM
    provider = ParameterValueProvider(ElementId(bip))
    evaluator = FilterStringBeginsWith()
    rule = FilterStringRule(provider, evaluator, "S", False)
    filter = ElementParameterFilter(rule)
    collector = FilteredElementCollector(DetailItemsAllDOC).OfCategory(BuiltInCategory.OST_DetailComponents).OfClass(FamilySymbol).WherePasses(filter).ToElements()

    #########Start Transaction
    t2 = TransactionManager.Instance
    t2.EnsureInTransaction(DetailItemsAllDOC)

    #Activating FamilySYmbol
    all = []
    for elements in collector:
        allelements = elements.Activate()
        all.append(allelements)

    #Placing new family

    loc = XYZ(0, 0,0)
    output = []

    newobjs = []

    for symball in collector:
        newobj = DetailItemsAllDOC.FamilyCreate.NewFamilyInstance(loc, symball, 0)
        newobjs.append(newobj)
    
    param = newobjs[0].LookupParameter("Visibility/Graphics Overrides")
    param.Set(32768)

    TransactionManager.ForceCloseTransaction(t2)
    return newobjs
