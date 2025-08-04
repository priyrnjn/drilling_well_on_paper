
from classes import MicroTask, MacroTask, Phase, DrillingOperation, RigOperationMode
from calculations import hole_volume_bbl_per_m, minimum_flow_rate_bph, minimum_flow_rate_bpm, wiper_trip, wiper_trip_riserless, round_trip, run_and_retrieve_WB, coring_time
#from config import pipe_od_in, surface_casing_depth, string_closed_disp, string_capacity, riser_annulus_vol, bottoms_up_12_25_in
from config import *
import math

def previous_well_operation_and_rig_move(previous_well_water_depth, sailing_distance, activity_rates):
    riser_jts_previous_well = math.ceil(previous_well_water_depth / 27.4)
    pull_out_mule_shoe = MacroTask("BOP & Riser Retrieval / pre rig move", [
        MicroTask("Pull Out Mule Shoe", previous_well_water_depth + 250, activity_rates['Tripping']),
        MicroTask("Lay_Dn_Cement_Head", 1, activity_rates['Lay_Dn_Cement_Head']),
    ])
    pull_out_bop = MacroTask("Pull Out BOP", [
        MicroTask("Rig_up_for_riser_handling", 1, activity_rates['Rig_up_for_riser_handling']),
        MicroTask("Unlatch_BOP", 1, activity_rates['Unlatch_BOP']),
        MicroTask("Secure_Choke_Kill_Boost_Goosenecks", 1, activity_rates['Secure_Choke_Kill_Boost_Goosenecks']),
        MicroTask("L_dn_dummy_riser_n_slip_jt", 1, activity_rates['L_dn_dummy_riser_n_slip_jt']),
        MicroTask("Tripping_BOP", riser_jts_previous_well, activity_rates['Tripping_BOP']),
        MicroTask("Receive_and_Park_BOP", 1, activity_rates['Receive_and_Park_BOP']),
        MicroTask("Sea_Fasten_Prepare_for_rig_move", 1, activity_rates['Sea_Fasten_Prepare_for_rig_move'])
    ])
    sailing_to_well = MacroTask("Sail to Well", [
        MicroTask("Sail to Well", sailing_distance, activity_rates['Sailing'])
    ])
    dp_calibration = MacroTask("DP Calibration", [
        MicroTask("DP Calibration", 1, activity_rates['DP Calibration'])
    ])
    return Phase("Phase 0: BOP & Riser Retrieval / pre rig move", [
        pull_out_mule_shoe,
        pull_out_bop,
        sailing_to_well,
        dp_calibration
    ])

