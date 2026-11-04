from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape,A4
from pathlib import Path
import json
O=Path('outputs/LEMOAdaptorBoard7_Compact_RevB/Copper_Plates');c=canvas.Canvas(str(O/'Copper_Plates_Drawing.pdf'),pagesize=landscape(A4));W,H=landscape(A4)
def txt(x,y,s,z=10):c.setFont('Helvetica',z);c.drawString(x,y,s)
for page,name in enumerate(['Lower','Upper'],1):
 c.rect(20,20,W-40,H-40);txt(35,H-44,f'Board7 Compact Rev B - {name} copper plate',18);txt(35,H-65,'PROTOTYPE / FOR QUOTATION - hardware and cable access fit check required',10)
 sc=2.7;ox,oy=83,135
 for edge in json.loads((O/(name+'_edges.json')).read_text()):
  p=c.beginPath();p.moveTo(ox+edge[0][0]*sc,oy+edge[0][1]*sc)
  for x,y in edge[1:]:p.lineTo(ox+x*sc,oy+y*sc)
  c.drawPath(p)
 for x,y in [(5,6),(60,6),(5,119),(60,119)]:
  X,Y=ox+x*sc,oy+y*sc;c.line(X-5,Y,X+5,Y);c.line(X,Y-5,X,Y+5)
 def dim(x1,y1,x2,y2,s):
  c.line(x1,y1,x2,y2)
  if y1==y2:
   for x in [x1,x2]:c.line(x,y1-3,x,y1+3)
   txt((x1+x2)/2-10,y1+5,s)
  else:
   for y in [y1,y2]:c.line(x1-3,y,x1+3,y)
   txt(x1-27,(y1+y2)/2,s)
 dim(ox,oy-22,ox+65*sc,oy-22,'65');dim(ox-22,oy,ox-22,oy+125*sc,'125')
 txt(ox,oy-44,'TOP VIEW - projected from STEP geometry',9)
 lines=['Material: T2 copper; thickness 2 mm','Quantity: 1 upper + 1 lower per assembly','Outer size: 65 x 125 mm','4 x DIA 3.4 THRU (M3 clearance, NOT tapped)','Datum: lower-left corner of outer rectangle','Hole centres (X,Y), mm:','(5,6), (60,6), (5,119), (60,119)','Hole pitch: 55 horizontal x 113 vertical']
 if name=='Upper':lines+=['Side access cutouts, through full thickness:','Left: X = 0 to 21.5; Y = 18 to 85','Right: X = 49 to 65; Y = 18 to 85','Each cutout height 67; central web width 27.5']
 else:lines+=['Full rectangular plate; no side access cutouts.']
 lines+=['Proposed tolerances: hole centres +/-0.1 mm;','outline +/-0.2 mm; thickness per stock supplier.','Deburr edges; maintain conductive mounting contact.']
 for i,line in enumerate(lines):txt(330,480-i*19,line)
 txt(330,140,'Provisional gaps: upper 25 mm above PCB top;',10);txt(330,123,'lower 8 mm below PCB bottom. PCB thickness 1.6 mm.',10)
 txt(35,76,'Bond plates to PGND mounting pads only. Keep plates/hardware clear of SGND LEMO shells and live conductors.',9)
 c.line(20,62,W-20,62);txt(35,40,f'B7C-CU-{page:02d} | Rev B | 2026-10-29 | Units: mm | Do not scale | Sheet {page}/2',10);c.showPage()
c.save()
