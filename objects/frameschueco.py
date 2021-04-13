import sys
sys.path.append("C:\\Users\\tomas\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMengine\\functions\\Rhino_Modules")
sys.path.append("C:\\Users\\tomas\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMengine\\functions\\Rhino_Revit_Modules")
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

class Schuecoframe():
    """ 
    This class creates nested generic families in Revit containing detail items from detail cad drawings and creates an extrusion to represent a 3d window frame  inside a window family file
    It uses Revit family templates to create the type of families. 
    Parameters:
    dtemplpath(str):"Family detail template path"
    famname(str):"Family name"
    famdetname(str): "Family detail name"
    typename(str): "Name of the family type"
    famproftempath(str): "Family profile template path"
    contournm(str): "Name of the contour polyline in the rhino file" ** this is temporary

    """ 
    

    def __init__(self,dtemplpath,famname,famdetname,typename,famframetempath,contournm,reflinerh,refplane,extlocation,famwindow):
        ############## Variables  ###########
        
        self.objs= Select.AllObjectsName()
        
        self.docr=Revit.ActiveDBDocument
        
        ############## Function Calling ##############

        #self.objects(self.objs)  # 1 select all profile polylines from Rhino file _ consider erase the variable *** done (self.articles=) erased

        self.newfamdoc=self.newfam(dtemplpath,famname) # 2 Create a detail family doc for each detail inside the drawing

        self.detailitem(self.objects(self.objs),famdetname,dtemplpath) # 3 Creates a lists of detail families_Consider erease the variable *** done (self.nesteddetitem=) erased

        self.place_detailitem(self.newfamdoc) # 4 places the detail items in their place _ Consider erase the variable *** done (self.newdetfaminst=) erased

        self.famframe=self.prof_fam(famframetempath,typename) # famframe # 5 ------ ??? temp_path window template path?_  can be raplaced for other function-?

        self.reflinervt=self.refline(self.famframe,reflinerh,refplane) # 6 What should we do with this then?

        self.famload(self.newfamdoc,self.famframe) # 7 loads detail family to the frame family _Consider erase the variable *** done (self.proffile=) erased
        
        self.proffiledet=self.placedetail(self.famframe) # 8 ------- ???? _Consider erase the variable

        self.revitcontour=self.revitlines(contournm) # 9 converts rhino polyline contour into revit contour

        self.revitextrusion=self.revit_extrusion(self.famframe,self.revitcontour,extlocation) # 10 Creates Profile extrusion inside revit profile family

        self.cornervoids(self.famframe,contournm)  # 11 Creates voids
        
        #self.lockrvt=self.lock(self.proffamil,self.reflinervt,self.revitextrusion) 

        self.dimension(self.famframe,refplane) # 11 Creates dimension parameter in profile family _ Consider erase the variable 

        self.famload(self.famframe,famwindow) # 12 Loads profile family into mother family _ Consider erase the variable

        #self.load_frame() ## Variable?
    
        self.windowdim(famwindow)
  

    # success :)

    def objects (self,obj):    
        objsfam = [x for x in obj if not "a_" in x]
        return objsfam

    # success :)   

    def newfam (self,temp,name): #always self in object methods.  # this should create a new family doc that hosts the detail family list 
        # temp=self.newfam_det_temp_path #self missing
        # name=self.newfam_name #self missing
        return Create.FamilyNew(temp,name)
    
    #newdetfaminst=newfam(dtemplpath,famname)
    
    # sucess :)
    # delete gaskets and isolation in rhino file
    def detailitem (self,familyobjects,famdetname,dtemplpath): # this should create a list of families 

        #familyobjects=self.objects(self.objs)
        #detailname=self.newfam_detail_name #self missing
        #temppath=self.newfam_det_temp_path #self missing
        famnew=self.newfamdoc 
        #print famnew
        output=[]
        for i,j in enumerate(familyobjects,1):
            output.append(Create.DetailItems(j,famdetname+str(i),famnew,dtemplpath))
        return output

    #newdetailfamilydoc=self.newfam()
    # :)  succeess 

    def place_detailitem(self,fam): # this places the detail item files in their place . Outputs a family instances list
        #print fam
        return Place.DetailItems(fam)
    
    # :) Success 
    def prof_fam(self,path,name_type):### Error
        # path=self.newfam_prof_temp_path #self missing
        # name_type=self.typename #self missing
        return Create.FamilyNew(path,name_type)
    # :) Success 
    def famload (self,detaildoc,famprof): 
        #famprof=prof_fam()
        return detaildoc.LoadFamily(famprof)
    # :) Success
    def placedetail (self,famprof):
        #famprof=self.prof_fam(self.newfam_prof_temp_path,self.typename)
        return Place.DetailItemInprof(famprof)
    # :) Success
    def revitlines(self,prof_contour):
        #prof_contour=self.contour
        return ConvertPoly.ToRvtline(prof_contour)
    # :) Success :)
    def revit_extrusion(self,famprof,lines,locationref):
        # famprof=prof_fam()
        # lines=revitlines()
        return CreateExtrusion.NewProfile(famprof,lines,locationref,"Frame")

    def cornervoids(self,famframe,prof_contour): # new
        return Window.FrameCornerVoids(famframe,prof_contour)

    # :) Success 
    def refline(self,famprof,refl,refpl):
        return Create.ReferenceLine(famprof,refl,refpl)
    
    #:) :) :)
    def dimension(self,famprof,nrefname):
        return Create.NewDimension(famprof,nrefname,"Frame")

    def load_frame(self,famframe,famwindow): 
        return famframe.LoadFamily(famwindow)

    def windowdim(self,famwindow):
        return Window.Dimensions(famwindow)
    

if __name__ == '__main__':
    pass
