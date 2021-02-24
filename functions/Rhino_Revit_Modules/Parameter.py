# Enable Python support and load DesignScript library
import clr

clr.AddReference('RevitAPIUI')

#Import RevitAPI
clr.AddReference("RevitAPI")
#import Autodesk.Revit.DB as re
from Autodesk.Revit.DB import*
import Autodesk.Revit.Creation as oCreate
import Autodesk.Revit.ApplicationServices.Application 

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


def GetSet(famdoc, parametername, input):
    
    parameter = newfamily.FamilyManager.get_Parameter(parametername)

    setartparam = newfamily.FamilyManager.Set(parameter, input)
    
    return setartparam