import sys
sys.path.append("C:\\Users\\tomas\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMengine\\objects")
import rhinoscriptsyntax as rs
import profileschueco
import frameschueco
import windowschueco
import familyschueco
#import schuecobim as s
from RhinoInside.Revit import Revit, Convert

class unit():
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
        
        self.fname=()#"schueco_det_prof" # 02 --- shared
        
        self.fdname=()# "Schueco_ USC-Cust_ Det" # 03 --- shared
        
        self.contour= "a_simp-prof" # 04 --- shared  --- atomate?
        
        self.extrloc="Axis"  # 05 --- shared  ----  inside class?

        ###### Profile Creation Parameters #####

        self.path_prof_files=()#"C:\\Dropbox\\00_TOMAS\\00_PC\\01_Work\\00_Schueco\\Develping_projects_local\\Rhino_files\\Renamed_files\\{}".format(i) ### Change path!!!

        self.prof_files=[]#["V02_75mm"]#,"V04_75mm","V04_270mm","H01-2_75mm", "H01-1_75mm","H02_147mm")
        
        self.proftmplpth=""# "C:\\Dropbox\\00_TOMAS\\00_PC\\01_Work\\00_Schueco\\Develping_projects_local\\Revit Templates\\A_Profile.rft" #automate
        
        #self.profile_creation(self.path_prof_files,self.prof_files,self.detpth,self.fdname,self.fname,self.proftmplpth,self.contour,self.extrloc)


        #self.doc=()# Revit.ActiveDBDocument ### should be given




        ###### Window Creation Parameters #####

    """
            self.wtypename=""#"Schueco_UDC-80-UZB_Win-in_Family01"

            self.wtemppth=""#"D:\Schueco\Programming\Develping_projects_local\Revit Templates\F_Window.rft"



                ##### Frame Creation  Parameters #####

            
            self.frame_files = ["Schueco_UDC-80-UZB_Frame_H01"]#,"Schueco_UDC-80-UZB_Frame_H02","Schueco_UDC-80-UZB_Frame_V01","Schueco_UDC-80-UZB_Frame_V02"]
            
            self.frametmplpth= "D:\\Schueco\\Programming\\Develping_projects_local\\Revit Templates\\D_Frame_Window.rft" #automate


            ###### Family Parameters #####
            
            ###### Profile placement parameters ####

                    ##  VERTICAL 

                        ### no mirror profiles ##

            self.nmirrpv= Non mirror vertical profiles names ("V02_75mm","V04_270mm")
            self.vnmirrk= Non mirror vertical profiles placement location keys ("C,Axis,1","B,Axis,1.01")
            self.vnmirrenpl= Non mirror vertical profiles placement end-planes ("3.01","2.01")

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

            self.lckkeyw= Window placement location key
            self.heightw= Window panel placement height end-plane
            self.widthw= Window panel placement width end-plane
        
        ##### Profile Creation Functions ####

    """

    

    def profile_creation(self,path_prof_files,prof_files,detpth,fdname,fname,proftmplpth,contour,extrloc):
        for i in prof_files:
            path = (path_prof_files+"{}").format(i) 
            rs.DocumentModified(False)
            rs.Command("! _-New None")
            rs.Command('-Open "{}" _Enter'.format(path))
            filedname=(fdname+"{}").format(i)
            profileschueco.Schuecoprofile(detpth,filedname,fdname,i,proftmplpth,contour,extrloc)
            rs.Command("! _-New None")
            
            ##### Window Creation Functions ####

            # window=s.windowschueco.Schuecowindow()
            # famwindow=window.famwindow(wtemppth,wtypename)


    def create_profile(self):
        return self.profile_creation(self.path_prof_files,self.prof_files,self.detpth,self.fdname,self.fname,self.proftmplpth,self.contour,self.extrloc)
            #### Frame Creation Functions 
    """
    def frame_creation(self,path,dname,detpth,fname,frametmplpth,extrloc,famwindow):
        for i in files:
            #path = "C:\\Dropbox\\00_TOMAS\\00_PC\\01_Work\\00_Schueco\\Develping_projects_local\\Rhino_files\\Renamed_files\\{}".format(i) ### Change path!!!
            #print (path)
            rs.DocumentModified(False)
            rs.Command("! _-New None")
            rs.Command('-Open "{}" _Enter'.format(path))
            fdname=(dname+"{}").format(i)
            frameschueco.Schuecoframe(detpth,fname,fdname,i,frametmplpth,contour,extrloc,famwindow)
            rs.Command("! _-New None")


    ##### Family Functions ####

    # Vplace=s.familyschueco.SchuecoFamily()
    # Hplace=s.familyschueco.SchuecoFamily()
    # panelgl=s.familyschueco.SchuecoFamily()
    # panelsp=s.familyschueco.SchuecoFamily()

   """