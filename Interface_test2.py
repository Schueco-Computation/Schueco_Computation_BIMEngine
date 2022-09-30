import os
import schuecobim as s

unit=s.schuecosystem.Unit() # Creates Unit instance

###### Profile Creation Parameters #####

unit.path_prof_files = "K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Projects\\Great Charles Square_Brimingham\\3dm\\"

unit.prof_files=os.listdir(unit.path_prof_files)

unit.create_profile() #Creates profiles

unit.csv_path="C:\\Users\\ramijc\\Schueco\\BIM Workflow\\Projects\\Great Charles Square_Brimingham\\Csv\\"

unit.faminstance=unit.create_family() #Create Family instance

##### Window Creation Profiles ##### 

unit.path_frame_files = "K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Projects\\Great Charles Square_Brimingham\\3dm\\FrameFiles\\"

##### Frame Creation  Parameters #####

unit.frame_files=os.listdir(unit.path_frame_files)


#unit.ventname = "Schueco_VentPanel-Window_170mm"

unit.wtypename="Schueco_Cust_Win-in_Family01"



unit.create_window("Win") #Creates window


unit.family_profile_placement() # places profiles in family instance


unit.family_window_placement() # Places window in family instance


unit.family_panel_placement() # Places panel in family instance
