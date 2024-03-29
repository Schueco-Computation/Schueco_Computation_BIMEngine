import os
import schuecobim as s

unit=s.schuecosystem.Unit() # Creates Unit instance

###### Profile Creation Parameters #####

unit.path_prof_files = "K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Projects\\Business Centre Al Farabi\\3dm\\"

unit.prof_files=os.listdir(unit.path_prof_files)

##### Window Creation Profiles ##### 

windowtype = "Vent"

unit.path_frame_files = "K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Projects\\Business Centre Al Farabi\\3dm\\Frames\\"

unit.ventname = "Schueco_VentPanel-Window_170mm"

unit.wtypename="Schueco_UDC-80-UZB_Win-in_Family01"

unit.windowtype = windowtype

unit.path_vent_files = "K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Projects\\Business Centre Al Farabi\\3dm\\Vent panel\\"

##### Frame Creation  Parameters #####

unit.frame_files = ["Schueco_Cust_Frame_H01_20mm","Schueco_Cust_Frame_H02_20mm"]

unit.csv_path="C:\\Users\\ramijc\\Schueco\\BIM Workflow\\Projects\\Business Centre Al Farabi\\Csv\\"


unit.faminstance=unit.create_family() #Create Family instance

unit.create_profile() #Creates profiles"""


unit.create_window(windowtype) #Creates window


unit.family_profile_placement() # places profiles in family instance


unit.family_window_placement() # Places window in family instance


unit.family_panel_placement() # Places panel in family instance
