# Enable Python support and load DesignScript library
import sys
sys.path.append("C:\\Users\\tomas\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMengine\\functions\\Rhino_Modules")
sys.path.append("C:\\Users\\tomas\\AppData\\Roaming\\McNeel\\Rhinoceros\\7.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib\\Schueco_Computation_BIMengine\\functions\\Rhino_Revit_Modules")
import Family



class SchuecoFamily():

    """ Schueco Family """

    def __init__(self):
      
        pass

    def instanceplacementV(self,Document,TypeName,LocationKeyV,EndRefPlaneV,MirrorBoolean):
        return Family.NewVerticalProfileInstace(Document,TypeName,LocationKeyV,EndRefPlaneV,MirrorBoolean)
    
    def instanceplacementH(self,Document,TypeName,LocationKeyH,EndRefPlaneH,MirrorBoolean):
        return Family.NewHorizontalProfileInstace(Document,TypeName,LocationKeyH,EndRefPlaneH,MirrorBoolean)
    
    def panelplacement(self,Document,Typepanel, Thickness, LocationKey, EndHeigthRefPlane, EndWidthRefPlane):
        return Family.NewPanel(Document,Typepanel, Thickness, LocationKey, EndHeigthRefPlane, EndWidthRefPlane)

    def windowinstace(self,Document,wtypename,LocationKey,Higrefplane,EndWidthRefPlane):
        return Family.NewWindowInstance(Document,wtypename,LocationKey,Higrefplane,EndWidthRefPlane)


if __name__ == '__main__':
    pass