def top_hole_section(water_depth, surface_casing_bml, conductor_casing_bml, string_capacity, activity_rates, jetting_conductor=True):
    investigative_hole = MacroTask("Investigative Hole", [
        MicroTask("Continue RIH 12-1/4'' IH BHA", water_depth / 2, activity_rates['Tripping']),
        MicroTask("Drill 12-1/4'' IH Hole", surface_casing_bml, activity_rates['Drilling_IH']), 
        MicroTask("Wiper Trip", 1, wiper_trip_riserless(water_depth + surface_casing_bml, water_depth, 12.25, string_closed_disp,water_depth,string_capacity, activity_rates)),
        MicroTask("Circulation", hole_volume_bbl_per_m(12.25) * surface_casing_bml * 2, minimum_flow_rate_bph(12.25, 5.5)),
        MicroTask("POOH 12-1/4'' IH BHA", water_depth + surface_casing_bml, activity_rates['Tripping']),
        MicroTask("Slip and Cut", 1, activity_rates['Slip_and_Cut'])
    ])
    conductor_drilling = MacroTask("Drill 42'' Hole", [
        MicroTask("Make Up MWD BHA", 1, activity_rates['BHA_Make_Up_LWD']),
        MicroTask("Run 26'' x 42'' BHA", water_depth, activity_rates['Tripping']),
        MicroTask("Drill 42''", conductor_casing_bml, activity_rates["Drilling_42_in"], RigOperationMode.ROTATE_CIRCULATE),
        MicroTask("Circulate, POOH", 1, wiper_trip_riserless(water_depth + conductor_casing_bml, water_depth, 42, string_closed_disp, water_depth, string_capacity, activity_rates)),
        MicroTask('Wait for Soaking & RIH', 1, 1/4),
        MicroTask("Circulation", (hole_volume_bbl_per_m(42) * conductor_casing_bml + string_capacity * (conductor_casing_bml + water_depth)) * 2, 1000 / 42),
        MicroTask("POOH", conductor_casing_bml + water_depth, activity_rates['Tripping'], RigOperationMode.POOH),
    ])
    conductor_casing = MacroTask("Run Conductor Casing", [
        MicroTask("Change_Pipe_Handler", 1, activity_rates['Change_Pipe_Handler']), 
        MicroTask("Run Conductor Casing", math.ceil(conductor_casing_bml / 12), activity_rates['Casing_Lowering_36_in'], RigOperationMode.RIH),
        MicroTask("Install_Ball_Valves_Slope_Indicator_Latch_Mud_Mat", 1, activity_rates['Install_Ball_Valves_Slope_Indicator_Latch_Mud_Mat']),
        MicroTask("Tripping_36_Casing_on_Landing_String", water_depth - surface_casing_bml, activity_rates['Tripping_36_Casing_on_Landing_String']),
        MicroTask("Tripping_36_Casing_on_Landing_String_OH", surface_casing_bml, activity_rates['Tripping_36_Casing_on_Landing_String_OH']),
        MicroTask("Circulation", 1, 1),
        MicroTask("Cement Conductor Casing", 1, activity_rates['36_Casing_Cementation']),
        MicroTask("Wait on Cement", 1, activity_rates['36_Casing_WOC']),
        MicroTask("Release Cart Tool and POOH", water_depth, activity_rates['Tripping']),
        MicroTask("B_Off_Cart_Tool_PO_Inner_String", 1, activity_rates['B_Off_Cart_Tool_PO_Inner_String']),
    ])
    jet_conductor_casing = MacroTask("Jet 36'' Casing", [
        MicroTask("Change_Pipe_Handler", 1, activity_rates['Change_Pipe_Handler']), 
        MicroTask("Run Conductor Casing", math.ceil(conductor_casing_bml / 12), activity_rates['Casing_Lowering_36_in'], RigOperationMode.RIH),
        MicroTask("Install_Ball_Valves_Slope_Indicator_Latch_Mud_Mat", 1, activity_rates['Install_Ball_Valves_Slope_Indicator_Latch_Mud_Mat']),
        MicroTask("Tripping_36_Casing_on_Landing_String", water_depth - surface_casing_bml, activity_rates['Tripping_36_Casing_on_Landing_String']),
        MicroTask("Tripping_36_Casing_on_Landing_String_OH", surface_casing_bml, activity_rates['Tripping_36_Casing_on_Landing_String_OH']),
        MicroTask("Jet Conductor Casing", 1, 9),   # Fixed duration for jetting
        MicroTask("Wait on soaking", 1, 12),       # Fixed wait time
    ])
    surface_drilling = MacroTask("Drill 26'' Hole", [
        MicroTask("Change_Pipe_Handler", 1, activity_rates['Change_Pipe_Handler']),
        MicroTask("Make Up Mud Motor, MWD BHA", 1, activity_rates['BHA_Make_Up_LWD']),
        MicroTask('RIH 26\'\' BHA', water_depth + conductor_casing_bml - 50, activity_rates['Tripping']),
        MicroTask('RIH with wash down and Tag cement', 30, activity_rates['Tripping_Wash_Dn']),
        MicroTask('Drill Cement & clear rat hole', 50, activity_rates['Drill_Cement_36_Casing']),
        MicroTask("Drill 26''", surface_casing_bml - conductor_casing_bml, activity_rates['Drilling_26_in'], RigOperationMode.ROTATE_CIRCULATE),
        MicroTask('Wiper Trip', 1, wiper_trip_riserless(surface_casing_depth, conductor_casing_bml, 26, string_closed_disp, water_depth, string_capacity, activity_rates)),
        MicroTask("Circulate", (hole_volume_bbl_per_m(26) * surface_casing_bml + string_capacity * surface_casing_depth) * 2, (1000 / 42) * 60),
        MicroTask('POOH 26\'\' BHA', surface_casing_depth, activity_rates['Tripping'], RigOperationMode.POOH),
        MicroTask("Break Off BHA", 1, activity_rates['BHA_Break_Off_LWD']),
    ])
    drill_ahead_surface_drilling = MacroTask("Drill 26'' Hole", [
        MicroTask("Drill 26''", surface_casing_bml - conductor_casing_bml, activity_rates['Drilling_26_in'], RigOperationMode.ROTATE_CIRCULATE),
        MicroTask('Wiper Trip', 1, wiper_trip_riserless(surface_casing_depth, conductor_casing_bml, 26, string_closed_disp, water_depth, string_capacity, activity_rates)),
        MicroTask("Circulate", (hole_volume_bbl_per_m(26) * surface_casing_bml + string_capacity * surface_casing_depth) * 2, (1000 / 42) * 60),
        MicroTask('POOH 26\'\' BHA', surface_casing_depth, activity_rates['Tripping'], RigOperationMode.POOH),
        MicroTask("Break Off BHA", 1, activity_rates['BHA_Break_Off_LWD']),
    ])

    surface_casing = MacroTask("Run 20'' Casing & Cement", [
        MicroTask('Rig_up_for_Casing', 1, activity_rates['Rig_up_for_Casing']),
        MicroTask('Run_Check_Float_Fun_20_Casing', 1, activity_rates['Run_Check_Float_Fun_20_Casing']),
        MicroTask("Run 20'' Casing", math.ceil(surface_casing_bml / 12), activity_rates['Casing_Lowering_20_in'], RigOperationMode.RIH),
        MicroTask('M_Up_HPWHH_Run_Inner_String_Engage_Cart_to_HPWHH', 1, activity_rates['M_Up_HPWHH_Run_Inner_String_Engage_Cart_to_HPWHH']),
        MicroTask('Tripping_Casing_on_Landing_String', water_depth - surface_casing_bml, activity_rates['Tripping_Casing_on_Landing_String']),
        MicroTask('Tripping_Casing_on_Landing_String_OH', surface_casing_bml, activity_rates['Tripping_Casing_on_Landing_String_OH']),
        MicroTask("Cementing 20'' Casing", 1, activity_rates['Cementing_20_in']),
        MicroTask("Wait on Cement", 1, activity_rates['WOC_20_in']),
        MicroTask('Release_Cart_from_HPWHH', 1, activity_rates['Release_Cart_from_HPWHH']),
        MicroTask('POOH Cart Tool to surface', water_depth, activity_rates['Tripping'], RigOperationMode.POOH),
    ])
    
    if(jetting_conductor):
        return Phase(" Top Hole", [
            investigative_hole,
            jet_conductor_casing, 
            drill_ahead_surface_drilling,
            surface_casing            
        ])
    else:
        return Phase(" Top Hole", [
            investigative_hole,
            conductor_drilling,
            conductor_casing,
            surface_drilling,
            surface_casing
        ])
    
