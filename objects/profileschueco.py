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

class Schuecoprofile():
    """ 
    This class creates nested generic families in Revit containing detail items from detail cad drawings and creates an extrusion to represent a 3d profile inside a mother family unit
    It uses Revit family templates to create the type of families. 
    Parameters:
    dtemplpath(str):"Family detail template path"
    famname(str):"Family name"
    famdetname(str): "Family detail name"
    typename(str): "Name of the family type"
    famproftempath(str): "Family profile template path"
    contournm(str): "Name of the contour polyline in the rhino file" ** this is temporary

    """ 
    

    def __init__(self,dtemplpath,famname,famdetname,typename,famproftempath,contournm,reflinerh,refplane,extlocation):
        # self.articles=blockorg.block_org()
        # self.corners=corners.corners()
        # self.polyline=simplify.simplify()
        self.objs= Select.AllObjectsName()
        self.newfam_det_temp_path= dtemplpath
        self.newfam_name= famname
        self.newfam_detail_name= famdetname
        self.typename= typename
        self.newfam_prof_temp_path= famproftempath
        self.contour= contournm
        self.reflinerh= reflinerh
        self.refplane= refplane
        self.docr=Revit.ActiveDBDocument
        ############## Variables  ###########
        self.articles= self.objects(self.objs)
        self.newfamdoc=self.newfam(dtemplpath,famname)
        self.nesteddetitem=self.detailitem(self.objects(self.objs))
        self.newdetfaminst=self.place_detailitem(self.newfamdoc)
        self.proffamil=self.prof_fam(famproftempath,typename)
        self.proffile=self.famload(self.newfamdoc,self.proffamil) #Family
        self.proffiledet=self.placedetail(self.proffamil)
        self.revitcontour=self.revitlines(self.contour)
        self.revitextrusion=self.revit_extrusion(self.proffamil,self.revitcontour,extlocation)
        self.reflinervt=self.refline(self.proffamil,reflinerh,refplane)
        self.lockrvt=self.lock(self.proffamil,self.reflinervt,self.revitextrusion)
        self.ndimension=self.dimension(self.proffamil,refplane)
        self.famprofload=self.famload(self.proffamil,self.docr)
    
    
  

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
    def detailitem (self,familyobjects): # this should create a list of families 

        familyobjects=self.objects(self.objs)
        detailname=self.newfam_detail_name #self missing
        temppath=self.newfam_det_temp_path #self missing
        famnew=self.newfamdoc 
        #print famnew
        output=[]
        for i,j in enumerate(familyobjects,1):
            output.append(Create.DetailItems(j,detailname+str(i),famnew,temppath))
        return output

    #newdetailfamilydoc=self.newfam()
    # :)  succeess 

    def place_detailitem(self,fam): # this places the detail item files in their place . Outputs a family instances list
        #print fam
        return Place.DetailItems(fam)
    
    # :) Success ' can be replaced by newfam()
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
        return CreateExtrusion.NewProfile(famprof,lines,locationref,1)
    # :) Success 
    def refline(self,famprof,refl,refpl):
        return Create.ReferenceLine(famprof,refl,refpl)
    # :) Success
    def lock(self,famprof,refline,prof):
        return Create.NewAlignment(famprof,refline,prof)
    #:) :) :)
    def dimension(self,famprof,nrefname):
        return Create.NewDimension(famprof,nrefname)

if __name__ == '__main__':
    pass
