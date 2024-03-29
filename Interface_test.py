
import schuecobim as s

unit=s.schuecosystem.Unit() # Creates Unit instance

unit.detpth= "K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Revit templates\\Detail Item.rft" # 01 --- shared 

unit.fdname = "Schueco_USC-Cust_Det" # 03 --- shared

###### Profile Creation Parameters #####

# unit.prof_files=["V02_75mm","V04_75mm","V04_270mm","H01-2_75mm", "H01-1_75mm","H02_147mm"]

unit.proftmplpth= "K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Revit templates\\A_Profile.rft" #automate

# unit.path_prof_files = "C:\\Dropbox\\00_TOMAS\\00_PC\\01_Work\\00_Schueco\\Develping_projects_local\\Rhino_files\\Renamed_files\\"

##### Window Creation Profiles #####

#unit.path_frame_files = "C:\\Dropbox\\00_TOMAS\\00_PC\\01_Work\\00_Schueco\\Develping_projects_local\\Rhino_files\\FrameFiles\\"

unit.wtypename="Schueco_AWS75_SI_Window_Family01"

#unit.wtemppth="K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Revit templates\\Family TEMPLATE.rft"

unit.windowtype="Window"

##### Frame Creation  Parameters #####

#unit.frame_files = ["Schueco_UDC-80-UZB_Frame_H01","Schueco_UDC-80-UZB_Frame_H02","Schueco_UDC-80-UZB_Frame_V01","Schueco_UDC-80-UZB_Frame_V02"]

unit.frametmplpth= "K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Revit templates\\D_Frame_Window.rft" #automate

unit.faminstance=unit.create_family() #Create Family instance

#unit.create_profile() #Creates profiles

unit.create_window("Window") #Creates window


# unit.family_profile_placement() # places profiles in family instance


# unit.family_window_placement() # Places window in family instance


# unit.family_panel_placement() # Places panel in family instance

#