def bop_lowering(water_depth, conductor_casing_bml, surface_casing_bml, surface_casing_depth, string_capacity, activity_rates):
    riser_jts = math.ceil(water_depth / 27.4) 
    bop_lowering = MacroTask("BOP Lowering", [
        MicroTask("Rig_up_for_riser_handling", 1, activity_rates['Rig_up_for_riser_handling']),
        MicroTask('Run_BOP_Splash_Zone', 1, activity_rates['Run_BOP_Splash_Zone']),
        MicroTask('Run BOP on Riser', riser_jts, activity_rates['Tripping_BOP']),
        MicroTask('Pressure Test Choke, Kill, Boost & Conduit Lines', math.ceil(water_depth / 500), activity_rates['Pr_Test_C_K_B_C']),
        MicroTask('Run_Slip_Jt_Landing_Jt', 1, activity_rates['Run_Slip_Jt_Landing_Jt']),
        MicroTask('Install_C_K_B_C_Goosenecks', 1, activity_rates['Installl_C_K_B_C_Goosenecks']),
        MicroTask('Pressure Test Choke, Kill & Boost Goosenecks', 1, activity_rates['Pr_Test_C_K_B_C']),
        MicroTask('Install_Saddle_Loops_Engage_MRT', 1, activity_rates['Install_Saddle_Loops_Engare_MRT']),
        MicroTask('Land & Latch BOP. Carry Out Pick up and Slump Test', 1, activity_rates['Land_Latch_BOP_Pick_Up_Test_Slump_Test']),
        MicroTask('Pressure Test Connector. Stroke out Slip Jt & Lay Dn Landing Jt', 1, activity_rates['Pr_Test_Connector_Stroke_Out_Slip_Jt_L_Dn_Landing_Jt']),
        MicroTask('Install_Diverter', 1, activity_rates['Install_Diverter']),
        MicroTask('Rig Down Spider & Gimbal', 1, activity_rates['Rig_Dn_Spider_Gimbal']),
    ])
    return Phase("Phase 2: Surface Section", [
        bop_lowering
    ])

