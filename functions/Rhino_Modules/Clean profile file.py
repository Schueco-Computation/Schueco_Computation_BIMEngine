import rhinoscriptsyntax as rs



lines=rs.AllObjects(False)

#for i in lines:
#    if rs.ObjectName(i) == None:
#        rs.DeleteObject(i)

for i in lines:
    print rs.ObjectName(i)
    
