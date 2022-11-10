import sys
sys.path.append("C:\\Users\\menatj\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMEngine\\objects")
sys.path.append("C:\\Users\\menatj\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMEngine\\functions\\Rhino_Modules")
sys.path.append("C:\\Users\\menatj\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMEngine\\functions\\Rhino_Revit_Modules")
import rhinoscriptsyntax as rs
import schuecobim as s
from RhinoInside.Revit import Revit, Convert
import blockorg
import blockorg_00
import block_finder_ref
import block_finder_mirr

##### //// PROFILE CREATION PARAMETERS //// ##### 

files=["V02_75mm"]#,"V04_75mm","V04_270mm","H01-2_75mm", "H01-1_75mm","H02_147mm")
detpth= "K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Revit templates\\Detail Item.rft" #automate
fname= "schueco_det_prof"
fdname = "Schueco_ USC-Cust_ Det_ H02_"
proftmplpth= "K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Revit templates\\A_Profile.rft" #automate
contour= "a_simp-prof" # atomate
#refline="a_ref-line1" # automate
#refpl="Reference line 1"
extrloc="Axis" # inside class
doc= Revit.ActiveDBDocument

"""
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

"""

###### Profile Creation ####


# for i in files:
#     path = "C:\\Dropbox\\00_TOMAS\\00_PC\\01_Work\\00_Schueco\\Develping_projects_local\\Rhino_files\\Renamed_files\\{}".format(i) ### Change path!!!
#     #print (path)
#     rs.DocumentModified(False)
#     rs.Command("! _-New None")
#     rs.Command('-Open "{}" _Enter'.format(path))
#     fdname="Schueco_ USC-Cust_ Det_{}".format(i)
#     s.profileschueco.Schuecoprofile(detpth,fname,fdname,i,proftmplpth,contour,extrloc)
#     rs.Command("! _-New None")

profile_names= []
        
inst_list=block_finder_ref.block_finder()[0]
inst_list_id=block_finder_ref.block_finder()[1]

for a,b in enumerate(inst_list):
    ax=""
    for b_o in rs.BlockObjects(b):
        if rs.ObjectLayer(b_o)== "y":
            ax=rs.ObjectLayer(b_o)

    i= (str(b)+ "_" + str(a))
    profile_names.append(i)
    if "_V" in i and ax!= "y":
        block_finder_ref.block_mover(b,270,"a_ref-line2")
        rs.SelectObject(inst_list_id[a][0])
        rs.ZoomSelected()
        rs.Command("_Isolate")
        inst_unpk=blockorg_00.block_org(inst_list_id[a])
        s.profileschueco.Schuecoprofile(detpth,fname,fdname,inst_unpk,i,proftmplpth,contour,extrloc)
        guids=inst_unpk[2]
        rs.Command("_Show")
        rs.Command("_Zoom_Extent")
        rs.LockObjects(guids)

    elif "_V" in i and ax== "y":
        block_finder_ref.block_mover(b,270,"y")
        rs.SelectObject(inst_list_id[a][0])
        rs.ZoomSelected()
        rs.Command("_Isolate")
        inst_unpk=blockorg_00.block_org(inst_list_id[a])
        s.profileschueco.Schuecoprofile(detpth,fname,fdname,inst_unpk,i,proftmplpth,contour,extrloc)
        guids=inst_unpk[2]
        rs.Command("_Show")
        rs.Command("_Zoom_Extent")
        rs.LockObjects(guids)
    else:
        ""

    if "_H" in i and ax!= "y":
        block_finder_mirr.block_mover(b,inst_list_id[a],180,"a_ref-line2")
        rs.SelectObject(inst_list_id[a][0])
        rs.ZoomSelected()
        rs.Command("_Isolate")
        inst_unpk=blockorg_00.block_org(inst_list_id[a])
        s.profileschueco.Schuecoprofile(detpth,fname,fdname,inst_unpk,i,proftmplpth,contour,extrloc)
        guids=inst_unpk[2]
        rs.Command("_Show")
        rs.Command("_Zoom_Extent")
        rs.LockObjects(guids)

    elif "_H" in i and ax== "y":
        block_finder_mirr.block_mover(b,inst_list_id[a],180,"y")
        rs.SelectObject(inst_list_id[a][0])
        rs.ZoomSelected()
        rs.Command("_Isolate")
        inst_unpk=blockorg_00.block_org(inst_list_id[a])
        s.profileschueco.Schuecoprofile(detpth,fname,fdname,inst_unpk,i,proftmplpth,contour,extrloc)
        guids=inst_unpk[2]
        rs.Command("_Show")
        rs.Command("_Zoom_Extent")
        rs.LockObjects(guids)
    else:
        ""
"""


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
"""