def intermediate_casing(water_depth, surface_casing_bml, surface_casing_depth, intermediate_casing_depth, logging_days_intermediate, bottoms_up_17_5_in, intermediate_section_cores, activity_rates, pilot_hole):
    coring_microtasks = []
    for i, coring_depth in enumerate(intermediate_section_cores, start=1):
        coring_microtasks.append(
            MicroTask(f"Coring at depth {coring_depth}", 1, coring_time(coring_depth, intermediate_casing_depth, 17.5, bottoms_up_12_25_in, activity_rates, pipe_od_in, core_no=i, core_length=9))
        )
    intermediate_drilling = MacroTask("Drill 17.5'' Hole", [
        MicroTask('slip_and_cut', 1, activity_rates['Slip_and_Cut']),
        MicroTask('Change_Pipe_Handler', 1, activity_rates['Change_Pipe_Handler']),
        MicroTask('Surface Equipment Pressure Test', 1, activity_rates['Surface_Equipment_Pr_Test']),
        MicroTask('Make up LWD BHA', 1, activity_rates['BHA_Make_Up_LWD']),
        MicroTask('Run 17-1/2\'\' BHA', water_depth + surface_casing_bml - 50, activity_rates['Tripping']),
        MicroTask('BOP Pressure Test', 1, activity_rates['BOP_Pressure_Test']),
        MicroTask('Continue RIH with Wash Dn & Tag Cement', 30, activity_rates['Tripping_Wash_Dn']),
        MicroTask('Drill_Shoe_Track_LOT', 1, activity_rates['Drill_Shoe_Track_LOT']),
        MicroTask('Fingerprint_Flow_Back', 1, activity_rates['Fingerprint_Flow_Back']),
        MicroTask("Drill 17.5''", intermediate_casing_depth - surface_casing_depth, activity_rates['Drilling_17.5_in'], RigOperationMode.ROTATE_CIRCULATE),
        #MicroTask('Circulations for Bottoms up (3 times)', bottoms_up_17_5_in * 3, minimum_flow_rate_bph(17.5, 5.5)),
        *coring_microtasks,
        MicroTask('Wiper Trip', 1, wiper_trip(intermediate_casing_depth, surface_casing_depth, 17.5, string_closed_disp, water_depth, string_capacity, riser_annulus_vol, activity_rates)),
        MicroTask("Circulate", bottoms_up_17_5_in, activity_rates['Circulation']),
        MicroTask("POOH", intermediate_casing_depth, activity_rates['Tripping'], RigOperationMode.POOH),
    ])

    run_dumb_iron_bha_carry_out_lot = MacroTask("RIH dumb iron BHA and Carry out LOT", [
        MicroTask('slip_and_cut', 1, activity_rates['Slip_and_Cut']),
        MicroTask('Change_Pipe_Handler', 1, activity_rates['Change_Pipe_Handler']),
        MicroTask('Surface Equipment Pressure Test', 1, activity_rates['Surface_Equipment_Pr_Test']),
        MicroTask('Make up Dumb Iron BHA', 1, activity_rates['BHA_Make_Up_LWD']),
        MicroTask('Run 17-1/2\'\' BHA', water_depth + surface_casing_bml - 50, activity_rates['Tripping']),
        MicroTask('BOP Pressure Test', 1, activity_rates['BOP_Pressure_Test']),
        MicroTask('Continue RIH with Wash Dn & Tag Cement', 30, activity_rates['Tripping_Wash_Dn']),
        MicroTask('Drill_Shoe_Track_LOT', 1, activity_rates['Drill_Shoe_Track_LOT']),
        #MicroTask('Fingerprint_Flow_Back', 1, activity_rates['Fingerprint_Flow_Back']),
        #MicroTask("Drill 17.5''", intermediate_casing_depth - surface_casing_depth, activity_rates['Drilling_17.5_in'], RigOperationMode.ROTATE_CIRCULATE),
        #MicroTask('Circulations for Bottoms up (3 times)', bottoms_up_17_5_in * 3, minimum_flow_rate_bph(17.5, 5.5)),
        #MicroTask('Wiper Trip', 1, wiper_trip(intermediate_casing_depth, surface_casing_depth, 17.5)),
        #MicroTask("Circulate", bottoms_up_17_5_in, activity_rates['Circulation']),
        MicroTask("POOH", surface_casing_depth+5, activity_rates['Tripping'], RigOperationMode.POOH),
    ])

    drill_pilot_hole = MacroTask("Drill 12.25'' Pilot Hole", [
        MicroTask('slip_and_cut', 1, activity_rates['Slip_and_Cut']),
        MicroTask('Change_Pipe_Handler', 1, activity_rates['Change_Pipe_Handler']),
        MicroTask('Surface Equipment Pressure Test', 1, activity_rates['Surface_Equipment_Pr_Test']),
        MicroTask('Make up LWD BHA', 1, activity_rates['BHA_Make_Up_LWD']),
        MicroTask('Run 12.25\'\' BHA', water_depth + surface_casing_bml - 50, activity_rates['Tripping']),
        MicroTask('BOP Pressure Test', 1, activity_rates['BOP_Pressure_Test']),
        MicroTask('Continue RIH with Wash Dn & Tag Cement', 30, activity_rates['Tripping_Wash_Dn']),
        MicroTask('Drill_Shoe_Track_LOT', 1, activity_rates['Drill_Shoe_Track_LOT']),
        MicroTask('Fingerprint_Flow_Back', 1, activity_rates['Fingerprint_Flow_Back']),
        MicroTask("Drill 12.25''", intermediate_casing_depth - surface_casing_depth - 10, activity_rates['Drilling_12.25_in'], RigOperationMode.ROTATE_CIRCULATE),
        *coring_microtasks,
        #MicroTask(f"Coring at depth {coring_depth_1}", 1, coring_time(coring_depth_1, surface_casing_depth, 12.25, core_no=1, core_length=9)),
        MicroTask("POOH", surface_casing_depth + 10, activity_rates['Tripping'], RigOperationMode.POOH),
    ])

    wireline_log_intermediate_casing = MacroTask("Wireline Logging", [
        MicroTask("Wireline Logging", 1, 1/(logging_days_intermediate*24)),
        # Uncomment if roundtrip is needed
        # MicroTask("Roundtrip for logging", 1, round_trip(intermediate_casing_depth, surface_casing_depth, 17.5)),
    ])

    enlarge_pilot_hole = MacroTask("Enlarge Pilot Hole", [
        MicroTask("Change_Pipe_Handler", 1, activity_rates['Change_Pipe_Handler']),
        MicroTask("Make up MWD BHA", 1, activity_rates['BHA_Make_Up_LWD']),
        MicroTask("Run 17.5'' BHA", surface_casing_depth, activity_rates['Tripping']),
        MicroTask("Enlarge 12.25'' Hole to 17.5''", intermediate_casing_depth - surface_casing_depth, activity_rates['Drilling_17.5_in'] * 3, RigOperationMode.ROTATE_CIRCULATE),
        MicroTask("Wiper Trip", 1, wiper_trip(intermediate_casing_depth, surface_casing_depth, 17.5,  string_closed_disp, water_depth, string_capacity, riser_annulus_vol, activity_rates)),
        MicroTask("Circulate", bottoms_up_17_5_in, activity_rates['Circulation']),
        MicroTask("POOH", intermediate_casing_depth, activity_rates['Tripping'], RigOperationMode.POOH),
    ])

    intermediate_casing = MacroTask("Run 13.375'' Casing & Cement", [
        # Uncomment if roundtrip is needed
        # MicroTask("Roundtrip for Casing Lowering", 1, round_trip(intermediate_casing_depth, surface_casing_depth, 17.5)),
        MicroTask('Retrieve Wear Bush', 1, run_and_retrieve_WB(activity_rates, water_depth)),
        MicroTask("Rig_up_for_Casing", 1, activity_rates['Rig_up_for_Casing']),
        MicroTask("Run_Check_Float_Fun_13.625_Casing", 1, activity_rates['Run_Check_Float_Fun_13.625_Casing']),
        MicroTask("Run 13.375'' Casing", math.ceil((intermediate_casing_depth - water_depth) / 12), activity_rates['Casing_Lowering_13-3/8_in'], RigOperationMode.RIH),
        MicroTask('Tripping_Casing_on_Landing_String', water_depth, activity_rates['Tripping_Casing_on_Landing_String']),
        MicroTask('Land_Latch_Casing_Indexing_Pick_up_test', 1, activity_rates['Land_Latch_Casing_Indexing_Pick_up_test']),
        MicroTask('Cementing_13-3/8_in', 1, activity_rates['Cementing_13-3/8_in']),
        MicroTask('Set_Seal_Assembly', 1, activity_rates['Set_Seal_Assembly']),
        MicroTask('Release_PADPRT_L_Dn_Cement_Head', 1, activity_rates['Release_PADPRT_L_Dn_Cement_Head']),
        MicroTask('POOH PADPRT to surface', water_depth, activity_rates['Tripping']),
        MicroTask('slip_and_cut', 1, activity_rates['Slip_and_Cut']),
        MicroTask('Set Wear Bush at Wellhead', 1, run_and_retrieve_WB(activity_rates, water_depth)),
    ])

    if(pilot_hole):
        return Phase(" Intermediate Casing", [
            run_dumb_iron_bha_carry_out_lot,
            drill_pilot_hole,
            wireline_log_intermediate_casing,
            enlarge_pilot_hole,
            intermediate_casing
        ])
    else:
        return Phase(" Intermediate Casing", [
            intermediate_drilling,
            wireline_log_intermediate_casing,
            intermediate_casing 
        
    ])

