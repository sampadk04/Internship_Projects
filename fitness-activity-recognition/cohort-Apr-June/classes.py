#### NEW CLASSES HERE ####

# Excersices can be broadly categorized as: https://www.livestrong.com/article/534321-five-types-of-fitness-training/
## High intensity/speed
aerobic = ['jump_rope','jumping_jacks','dancing','jumping', 'x_jumps', 'running', 'all_fours_warm_up',
  'skii_hops','squat_jumps', 'lateral_squad_jumps','lateral_squat_jumps','lateral_shuffle','walking']

coordination_agility = ['agility_feet', 'run_in_place','standing_skips','high_knees', 
  'mountain_climbers','mountain_climber','boxing','high_knee_sprints','high_knee_sprint', 
  'burpy_crawl_combo','burpy', 'pace_skips', 'criss_cross','cross_crunches','surfer_hops',
  'split_hop','lower_knee_hop','torso_up_double_leg_extension'] # Could also fit in as a subclass of aerobic activities
# Could maybe also fit in with calisthenics?: 'burpy_crawl_combo','burpy'

## NOTE: Uncomment if combining coordination_agility with aerobic
# [aerobic.append(item) for item in coordination_agility]

## Medium intensity/speed and lifting 
# each below are subtypes of strength training (can use uniquely or put under strength training)
weight_bearing = ['bodyweight_squats','lateral_lunges','lunges','squats','body_weight_squats',
  'lateral_squat_walk_reverse_lundge','squat_hold_reverse_lundge','lateral_squat_walk_reverse_lundge',
  'body_weight_squat_toes','drop_squats']

# non_wieght_bearing = ['torso_up_double_leg_extension', 'hamstring_curl_right','hamstring_curl_left'] # (aka prone strength training)

calisthenics = ['knees_to_elbow', 'loaded_beast_push_up','modified_push_ups','crunches','pushups',
   'pullups','wall_pushups','pulse_ups_right','pulse_ups_left','straight_left_leg_pulse'] # (bodyweight excersizes)

weightlifting = ['bench_press','triceps','donkey_press','front_press','front_up_pulse']

## NOTE: Uncomment below if combining above classes into single strength training class
# comb_list =[weight_bearing, non_wieght_bearing, calisthenics, weightlifting]
# strength_training = [item for sublist in comb_list for item in sublist] # flat strength training list if single class preferred.

##### Lower intensity/speed (flexibility, stability) ######
balance_stability = ['bear_hold_knee_taps','bear_hold_shoulder_taps','bear_hold',
  'fullbody_walkouts', 'lay_down_knees_up', 'lay_down_one_knee_up','lay_down_knee_up_down',
  'lay_down_knee_swing_shoulder_blades_up','fire_hydrants','roll_up','alternating_deadbug',
  'single_bent_leg_lower','double_bent_leg_lower', 'double_leg_extension', 'upper_body_up_criss_cross',
  'bear_hold_taps','bear_crawl','forward_plank','left_side_plank','right_side_plank','arm_plank',
  'modified_arm_plank','left_side_plank_reaching','right_side_plank_reaching','kickbacks_right_glute',
  'straight_right_leg_pulse','kickbacks_left_glute','hip_bridge','forearm_plank','high_plank',
  'high_plank_right_leg_press','push_hip_up_right_leg','push_hip_up_left_leg','high_plank_shoulder_feet_combo',
  'straight_leg_lifts','push_hip_up_right_leg_up','hip_up_right_swing_down','push_hip_up_left_leg_up','hip_up_left_swing_down',
  'high_plank_left_leg_press','reverse_dog_crunch', 'all_fours_drive','forearm_plank_rocking','upper_body_up_double_leg_extension',
  'front_laying_leg_lifts','front_laying_arms_legs_lifts','plank_dynamic','plank_static','side_plank_dynamic','plank', 'hamstring_curl_right','hamstring_curl_left']
# Could fit in elsewhere also (calisthenics): alternating_deadbug, fire_hydrants, kickbacks_right_glute, 

flexibility = ['yoga,stretching','streching','yoga,','yoga,ground','yoga,all_four','yoga,standing'
  'strech','stretching', 'down_dog','up_dog','runners_lundge_reach','table_top','all_fours',
   'knees_to_chest','cat_cow','all_fours_elbow_spine_stretch','up_down_dog']
# Could be further split into dynamic and static stretches

idle = ['idle','all_fours_idle','standing','standing,talking','talking,walking','talking','standing_idle','standing_writing','walking_idle','kneeling_idle','table_top_position_idle','sitting','sitting_idle' 'laying_flat','laying_down_idle','laydown_faceup','laying_down_face_up','front_laying_position','laying_down_flat','laydown_face_up','laydown_flat','front_laying_idle', 'hanging']
doubt = ['transition','glutes','shuffle_position', 'adjusting','pointing']
remove = ['slides', 'off_screen', 'slide', 'pointing', 'offscreen','intro_page']