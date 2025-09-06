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
    def __init__(self, name: str, quantity: float, rate: float, 
                 mode: RigOperationMode = None,
                 start_depth: float = None, end_depth: float = None):
        self.name = name
        self.quantity = quantity
        self.rate = rate
        self.mode = mode
        self.start_depth = start_depth
        self.end_depth = end_depth
        self.bit_depth = None        # will be updated later
        self.drilled_depth = None    # will be updated later

    @property
    def estimated_time(self) -> float:
        return self.quantity / self.rate if self.rate else 0


'''
class MicroTask:
    def __init__(self, name: str, quantity: float, rate: float, mode: RigOperationMode = None):
        self.name = name
        self.quantity = quantity
        self.rate = rate
        self.mode = mode

    @property
    def estimated_time(self) -> float:
        return self.quantity / self.rate if self.rate else 0

        
'''

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
    def __init__(self, name: str, phases):
        self.name = name
        self.phases = phases
        self.current_bit_depth = 0
        self.drilled_depth = 0

    def execute(self):
        for phase in self.phases:
            for macro in phase.macro_tasks:
                for task in macro.micro_tasks:
                    # Update depths
                    if "Drill" in task.name:
                        task.start_depth = self.current_bit_depth
                        self.current_bit_depth += task.quantity
                        self.drilled_depth = max(self.drilled_depth, self.current_bit_depth)
                        task.end_depth = self.current_bit_depth

                    elif "POOH" in task.name:
                        task.start_depth = self.current_bit_depth
                        # If no quantity, assume to surface
                        if task.quantity:
                            self.current_bit_depth = max(0, self.current_bit_depth - task.quantity)
                        else:
                            self.current_bit_depth = 0
                        task.end_depth = self.current_bit_depth

                    elif "RIH" in task.name:
                        task.start_depth = self.current_bit_depth
                        self.current_bit_depth += task.quantity
                        task.end_depth = self.current_bit_depth

                    else:
                        task.start_depth = self.current_bit_depth
                        task.end_depth = self.current_bit_depth

                    # Save bit & drilled depth into the task
                    task.bit_depth = self.current_bit_depth
                    task.drilled_depth = self.drilled_depth

    def total_time(self) -> float:
        return sum(phase.total_time() for phase in self.phases)

    def display_plan(self) -> pd.DataFrame:
        self.execute()
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
                        "Cumulative Time (days)": round(cumulative_time_hr / 24, 2),
                        "Start Depth (m)": micro.start_depth,
                        "End Depth (m)": micro.end_depth,
                        "Bit Depth (m)": micro.bit_depth,
                        "Drilled Depth (m)": micro.drilled_depth,
                    })
        df = pd.DataFrame(rows)
        print(f"\n📘 Subsea Well Drilling Plan: {self.name}")
        print(df)
        print(f"\n🕒 Total Estimated Time: {self.total_time():.2f} hr ({self.total_time()/24:.2f} days)\n")
        return df



'''    
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




class DepthTracker:
    def __init__(self):
        self.bit_depth = 0
        self.drilled_depth = 0

    def process_task(self, task: MicroTask):
        # If explicit depths are provided, update directly
        if task.start_depth is not None and task.end_depth is not None:
            self.bit_depth = task.end_depth
            if "Drill" in task.name:  # drilling increases drilled depth
                self.drilled_depth = max(self.drilled_depth, task.end_depth)

        # Assign values back to the task
        task.bit_depth = self.bit_depth
        task.drilled_depth = self.drilled_depth
'''