def production_casing(water_depth, intermediate_casing_depth, production_casing_depth, logging_days_production, production_section_cores, bottoms_up_12_25_in, pipe_od_in, activity_rates, number_of_cores =0):
    coring_microtasks = []
    for i, coring_depth in enumerate(production_section_cores, start=1):
        coring_microtasks.append(
            MicroTask(f"Coring at depth {coring_depth}", 1, coring_time(coring_depth, intermediate_casing_depth, 17.5, bottoms_up_12_25_in, activity_rates, pipe_od_in, core_no=i, core_length=9))
        )
    production_drilling = MacroTask("Drill 12.25'' Hole", [
        MicroTask("Change_Pipe_Handler", 1, activity_rates['Change_Pipe_Handler']),
        MicroTask('Lay_Dn_Cement_Head', 1, activity_rates['Lay_Dn_Cement_Head']),
        MicroTask("Make up LWD BHA", 1, activity_rates['BHA_Make_Up_LWD']),
        MicroTask("Run 12.25'' BHA", intermediate_casing_depth - 300, activity_rates['Tripping']),
        MicroTask('BOP_Function_Test', 1, activity_rates['BOP_Function_Test']),
        MicroTask('Choke_Drill', 1, activity_rates['Choke_Drill']),
        MicroTask("Continue RIH with Wash Dn & Tag Cement", 30, activity_rates['Tripping_Wash_Dn']),
        MicroTask("Drill_Shoe_Track_LOT", 1, activity_rates['Drill_Shoe_Track_LOT']),
        MicroTask("Fingerprint_Flow_Back", 1, activity_rates['Fingerprint_Flow_Back']),
        MicroTask("Drill 12.25''", production_casing_depth - intermediate_casing_depth - 10, activity_rates['Drilling_12.25_in'], RigOperationMode.ROTATE_CIRCULATE),
        *coring_microtasks,
        #MicroTask(f"Coring at depth {coring_depth_2}", 1, coring_time(coring_depth_2, intermediate_casing_depth, 12.25, core_no=2, core_length=9)),
        MicroTask("wiper_trip", 1, wiper_trip(production_casing_depth, intermediate_casing_depth, 12.25, string_closed_disp, water_depth, string_capacity, riser_annulus_vol, activity_rates)),
        MicroTask("Circulate", bottoms_up_12_25_in, minimum_flow_rate_bph(12.25, pipe_od_in)),
        MicroTask("POOH 12.25'' BHA to casing shoe", production_casing_depth - intermediate_casing_depth, activity_rates['Tripping_Pump_Out'], RigOperationMode.POOH),
        MicroTask("POOH 12.25'' BHA to surface", intermediate_casing_depth - 300, activity_rates['Tripping'], RigOperationMode.POOH),
        MicroTask("Break Off BHA", 1, activity_rates['BHA_Break_Off_LWD']),
    ])

    first_part_logging_hrs = 4*24
    round_trip_time = round_trip(production_casing_depth, intermediate_casing_depth, 12.25, string_closed_disp, water_depth, string_capacity, riser_annulus_vol, activity_rates)
    second_part_logging_hrs = (logging_days_production*24 - first_part_logging_hrs)       

    wireline_log_production_casing = MacroTask("Wireline Logging", [
        MicroTask("Wireline Logging", 1, 1/first_part_logging_hrs),
        MicroTask("Roundtrip for logging", 1, round_trip_time),
        MicroTask('Wireline_Logging_part_2', 1, 1/second_part_logging_hrs)
    ])

    wireline_log_production_casing_without_roundtrip = MacroTask("Wireline Logging", [
        MicroTask("Wireline Logging", 1, 1/(logging_days_production*24))
    ])

    production_casing = MacroTask("Run 9-5/8'' Casing & Cement", [
        MicroTask('Roundtrip for Casing Lowering', 1, round_trip(production_casing_depth, intermediate_casing_depth, 12.25, string_closed_disp, water_depth, string_capacity, riser_annulus_vol, activity_rates)),
        MicroTask('Retrieve Wear Bush', 1, run_and_retrieve_WB(activity_rates, water_depth)),
        MicroTask("Change_Pipe_Handler", 1, activity_rates['Change_Pipe_Handler']),
        MicroTask("Run_Check_Float_Fun_9.625_Casing", 1, activity_rates['Run_Check_Float_Fun_13.625_Casing']),
        MicroTask("Run 9-5/8'' Casing", math.ceil((production_casing_depth - water_depth) / 12), activity_rates['Casing_Lowering_13-3/8_in'], RigOperationMode.RIH),
        MicroTask("Tripping_Casing_on_Landing_String", intermediate_casing_depth - (production_casing_depth - water_depth), activity_rates['Tripping_Casing_on_Landing_String']),
        MicroTask("Tripping_Casing_on_Landing_String_OH", production_casing_depth - intermediate_casing_depth, activity_rates['Tripping_Casing_on_Landing_String_OH']),
        MicroTask('Cementing_9-5/8_in', 1, activity_rates['Cementing_13-3/8_in']),
        MicroTask('Set_Seal_Assembly', 1, activity_rates['Set_Seal_Assembly']),
        MicroTask('Release_PADPRT_L_Dn_Cement_Head', 1, activity_rates['Release_PADPRT_L_Dn_Cement_Head']),
        MicroTask('POOH PADPRT to surface', water_depth, activity_rates['Tripping']),
        MicroTask('slip_and_cut', 1, activity_rates['Slip_and_Cut']),
        MicroTask('Set Wear Bush at Wellhead', 1, run_and_retrieve_WB(activity_rates, water_depth)),
    ])


    if(logging_days_production>6):
        return Phase(" Production Casing", [
            production_drilling,
            wireline_log_production_casing,
            production_casing
            ])
    else:
        return Phase("Production Casing", [
            production_drilling,
            wireline_log_production_casing_without_roundtrip,
            production_casing
            ])


