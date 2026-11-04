from pathlib import Path
import shutil,pcbnew as p
S=Path('outputs/LEMOAdaptorBoard7_Compact_RevA');O=Path('outputs/LEMOAdaptorBoard7_Compact_RevB');O.mkdir(exist_ok=True)
for n in ['LEMOAdaptorBoard7.kicad_pcb','LEMOAdaptorBoard7.kicad_sch','LEMOAdaptorBoard7.kicad_pro','Board7.kicad_sym','fp-lib-table','sym-lib-table','pinmap.json']:shutil.copy(S/n,O/n)
for n in ['Board7.pretty','Assembly']:shutil.copytree(S/n,O/n,dirs_exist_ok=True)
(O/'review').mkdir(exist_ok=True)
b=p.LoadBoard(str(O/'LEMOAdaptorBoard7.kicad_pcb'));v=lambda x,y:p.VECTOR2I(round(x*1e6),round(y*1e6));nets={n.GetNetname():n for n in b.GetNetsByNetcode().values()}
for f in b.GetFootprints():
 if f.GetReference().startswith('LEMO'):f.Move(v(7.5,0))
for t in b.GetTracks():
 a=p.ToMM(t.GetStart());e=p.ToMM(t.GetEnd());n=t.GetNetname()
 if n.startswith('/Signal'):
  if a[0]<40:t.SetStart(v(a[0]+7.5,a[1]))
  if e[0]<40:t.SetEnd(v(e[0]+7.5,e[1]))
 if n=='/SGND' and a[0]<40:t.Move(v(7.5,0))
polys=[]
for z in b.Zones():
 poly=p.SHAPE_POLY_SET();poly.NewOutline();pts=[(39.5,64),(88,64),(88,125.5),(39.5,125.5)] if z.GetNetname()=='/SGND' else [(30.5,20.5),(94.5,20.5),(94.5,144.5),(30.5,144.5)]
 for x,y in pts:poly.Append(round(x*1e6),round(y*1e6))
 if z.GetNetname()=='/PGND':
  poly.NewHole()
  for x,y in [(38.5,61),(38.5,126.5),(94,126.5),(94,61)]:poly.Append(round(x*1e6),round(y*1e6),-1,0)
 polys.append(poly);z.SetOutline(poly);z.UnFill()
for y in [59,65,80,95,110,125,130]:
 t=p.PCB_VIA(b);t.SetPosition(v(34.5,y));t.SetWidth(p.FromMM(.6));t.SetDrill(p.FromMM(.3));t.SetLayerPair(p.F_Cu,p.B_Cu);t.SetNet(nets['/PGND']);b.Add(t)
for d in b.GetDrawings():
 if isinstance(d,p.PCB_TEXT):d.SetText(d.GetText().replace('REV A','REV B'))
 if isinstance(d,p.PCB_SHAPE) and d.GetLayer()==p.Dwgs_User and p.ToMM(d.GetStart())[0]==30:d.SetEnd(v(51.5,127))
p.SaveBoard(str(O/'LEMOAdaptorBoard7.kicad_pcb'),b);b=p.LoadBoard(str(O/'LEMOAdaptorBoard7.kicad_pcb'));p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(O/'LEMOAdaptorBoard7.kicad_pcb'),b)
f=O/'LEMOAdaptorBoard7.kicad_sch';f.write_text(f.read_text().replace('(rev "Compact A")','(rev "Compact B")'))
