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

import schuecobim as s



window=s.windowschueco.Schuecowindow()

#from imp import reload

### Windowobject variable input ###

wtypename="Schueco_UDC-80-UZB_Win-in_Family01"
wtemppth="D:\Schueco\Programming\Develping_projects_local\Revit Templates\F_Window.rft"

#print window.placehold

famwindow=window.famwindow(wtemppth,wtypename)

### Windowobject run funcion ###

#famwindow=s.windowschueco.Schuecowindow()

files = ["Schueco_UDC-80-UZB_Frame_H01"]#,"Schueco_UDC-80-UZB_Frame_H02","Schueco_UDC-80-UZB_Frame_V01","Schueco_UDC-80-UZB_Frame_V02"]
detpth= "D:\\Schueco\\Programming\\Develping_projects_local\\Revit Templates\\Detail Item.rft" #automate
fname= "schueco_det_prof"
fdname = "Schueco_ USC-Cust_ Det"
frametmplpth= "D:\\Schueco\\Programming\\Develping_projects_local\\Revit Templates\\D_Frame_Window.rft" #automate
contour= "a_simp-prof" # atomate
#refline="a_ref-line1" # automate
#refpl="Reference line 1"
extrloc="Axis" # inside class
doc= Revit.ActiveDBDocument

for a in files:
    path = "C:\\Dropbox\\00_TOMAS\\00_PC\\01_Work\\00_Schueco\\Develping_projects_local\\Rhino_files\\FrameFiles\\{}".format(a) ### Change path!!!
    #print (path)
    rs.DocumentModified(False)
    rs.Command("! _-New None")
    rs.Command('-Open "{}" _Enter'.format(path))
    s.frameschueco.Schuecoframe(detpth,fname,fdname,a,frametmplpth,contour,extrloc,famwindow)
    rs.Command("! _-New None")

window.windowpanel(famwindow)

frplaces=["Bottom"]#,"Top","Right","Left"]

for i,j in enumerate(files):
    if "H" in j:
        #print j
        window.placefrhor(famwindow,j,frplaces[i])
    else:
        window.placefrvert(famwindow,j,frplaces[i])


famwindow.LoadFamily(doc)

family=s.familyschueco.SchuecoFamily()

family.windowinstace(doc,wtypename,"A.01,Axis,1.01","2.01","B.01")