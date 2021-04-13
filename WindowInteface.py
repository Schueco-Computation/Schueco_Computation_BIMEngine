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

import schueco
#from imp import reload

doc = Revit.ActiveDBDocument
files = ["Schueco_UDC-80-UZB_Frame_H01","Schueco_UDC-80-UZB_Frame_H02","Schueco_UDC-80-UZB_Frame_V01","Schueco_UDC-80-UZB_Frame_V02"]
wtypename = "Schueco_UDC-80-UZB_Win-in_Family01" 
famwindow = schueco.Create.FamilyNew("D:\F_Window.rft", wtypename) #windowtemplate

for a in files:
    path = "C:\\Users\\ramijc\\Desktop\\New folder\\{}".format(a) ### Change path!!!
    #print (path)
    rs.DocumentModified(False)
    rs.Command("! _-New None")
    rs.Command('-Open "{}" _Enter'.format(path))
    
    objs = schueco.Select.AllObjectsName()

    objsfam = [x for x in objs if not "a_" in x]

    newfam = schueco.Create.FamilyNew("D:\Detail Item.rft", "Schueco_Det_Prof")

    output = []

    for i,j in enumerate(objsfam, 1):
        f = schueco.Create.DetailItems(j, "Schueco_ USC-Cust_ Det_ H02_"+ str(i), newfam, "D:\Detail Item.rft" )
        output.append(f)

    place = schueco.Place.DetailItems(newfam)

    ###################################

    rvtlines = schueco.ConvertPoly.ToRvtline("a_simp-prof")

    famframe = schueco.Create.FamilyNew("D:\D_Frame_Window.rft", a)

    loadet = newfam.LoadFamily(famframe)

    placedet = schueco.Place.DetailItemInprof(famframe)

    #Updated
    prof = schueco.CreateExtrusion.NewProfile(famframe, rvtlines, "Axis", "Frame")

    #New: CornerVoids

    void = schueco.Window.FrameCornerVoids(famframe, "a_simp-prof")

    refl = schueco.Create.ReferenceLine(famframe, "a_ref-line1", "Reference line 1")

    #Arreglar
    #lock = schueco.Create.NewAlignment(famframe, refl, prof)

    #Updated

    dim = schueco.Create.NewDimension(famframe, "Reference line 1", "Frame")

    load = famframe.LoadFamily(famwindow)
    
    #New: Dimension parameters for window family

    paramdim = schueco.Window.Dimensions(famwindow)

    rs.Command("! _-New None")


#New: NewFrameInstance

framevOne = schueco.Window.NewVerticalFrameInstance(famwindow, "Schueco_UDC-80-UZB_Frame_V01", "Right", False)
framevTwo = schueco.Window.NewVerticalFrameInstance(famwindow, "Schueco_UDC-80-UZB_Frame_V02", "Left", False)

framehOne = schueco.Window.NewHorizontalFrameInstance(famwindow,"Schueco_UDC-80-UZB_Frame_H01", "Bottom", False)
framehTwo = schueco.Window.NewHorizontalFrameInstance(famwindow, "Schueco_UDC-80-UZB_Frame_H02", "Top", False)

#New: NewPanel Instance

window = schueco.Window.NewPanel(famwindow, "Glz", 41)




### interface #### 

load = famwindow.LoadFamily(doc)

winInstance = schueco.Family.NewWindowInstance(doc, wtypename, "A.01,Axis,1.01", "2.01", "B.01")

print winInstance