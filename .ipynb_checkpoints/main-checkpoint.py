from typing import List

class MicroTask:
    def __init__(self, name: str, quantity: float, rate: float):
        self.name = name
        self.quantity = quantity  # total units (e.g., 500 m, 100 joints)
        self.rate = rate          # units per hour (e.g., 20 m/hr)

    @property
    def estimated_time(self) -> float:
        if self.rate == 0:
            raise ValueError(f"Rate for '{self.name}' cannot be zero.")
        return self.quantity / self.rate

    def __repr__(self):
        return f"{self.name}: {self.quantity} units @ {self.rate} units/hr → {self.estimated_time:.2f} hr"


class MacroTask:
    def __init__(self, name: str, micro_tasks: List[MicroTask]):
        self.name = name
        self.micro_tasks = micro_tasks

    def total_time(self) -> float:
        return sum(task.estimated_time for task in self.micro_tasks)

    def __repr__(self):
        return f"{self.name}: {self.total_time():.2f} hr"


class DrillingOperation:
    def __init__(self, name: str, macro_tasks: List[MacroTask]):
        self.name = name
        self.macro_tasks = macro_tasks

    def total_time(self) -> float:
        return sum(macro.total_time() for macro in self.macro_tasks)

    def display_plan(self):
        print(f"\n📘 Drilling Operation Plan: {self.name}")
        for macro in self.macro_tasks:
            print(f"\n🔹 {macro.name} - Total: {macro.total_time():.2f} hr")
            for micro in macro.micro_tasks:
                print(f"   ▫ {micro}")
        print(f"\n🕒 Total Estimated Time for Well: {self.total_time():.2f} hr\n")

# Define MicroTasks
pull_out_mule_shoe = MicroTask('Pull Out Mule Shoe', quantity= 2820, rate= 500)
rig_up_riser_handling_eqpt =  MicroTask('Rig up for Risers Handling', quantity = 1, rate = 0.1333)
unlatch_bop =  MicroTask('Unlatch BOP',  quantity= 1, rate=1)
secure_c_k_b_goosenecks = MicroTask('Secure Goosenecks', quantity= 1, rate = 0.25)
l_dn_dummy_riser_n_slip_jt = MicroTask('Lay Down Landing Jt & Slip Jt', quantity=1 , rate = 0.5)



drill_500m = MicroTask("Drill 12.25'' Hole", quantity=500, rate=20)  # 500 m at 20 m/hr





connect_20_joints = MicroTask("Connect Drill Pipe", quantity=20, rate=5)  # 5 joints/hr
circulate_clean = MicroTask("Circulate Hole Clean", quantity=2, rate=1)  # 2 hours (rate = 1 hr/hr)

# MacroTasks
pre_rigmove = MacroTask("Previous well operations", [pull_out_mule_shoe, rig_up_riser_handling_eqpt, unlatch_bop, secure_c_k_b_goosenecks, l_dn_dummy_riser_n_slip_jt])

drilling = MacroTask("Drilling Section", [drill_500m, connect_20_joints, circulate_clean])

# Another macro task
run_30_joints = MicroTask("Run Casing", quantity=30, rate=6)  # 30 joints @ 6 joints/hr
cement_job = MicroTask("Cement Casing", quantity=1, rate=1)   # 1 job @ 1 job/hr
casing = MacroTask("Casing Operation", [run_30_joints, cement_job])

# Full operation
operation = DrillingOperation("Well A", [pre_rigmove, drilling, casing])
operation.display_plan()
