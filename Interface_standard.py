# coding=utf-8
import os
import schuecobim as s

unit=s.schuecosystem_standard.Unit() # Creates Unit instance

#unit.detpth= "D:\\Detail Item.rft" # 01 --- shared 

unit.fdname = "Schueco_Cust_Det" # 03 --- shared

###### Profile Creation Parameters #####

#unit.proftmplpth= "K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Revit templates\\A_profile.rft" #automate

#unit.path_prof_files = "K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Projects\\Standard project\\3dm\\"

#unit.prof_files=os.listdir(unit.path_prof_files)



##### Window Creation Profiles ##### 

unit.path_frame_files = "C:\\Users\\ramijc\\Schueco\\BIM Workflow\\Projects\\Schüco UZB, Bielefeld\\Costs\\Rhino frames\\"

unit.ventname = "Schueco_Cust_170mm"

unit.wtypename="Schueco_Cust_Window_Family01"

unit.wtemppth="K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Revit templates\\F_Window.rft"

##### Frame Creation  Parameters #####

unit.frame_files = ["Schueco_Cust_Frame_H01_20mm.3dm", "Schueco_UDC-80-UZB_Frame_H02.3dm"]

#unit.frametmplpth= "K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Revit templates\\D_Frame_Window.rft" #automate



unit.csv_path="C:\\Users\\ramijc\\Schueco\\BIM Workflow\\Projects\\Business Centre Al Farabi\\Csv\\"

unit.faminstance=unit.create_family() #Create Family instance

#unit.create_profile() #Creates profiles"""




unit.create_window("Win") #Creates window


#unit.family_profile_placement() # places profiles in family instance


unit.family_window_placement() # Places window in family instance


#unit.family_panel_placement() # Places panel in family instance
