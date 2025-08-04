import math
from config import string_closed_disp, water_depth, string_capacity, riser_annulus_vol


def hole_volume_bbl_per_m(diameter_in_inches):
    diameter_m = diameter_in_inches * 0.0254
    volume_m3_per_m = math.pi * (diameter_m / 2) ** 2
    volume_bbl_per_m = volume_m3_per_m / 0.158987294928
    return volume_bbl_per_m
def minimum_flow_rate_bpm(hole_diameter_in, pipe_od_in, v_ft_min=150):
    #v_ft_min = 150  # Using a constant value for minimum velocity
    annular_area_in2 = (math.pi / 4) * (hole_diameter_in**2 - pipe_od_in**2)
    flow_rate_bpm = ((v_ft_min * annular_area_in2) / 1029)  # Convert bbl/min to GPM (1 bbl = 42 gallons)
    return flow_rate_bpm

def minimum_flow_rate_bph(hole_diameter_in, pipe_od_in, v_ft_min=150):
    flow_rate_bph = minimum_flow_rate_bpm(hole_diameter_in, pipe_od_in, v_ft_min)*60    
    return flow_rate_bph
def wiper_trip(bit_depth, shoe_depth, hole_size, string_closed_disp, water_depth, string_capacity, riser_annulus_vol, activity_rates):
    if hole_size >= 20:
        circulation_volume = ((hole_volume_bbl_per_m(hole_size) - string_closed_disp) * (bit_depth - water_depth) + string_capacity * bit_depth) * 2
        circulation_time = (circulation_volume / (1000 / 42)) / 60  # Assuming pipe OD is 5.5 inches
    else:
        circulation_volume = riser_annulus_vol + (hole_volume_bbl_per_m(hole_size) - string_closed_disp) * (bit_depth - water_depth)
        circulation_time = (circulation_volume / minimum_flow_rate_bpm(hole_size, 5.5)) / 60  # Assuming pipe OD is 5.5 inches

    print(minimum_flow_rate_bpm(hole_size, 5.5))
    print(f"Circulation volume: {circulation_volume:.2f} bbl")
    print(f"Circulation time: {circulation_time:.2f} hours")

    tripping_time = (bit_depth - shoe_depth) * 2 / activity_rates['Tripping_OH']  # Assuming a tripping speed of 30 m/hr
    print(f"Tripping time: {tripping_time:.2f} hours")

    return 1/(circulation_time + tripping_time)

    
def wiper_trip_riserless(bit_depth, shoe_depth, hole_size, string_closed_disp, water_depth, string_capacity, activity_rates):
    circulation_volume = ((hole_volume_bbl_per_m(hole_size) - string_closed_disp) * (bit_depth - water_depth) + string_capacity * bit_depth) * 2
    if hole_size >= 20:
        circulation_time = (circulation_volume / (1000 / 42)) / 60  # Assuming pipe OD is 5.5 inches
    else:
        circulation_time = (circulation_volume / minimum_flow_rate_bpm(hole_size, 5.5)) / 60  # Assuming pipe OD is 5.5 inches
    print(minimum_flow_rate_bpm(hole_size, 5.5))
    print(f"Circulation volume: {circulation_volume:.2f} bbl")
    print(f"Circulation time: {circulation_time:.2f} hours")
    tripping_time = (bit_depth - shoe_depth) * 2 / activity_rates['Tripping_OH']  # Assuming a tripping speed of 30 m/hr
    print(f"Tripping time: {tripping_time:.2f} hours")
    return 1/(circulation_time + tripping_time)
def round_trip(bit_depth, shoe_depth, hole_size, string_closed_disp, water_depth, string_capacity, riser_annulus_vol, activity_rates):
    tripping_time_above_shoe = shoe_depth*2 / activity_rates['Tripping'] 
    print(f"Tripping time above shoe: {tripping_time_above_shoe:.2f} hours")
    wiper_trip_time = wiper_trip(bit_depth, shoe_depth, hole_size, string_closed_disp, water_depth, string_capacity, riser_annulus_vol, activity_rates)  
    print(f"Wiper trip time: {wiper_trip_time:.2f} hours")    
    return 1/(tripping_time_above_shoe + wiper_trip_time)
def run_and_retrieve_WB(activity_rates, water_depth):
    bha_make_up_time = activity_rates['M_up_WBRRT_Jet_Sub_BHA']
    tripping_time = 2*water_depth / activity_rates['Tripping']
    set_or_retrieve_time_WB = activity_rates['Jet_WH_Install_WB_Release_WBRRT']
    return 1/(bha_make_up_time + tripping_time + set_or_retrieve_time_WB)
def coring_time(bit_depth, shoe_depth, hole_size, bottoms_up_12_25_in, activity_rates, pipe_od_in, core_no = 1, core_length = 9):
    ''' Circulate (assume to cut one core there is two times circulation for bottoms up)
    Pull out Drilling BHA
    RIH Coring BHA
    Cut Core
    POOH Coring BHA
    RIH Drilling BHA
    '''
    circulation_time = (bottoms_up_12_25_in / minimum_flow_rate_bpm(12.25, pipe_od_in))/60 #Circulate Bottoms Up one extra time for cutting core
    roundtrip_for_BHA = 1/round_trip(bit_depth, shoe_depth, hole_size, string_closed_disp, water_depth, string_capacity, riser_annulus_vol, activity_rates)  # Assuming this function handles the tripping and wiper trip
    if core_no > 1:
        coring_bha_make_up_time = activity_rates['BHA_Make_Up_Coring_Subsequent'] # Assuming make-up time is the same for each core
    else:
        coring_bha_make_up_time = activity_rates['BHA_Make_Up_Coring']
    trip_in_coring_bha = bit_depth / activity_rates['Tripping']  
    trip_out_coring_bha = bit_depth / activity_rates['Tripping_Coring']  
    coring_time = core_length / activity_rates['Cut_Core']
    coring_trip_total_time = coring_bha_make_up_time + trip_in_coring_bha + coring_time + trip_out_coring_bha
    print(f"Circulation time: {circulation_time:.2f} hours")
    print(f"Roundtrip for BHA: {roundtrip_for_BHA:.2f} hours")
    print(f"Coring time: {coring_time:.2f} hours")      
    print(f"Coring trip total time: {coring_trip_total_time:.2f} hours")
    print(f"coring bha make up time: {coring_bha_make_up_time:.2f} hours")
    coring_time_1 = circulation_time + roundtrip_for_BHA + coring_trip_total_time
    print(f"Coring_time: {coring_time_1: .2f} hours")

    return 1/(circulation_time + roundtrip_for_BHA + coring_trip_total_time)
#from config import *
#from data_loaders import activity_rates
#coring_time(3900, 3200, 12.25, bottoms_up_12_25_in, activity_rates, pipe_od_in, core_no=1, core_length=9)

