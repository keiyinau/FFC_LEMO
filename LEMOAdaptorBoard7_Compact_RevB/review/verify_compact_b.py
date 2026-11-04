import pcbnew as p,json,math
from pathlib import Path
O=Path('outputs/LEMOAdaptorBoard7_Compact_RevB');b=p.LoadBoard(str(O/'LEMOAdaptorBoard7.kicad_pcb'));a=p.LoadBoard('outputs/LEMOAdaptorBoard7_Compact_RevA/LEMOAdaptorBoard7.kicad_pcb');fs={f.GetReference():f for f in b.GetFootprints()};old={f.GetReference():f for f in a.GetFootprints()}
for r,f in fs.items():
 assert sorted((q.GetNumber(),q.GetNetname()) for q in f.Pads())==sorted((q.GetNumber(),q.GetNetname()) for q in old[r].Pads())
 if not r.startswith('LEMO'):assert f.GetPosition()==old[r].GetPosition()
 else:assert abs(p.ToMM(f.GetPosition())[0]-43)<1e-6
assert [(p.ToMM(d.GetStart()),p.ToMM(d.GetEnd())) for d in b.GetDrawings() if d.GetLayer()==p.Edge_Cuts]==[(p.ToMM(d.GetStart()),p.ToMM(d.GetEnd())) for d in a.GetDrawings() if d.GetLayer()==p.Edge_Cuts]
def covered(net,layer,x,y):return any(z.GetNetname()==net and z.GetLayer()==layer and z.HitTestFilledArea(layer,p.VECTOR2I(round(x*1e6),round(y*1e6))) for z in b.Zones())
for layer in [p.F_Cu,p.B_Cu]:
 for yi in range(610,1266):
  for xi in range(310,381,5):assert covered('/PGND',layer,xi/10,yi/10),(xi,yi,layer)
for t in b.GetTracks():
 if isinstance(t,p.PCB_VIA) or not t.GetNetname().startswith('/Signal'):continue
 s=p.ToMM(t.GetStart());e=p.ToMM(t.GetEnd());n=max(1,math.ceil(math.dist(s,e)/.05))
 for j in range(n+1):
  x=s[0]+(e[0]-s[0])*j/n;y=s[1]+(e[1]-s[1])*j/n
  if x>=47.5:assert covered('/SGND',p.B_Cu,x,y),(x,y)
assert [f.GetReference() for f in fs.values() if {'/PGND','/SGND'}<=set(q.GetNetname() for q in f.Pads())]==['R_GND']
report={'pad_mapping_preserved':True,'outline_mounts_non_LEMO_positions_unchanged':True,'LEMO_move_inward_mm':7.5,'mating_end_estimate_global_x_mm':29,'board_left_x_mm':30,'main_signal_span_mm':39.52,'left_PGND_nominal_corridor_mm':8,'PGND_rail_fill_grid_pass_both_layers':True,'SGND_signal_centreline_pass_x_ge_47p5':True,'SI_and_physical_fit_validated':False}
(O/'review/design_checks.json').write_text(json.dumps(report,indent=2));print(report)
