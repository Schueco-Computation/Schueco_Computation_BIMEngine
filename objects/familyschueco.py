# Enable Python support and load DesignScript library
import sys
sys.path.append("C:\\Users\\tomas\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMengine\\functions\\Rhino_Modules")
sys.path.append("C:\\Users\\tomas\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMengine\\functions\\Rhino_Revit_Modules")
import Family

class SchuecoFamily():

    """" Schueco Family """

    def __init__(self,Document, TypeName, LocationKeyV, EndRefPlaneV,LocationKeyH,EndRefPlaneH, MirrorBoolean):
        self.instanceplacementV=family.NewVerticalProfileInstace(Document,TypeName,LocationKeyV,EndRefPlaneV,MirrorBoolean)
        self.instanceplacementH=family.NewHorizontalProfileInstace(Document,TypeName,LocationKeyH,EndRefPlaneH,MirrorBoolean)
    
if __name__ == '__main__':
    pass
