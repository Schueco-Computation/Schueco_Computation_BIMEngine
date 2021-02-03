import rhinoscriptsyntax as rs
from Rhino import Geometry as rc
from Rhino import DocObjects as ro
import scriptcontext as sc

def corners():
    
    ##### polycurve Selection ####
    
    polylines=rs.ObjectsByType(4)
    prof_poly=[]
    prof_poly_l=[]
    for i in polylines:
        if "SP" in  rs.ObjectName(i):
            prof_poly.append(i)
            prof_poly_l.append(rs.CurveLength(i))
            
    
    
    prof=(prof_poly[(prof_poly_l.index(max(prof_poly_l)))])
    prof_split=rs.ExplodeCurves(prof,0)
    arcs=[]
    arcs_boundb=[]

                                                    # Create Layer for exploted profile Arcs
    for i in prof_split:                                            # Create bounding boxes around every Arc
        if rs.IsArc(i):
            arcs.append(i)
            prof_split.pop(prof_split.index(i))
            arcs_boundb.append((rs.BoundingBox(i)))
    bbxs=[]
    for i in arcs_boundb:
        bbxs.append(rs.AddSrfPt(i[0:4]))

    ############## Surface Split with RhinoCommon #########

    bbxs_split=[]

    for i, j in enumerate(bbxs):
        cutter=[rs.coercecurve(arcs[i])]
        brep=rs.coercebrep(j).Faces[0]
        bbxs_split.append(rc.BrepFace.Split(brep,cutter,0.01))

    bbxs_split_f=[]

    for i in bbxs_split:
        bbxs_split_f.append(i.Faces)

    bbxs_split_a=[]
    bbxs_split_f2=[]
    for i in bbxs_split_f:
        bbxs_split_a.append([])
        bbxs_split_f2.append([])
        for j in i:
            bbxs_split_f2[(bbxs_split_f.index(i))].append(j)
            bbxs_split_a[(bbxs_split_f.index(i))].append(rc.AreaMassProperties.Compute(rc.Mesh.CreateFromSurface(j)).Area)


    for i, j  in enumerate(bbxs_split_a):
        popindex=j.index(max(j))
        bbxs_split_f2[i].pop(popindex)

    srf_edg=[]
    for i in (bbxs_split_f2):
        for j in i:
            srf_edg.append(rs.DuplicateEdgeCurves(sc.doc.Objects.AddBrep((j).DuplicateFace(1))))

    for i in srf_edg:
        for j in i:
           if rs.IsArc(j):
               rs.DeleteObject(j)
               srf_edg[srf_edg.index(i)].pop(srf_edg[srf_edg.index(i)].index(j)) ###


    for i in srf_edg:
        for j in i:
            prof_split.append(j)

    rs.AddLayer("Joined_prof",255,0,0)
    join_prof=rs.JoinCurves(prof_split)
    for i in join_prof:
        if rs.IsCurveClosed(i):
            rs.ObjectLayer(i,"Joined_prof")
    rs.LayerVisible("Joined_prof",True)
    sc.doc.Objects.Delete(rs.ObjectsByLayer("0"), True)
return join_prof

if __name__ == '__main__':
    corners()
