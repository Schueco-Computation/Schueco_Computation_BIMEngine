import rhinoscriptsyntax as rs
import Rhino.Geometry as rc
import scriptcontext as sc
import block_exploder



def block_org(bl):
    """
    
    input: objects ID (First level profile block e.g Sch_V_00...)
    output: articles_area,fil_names_list,objs_guids 

    """
    block_ob=rs.ExplodeBlockInstance(bl)


    items=block_exploder.block_reader(block_ob)
    list_g=((items)[1])
    list_n=((items)[0])

    nameschange = []
    for x in list_n:
        if "_" in x:
            nameschange.append(x.split("_")[0])
        else:
            nameschange.append(x)

    newnames = []
    for i,v in enumerate(nameschange):
        totalcount = nameschange.count(v)
        count = nameschange[:i].count(v)
        
        newnames.append(v + str("/") + str(count + 1) if totalcount > 1 else v)


    fil_names=[]
    for i,j in enumerate(list_g):
        for k in j:
            for l in rs.NormalObjects():
                if k == l:
                    (rs.ObjectName(k,newnames[i]))
                    fil_names.append(newnames[i])

    fil_names_list=[]               
    for i in set(fil_names):
        fil_names_list.append(i)


    objs_guids=rs.NormalObjects()
    # for i in set(fil_names):
    #     objs_guids.append(rs.ObjectByName(i))

    # # group hatches by name and calculate the hatch area 
    
    hatch=rs.ObjectsByType(65536)

    nameh=[]
    #rs.AddLayer("Hatches", None , False,True)
    
    for i in hatch:
        #rs.ObjectLayer(i,"Hatches")
        nameh.append(rs.ObjectName(i))

    uniqu_namesh=set(nameh)
    hatch_area=[]
    for i,j in enumerate(uniqu_namesh):
        hatch_area.append([])
        for k, l in enumerate(nameh):
            if l == j:
                try:
                    hatch_area[i].append(rs.Area(hatch[k]))
                except:
                        ""

    articles_area={}
    
    for i,j in enumerate(set(nameh)):
        if j != None:
            articles_area.update({j :(sum(hatch_area[i])*10**-6)})
        # else:    
        #     articles_area.update({"hatch":float(1)})

   
    rs.DeleteObjects(rs.ObjectsByType(65536))
    # objects=[]

    # for i in names:

    #     if len(rs.ObjectsByName(i))>0:
    #         objects.append(rs.ObjectsByName(i))
    #     else:
    #         names.pop(names.index(i))

    # qtty=[]

    # for i in names:
    #      qtty.append(names.count(i))

    
    #### Reduce Polylines points #####
    
    degrees=(rs.NormalObjects())
    for i in degrees:
        rs.SelectObject(i)
        rs.Command('-ChangeDegree _Deformable=Yes 1 _Enter')
        
    reduced=(rs.NormalObjects())

    for i in reduced:
        rs.SelectObject(i)
        rs.Command('-ReducePolyline  0.9 _Enter')

   
    ##### Naming reference lines and simplified profile #####

    # curvelist=["a_simp-prof","a_ref-line1","a_ref-line2","a_void"]
    # for i in curvelist:
    #     try:
    #         rs.ObjectName(rs.ObjectsByLayer(i),i)
    #     except:
    #             ""

    ##### Cleaning file ####
    
    rest=rs.NormalObjects()

#    for i in rest:
#        if rs.ObjectName(i) == None:
#            #print (rs.ObjectName(i))
#            rs.DeleteObjects(i)
#        elif rs.CurveLength(i) < float(0.8):
#            rs.DeleteObjects(i)
    
    ##### Article numbers Dictionaries #####

    rs.UnselectObjects(rs.NormalObjects())
   
    return articles_area,fil_names_list,objs_guids



if __name__ == '__main__':
    pass

