import streamlit as st
import pandas as pd
import math

from config import *

##from config import previous_well_water_depth, water_depth, surface_casing_bml, conductor_casing_bml, string_capacity, jetting_conductor
from data_loaders import activity_rates
from well_plan_builder import build_well_plan

st.set_page_config(page_title="Subsea Well Plan", layout="wide")

st.title("📅 Subsea Well Drilling Plan Dashboard")

# Sidebar Inputs
st.sidebar.header("Well Parameters")

# Sidebar Inputs for parameters you want user to modify
previous_well_water_depth_input = st.sidebar.number_input("Previous Well Water Depth (m)", value=well_parameters['previous_well_water_depth'])
water_depth_input = st.sidebar.number_input("Water Depth (m)", value=well_parameters['water_depth'])

surface_casing_bml_input = st.sidebar.number_input("Surface Casing BML (m)", value=well_parameters['surface_casing_bml'])
logging_days_intermediate_input = st.sidebar.number_input("Logging Days Intermediate Casing", value=well_parameters['logging_days_intermediate'])
logging_days_production_input = st.sidebar.number_input("Logging Days Production Casing", value=well_parameters['logging_days_production'])
logging_days_liner_input = st.sidebar.number_input("Logging Days Liner Casing", value=well_parameters['logging_days_liner'])

#intermediate_casing_depth_input = st.sidebar.number_input("Intermediate Casing Depth (m)", value=well_parameters['intermediate_casing_depth'])

#well_td_input = st.sidebar.number_input("Target Depth (m)", value=well_parameters['well_td'])
jetting_conductor_input = st.sidebar.checkbox("Jetting Conductor", value=well_parameters['jetting_conductor'])
pilot_hole_input = st.sidebar.checkbox("Pilot Hole prior to 17-1/2'' Hole", value=well_parameters['pilot_hole'])

st.sidebar.header("Select Sections to Include")
include_intermediate_casing = st.sidebar.checkbox("Include Intermediate Casing", value=True)
include_liner_casing = st.sidebar.checkbox("Include Liner Casing", value=True)

if include_intermediate_casing:
    intermediate_casing_depth_input = st.sidebar.number_input("Intermediate Casing Depth (m)", value=well_parameters['intermediate_casing_depth'], key = 'intermediate_casing_depth_input')
else:
    intermediate_casing_depth_input = well_parameters['surface_casing_depth']  # Mark as None when section is skipped

if include_liner_casing:
    production_casing_depth_input = st.sidebar.number_input("Production Casing Depth", value=well_parameters['production_casing_depth'], key='production_casing_depth_input')
    well_td_input = st.sidebar.number_input("Well Target Depth", value=well_parameters['well_td'], key='well_td_input')
else:
    well_td_input = st.sidebar.number_input("Well Target Depth", value=well_parameters['well_td'], key='well_td_input_no_liner')
    production_casing_depth_input=well_td_input


# Initialize Coring Depths in Session State
if 'coring_depths' not in st.session_state:
    st.session_state.coring_depths = [well_td-200]  # Default values
st.sidebar.header("Coring Depths Configuration")
# Buttons to Add/Remove Depths
add_depth = st.sidebar.button("➕ Add Coring Depth")
remove_depth = st.sidebar.button("➖ Remove Last Depth")
# Handle Button Clicks
if add_depth:
    st.session_state.coring_depths.append(st.session_state.coring_depths[-1] + 100 if st.session_state.coring_depths else 2900)
if remove_depth and st.session_state.coring_depths:
    st.session_state.coring_depths.pop()

# Render Inputs for Each Coring Depth
updated_depths = []
for idx, depth in enumerate(st.session_state.coring_depths):
    new_depth = st.sidebar.number_input(f"Coring Depth {idx+1} (m)", value=depth, key=f'core_depth_{idx}')
    updated_depths.append(new_depth)

# Update Session State
st.session_state.coring_depths = updated_depths
# Display Current Coring Depths List
st.sidebar.write("Current Coring Depths:", st.session_state.coring_depths)
# Update well_parameters with this list
coring_depths_input = st.session_state.coring_depths

intermediate_section_cores_input = [depth for depth in coring_depths_input if  surface_casing_depth < depth <= intermediate_casing_depth]
production_section_cores_input = [depth for depth in coring_depths_input if intermediate_casing_depth < depth <= production_casing_depth]
liner_section_cores_input = [depth for depth in coring_depths_input if production_casing_depth < depth <= well_td]



st.sidebar.header("Activity Rates Adjustment")
adjust_activity_rates = {}
for activity, rate in activity_rates.items():
    adjust_activity_rates[activity] = st.sidebar.number_input(f"{activity}", value=rate)

# Build Plan Button
if st.button("Generate Well Plan"):
    # Update Parameters

    well_parameters.update({
    'previous_well_water_depth': previous_well_water_depth_input,
    'water_depth': water_depth_input,
    'surface_casing_bml': surface_casing_bml_input,
    'intermediate_casing_depth': intermediate_casing_depth_input,
    'production_casing_depth': production_casing_depth_input,
    'well_td': well_td_input,
    'intermediate_section_cores': intermediate_section_cores_input,
    'production_section_cores': production_section_cores_input,
    'liner_section_cores':liner_section_cores_input, 
    'jetting_conductor': jetting_conductor_input,
    'pilot_hole': pilot_hole_input,
    'include_intermediate_casing': include_intermediate_casing,
    'include_liner_casing': include_liner_casing,
    'logging_days_intermediate': logging_days_intermediate_input,
    'logging_days_production': logging_days_production_input,
    'logging_days_liner': logging_days_liner_input
    })

    # Build Well Plan
    plan_phases = build_well_plan(well_parameters, adjust_activity_rates)

    # Build DataFrame from Plan
    from classes import DrillingOperation
    drilling_plan = DrillingOperation("Subsea Well", plan_phases)
    df_plan = drilling_plan.display_plan()

    st.success("Well Plan Generated Successfully!")

    st.dataframe(df_plan, use_container_width=True)

    st.metric("Total Estimated Time (Days)", f"{round(drilling_plan.total_time()/24, 2)} Days")

    # Download Plan
    csv = df_plan.to_csv(index=False).encode('utf-8')
    st.download_button("Download Plan CSV", csv, "Subsea_Well_Plan.csv", "text/csv")
