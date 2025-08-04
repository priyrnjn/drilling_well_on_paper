from phase_of_operation import previous_well_operation_and_rig_move, top_hole_section, bop_lowering, intermediate_casing, production_casing, liner_casing, scraping_cbl_vdl_hermetical
from config import *
from classes import DrillingOperation
from data_loaders import activity_rates


def build_well_plan(well_parameters, activity_rates):
    phases = []

    # Always include these sections
    phases.append(
        previous_well_operation_and_rig_move(
            previous_well_water_depth=well_parameters['water_depth'],
            sailing_distance=well_parameters['sailing_distance'],
            activity_rates=activity_rates
        )
    )

    phases.append(
        top_hole_section(
            water_depth=well_parameters['water_depth'],
            surface_casing_bml=well_parameters['surface_casing_bml'],
            conductor_casing_bml=well_parameters['conductor_casing_bml'],
            string_capacity=well_parameters['string_capacity'],
            activity_rates=activity_rates,
            jetting_conductor=well_parameters['jetting_conductor']
        )
    )

    phases.append(
        bop_lowering(
            water_depth=well_parameters['water_depth'],
            surface_casing_bml=well_parameters['surface_casing_bml'],
            conductor_casing_bml=well_parameters['conductor_casing_bml'],
            surface_casing_depth=well_parameters['surface_casing_depth'],
            string_capacity=well_parameters['string_capacity'],
            activity_rates=activity_rates
        )
    )

    # Conditionally Include Intermediate Casing Section
    if well_parameters.get('include_intermediate_casing', True):
        phases.append(
            intermediate_casing(
                water_depth=well_parameters['water_depth'],
                surface_casing_bml=well_parameters['surface_casing_bml'],
                surface_casing_depth=well_parameters['surface_casing_depth'],
                intermediate_casing_depth=well_parameters['intermediate_casing_depth'],
                logging_days_intermediate = well_parameters['logging_days_intermediate'],
                bottoms_up_17_5_in=well_parameters['bottoms_up_17_5_in'],
                intermediate_section_cores=well_parameters['intermediate_section_cores'],
                activity_rates=activity_rates,
                pilot_hole=well_parameters['pilot_hole']
            )
        )

    # Always Include Production Casing
    phases.append(
        production_casing(
            water_depth=well_parameters['water_depth'],
            intermediate_casing_depth=well_parameters['intermediate_casing_depth'],
            production_casing_depth=well_parameters['production_casing_depth'],
            logging_days_production = well_parameters['logging_days_production'],
            production_section_cores=well_parameters['production_section_cores'],
            bottoms_up_12_25_in=well_parameters['bottoms_up_12_25_in'],
            pipe_od_in=well_parameters['pipe_od_in'],
            activity_rates=activity_rates
        )
    )

    # Conditionally Include Liner Casing Section
    if well_parameters.get('include_liner_casing', True):
        phases.append(
            liner_casing(
                water_depth=well_parameters['water_depth'],
                production_casing_depth=well_parameters['production_casing_depth'],
                well_td=well_parameters['well_td'],
                logging_days_liner = well_parameters['logging_days_liner'],
                liner_section_cores=well_parameters['liner_section_cores'],
                bottoms_up_8_5_in=well_parameters['bottoms_up_8_5_in'],
                pipe_od_in=well_parameters['pipe_od_in'],
                activity_rates=activity_rates
            )
        )

    # Conditionally Include Scraping, CBL/VDL Section
    if well_parameters.get('include_scraping_cbl', True):
        phases.append(
            scraping_cbl_vdl_hermetical(
                production_casing_depth=well_parameters['production_casing_depth'],
                well_td=well_parameters['well_td'],
                bottoms_up_8_5_in=well_parameters['bottoms_up_8_5_in'],
                activity_rates=activity_rates
            )
        )

    return phases




#well_plan = build_well_plan(well_parameters, activity_rates)
# Build the phases list
#phases = build_well_plan(well_parameters, activity_rates)
# Create DrillingOperation Object
#well_operation = DrillingOperation("Well DD-KG1", phases)
# Display the Plan DataFrame
#well_plan_df = well_operation.display_plan()