import sys
sys.path.append("C:\\Users\\ramijc\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMEngine\\functions\\Rhino_Modules")
sys.path.append("C:\\Users\\ramijc\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMEngine\\functions\\Rhino_Revit_Modules")
import blockorg
import corners
import simplify
import ConvertPoly
import Create
import CreateExtrusion
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

class Schuecovent():

    def __init__(self,dtemplpath,famname,famdetname,typename,famventtempath,contournm,extlocation,famwindow,contournmvoid):

        self.blockorg()
        self.docr=Revit.ActiveDBDocument
        self.allobjects = self.objs()
        
        self.newfamdoc=self.newfam(dtemplpath,famname)
        self.detailitem(self.objects(self.allobjects),famdetname,dtemplpath,self.newfamdoc)
        self.place_detailitem(self.newfamdoc)
        self.famvent=self.vent_fam(famventtempath,typename)
        self.reflinervt=self.refline(self.famvent)
        self.dimension(self.famvent)
        self.famload(self.newfamdoc,self.famvent)
        self.proffiledet=self.placedetail(self.famvent)
        self.revitcontour=self.revitlines(contournm)
        
        self.linesvoid = self.revitlinesvoid(contournmvoid)

        self.revitextrusion=self.revit_extrusion(self.famvent,self.revitcontour,extlocation)

        self.ventvoids(self.famvent, self.linesvoid, self.reflinervt, self.revitextrusion)

        self.famload(self.famvent,famwindow)


    def blockorg(self):
        return blockorg.block_org()
    
    def objs(self):
        return Select.AllObjectsName()

    def objects (self,obj):
        objsfam =[]
        for i in obj:
            if not "a_" in i:
                objsfam.append(i)
        return objsfam

    #def objects (self,obj):    
    #    objsfam = [x for x in obj if not "a_" in x]
    #    return objsfam

    def newfam (self,temp,name):
        return Create.FamilyNew(temp,name)
    
    def detailitem (self,familyobjects,famdetname,dtemplpath,famnew):  
            output=[]
            for i,j in enumerate(familyobjects,1):
                output.append(Create.DetailItems(j,famdetname+str(i),famnew,dtemplpath))
            return output

    def place_detailitem(self,fam):
        return Place.DetailItems(fam)
    
    def vent_fam(self,path,name_type):
        return Create.FamilyNew(path,name_type)
    
    def famload (self,detaildoc,famprof): 
        return detaildoc.LoadFamily(famprof)
   
    def placedetail (self,famprof):
        return Place.DetailItemInprof(famprof)
    
    def revitlines(self,prof_contour):
        return ConvertPoly.ToRvtline(prof_contour)
    
    def revit_extrusion(self,famprof,lines,locationref):
        return CreateExtrusion.NewProfile(famprof,lines,locationref,"Vent")

    def revitlinesvoid(self,prof_contour):
        return ConvertPoly.ToRvtline(prof_contour)
    
    def ventvoids(self,famprof, RvtVoidLines, ReferencePlane1, Solid):
        return Window.VentVoids(famprof, RvtVoidLines, ReferencePlane1, Solid)

    def refline(self,famprof):
        return Create.ReferenceLines(famprof,"Frame")
   
    def dimension(self,famprof):
        return Create.NewWidthDimension(famprof,"Vent")
    

if __name__ == '__main__':
    pass