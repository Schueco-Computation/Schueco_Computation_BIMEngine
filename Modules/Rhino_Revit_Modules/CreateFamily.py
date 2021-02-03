# Enable Python support and load DesignScript library
import clr

clr.AddReference('RhinoInside.Revit')
clr.AddReference('RevitAPIUI')

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

# The inputs to this node will be stored as a list in the IN variables.

##########################################
#Create revit family file

def New(TemplateFilePath, TypeName, articles):
    doc = Revit.ActiveDBDocument
    newfamily = doc.Application.NewFamilyDocument(TemplateFilePath)

    #########Start Transaction
    t1 = TransactionManager.Instance
    t1.EnsureInTransaction(newfamily)
    #Create family type

    newtype = newfamily.FamilyManager.NewType(TypeName)

    parameter = newfamily.FamilyManager.get_Parameter("Art. No.")

    setartparam = newfamily.FamilyManager.Set(parameter, articles)
    
    #########End Transaction
    TransactionManager.ForceCloseTransaction(t1)
    return newfamily
