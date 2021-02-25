# Enable Python support and load DesignScript library
import sys
sys.path.append("C:\\Users\\tomas\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMengine\\functions\\Rhino_Modules")
sys.path.append("C:\\Users\\tomas\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMengine\\functions\\Rhino_Revit_Modules")
# import blockorg
# import corners
# import simplify
# import ConvertPoly
# import Create
# import CreateExtrusion
# import CreateFamily
# import Parameter
# import Place
# import Select
import family
# import clr

# clr.AddReference('RhinoInside.Revit')
# clr.AddReference('RevitAPIUI')

# import rhinoscriptsyntax as rs
# import Rhino
# from Rhino import Geometry as rg
# import RhinoInside as ri
# clr.AddReference('ProtoGeometry')
# from Autodesk.DesignScript.Geometry import *

# #Import RevitAPI
# clr.AddReference("RevitAPI")
# #import Autodesk.Revit.DB as re
# from Autodesk.Revit.DB import*
# import Autodesk.Revit.Creation as oCreate
# import Autodesk.Revit.ApplicationServices.Application 

# # rhino.inside utilities
# from RhinoInside.Revit import Revit, Convert
# clr.ImportExtensions(Convert.Geometry)

# # Import DocumentManager and TransactionManager
# clr.AddReference("RevitServices")
# from RevitServices.Persistence import DocumentManager
# from RevitServices.Transactions import TransactionManager


#Document = Revit.ActiveDBDocument

class SchuecoFamily():

    """" Schueco Family """

    def __init__(self,Document, TypeName, LocationKeyV, EndRefPlaneV,LocationKeyH,EndRefPlaneH, MirrorBoolean):
        self.instanceplacementV=family.NewVerticalProfileInstace(Document,TypeName,LocationKeyV,EndRefPlaneV,MirrorBoolean)
        self.instanceplacementH=family.NewHorizontalProfileInstace(Document,TypeName,LocationKeyH,EndRefPlaneH,MirrorBoolean)
    
if __name__ == '__main__':
    pass
