import sys,json
from pathlib import Path
sys.path.insert(0,str(Path('work/squashfs-root/usr/lib').resolve()))
import FreeCAD as A,Part
O=Path('outputs/LEMOAdaptorBoard7_Compact_RevB/Copper_Plates');O.mkdir(exist_ok=True)
d=A.newDocument('Board7Compact');holes=[(5,6),(60,6),(5,119),(60,119)]
shapes={};report={}
for name in ['Lower','Upper']:
 s=Part.makeBox(65,125,2)
 for x,y in holes:s=s.cut(Part.makeCylinder(1.7,2,A.Vector(x,y,0)))
 if name=='Upper':
  for x,w in [(0,21.5),(49,16)]:s=s.cut(Part.makeBox(w,67,2,A.Vector(x,18,0)))
 assert s.isValid() and len(s.Solids)==1
 o=d.addObject('PartDesign::Feature',name+'_Plate');o.Shape=s;shapes[name]=s
 Part.export([o],str(O/(name+'_Plate.step')))
 edges=[]
 for e in s.Edges:
  pts=e.discretize(Deflection=.02)
  if all(abs(pt.z-2)<1e-6 for pt in pts):edges.append([[pt.x,pt.y] for pt in pts])
 (O/(name+'_edges.json')).write_text(json.dumps(edges))
 report[name]={'valid_solid':True,'volume_mm3':s.Volume,'bbox_mm':[s.BoundBox.XLength,s.BoundBox.YLength,s.BoundBox.ZLength]}
 o.Placement.Base.z=26.6 if name=='Upper' else -10
pcb=d.addObject('PartDesign::Feature','PCB_envelope');pcb.Shape=Part.makeBox(65,125,1.6)
for x,y in holes:pcb.Shape=pcb.Shape.cut(Part.makeCylinder(1.6,1.6,A.Vector(x,y,0)))
d.recompute();d.saveAs(str(O/'Compact_Sandwich.FCStd'))
(O/'CAD_checks.json').write_text(json.dumps(report,indent=2))
print(report)
