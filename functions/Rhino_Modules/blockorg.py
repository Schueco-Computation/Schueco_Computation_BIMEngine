import rhinoscriptsyntax as rs
import Rhino.Geometry as rc
import scriptcontext as sc

def block_org():

    names=[]

    ###### First explode #####

    a=rs.ObjectsByType(4096)

    for i in a:
        rs.ExplodeBlockInstance(i)

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

    ##### Article numbers Dictionaries #####

    articles={}
    keys=range(len(names))
    for i in keys:
        if "guiding" not in names[i]:
            articles[names[i]]=(qtty[i])
        
    ##### Article Number String ####
    articles_str= ''
    
    for i,j in articles.items():
        articles_str= articles_str + str (i) + ':' + str (j)+ ' '

    return (articles,articles_str)


if __name__ == '__main__':
    block_org()