def liner_casing(water_depth, production_casing_depth, well_td, logging_days_liner, liner_section_cores, bottoms_up_8_5_in, pipe_od_in, activity_rates):
    coring_microtasks = []
    for i, coring_depth in enumerate(liner_section_cores, start=1):
        coring_microtasks.append(
            MicroTask(f"Coring at depth {coring_depth}", 1, coring_time(coring_depth, production_casing_depth, 8.5, bottoms_up_12_25_in, activity_rates, pipe_od_in, core_no=i, core_length=9))
        )
    liner_phase_drilling = MacroTask("Drill 8.5'' Hole", [
        MicroTask("Change_Pipe_Handler", 1, activity_rates['Change_Pipe_Handler']),
        MicroTask("Make up LWD BHA", 1, activity_rates['BHA_Make_Up_LWD']),
        MicroTask("Run 8.5'' BHA", production_casing_depth - 300, activity_rates['Tripping']),
        MicroTask('BOP_Pressure_Test', 1, activity_rates['BOP_Pressure_Test']),
        MicroTask('Choke_Drill', 1, activity_rates['Choke_Drill']),
        MicroTask("Continue RIH with Wash Dn & Tag Cement", 30, activity_rates['Tripping_Wash_Dn']),
        MicroTask("Drill_Shoe_Track_LOT", 1, activity_rates['Drill_Shoe_Track_LOT']),
        MicroTask("Fingerprint_Flow_Back", 1, activity_rates['Fingerprint_Flow_Back']),
        MicroTask("Drill 8.5''", well_td - production_casing_depth - 10, activity_rates['Drilling_12.25_in'], RigOperationMode.ROTATE_CIRCULATE),
        *coring_microtasks,
        #MicroTask(f"Coring at depth {coring_depth_3}", 1, coring_time(coring_depth_3, production_casing_depth, 8.5, core_no=3, core_length=9)),
        #MicroTask(f"Coring at depth {coring_depth_4}", 1, coring_time(coring_depth_4, production_casing_depth, 8.5, core_no=4, core_length=9)),
        MicroTask("wiper_trip", 1, wiper_trip(well_td, production_casing_depth, 8.5, string_closed_disp, water_depth, string_capacity, riser_annulus_vol, activity_rates)),
        MicroTask("Circulate", bottoms_up_8_5_in, minimum_flow_rate_bph(8.5, pipe_od_in)),
        MicroTask("POOH 12.25'' BHA to casing shoe", well_td - production_casing_depth, activity_rates['Tripping_Pump_Out'], RigOperationMode.POOH),
        MicroTask("POOH 12.25'' BHA to surface", production_casing_depth - 300, activity_rates['Tripping'], RigOperationMode.POOH),
        MicroTask("Break Off BHA", 1, activity_rates['BHA_Break_Off_LWD']),
    ])

    first_part_logging_hrs = 4*24
    round_trip_time = round_trip(well_td, production_casing_depth, 8.5, string_closed_disp, water_depth, string_capacity, riser_annulus_vol, activity_rates)
    second_part_logging_hrs = logging_days_liner*24 - first_part_logging_hrs   

    wireline_log_liner_casing = MacroTask("Wireline Logging", [
        MicroTask("Basic Logs", 1, 1/first_part_logging_hrs),
        MicroTask("Roundtrip for logging", 1, round_trip_time),
        MicroTask('Advance_Logging', 1, 1/second_part_logging_hrs)
    ])

    wireline_log_liner_casing_without_roundtrip = MacroTask("Wireline Logging", [
        MicroTask("Wireline Logging", 1, 1/(logging_days_liner*24))
    ])


    production_liner = MacroTask("Run 7'' Liner & Cement", [
        MicroTask('Roundtrip for Casing Lowering', 1, round_trip(well_td, production_casing_depth, 8.5, string_closed_disp, water_depth, string_capacity, riser_annulus_vol, activity_rates)),
        MicroTask("Change_Pipe_Handler", 1, activity_rates['Change_Pipe_Handler']),
        MicroTask("Run_Check_Float_Fun_7''_Liner", 1, activity_rates['Run_Check_Float_Fun_13.625_Casing']),
        MicroTask("Run 7'' Liner", math.ceil((well_td - production_casing_depth + 150) / 12), activity_rates['Casing_Lowering_13-3/8_in'], RigOperationMode.RIH),
        MicroTask("Tripping_Casing_on_Landing_String", production_casing_depth - (well_td - production_casing_depth + 150), activity_rates['Tripping_Casing_on_Landing_String']),
        MicroTask("Tripping_Casing_on_Landing_String_OH", well_td - production_casing_depth, activity_rates['Tripping_Casing_on_Landing_String_OH']),
        MicroTask('Cementing_7\'\' Liner', 1, activity_rates['Cementing_13-3/8_in']),
        MicroTask('Set_Liner_Hanger_Seal', 1, activity_rates['Set_Seal_Assembly']),
        MicroTask('Release_Liner_Hanger_Running_Tool', 1, activity_rates['Release_PADPRT_L_Dn_Cement_Head']),
        MicroTask('POOH Liner Hanger Running Tool to surface', water_depth, activity_rates['Tripping']),
        MicroTask('slip_and_cut', 1, activity_rates['Slip_and_Cut']),
    ])

    if(logging_days_liner>6):
        return Phase(" Liner Casing", [
            liner_phase_drilling,
            wireline_log_liner_casing,
            production_liner
        ])
    else:
        return Phase("Liner Casing", [
            liner_phase_drilling,
            wireline_log_liner_casing_without_roundtrip,
            production_liner
        ])

def scraping_cbl_vdl_hermetical(production_casing_depth, well_td, bottoms_up_8_5_in, activity_rates):
    completion_prep = MacroTask("Scraping, CBL-VDL & Hermetical", [
        MicroTask("RIH Tandem Scraper from surface to Scraping depth", production_casing_depth - 500, activity_rates['Tripping'], RigOperationMode.RIH),
        MicroTask('Scrape Casing', well_td - production_casing_depth + 500, activity_rates['Tripping_Pump_Out']),
        MicroTask('POOH Tandem Scraping BHA', well_td, activity_rates['Tripping']),
        MicroTask('Record CBL VDL Log', 1, activity_rates['Logging'] * 5),
        MicroTask('Run Mule Shoe for hermetical and inflow test', well_td, activity_rates['Tripping']),
        MicroTask('Changeover Well Volume from WBM to sea water', bottoms_up_8_5_in, minimum_flow_rate_bph(8.5, 5)),
        MicroTask('Carry out Inflow & Hermetical Test', 1, 1/7),
    ])
    return Phase(" Scraping, CBL-VDL & Hermetical", [completion_prep])

