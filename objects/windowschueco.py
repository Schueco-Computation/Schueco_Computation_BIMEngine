import sys
sys.path.append("C:\\Users\\ramijc\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMEngine\\functions\\Rhino_Modules")
sys.path.append("C:\\Users\\ramijc\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMEngine\\functions\\Rhino_Revit_Modules")
import blockorg
import corners
import simplify
import ConvertPoly
import Create
import CreateExtrusion
#import CreateFamily
import Parameter
import Place
import Select
import Window

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

class Schuecowindow():
   
    def __init__(self):
        pass

        ######  Variables  ######
        """
        self.wtypename=""
        self.wtemppth=""
        self.doc=()
        self.placehold=self.wtypename
        ###### Automatic Functions ######
        
        self.famwindow(self.wtemppth,self.wtypename)
        self.windowpanel(self.famwindow(self.wtemppth,self.wtypename))
        #self.famwindow.LoadFamily(self.doc)
        """


    def famwindow (self,wtemppth,wtypename):
        return Create.FamilyNew(wtemppth,wtypename)
    
    def windowpanel(self,famwindow,ventname, thickness, materialname):
        return Window.NewPanel(famwindow, ventname, thickness, materialname)
    
    def placefrhor(self,famwindow,frame,place):
        return Window.NewHorizontalFrameInstance(famwindow,frame,place,False)
    
    def placefrvert(self,famwindow,frame,place):
        return Window.NewVerticalFrameInstance(famwindow,frame,place,False)

    def loadwindow(self,doc,famwindow):
        class FamilyOption(IFamilyLoadOptions):
	        def OnFamilyFound(self, familyInUse, overwriteParameterValues):
		        overwriteParameterValues = True
		        return True

	        def OnSharedFamilyFound(self, sharedFamily, familyInUse, source, overwriteParameterValues):
		        return True
        famwindow.LoadFamily(doc, FamilyOption())

    #def windowdim(self,famwindow, typepanel):
    #    return Window.Dimensions(famwindow,typepanel)
    

if __name__ == '__main__':
    pass
