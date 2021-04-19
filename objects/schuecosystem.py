import sys
sys.path.append("C:\\Users\\tomas\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMengine\\objects")
import rhinoscriptsyntax as rs
import profileschueco
import frameschueco
import windowschueco
import familyschueco
from RhinoInside.Revit import Revit, Convert

class Unit():
    """
                    ###### Shared Creation Parameters #####

                detpth= Detail template file path
                fname= Name of the detail family file that will be created
                fdname= Name of the detail that will be created
                contour= Cad drawing polylines Name inside of Rhino file representing profile or frame simplyfied contour
                extrloc= Revit mother family plane where the profile or window will be placed

                    ###### Profile Creation Parameters #####

                prof_files= Profile drawings names
                proftmplpth= Profile template file path

                    ###### Window Creation Parameters #####

                wtypename= Window type name 
                wtmppth= Window template file path

                        ###### Window frame creation parameters #####

                frame_files= Frame profiles drawings names
                frametmplpth= Frame file template file path


                    ###### Family parameters ######
                

                        ###### Profile placement parameters ######

                        ##  Vertical 

                            ### no mirror profiles ##

                nmirrpv= Non mirror vertical profiles names ("V02_75mm","V04_270mm")
                vnmirrk= Non mirror vertical profiles placement location keys ("C,Axis,1","B,Axis,1.01")
                vnmirrenpl= Non mirror vertical profiles placement end-planes ("3.01","2.01")

                            ### mirror profiles ###

                mirrpv= Mirror vertical profiles names ("V04_75mm","V02_75mm")
                vmirrk= Mirror vertical profiles placement location keys ("A,Axis,1","A,Axis,2.01")
                vmirrenpl= Mirror vertical profiles placement end-planes("2.01","3.01")
                
                
                        ## Horizontal

                Hp= Horizontal profiles names ("H02_147mm", "H01-2_75mm", "H01-1_75mm")
                hk= Horizontal profiles placement location keys ("A.01,Axis,2", "A,Axis,1", "A,Axis,3" )
                henpl= Horizontal profiles placement end-planes ("C.01", "C", "C")

                
                        ###### Panel placement parameters ######

            
                            ##### Glazing placement

                lckkeyp= Glazing panel placement location key "A.01,Axis,1.01"
                hegihtpnl= Glazing panel placement height end-plane "2.01"
                widthpnl= Glazing panel placement width end-plane"B.01"

                            ##### Spandrel placement

                
                lckkeysp= Spandrel panel placement location key "A.01,Ext. Axis 1,2.01"
                heightsp= Spandrel panel placement height end-plane"3.01"
                widthsp= Spandrel panel placement width end-plane"C.01"

                
                        ###### Window placement parameters #####

                lckkeyw= Window placement location key
                heightw= Window panel placement height end-plane
                widthw= Window panel placement width end-plane


                        ##### Csv data creation parameters #####


            
    """

    def __init__(self):

        ###### Shared Creation Parameters #####


        self.detpth=() #"C:\\Dropbox\\00_TOMAS\\00_PC\\01_Work\\00_Schueco\\Develping_projects_local\\Revit Templates\\Detail Item.rft" # 01 --- shared 
        
        self.fname="schueco_det_prof" # 02 --- shared
        
        self.fdname=()# "Schueco_ USC-Cust_ Det" # 03 --- shared
        
        self.contour= "a_simp-prof" # 04 --- shared  --- atomate?
        
        self.extrloc="Axis"  # 05 --- shared  ----  inside class?

        ###### Profile Creation Parameters #####

        self.path_prof_files=()#"C:\\Dropbox\\00_TOMAS\\00_PC\\01_Work\\00_Schueco\\Develping_projects_local\\Rhino_files\\Renamed_files\\{}".format(i) ### Change path!!!

        self.prof_files=[]#["V02_75mm"]#,"V04_75mm","V04_270mm","H01-2_75mm", "H01-1_75mm","H02_147mm")
        
        self.proftmplpth=""# "C:\\Dropbox\\00_TOMAS\\00_PC\\01_Work\\00_Schueco\\Develping_projects_local\\Revit Templates\\A_Profile.rft" #automate
        
        ###### Window Creation Parameters #####

        self.path_frame_files =""# "C:\\Dropbox\\00_TOMAS\\00_PC\\01_Work\\00_Schueco\\Develping_projects_local\\Rhino_files\\FrameFiles\\"
        
        self.wtypename=""#"Schueco_UDC-80-UZB_Win-in_Family01"

        self.wtemppth=""#"D:\Schueco\Programming\Develping_projects_local\Revit Templates\F_Window.rft"



            ##### Frame Creation  Parameters #####

        self.frame_files = ["Schueco_UDC-80-UZB_Frame_H01"]#,"Schueco_UDC-80-UZB_Frame_H02","Schueco_UDC-80-UZB_Frame_V01","Schueco_UDC-80-UZB_Frame_V02"]
        
        self.frametmplpth= "D:\\Schueco\\Programming\\Develping_projects_local\\Revit Templates\\D_Frame_Window.rft" #automate


    
            ###### Family Parameters #####

        self.faminstance=()

        self.doc= Revit.ActiveDBDocument
            ###### Profile placement parameters ####

                    ##  VERTICAL 

                        ### no mirror profiles ##

        self.nmirrpv=("V02_75mm","V04_270mm")
        self.vnmirrk= ("C,Axis,1","B,Axis,1.01")
        self.vnmirrenpl= ("3.01","2.01")
    """
                    ### mirror profiles ###

        self.mirrpv= Mirror vertical profiles names ("V04_75mm","V02_75mm")
        self.vmirrk= Mirror vertical profiles placement location keys ("A,Axis,1","A,Axis,2.01")
        self.vmirrenpl= Mirror vertical profiles placement end-planes("2.01","3.01")
        
        
                ## HORIZONTAL 

        self.Hp= Horizontal profiles names ("H02_147mm", "H01-2_75mm", "H01-1_75mm")
        self.hk= Horizontal profiles placement location keys ("A.01,Axis,2", "A,Axis,1", "A,Axis,3" )
        self.henpl= Horizontal profiles placement end-planes ("C.01", "C", "C")

        
                ###### Panel placement parameters ####

    
                    #### Glazing placement

        self.lckkeyp= Glazing panel placement location key "A.01,Axis,1.01"
        self.hegihtpnl= Glazing panel placement height end-plane "2.01"
        self.widthpnl= Glazing panel placement width end-plane"B.01"

                    ##### Spandrel placement

        self.lckkeysp= Spandrel panel placement location key "A.01,Ext. Axis 1,2.01"
        self.heightsp= Spandrel panel placement height end-plane"3.01"
        self.widthsp= Spandrel panel placement width end-plane"C.01"

            ##### Window Placement Parameters #####
    """
        self.lckkeyw= "A.01,Axis,1.01"
        self.heightw="2.01"
        self.widthw= "B.01"
        
    

    ##### Profile Creation Functions ####

    def profile_creation(self,path_prof_files,prof_files,detpth,fdname,fname,proftmplpth,contour,extrloc):
        for i in prof_files:
            path = (path_prof_files+"{}").format(i) 
            rs.DocumentModified(False)
            rs.Command('-Open "{}" _Enter'.format(path))
            filedname=(fdname+"{}").format(i)
            profileschueco.Schuecoprofile(detpth,filedname,fdname,i,proftmplpth,contour,extrloc)
           

    def create_profile(self):
        self.profile_creation(self.path_prof_files,self.prof_files,self.detpth,self.fdname,self.fname,self.proftmplpth,self.contour,self.extrloc)

    ##### Window Creation Functions ####

    def frame_creation(self,path_frame_files,frame_files,detpth,fdname,fname,frametmplpth,contour,extrloc,famwindow):
        for i in frame_files:
            path = (path_frame_files+"{}").format(i)
            rs.DocumentModified(False)
            rs.Command('-Open "{}" _Enter'.format(path))
            filedname=(fdname+"{}").format(i)
            frameschueco.Schuecoframe(detpth,fname,filedname,i,frametmplpth,contour,extrloc,famwindow)
        

    def frame_placement(self,frame_files,famwindow,window):

        frplaces=["Bottom","Top","Right","Left"]

        for i,j in enumerate(frame_files):
            if "H" in j:
        #print j
                window.placefrhor(famwindow,j,frplaces[i])
            else:
                window.placefrvert(famwindow,j,frplaces[i])


    def create_window(self):
        
        doc=self.doc

        window= windowschueco.Schuecowindow()

        famwindow= window.famwindow(self.wtemppth,self.wtypename)

        self.frame_creation(self.path_frame_files,self.frame_files,self.detpth,self.fdname,self.fname,self.frametmplpth,self.contour,self.extrloc,famwindow)

        self.frame_placement(self.frame_files,famwindow,window)

        window.windowpanel(famwindow)

        window.loadwindow(doc,famwindow)


        #return (window,famwindow)
        
        #### Frame Creation Functions 


    ##### Family Functions ####


    def create_family(self):
        
        familyschueco.SchuecoFamily()

    def family_profile_placement(self):

        doc=self.doc

        nmirrpv=self.mirrpv
        vnmirrk=self.vnmirrk
        vnmirrenpl=self.vnmirrenpl
        
        for i,j in enumerate(nmirrpv):

            self.faminstance.instanceplacementV(doc,j,vnmirrk[i],vnmirrenpl[i],1)

        mirrpv=self.mirrpv
        vmirrk=self.vmirrk
        vmirrenpl=self.vmirrenpl

        for i,j in enumerate(mirrpv):
            self.faminstance.instanceplacementH(doc,j,vmirrk[i],vmirrenpl[i],0)
        
        Hp=self.Hp
        hk=self.hk
        henpl=self.henpl

        for i,j in enumerate(Hp):
            self.faminstance.instanceplacementH(doc,j,hk[i],henpl[i],0)
    
    def family_panel_placement(self):

        doc=self.doc
        lckkeyp=self.lckkeyp
        hegihtpnl=self.hegihtpnl
        widthpnl=self.widthpnl

        self.faminstance.panelplacement(doc,"Glz",54,lckkeyp,hegihtpnl,widthpnl)

        lckkeysp=self.lckkeysp
        heightsp=self.heightsp
        widthsp=self.widthsp


        self.faminstance.panelplacement(doc,"Spandrel",276,lckkeysp,heightsp,widthsp)

    def family_window_placement(self):
        
        doc=self.doc
        wtypename=self.wtypename
        lckkeyw=self.lckkeyw
        heightw=self.heightw
        widthw=self.widthw
        
        self.faminstance.windowinstace(doc,wtypename,lckkeyw,heightw,widthw)