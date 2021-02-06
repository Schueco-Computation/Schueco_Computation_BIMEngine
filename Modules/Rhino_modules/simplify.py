import rhinoscriptsyntax as rs
import Rhino.Geometry as rc
import scriptcontext as sc
import math as m

def simplify():

    polyline=rs.ObjectsByLayer("Joined_prof")
    points=rs.CurveDiscontinuity(polyline,3)
    srf=rs.AddPlanarSrf(polyline)
    rad=7.00
    param=[]
    agnt2=[]
    
    
    for i in points: 
        agnt=rc.Circle(rs.coerce3dpoint(i),rad)
        event=rc.Intersect.Intersection.CurveBrep(rc.Circle.ToNurbsCurve(agnt),rs.coercebrep(srf),0.01,0.01)
        if len(event[1]) == 2:
            agnt2.append(agnt)
            param.append(event[1])
    
    
    angle_curves=[]
    for i in agnt2:
        angle_curves.append(rc.Curve.Split(rc.Circle.ToNurbsCurve(i),param[agnt2.index(i)]))
    
    
    simp_pts=[] 
    for i in angle_curves:
        for j in i:
            if m.floor(m.degrees((rc.Curve.GetLength(j))/rad)) == 90:
                simp_pts.append(agnt2[angle_curves.index(i)].Center)
            
    bound=rc.PolylineCurve.ToPolyline(rc.PolyCurve.ToPolyline(rs.coercecurve(polyline),0.001,0.01,0.4,170.0)).BoundingBox
    
    bound_l = []
    
    
    bound_pl=[]
    for i in (rc.BoundingBox.GetEdges(bound)[0:4]):
        bound_l.append(rc.Line.ToNurbsCurve(i))
    
    
    bound_pl=rc.Curve.JoinCurves(bound_l)
    bound_pts=rc.BoundingBox.GetCorners(bound)[0:4]
    bound_pts2=[]
    
    for i in simp_pts:
        if (rc.Curve.ClosestPoint(bound_pl[0],i,25.90))[0]:
             bound_pts2.append(rc.Polyline.ClosestPoint(rc.PolylineCurve.ToPolyline(bound_pl[0]),i))
             bound_pts2.append(i)
             
    
    for i in bound_pts:
        bound_pts2.append(i)
    
    poly_param=[]
    
    for p in bound_pts2:
        poly_param.append(rc.Curve.ClosestPoint(rs.coercecurve(polyline),p)[1])
    
    sortedt=sorted(poly_param)
    
    bound_pts_srt=[]
    for i in sortedt:
        bound_pts_srt.append(bound_pts2[poly_param.index(i)])
    
    openpoly=sc.doc.Objects.AddPolyline(bound_pts_srt)
    
    openline=rs.AddLine(rs.CurveEndPoint(openpoly),rs.CurveStartPoint(openpoly))
    
    lines=[openpoly,openline]
    
    closedpoly=rs.JoinCurves(lines,1)
    rs.ObjectName(closedpoly,"simp_prof")
    rs.DeleteObject(rs.ObjectsByType(8))
    
    return closedpoly
