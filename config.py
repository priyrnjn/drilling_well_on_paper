
import math
# Constants
previous_well_water_depth = 2820 # in meters
sailing = 280 #NM
water_depth_msl = 2090 #MSL
air_gap = 25
conductor_casing_bml = 80
surface_casing_bml = 630
pipe_od_in = 5.5  # in inches
intermediate_casing_depth = 3118
production_casing_depth = 3925
well_td = 5025
coring_depths = [2915, 3635, 4275, 4925]
jetting_conductor = True
pilot_hole = True
include_intermediate_casing = True
include_liner_casing = True

logging_days_intermediate = 3
logging_days_production = 8
logging_days_liner = 8

water_depth = water_depth_msl + air_gap
conductor_casing_depth = water_depth + conductor_casing_bml
surface_casing_depth = water_depth + surface_casing_bml

intermediate_section_cores = [depth for depth in coring_depths if  surface_casing_depth < depth <= intermediate_casing_depth]
production_section_cores = [depth for depth in coring_depths if intermediate_casing_depth < depth <= production_casing_depth]
liner_section_cores = [depth for depth in coring_depths if production_casing_depth < depth <= well_td]

no_of_cores_intermediate_section = len(intermediate_section_cores)
no_of_cores_production_section = len(production_section_cores)
no_of_cores_liner_section = len(liner_section_cores)


riser_jts_previous_well = math.ceil(previous_well_water_depth / 27.4)  # 27.4 m per riser joint
riser_jts = math.ceil(water_depth / 27.4) 

#Coring Depths:
coring_depth_1 = 2915
coring_depth_2 = 3635  
coring_depth_3 = 4275
coring_depth_4 = 4925


string_closed_disp = 0.0964    # bbl/m
string_capacity = 0.0695 # bbl/m
riser_annulus_capacity = 1.1505 - string_closed_disp  # bbl/m

choke_line_vol = 0.0645341 * water_depth  # in bbl, assuming choke line volume is 0.0645341 bbl/m

riser_annulus_vol = riser_annulus_capacity * water_depth  # in bbl
riser_vol = 1.1505 * water_depth

casing_capacity_36_in = 3.47073
casing_capacity_20_in = 1.11804
casing_capacity_13_3_8_in = 0.491207
casing_capacity_9_5_8_in = 0.23215  # 53.5 ppf bbl/m
casing_capacity_7_in = 0.121848   # 29 ppf bbl/m

OH_42_in = 5.621946
OH_26_in = 2.154435
OH_17_5_in = 0.9760052
OH_12_25_in = 0.478242
OH_8_5_in = 0.2302465

casing_annulus_vol_36_in = casing_capacity_36_in - string_closed_disp  # bbl/m
casing_annulus_vol_20_in = casing_capacity_20_in - string_closed_disp   # bbl/m         
casing_annulus_vol_13_3_8_in = casing_capacity_13_3_8_in - string_closed_disp  # bbl/m
casing_annulus_vol_9_5_8_in = casing_capacity_9_5_8_in - string_closed_disp  # bbl/m
casing_annulus_vol_7_in = casing_capacity_7_in - string_closed_disp  # bbl/m

OH_annulus_vol_42_in = OH_42_in - string_closed_disp
OH_annulus_vol_26_in = OH_26_in - string_closed_disp
OH_annulus_vol_17_5_in = OH_17_5_in - string_closed_disp
OH_annulus_vol_12_25_in = OH_12_25_in - string_closed_disp
OH_annulus_vol_8_5_in = OH_8_5_in - string_closed_disp


bottoms_up_17_5_in = riser_annulus_vol + OH_annulus_vol_17_5_in*(intermediate_casing_depth-surface_casing_depth)+casing_annulus_vol_20_in*(surface_casing_depth-water_depth)
bottoms_up_12_25_in = riser_annulus_vol+ OH_annulus_vol_12_25_in*(production_casing_depth-intermediate_casing_depth) + casing_annulus_vol_13_3_8_in*(intermediate_casing_depth-water_depth)
bottoms_up_8_5_in = riser_annulus_vol + OH_annulus_vol_8_5_in*(well_td-production_casing_depth) + casing_annulus_vol_9_5_8_in*(production_casing_depth-water_depth)


    
    
well_parameters = {
        'previous_well_water_depth': previous_well_water_depth,
        'water_depth': water_depth,
        'riser_jts_previous_well': riser_jts_previous_well,
        'riser_joints': riser_jts,
        'sailing_distance': sailing,
        'surface_casing_bml': surface_casing_bml,
        'conductor_casing_bml': conductor_casing_bml,
        'surface_casing_depth': surface_casing_depth,
        'intermediate_casing_depth': intermediate_casing_depth,
        'production_casing_depth': production_casing_depth,
        'well_td': well_td,
        'logging_days_intermediate': logging_days_intermediate,
        'logging_days_production': logging_days_production,
        'logging_days_liner': logging_days_liner,
        'bottoms_up_17_5_in': bottoms_up_17_5_in,
        'bottoms_up_12_25_in': bottoms_up_12_25_in,
        'bottoms_up_8_5_in': bottoms_up_8_5_in,
        'pipe_od_in': pipe_od_in,
        'string_capacity': string_capacity,
        'jetting_conductor': jetting_conductor,
        'pilot_hole': pilot_hole,
        'intermediate_section_cores': intermediate_section_cores,
        'production_section_cores': production_section_cores,
        'liner_section_cores': liner_section_cores,
        'include_intermediate_casing': include_intermediate_casing, 
        'include_liner_casing': include_liner_casing

    }

#print(well_parameters)