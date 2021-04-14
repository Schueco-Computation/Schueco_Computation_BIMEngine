import rhinoscriptsyntax as rs
import schuecobim as s
from RhinoInside.Revit import Revit, Convert

class unit ():

    def __init__(self):
        
    #### //// PROFILE FILES //// ####
    files=("V02_75mm","V04_75mm","V04_270mm","H01-2_75mm", "H01-1_75mm","H02_147mm")
    
    
    ##### //// PROFILE CREATION PARAMETERS //// ##### 
    detpth= "E:\Schueco\Programming\Revit_Templates\Detail Item.rft" #automate
    fname= "schueco_det_prof"
    fdname = "Schueco_ USC-Cust_ Det_ H02_"
    proftmplpth= "E:\Schueco\Programming\Revit_Templates\A_Profile.rft" #automate
    contour= "a_simp-prof" # atomate
    refline="a_ref-line1" # automate
    refpl="Reference line 1"
    extrloc="Axis" # inside class
    doc= Revit.ActiveDBDocument

    ##### /// WINDOW CREATON PARAMETERS /// ####

    famwindow= ()
    wtypename= () #  is repeated

    ##### //// FRAME CREATION PARAMETERS //// #####

    files=()
    wtypename= ()

    



    ################################# //// FAMILY OBJECTS PARAMETERS //// ############################
    
    ## //// VERTICAL PROFILES PLACEMENT PARAMETERS  ///###
    ### no mirror profiles##
    nmirrpv=("V02_75mm","V04_270mm")
    vnmirrk=("C,Axis,1","B,Axis,1.01")
    vnmirrenpl=("3.01","2.01")
    ### mirror profiles ###
    mirrpv=("V04_75mm","V02_75mm")
    vmirrk=("A,Axis,1","A,Axis,2.01")
    vmirrenpl=("2.01","3.01")
    Vplace=s.familyschueco.SchuecoFamily()


    ### /// HORIZONTAL PROFILES PLACEMENT PARAMETERS /// ###
    Hp=("H02_147mm", "H01-2_75mm", "H01-1_75mm")
    hk=("A.01,Axis,2", "A,Axis,1", "A,Axis,3" )
    henpl=("C.01", "C", "C")

    Hplace=s.familyschueco.SchuecoFamily()
    ###### /// panels/// ####
    panelgl=s.familyschueco.SchuecoFamily()

    ####cglazong
    lckkeyp="A.01,Axis,1.01"
    hegihtpnl="2.01"
    widthpnl="B.01"
    ##### spandrell
    panelsp=s.familyschueco.SchuecoFamily()
    lckkeysp= "A.01,Ext. Axis 1,2.01"
    heightsp="3.01"
    widthsp="C.01"

    ###### Profile Creation ####


    #for i in files:
    #    path = "C:\\Dropbox\\00_TOMAS\\00_PC\\01_Work\\00_Schueco\\Develping_projects_local\\Rhino_files\\Renamed_files\\{}".format(i) ### Change path!!!
    #    #print (path)
    #    rs.DocumentModified(False)
    #    rs.Command("! _-New None")
    #    rs.Command('-Open "{}" _Enter'.format(path))
    #    fdname="Schueco_ USC-Cust_ Det_{}".format(i)
    #    s.profileschueco.Schuecoprofile(detpth,fname,fdname,i,proftmplpth,contour,refline,refpl,extrloc)
    #    rs.Command("! _-New None")


    ##### Profile Placement #####

    for i,j in enumerate(nmirrpv):
        Vplace.instanceplacementV(doc,j,vnmirrk[i],vnmirrenpl[i],1)

    for i,j in enumerate(mirrpv):
        Vplace.instanceplacementV(doc,j,vmirrk[i],vmirrenpl[i],0)

    for i,j in enumerate(Hp):
        Hplace.instanceplacementH(doc,j,hk[i],henpl[i],0)


    #### Panel Placement #####


    panelgl.panelplacement(doc,"Glz",54,lckkeyp,hegihtpnl,widthpnl)
    panelsp.panelplacement(doc,"Spandrel",276,lckkeysp,heightsp,widthsp)