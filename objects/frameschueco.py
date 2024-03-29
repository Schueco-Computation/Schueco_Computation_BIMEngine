import sys
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

class Schuecoframe():
   
    def __init__(self,dtemplpath,famname,famdetname,inst,typename,famframetempath,contournm,extlocation,famwindow):
        
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
        

        #self.inst=blockorg_00.block_org(typeID) ## Remove funtcion from object class.


        self.docr=Revit.ActiveDBDocument
        
        #self.objs= Select.AllObjectsName()
        
        ############## Function Calling ##############

        self.newfamdoc=self.newfam(dtemplpath,famname) # 2 Create a detail family doc for each detail inside the drawing

        ## pass parameters of rhino guids and names from outside of Schuecoframe 
        self.detailitem(inst[1],inst[0],famdetname,dtemplpath,self.newfamdoc) # 3 Creates a lists of detail families_Consider erease the variable *** done (self.nesteddetitem=) erased


        self.place_detailitem(self.newfamdoc) # 4 places the detail items in their place _ Consider erase the variable *** done (self.newdetfaminst=) erased

        self.famframe=self.prof_fam(famframetempath,typename) # famframe # 5 ------ ??? temp_path window template path?_  can be raplaced for other function-?

        self.reflinervt=self.refline(self.famframe) # 6 What should we do with this then?

        self.famload(self.newfamdoc,self.famframe) # 7 loads detail family to the frame family _Consider erase the variable *** done (self.proffile=) erased
        
        self.proffiledet=self.placedetail(self.famframe) # 8 ------- ???? _Consider erase the variable

        self.revitcontour=self.revitlines(contournm) # 9 converts rhino polyline contour into revit contour

        self.revitextrusion=self.revit_extrusion(self.famframe,self.revitcontour,contournm,extlocation) # 10 Creates Profile extrusion inside revit profile family

        self.cornervoids(self.famframe,contournm)  # 11 Creates voids

        self.dimension(self.famframe) # 11 Creates dimension parameter in profile family _ Consider erase the variable 

        self.famload(self.famframe,famwindow) # 12 Loads profile family into mother family _ Consider erase the variable
  

    def newfam (self,temp,name):
        return Create.FamilyNew(temp,name)
    
    def detailitem (self,objectname,dic,famdetname,dtemplpath,famnew):  # deals with GUIDs rhino. 
            output=[]
            for i,j in enumerate(objectname,1):
                output.append(Create.DetailItems(j,dic,famdetname+str(i),famnew,dtemplpath))
            return output

    def place_detailitem(self,fam):
        return Place.DetailItems(fam)
    
    def prof_fam(self,path,name_type):
        return Create.FamilyNew(path,name_type)
    
    def famload(self,detaildoc,famprof):
        return detaildoc.LoadFamily(famprof)
   
    def placedetail (self,famprof):
        return Place.DetailItemInprof(famprof)
    
    def revitlines(self,prof_contour): #Rhino Contour to Revit
        return ConvertPoly.ToRvtline(prof_contour)
    
    def revit_extrusion(self,famprof,lines,prof_contour,locationref):
        return CreateExtrusion.NewProfile(famprof,lines,prof_contour,locationref,"Frame")

    def cornervoids(self,famprof,prof_contour): 
        return Window.FrameCornerVoids(famprof,prof_contour) # Rhino boundingbox

    def refline(self,famprof):  # Rhino Ref_lines to Revit  
        return Create.ReferenceLines(famprof,"Frame") 
   
    def dimension(self,famprof): # Rhino Reflines
        return Create.NewWidthDimension(famprof,"Frame")
    

if __name__ == '__main__':
    pass

#Example of Child Class
"""
class Schuecovent(Schuecoframe):

    def __init__(self,dtemplpath,famname,famdetname,typename,famframetempath,contournm,extlocation,famwindow,contournmvoid):
        Schuecoframe.__init__(self,dtemplpath,famname,famdetname,typename,famframetempath,contournm,extlocation,famwindow)

        self.dimension(self.famframe)
        self.rvtlinesvoid = self.revitlinesvoid(contournmvoid) 
        self.revitextrusion = self.revit_extrusion(self.famframe,self.revitcontour,extlocation)
        self.voids(self.famframe,self.rvtlinesvoid, self.reflinervt, self.revitextrusion)
        self.windowdim(famwindow)

    def dimension(self,famprof):
        return Create.NewWidthDimension(famprof,"Vent")

    def revitlinesvoid(self,prof_contour):
        return ConvertPoly.ToRvtline(prof_contour)
    
    def revit_extrusion(self,famprof,lines,locationref):
        return CreateExtrusion.NewProfile(famprof,lines,locationref,"Vent")

    def cornervoids(self,famprof,prof_contour): pass
        #return Window.FrameCornerVoids(famprof,prof_contour)

    def voids(self,famprof, RvtVoidLines, ReferencePlane1, Solid): 
        return Window.VentVoids(famprof, RvtVoidLines, ReferencePlane1, Solid)

    def windowdim(self,famwindow):
        return Window.Dimensions(famwindow,"Vent")
      
if __name__ == '__main__':
    pass"""