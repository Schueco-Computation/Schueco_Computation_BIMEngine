
import rhinoscriptsyntax as rs
import Rhino.Geometry as rc
import Rhino
import scriptcontext as sc


#block_ob=rs.ExplodeBlockInstance(rs.BlockInstances("Sch_V_F_00"))


Block_Names=[]
Block_Obj=[]
def block_reader(b_obj):  
    """
        input: list of objects inside of first block level
        output: objects from all exploded nested blocks
    """
    for i, j in enumerate(b_obj):
        if rs.ObjectType(j) == 4096: 
            Ins_n=rs.BlockInstanceName(j) 
            Block_Names.append(Ins_n)
            obj=rs.ExplodeBlockInstance(j)
            Block_Obj.append(obj)
            for k,l in enumerate(obj):
                if  rs.ObjectType(l) == 4096:
                    block_reader([l])
                else:
                    rs.ObjectName(l,Ins_n)
                    

    return Block_Names,Block_Obj           

if __name__ == '__main__':
    pass
