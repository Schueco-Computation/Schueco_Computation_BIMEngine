import os
import schuecobim as s

unit=s.schuecosystem.Unit() # Creates Unit instance

#unit.detpth= "D:\\Detail Item.rft" # 01 --- shared 

unit.fdname = "Schueco_Cust_Det" # 03 --- shared

###### Profile Creation Parameters #####

unit.proftmplpth= "K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Revit templates\\A_profile.rft" #automate

unit.path_prof_files = "C:\\Users\\ramijc\\Desktop\\Try\\"

unit.prof_files=os.listdir(unit.path_prof_files)



##### Window Creation Profiles ##### 

#unit.path_frame_files = "C:\\Dropbox\\00_TOMAS\\00_PC\\01_Work\\00_Schueco\\Develping_projects_local\\Rhino_files\\FrameFiles\\"

#unit.ventname = "Schueco_VentPanel-Window_170mm"

#unit.wtypename="Schueco_UDC-80-UZB_Win-in_Family01"

#unit.wtemppth="D:\Schueco\Programming\Develping_projects_local\Revit Templates\F_Window.rft"

##### Frame Creation  Parameters #####

#unit.frame_files = ["Schueco_Cust_Frame_H01_20mm","Schueco_Cust_Frame_H02_20mm"]

#unit.frametmplpth= "D:\\Schueco\\Programming\\Develping_projects_local\\Revit Templates\\D_Frame_Window.rft" #automate



unit.csv_path="C:\\Users\\ramijc\\Schueco\\BIM Workflow\\Projects\\Business Centre Al Farabi\\Csv\\"

unit.faminstance=unit.create_family() #Create Family instance

unit.create_profile() #Creates profiles"""




#unit.create_window("Vent") #Creates window


#unit.family_profile_placement() # places profiles in family instance


#unit.family_window_placement() # Places window in family instance


#unit.family_panel_placement() # Places panel in family instance
