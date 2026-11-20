import opendssdirect as dss
dss.run_command("Clear")

# The source: a 12.47 kV three-phase substation
dss.run_command("New Circuit.Tiny basekv=12.47 pu=1.0 phases=3")

# Two 2-mile line segments: SourceBus -> Mid -> End
# r1, x1 are resistance and reactance per mile, in ohms
dss.run_command("New Line.Feeder1 bus1=SourceBus bus2=Mid phases=3 length=2 r1=0.3 x1=0.6")
dss.run_command("New Line.Feeder2 bus1=Mid bus2=End phases=3 length=2 r1=0.3 x1=0.6")

# Two customers (kw = real power, pf = power factor)
dss.run_command("New Load.House1 bus1=Mid phases=3 kv=12.47 kw=1000 pf=0.95")
dss.run_command("New Load.House2 bus1=End phases=3 kv=12.47 kw=2000 pf=0.95")

# Tell OpenDSS what 1.0 pu means, then solve
dss.run_command("Set voltagebases=[12.47]")
dss.run_command("CalcVoltageBases")
dss.run_command("Solve")

# Print the results
for name, v in zip(dss.Circuit.AllNodeNames(), dss.Circuit.AllBusMagPu()):
    print(f"{name:15s} {v:.4f} pu")
print("Total losses (kW):", dss.Circuit.Losses()[0] / 1000)