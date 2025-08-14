# main.py

from classes import DrillingOperation
from well_plan_builder import build_well_plan
##import config  # Load global variables like activity_rates, water_depth, etc.
from data_loaders import activity_rates
from config import well_parameters
import math

print(well_parameters)

def main():
    # You can create a parameters dictionary or use directly from config


    # Build Phases using well_plan_builder.py
    phases = build_well_plan(well_parameters, activity_rates)

    # Create DrillingOperation
    operation = DrillingOperation("Subsea Well Plan", phases)

    # Display the Plan
    df_plan = operation.display_plan()

    # Save to Excel (Optional)
    df_plan.to_excel("ANE-C.xlsx", index=False)

if __name__ == "__main__":
    print(well_parameters['jetting_conductor'])
    main()

    
 