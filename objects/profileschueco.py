import sys
sys.path.append("C:\\Users\\menatj\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMEngine\\objects")
sys.path.append("C:\\Users\\menatj\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMEngine\\functions\\Rhino_Modules")
sys.path.append("C:\\Users\\menatj\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMEngine\\functions\\Rhino_Revit_Modules")
import blockorg_00
import corners
import simplify
import ConvertPoly
import Create
import CreateExtrusion
import Parameter
import Place
import Select

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
    


class Schuecoprofile():

    
    def __init__(self,dtemplpath,famname,famdetname,inst,typename,famproftempath,contournm,extlocation):
        
        """
        inputs =>

        1.- dtemplpath : Detail template path (Shared)
        2.- famname : Detail Mother family Name (Shared)
        3.- famdetname : Each article number as detail item (Shared)
        4.- inst : boundled block ID ()
        5.- typename : boundled block Name ()
        6.- famframetempath : 
        7.- contournm
        8.- extlocation :
        9.- famwindow: 

        """
        
        
        
        ############## Variables  ###########
        
        #self.elements = blockorg_00.block_org(typename)
        
        self.docr=Revit.ActiveDBDocument

        #self.objs= Select.AllObjectsName()
       
    
        ############## Function Calling ##############
        prb=inst

        self.newfamdoc=self.newfam(dtemplpath,famname) # 2 Create detail 

        self.detailitem(inst[1], inst[0],famdetname,dtemplpath,self.newfamdoc) # 3 Create a detail family doc for each item

        self.place_detailitem(self.newfamdoc) # 4 Places the detail items in their place

        self.proffamil=self.prof_fam(famproftempath,typename)

        self.reflinervt=self.refline(self.proffamil)
        
        self.famload(self.newfamdoc,self.proffamil) #Family
        
        self.proffiledet=self.placedetail(self.proffamil)
        
        self.revitcontour=self.revitlines(contournm)
        
        self.revitextrusion=self.revit_extrusion(self.proffamil,self.revitcontour,contournm,extlocation)
        
        self.dimension(self.proffamil)
        
        self.famload(self.proffamil,self.docr)
    
    """
    def blockorg(self):
        return blockorg.block_org()

    def objects (self,obj):   
        #objsfam = [x for x in obj if not "a_" or "Ref" in x]
        objsfam =[]
        for i in obj:
            if not "a_" in i:
                objsfam.append(i)
        return objsfam"""

    def newfam (self,temp,name): 
        return Create.FamilyNew(temp,name)
    
    def detailitem (self,objectname,dic,famdetname,dtemplpath,famnew):
        output=[]
        for i,j in enumerate(objectname,1):
            output.append(Create.DetailItems(j,dic,famdetname+str(i),famnew,dtemplpath))
        return output

    def place_detailitem(self,fam): 
        return Place.DetailItems(fam)
    
    def prof_fam(self,path,name_type):
        return Create.FamilyNew(path,name_type)

    def famload (self,detaildoc,famprof):
        return detaildoc.LoadFamily(famprof)
    
    def placedetail (self,famprof):
        return Place.DetailItemInprof(famprof)
    
    def revitlines(self,prof_contour):
        return ConvertPoly.ToRvtline(prof_contour)
    
    def revit_extrusion(self,famprof,lines,prof_contour,locationref):
        return CreateExtrusion.NewProfile(famprof,lines,locationref,prof_contour,"Profile")
     
    def refline(self,famprof):
        return Create.ReferenceLines(famprof,"Profile")
    
    def dimension(self,famprof):
        return Create.NewWidthDimension(famprof,"Profile")

if __name__ == '__main__':
    pass
