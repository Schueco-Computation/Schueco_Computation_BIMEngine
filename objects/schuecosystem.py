import sys
sys.path.append("C:\\Users\\ramijc\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMEngine\\objects")
sys.path.append("C:\\Users\\ramijc\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMEngine\\functions\\Rhino_Modules")
sys.path.append("C:\\Users\\ramijc\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMEngine\\functions\\Rhino_Revit_Modules")
import rhinoscriptsyntax as rs
import profileschueco
import frameschueco
import ventschueco
import windowschueco
import familyschueco
import block_finder
import blockorg_00
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


        self.detpth="K:\\Engineering\\Abteilungen\ES\\Computation\\BIM_strategie\\BIM Workflow\\Revit templates\\Detail Item.rft" # 01 --- shared 
        
        self.fname="Schueco_Det_Prof" # 02 --- shared
        
        self.fdname="Schueco_Cust_Det"# "Schueco_ USC-Cust_ Det" # 03 --- shared
        
        self.contour= "a_simp-prof" # 04 --- shared  --- atomate?
        
        self.extrloc="Axis"  # 05 --- shared  ----  inside class?

        ###### Profile Creation Parameters #####

        self.path_prof_files=()#"C:\\Dropbox\\00_TOMAS\\00_PC\\01_Work\\00_Schueco\\Develping_projects_local\\Rhino_files\\Renamed_files\\{}".format(i) ### Change path!!!

        self.prof_files=[]#["V02_75mm"]#,"V04_75mm","V04_270mm","H01-2_75mm", "H01-1_75mm","H02_147mm")
        
        self.proftmplpth="K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Revit templates\\A_profile.rft"# "C:\\Dropbox\\00_TOMAS\\00_PC\\01_Work\\00_Schueco\\Develping_projects_local\\Revit Templates\\A_Profile.rft" #automate


        ###### Window Creation Parameters #####

        self.path_frame_files =""#"K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Projects\\Business Centre Al Farabi\\3dm\\Frames\\"# "C:\\Dropbox\\00_TOMAS\\00_PC\\01_Work\\00_Schueco\\Develping_projects_local\\Rhino_files\\FrameFiles\\"
        
        self.wtypename="Schueco_AWS75.SI_Window_Family01"

        self.wtemppth="K:\\Engineering\\Abteilungen\ES\\Computation\\BIM_strategie\\BIM Workflow\\Revit templates\\F_Window_.rft"


        self.windowtype = ""


            ##### Frame Creation  Parameters #####

        self.frame_files = ""#["Schueco_UDC-80-UZB_Frame_H01"],"Schueco_UDC-80-UZB_Frame_H02","Schueco_UDC-80-UZB_Frame_V01","Schueco_UDC-80-UZB_Frame_V02"]
        
        self.frametmplpth= "K:\\Engineering\\Abteilungen\ES\\Computation\\BIM_strategie\\BIM Workflow\\Revit templates\\D_Frame_Window - 23.rft" #automate

            ##### Vent Creation Parameters

        self.path_vent_files = "" #"K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Projects\\Business Centre Al Farabi\\3dm\\Vent panel\\"
        self.ventname = "" #Name del Vent
        self.venttempath = "K:\\Engineering\\Abteilungen\ES\\Computation\\BIM_strategie\\BIM Workflow\\Revit templates\\C_VentPanels.rft"
        self.contournmvoid = "a_void"

            ###### Family Parameters #####

        self.faminstance=()

        self.doc= Revit.ActiveDBDocument
            ###### Profile placement parameters ####

                    ##  VERTICAL 

                        ### no mirror profiles ##
        
        self.nmirrpv=["Schueco_Cust_Prof_H01_32mm","Schueco_Cust_Prof_H02_65mm"]
        self.vnmirrk= ["A,Axis,1","B,Axis,1.01"]
        self.vnmirrenpl= ["4","4.01"]
        
                    ### mirror profiles ###

        self.mirrpv= ["Schueco_Cust_Prof_H01_32mm"]
        self.vmirrk= ["C,Axis,1"]
        self.vmirrenpl= ["4"] 
        
        
                ## HORIZONTAL 
        
        self.Hp= ["Schueco_Cust_Prof_H02_65mm", "Schueco_Cust_Prof_H02_65mm", "Schueco_Cust_Prof_V01_52mm", "Schueco_Cust_Prof_V02_37mm"]
        self.hk= ["A.01,Axis,2", "A.01,Axis,3", "A.01,Axis,1", "A.01,Axis,4"]
        self.henpl= ["B.01", "B.01", "C.01", "C.01"]


        self.csv_path=()

                ###### Panel placement parameters ####

    
                    #### Glazing placement
        
        self.lckkeyg= ["A.01,Axis,1.01"]
        self.hegihtg=["2.01"]#["3.01"]
        self.widthg=["B.01"]
        self.thckg= [41]
        self.matnamegl=["SCH_Glass"]

                    #### Panel placement
        
        self.lckkeypnl= ["B.02,Ext. Axis 1,1.01", "B.02,Int. Axis 4,1.01", "B.02,Ext. Axis 2,1.01"]
        self.hegihtpnl=["4.01","4.01", "4.01"]
        self.widthpnl=["C.01","C.01", "C.01" ]
        self.thckpnl= [3,2,200]
        self.matnamepnl=["Aluminium (European)", "coil", "Default"]


                ##### Spandrel placement
        
        self.lckkeysp=["A.01,Ext. Axis 1,3.02"]
        self.heightsp= ["4.01"]
        self.widthsp= ["B.01"]
        self.thckspnd=[2]
        self.matnamesp=["Aluminium (European)"]

                ##### Internal panel placement
        
        self.lckkeyip=["A.01,Int. Axis 1,3.02","B.02,Int. Axis 3,1.01","A.01,Int. Axis 2,3.02"]
        self.heightip= ["4.01","4.01","4.01"]
        self.widthip= ["B.01","C.01","B.01"]
        self.thckip=[149,170,2]
        self.matnameip=["Mineral Wool", "Mineral Wool", "coil"]
            
            
            ##### Window Placement Parameters #####
        
        self.lckkeyw= "A.01,Axis,2.02"
        self.heightw="3.01"
        self.widthw= "B.01"
        
    

    ##### Profile Creation Functions ####

    def profile_creation(self,path_prof_files,prof_files,detpth,fdname,fname,proftmplpth,contour,extrloc):
        for i in prof_files:
            if ".3dm" in i:
                path = (path_prof_files+"{}").format(i)
                dname=i.split(".")[0]
                rs.DocumentModified(False)
                rs.Command('-Open "{}" _Enter'.format(path))
                rs.Command('-SaveAs "{}" _Enter'.format(path_prof_files+"3dm\\"+dname))
                filedname=(fdname+"{}").format(dname)
                profileschueco.Schuecoprofile(detpth,fname,fdname,dname,proftmplpth,contour,extrloc)# i was replaced
           

    def create_profile(self):
        return self.profile_creation(self.path_prof_files,self.prof_files,self.detpth,self.fdname,self.fname,self.proftmplpth,self.contour,self.extrloc)

    ##### Window Creation Functions ####

    def frame_creation(self,detpth,fdname,fname,inst_unpk,i,frametmplpth,contour,extrloc,famwindow):
        """
        
        inputs =>

        1.- detpath : Detail template path (Shared)
        2.- fdname : Detail Mother family Name (Shared)
        3.- famdetname : Each article number as detail item (Shared)
        4.- typeID : boundled block ID ()
        5.- typename : boundled block Name ()
        6.- famframetempath : Frame family template file 
        7.- contournm : closed polyline name representing a simplified frame section 
        8.- extlocation : reference plane location name
        9.- famwindow: Window family created in the bacground
        
        
        """
        frameschueco.Schuecoframe(detpth,fdname,fname,inst_unpk,i,frametmplpth,contour,extrloc,famwindow)
        """
        inst_list=block_finder.block_finder()[0]

        for b in inst_list:
            i= (rs.BlockInstanceName(b))
            rs.SelectObject(b)
            rs.ZoomSelected()
            rs.Command("_Isolate")
            inst_unpk=blockorg_00.block_org(b)
            frame=frameschueco.Schuecoframe(detpth,fdname,fname,inst_unpk,i,frametmplpth,contour,extrloc,famwindow)
            rs.Command("_Show")
            guids=inst_unpk[2]
            rs.LockObjects(guids)
        """ 
            
        
        # for i in frame_files:
        #     path = (path_frame_files+"{}").format(i)
        #     rs.DocumentModified(False)
        #     rs.Command('-Open "{}" _Enter'.format(path))
        #     filedname=(fdname+"{}").format(i)
        #    frameschueco.Schuecoframe(detpth,fname,filedname,i,frametmplpth,contour,extrloc,famwindow)
        


    def frame_placement(self,famwindow,window,frame_name):
        frame_files=frame_name
        window.placefrhor(famwindow,frame_files[1],"Bottom")
        window.placefrvert(famwindow,frame_files[1],"Right")
        window.placefrhor(famwindow,frame_files[0],"Top")
        window.placefrvert(famwindow,frame_files[0],"Left")

        """frplaces=["Bottom","Top","Right","Left"]

        for i,j in enumerate(frame_files):
            if "H" in j:
        #print j
                window.placefrhor(famwindow,j,frplaces[i])
            else:
                window.placefrvert(famwindow,j,frplaces[i])"""


    def ventpanel_creation(self,path_vent_files,ventname,detpth,fdname,fname,venttempath,contour,extrloc,famwindow,contournmvoid):
        path = (path_vent_files+"{}").format(ventname)
        rs.DocumentModified(False)
        rs.Command("! _-New None")
        rs.Command('-Open "{}" _Enter'.format(path))
        ventschueco.Schuecovent(detpth,fname,fdname,ventname,venttempath,contour,extrloc,famwindow,contournmvoid)

    def create_window(self, windowtype):
        
        doc=self.doc

        window= windowschueco.Schuecowindow()

        famwindow= window.famwindow(self.wtemppth,self.wtypename)
        frame_names= []
        
        inst_list_id=block_finder.block_finder()[0]
        inst_list=block_finder.block_finder()[1]
        
        for a,b in enumerate(inst_list):
            # i= (rs.BlockInstanceName(b))
            i= (str(b) + "_" + str(a))
            frame_names.append(i)
            rs.SelectObject(rs.BlockInstances(b))
            rs.ZoomSelected()
            rs.Command("_Isolate")
            inst_unpk=blockorg_00.block_org(rs.BlockInstances(b))
            self.frame_creation(self.detpth,self.fdname,self.fname,inst_unpk,i,self.frametmplpth,self.contour,self.extrloc,famwindow)
            guids=inst_unpk[2]
            #window.windowdim(famwindow, self.windowtype)
            rs.Command("_Show")
            rs.Command("_Zoom_Extent")
            rs.DeleteObjects(guids)

        
        #self.frame_creation(self.detpth,self.fdname,self.fname,self.frametmplpth,self.contour,self.extrloc,famwindow)

        if windowtype == "Vent":
            self.ventpanel_creation(self.path_vent_files,self.ventname,self.detpth,self.fdname,self.fname,self.venttempath,self.contour,self.extrloc,famwindow,self.contournmvoid)
            window.windowpanel(famwindow,self.ventname, 41.04)
        else:
            window.windowpanel(famwindow,"Glz", 41.04, "SCH_Glass")

        #window.windowdim(famwindow, windowtype) #Crea una familia de ventana? Se puede incluir en el forloop?

        #self.frame_placement(famwindow,window,frame_names)

        window.loadwindow(doc,famwindow)


        #return (window,famwindow)
        
        #### Frame Creation Functions 


    ##### Family Functions ####


    def create_family(self):

        return familyschueco.SchuecoFamily()

    def family_profile_placement(self):

        doc=self.doc

        nmirrpv=self.nmirrpv
        vnmirrk=self.vnmirrk
        vnmirrenpl=self.vnmirrenpl
        
        for i,j in enumerate(nmirrpv):

            self.faminstance.instanceplacementV(doc,j,vnmirrk[i],vnmirrenpl[i],0)

        mirrpv=self.mirrpv
        vmirrk=self.vmirrk
        vmirrenpl=self.vmirrenpl

        for i,j in enumerate(mirrpv):

            self.faminstance.instanceplacementV(doc,j,vmirrk[i],vmirrenpl[i],1)
        
        Hp=self.Hp
        hk=self.hk
        henpl=self.henpl

        for i,j in enumerate(Hp):
            self.faminstance.instanceplacementH(doc,j,hk[i],henpl[i],0)

        TypeName=nmirrpv+mirrpv+Hp
        LocationKey=vnmirrk+vmirrk+hk
        EndRefPlane=vnmirrenpl+vmirrenpl+henpl
        filepath=self.csv_path
        self.faminstance.csv(TypeName,LocationKey,EndRefPlane,filepath)

    def family_panel_placement(self):

        doc=self.doc
        
        lckkeysp=self.lckkeysp
        heightsp=self.heightsp
        widthsp=self.widthsp
        thckspn=self.thckspnd
        matnamesp=self.matnamesp

        for i,j in enumerate(lckkeysp):
            self.faminstance.panelplacement(doc,"Spandrel",thckspn[i],j,heightsp[i],widthsp[i],matnamesp[i])

        
        lckkeyg=self.lckkeyg
        hegihtg=self.hegihtg
        widthg=self.widthg
        thckg=self.thckg
        matnamegl=self.matnamegl

        for i,j in enumerate(lckkeyg):
            self.faminstance.panelplacement(doc,"Glz",thckg[i],j,hegihtg[i],widthg[i],matnamegl[i])

        lckkeypnl=self.lckkeypnl
        hegihtpnl=self.hegihtpnl
        widthpnl=self.widthpnl
        thckpnl=self.thckpnl
        matnamepnl=self.matnamepnl

        for i,j in enumerate(lckkeypnl):
            self.faminstance.panelplacement(doc,"Panel",thckpnl[i],j,hegihtpnl[i],widthpnl[i],matnamepnl[i])
    
        lckkeyip=self.lckkeyip
        heightip=self.heightip
        widthip=self.widthip
        thckip=self.thckip
        matnameip=self.matnameip

        for i,j in enumerate(lckkeyip):
            self.faminstance.panelplacement(doc,"IntPanel",thckip[i],j,heightip[i],widthip[i],matnameip[i])



    def family_window_placement(self):
        
        doc=self.doc
        wtypename=self.wtypename
        lckkeyw=self.lckkeyw
        heightw=self.heightw
        widthw=self.widthw
        
        self.faminstance.windowinstace(doc,wtypename,lckkeyw,heightw,widthw)