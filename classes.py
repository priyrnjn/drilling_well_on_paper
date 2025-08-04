from enum import Enum
from typing import List
import pandas as pd
 
class RigOperationMode(Enum):
    RIH = "Running In"
    POOH = "Pulling Out"
    CIRCULATE = "Circulate"
    ROTATE = "Rotate"
    ROTATE_CIRCULATE = "Rotate & Circulate"
    RIH_ROTATE_CIRCULATE = "RIH + Rotate + Circulate"
    POOH_ROTATE_CIRCULATE = "POOH + Rotate + Circulate"

class MicroTask:
    def __init__(self, name: str, quantity: float, rate: float, mode: RigOperationMode = None):
        self.name = name
        self.quantity = quantity
        self.rate = rate
        self.mode = mode

    @property
    def estimated_time(self) -> float:
        return self.quantity / self.rate if self.rate else 0
class MacroTask:
    def __init__(self, name: str, micro_tasks: List[MicroTask]):
        self.name = name
        self.micro_tasks = micro_tasks

    def total_time(self) -> float:
        return sum(task.estimated_time for task in self.micro_tasks)
class Phase:
    def __init__(self, name: str, macro_tasks: List[MacroTask]):
        self.name = name
        self.macro_tasks = macro_tasks

    def total_time(self) -> float:
        return sum(macro.total_time() for macro in self.macro_tasks)
    
class DrillingOperation:
    def __init__(self, name: str, phases: List[Phase]):
        self.name = name
        self.phases = phases

    def total_time(self) -> float:
        return sum(phase.total_time() for phase in self.phases)

    def display_plan(self) -> pd.DataFrame:
        rows = []
        cumulative_time_hr = 0
        for phase in self.phases:
            for macro in phase.macro_tasks:
                for micro in macro.micro_tasks:
                    est_time = micro.estimated_time
                    cumulative_time_hr += est_time
                    rows.append({
                        #"Phase": phase.name,
                        "Macro Task": macro.name,
                        "Micro Task": micro.name,
                        #"Operation Mode": micro.mode.value if micro.mode else "N/A",
                        "Quantity": micro.quantity,
                        "Rate (units/hr)": micro.rate,
                        "Estimated Time (hr)": round(est_time, 2),
                        "Estimated Time (days)": round(est_time/24, 2),
                        "Cumulative Time (days)": round(cumulative_time_hr / 24, 2)
                    })
        df = pd.DataFrame(rows)
        print(f"\n📘 Subsea Well Drilling Plan: {self.name}")
        print(df)
        print(f"\n🕒 Total Estimated Time: {self.total_time():.2f} hr ({self.total_time()/24:.2f} days)\n")
        return df