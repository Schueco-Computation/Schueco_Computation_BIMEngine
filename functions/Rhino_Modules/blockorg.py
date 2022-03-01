import rhinoscriptsyntax as rs
import Rhino.Geometry as rc
import scriptcontext as sc

def block_org():

    names=[]

    guid =rs.ObjectsByType(4096)

    oldnames = []

    for x in guid:
        oldnames.append(rs.BlockInstanceName(x))

    nameschange = []
    for x in oldnames:
        if "_" in x:
            nameschange.append(x.split("_")[0])
        else:
            nameschange.append(x)

    newnames = []
    for i, v in enumerate(nameschange):
        totalcount = nameschange.count(v)
        count = nameschange[:i].count(v)
        newnames.append(v + str("/") + str(count + 1) if totalcount > 1 else v)

    rename=[]
    for i,j in enumerate(guid):
        rename.append(rs.ObjectName(j,newnames[i]))

    ###### First explode #####
    """
    a=rs.ObjectsByType(4096)

    for i in a:
        rs.ExplodeBlockInstance(i)
    """
    ###### Nested explode #####

    def explode_em(blocks, name):
        for Id in blocks:
            if rs.IsBlockInstance(Id):
                names.append(rs.BlockInstanceName(Id))
                rs.ObjectName(rs.BlockObjects(rs.BlockInstanceName(Id)),name)
                blocks=rs.ExplodeBlockInstance(Id)

                if blocks:
                    explode_em(blocks, name)

    for x in newnames:
        y = rs.ObjectsByName(x)
        for z in y:
            explode_em([z], x)


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

    curvelist=["a_simp-prof","a_ref-line1","a_ref-line2","a_void"]
    for i in curvelist:
        try:
            rs.ObjectName(rs.ObjectsByLayer(i),i)
        except:
                ""

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
