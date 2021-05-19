import rhinoscriptsyntax as rs
import Rhino.Geometry as rc
import scriptcontext as sc

def block_org():

    names=[]

    ###### First explode #####
    """
    a=rs.ObjectsByType(4096)

    for i in a:
        rs.ExplodeBlockInstance(i)
    """
    ###### Nested explode #####

    y=rs.ObjectsByType(4096)

    def explode_em(blocks):
        for Id in blocks:
            if rs.IsBlockInstance(Id):
                names.append(rs.BlockInstanceName(Id))
                rs.ObjectName(rs.BlockObjects(rs.BlockInstanceName(Id)),(rs.BlockInstanceName(Id)))
                blocks=rs.ExplodeBlockInstance(Id)

                if blocks:
                    explode_em(blocks)

    for z in y:

        explode_em([z])


    rs.DeleteObjects(rs.ObjectsByType(65536))
    objects=[]

    for i in names:

        if len(rs.ObjectsByName(i))>0:
            objects.append(rs.ObjectsByName(i))
        else:
            names.pop(names.index(i))

    qtty=[]

    for i in names:
         qtty.append(names.count(i))


    #### Reduce Polylines points #####
    
    degrees=(rs.AllObjects())
    for i in degrees:
        rs.SelectObject(i)
        rs.Command('-ChangeDegree _Deformable=Yes 1 _Enter')
        
    reduced=(rs.AllObjects())

    for i in reduced:
        rs.SelectObject(i)
        rs.Command('-ReducePolyline  0.8 _Enter')

   
    ##### Naming reference lines and simplified profile #####

    curvelist=["a_simp-prof","a_ref-line1","a_ref-line2"]
    for i in curvelist:
        rs.ObjectName(rs.ObjectsByLayer(i),i)


    ##### Cleaning file ####

    rest=rs.AllObjects()

    for i in rest:
        if rs.ObjectName(i) == None:
            #print (rs.ObjectName(i))
            rs.DeleteObjects(i)
        elif rs.CurveLength(i) < float(0.8):
            rs.DeleteObjects(i)

    ##### Article numbers Dictionaries #####



    articles={}
    keys=range(len(names))
    for i in keys:
        if "guiding" not in names[i]:
            articles[names[i]]=(qtty[i])
        
    
    rs.UnselectObjects(rs.AllObjects())

    ##### Article Number String ####
    articles_str= ''
    
    for i,j in articles.items():
        articles_str= articles_str + str (i) + ':' + str (j)+ ' '

    return (articles,articles_str)


if __name__ == '__main__':
    block_org()
