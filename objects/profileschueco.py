import sys
sys.path.append("C:\\Users\\tomas\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMengine\\functions\\Rhino_modules")
sys.path.append("C:\\Users\\tomas\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMengine\\functions\\Rhino_Revit_Modules")
import blockorg
import corners
import simplify
import ConvertPoly
import Create
import CreateExtrusion
import CreateFamily
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
#dtemplpath,famname,famdetname,typename,famproftempath,contour
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
    def __init__(self,dtemplpath,famname,famdetname,typename,famproftempath,contournm):
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
        ############## automatic functions ###########
        self.objects(self.objs)
        self.newfam(dtemplpath,famname)
        self.detailitem(self.objects(self.objs))
        self.place_detailitem(self.newfam(famproftempath,famdetname))
        self.prof_fam(famproftempath,typename)
        self.famload(self.prof_fam(famproftempath,typename))
    
    
    
    
    def objects (self,obj):    
        objsfam = [x for x in obj if not "a_" in x]
        return objsfam
       
    def newfam (self,temp,name): #always self in object methods. 
        temp=self.newfam_det_temp_path #self missing
        name=self.newfam_name #self missing
        return Create.FamilyNew(temp,name)

    def detailitem (self,familyobjects):
        familyobjects=self.objects(self.objs)
        detailname=self.newfam_detail_name #self missing
        temppath=self.newfam_det_temp_path #self missing
        famnew=self.newfam(temppath,detailname)
        output=[]
        for i,j in enumerate(familyobjects,1):
            output.append(Create.DetailItems(j,detailname+str(i),famnew,temppath))
        return output
    
    def place_detailitem(self,fam):
        fam=self.newfam(self.newfam_det_temp_path,self.newfam_detail_name)
        return Place.DetailItems(fam)
    
    def prof_fam(self,path,name_type):
        path=self.newfam_prof_temp_path #self missing
        name_type=self.typename #self missing
        return Create.FamilyNew(path,name_type)

    def famload (self,famprof):
        #famprof=prof_fam()
        return self.newfam(self.newfam_det_temp_path,self.newfam_name).LoadFamily(famprof)

    def placedetail (famprof):
        famprof=self.prof_fam()
        return Place.DetailItemInprof(famprof)
    
    def revitlines(prof_contour):
        prof_contour=self.contour
        return ConvertPoly.ToRvtline(prof_contour)

    def revit_extrusion(famprof,lines):
        famprof=prof_fam()
        lines=revitlines()
        return CreateExtrusion(famprof,lines,0)

    # def ref1 ():


    # def art():
    #     s.blockorg.block_org()


# profA=Profile()
# print profA.articles,profA.corners,profA.polyline

if __name__ == '__main__':
    pass
