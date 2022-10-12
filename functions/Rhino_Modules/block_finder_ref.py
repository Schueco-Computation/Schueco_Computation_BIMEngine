
import rhinoscriptsyntax as rs
import Rhino.Geometry as rc
import scriptcontext as sc



def block_finder():
    """
    
    input => Gets all block instances name from Rhino active Doc
    returns => Block instances Names list
    
    """
    # Getting block names 

    prof_bnames= rs.BlockNames()        
    
    # Filtering Named block
    
    bl_inst=[]
    bl_inst_names=[]
    for i in prof_bnames:               
        if "Schueco" in i: 
            bl_inst.append(rs.BlockInstances(i))
            bl_inst_names.append(i)     
    return bl_inst_names,bl_inst



def block_mover(j):
    
    """
    input => Takes block instance name
    returns => Transformed Instance GUID

    """
    oblist=rs.BlockObjects(j)
    curves=[]
    for k in oblist:
        name=rs.ObjectName(k)
        if name == "a_ref-line2" or name == "axis":
            curves.append(k)
    ins_point= rs.CurveCurveIntersection(curves[0],curves[1])
    origin=ins_point[0][1]
    bl_pos= rs.BlockInstanceInsertPoint(rs.BlockInstances(j))
    t_point=origin+bl_pos
    m_vector=(rs.VectorCreate(rs.CreatePoint(0,0,0),rs.CreateVector(t_point)))
    ins = rs.BlockInstances(j)
    rs.MoveObjects(ins,m_vector)
    rotate=rs.RotateObject(ins,rs.CreatePoint(0,0,0),180)
    #rt_bl_inst=rs.MirrorObject(bl_inst[i],rs.CreatePoint(0,0,0),rs.CreatePoint(0,1,0),True)
    
    
    return ins

    
if __name__ == '__main__':
    block_finder()