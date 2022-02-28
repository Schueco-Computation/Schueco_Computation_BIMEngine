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
##BEFORE RUNNING REMEMBER TO LOAD THE wINDOW FAMILY FIRST INTO THE fAMILY UNIT AND OVERWRITE ALL ELEMENTS

doc = Revit.ActiveDBDocument
files = "Schueco_VentPanel-Window_170mm"
wtypename = "Schueco_VentPanel-Window_170mm"
#famwindow = schueco.Create.FamilyNew("D:\F_Window.rft", wtypename)


objs = schueco.Select.AllObjectsName()

objsfam = [x for x in objs if not "a_" in x]

newfam = schueco.Create.FamilyNew("K:\Engineering\Abteilungen\ES\Computation\BIM_strategie\BIM Workflow\Revit templates\Detail Item.rft", "Schueco_Det_Prof")

output = []

for i,j in enumerate(objsfam, 1):
    f = schueco.Create.DetailItems(j, "Schueco_Cust_Det_VentPanel_"+ str(i), newfam, "K:\Engineering\Abteilungen\ES\Computation\BIM_strategie\BIM Workflow\Revit templates\Detail Item.rft" )
    output.append(f)

place = schueco.Place.DetailItems(newfam)

###################################

famvent = schueco.Create.FamilyNew("K:\Engineering\Abteilungen\ES\Computation\BIM_strategie\BIM Workflow\Revit templates\C_VentPanels.rft", files)

#Reference Lines ya fue actualizada en visual studio code

refl = schueco.Create.ReferenceLines(famvent, "Frame")

#New update for widthdimension to take in consideration vent --> LISTO

dim = schueco.Create.NewWidthDimension(famvent, "Vent")

loadet = newfam.LoadFamily(famvent)

placedet = schueco.Place.DetailItemInprof(famvent)

#New update for this function --> LISTO

rvtlines = schueco.ConvertPoly.ToRvtline("a_simp-prof")

#New: for vent
rvtlinesvoid = ToRvtline("a_void")

#New: update for extrusion to take in consideration vent too --> LISTO

prof = schueco.CreateExtrusion.NewProfile(famvent, rvtlines, "Axis", "Vent")

#New: VentVoids --> LISTO

void = schueco.Window.VentVoids(famvent, rvtlinesvoid, refl, prof)

load = famvent.LoadFamily(doc)

# New update for this function to take in consideration vent too --> LISTO

paramdim = schueco.Window.Dimensions(doc, "Schueco_VentPanel-Window_170mm")
#    rs.Command("! _-New None")


#NewFrameInstance

framevOne = schueco.Window.NewVerticalFrameInstance(doc, "Schueco_Cust_Frame_V01_20mm", "Right", False)
framevTwo = schueco.Window.NewVerticalFrameInstance(doc, "Schueco_Cust_Frame_V02_20mm", "Left", False)
framehOne = schueco.Window.NewHorizontalFrameInstance(doc, "Schueco_Cust_Frame_V01_20mm", "Bottom", False)
framehOne = schueco.Window.NewHorizontalFrameInstance(doc, "Schueco_Cust_Frame_V02_20mm", "Top", False)

#New update Panel Instance to take in consideration vent too --> LISTO

window = schueco.Window.NewPanel(doc, "Schueco_VentPanel-Window_170mm", 41)

print window