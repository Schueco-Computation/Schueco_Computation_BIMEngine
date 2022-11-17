
import schuecobim as s


##########  Nyr Landspitali #########


unit=s.schuecosystem.Unit() # Creates Unit instance

unit.detpth= "K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Revit templates\\Detail Item.rft" # 01 --- shared 

unit.fdname = "Schueco_Cust_Det" # 03 --- shared

###### Profile Creation Parameters #####

unit.sel_blocks=["Schueco_Cust_Prof_H01_70mm","Schueco_Cust_Prof_H02_116mm","Schueco_Cust_Prof_H03_70mm","Schueco_Cust_Prof_H01.1_70mm","Schueco_Cust_Prof_H02.1_116mm","Schueco_Cust_Prof_H02.2_116mm","Schueco_Cust_Prof_V01_75mm","Schueco_Cust_Prof_V02_116mm","Schueco_Cust_Prof_V01.1_75mm","Schueco_Cust_Prof_V01.2_75mm","Schueco_Cust_Frame_H1_87mm"]

unit.proftmplpth= "K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Revit templates\\A_Profile.rft" #automate


##### Window Creation Profiles #####


unit.wtypename="Schueco_Cust_Window_Family01"

#unit.wtemppth="K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Revit templates\\Family TEMPLATE.rft"

unit.windowtype="Window"

##### Frame Creation  Parameters #####

unit.frametmplpth= "K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Revit templates\\D_Frame_Window.rft" #automate

unit.faminstance=unit.create_family() #Create Family instance

unit.create_profile() #Creates profiles

unit.create_window("Window") #Creates window


unit.csv_path="K:\\Engineering\\Abteilungen\\ES\\Computation\\BIM_strategie\\BIM Workflow\\Projects\\Nyr Landspitali\\Csv\\"


unit.family_profile_placement() # places profiles in family instance


unit.family_window_placement() # Places window in family instance


unit.family_panel_placement() # Places panel in family instance

#