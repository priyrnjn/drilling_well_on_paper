# well_calculations.py
import math
import config as cfg

# --- Depth Calculations ---
water_depth = cfg.water_depth_msl + cfg.air_gap
conductor_casing_depth = water_depth + cfg.conductor_casing_bml
surface_casing_depth = water_depth + cfg.surface_casing_bml

# --- Riser Joints ---
riser_jts_previous_well = math.ceil(cfg.previous_well_water_depth / cfg.riser_joint_length)
riser_jts = math.ceil(water_depth / cfg.riser_joint_length)

# --- Coring Section Depth Classification ---
intermediate_section_cores = [
    d for d in cfg.coring_depths
    if surface_casing_depth < d <= cfg.intermediate_casing_depth
]
production_section_cores = [
    d for d in cfg.coring_depths
    if cfg.intermediate_casing_depth < d <= cfg.production_casing_depth
]
liner_section_cores = [
    d for d in cfg.coring_depths
    if cfg.production_casing_depth < d <= cfg.well_td
]

# --- Counts ---
no_of_cores_intermediate_section = len(intermediate_section_cores)
no_of_cores_production_section = len(production_section_cores)
no_of_cores_liner_section = len(liner_section_cores)

# --- Volumes ---
riser_annulus_capacity = cfg.riser_capacity_total - cfg.string_closed_disp
riser_annulus_vol = riser_annulus_capacity * water_depth
riser_vol = cfg.riser_capacity_total * water_depth
choke_line_vol = cfg.choke_line_capacity * water_depth

# --- Annulus Volumes ---
casing_annulus_vol_36_in = cfg.casing_capacity_36_in - cfg.string_closed_disp
casing_annulus_vol_20_in = cfg.casing_capacity_20_in - cfg.string_closed_disp
casing_annulus_vol_13_3_8_in = cfg.casing_capacity_13_3_8_in - cfg.string_closed_disp
casing_annulus_vol_9_5_8_in = cfg.casing_capacity_9_5_8_in - cfg.string_closed_disp
casing_annulus_vol_7_in = cfg.casing_capacity_7_in - cfg.string_closed_disp

OH_annulus_vol_42_in = cfg.OH_42_in - cfg.string_closed_disp
OH_annulus_vol_26_in = cfg.OH_26_in - cfg.string_closed_disp
OH_annulus_vol_17_5_in = cfg.OH_17_5_in - cfg.string_closed_disp
OH_annulus_vol_12_25_in = cfg.OH_12_25_in - cfg.string_closed_disp
OH_annulus_vol_8_5_in = cfg.OH_8_5_in - cfg.string_closed_disp

# --- Bottoms Up Calculations ---
bottoms_up_17_5_in = (
    riser_annulus_vol +
    OH_annulus_vol_17_5_in * (cfg.intermediate_casing_depth - surface_casing_depth) +
    casing_annulus_vol_20_in * (surface_casing_depth - water_depth)
)

bottoms_up_12_25_in = (
    riser_annulus_vol +
    OH_annulus_vol_12_25_in * (cfg.production_casing_depth - cfg.intermediate_casing_depth) +
    casing_annulus_vol_13_3_8_in * (cfg.intermediate_casing_depth - water_depth)
)

bottoms_up_8_5_in = (
    riser_annulus_vol +
    OH_annulus_vol_8_5_in * (cfg.well_td - cfg.production_casing_depth) +
    casing_annulus_vol_9_5_8_in * (cfg.production_casing_depth - water_depth)
)

# --- Well Parameters Dictionary ---
well_parameters = {
    "previous_well_water_depth": cfg.previous_well_water_depth,
    "water_depth": water_depth,
    "riser_jts_previous_well": riser_jts_previous_well,
    "riser_joints": riser_jts,
    "sailing_distance": cfg.sailing,
    "surface_casing_bml": cfg.surface_casing_bml,
    "conductor_casing_bml": cfg.conductor_casing_bml,
    "surface_casing_depth": surface_casing_depth,
    "intermediate_casing_depth": cfg.intermediate_casing_depth,
    "production_casing_depth": cfg.production_casing_depth,
    "well_td": cfg.well_td,
    "logging_days_intermediate": cfg.logging_days_intermediate,
    "logging_days_production": cfg.logging_days_production,
    "logging_days_liner": cfg.logging_days_liner,
    "bottoms_up_17_5_in": bottoms_up_17_5_in,
    "bottoms_up_12_25_in": bottoms_up_12_25_in,
    "bottoms_up_8_5_in": bottoms_up_8_5_in,
    "pipe_od_in": cfg.pipe_od_in,
    "string_capacity": cfg.string_capacity,
    "jetting_conductor": cfg.jetting_conductor,
    "pilot_hole": cfg.pilot_hole,
    "intermediate_section_cores": intermediate_section_cores,
    "production_section_cores": production_section_cores,
    "liner_section_cores": liner_section_cores,
    "include_intermediate_casing": cfg.include_intermediate_casing,
    "include_liner_casing": cfg.include_liner_casing,
}

