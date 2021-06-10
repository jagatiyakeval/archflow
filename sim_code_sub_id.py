import json
from pprint import pprint
from itertools import combinations, combinations_with_replacement, permutations

with open("_sim_code_dict.json", 'r') as annotation_file:
    sim_code_data = json.load(annotation_file)

sub_id_dict = dict(map(reversed, sim_code_data.items()))

# pprint(sub_id_dict)

perm_list = list(sub_id_dict.keys())
perm = permutations(perm_list, 2)
perm_dict = []
for p in list(perm):
    # print(f'permutations : {p[0]} --> {p[1]}')
    perm_dict.append((p[0],p[1]))

pprint(perm_dict)


_perm_lst = [('livingroom_1', 'bedroom_1a'),
 ('livingroom_1', 'bedroom_1b'),   
 ('livingroom_1', 'toilets_1'),    
 ('livingroom_1', 'serventroom_1'),
 ('livingroom_1', 'balcony_1'),    
 ('livingroom_1', 'kitchen_1'),    
 ('livingroom_1', 'store_1'),      
 ('livingroom_1', 'entry_1'),      
 ('livingroom_1', 'veranda_1'),    
 ('livingroom_1', 'dining_1'),     
 ('livingroom_1', 'study_1'),      
 ('bedroom_1a', 'livingroom_1'),
 ('bedroom_1a', 'bedroom_1b'),
 ('bedroom_1a', 'toilets_1'),
 ('bedroom_1a', 'serventroom_1'),
 ('bedroom_1a', 'balcony_1'),
 ('bedroom_1a', 'kitchen_1'),
 ('bedroom_1a', 'store_1'),
 ('bedroom_1a', 'entry_1'),
 ('bedroom_1a', 'veranda_1'),
 ('bedroom_1a', 'dining_1'),
 ('bedroom_1a', 'study_1'),
 ('bedroom_1b', 'livingroom_1'),
 ('bedroom_1b', 'bedroom_1a'),
 ('bedroom_1b', 'toilets_1'),
 ('bedroom_1b', 'serventroom_1'),
 ('bedroom_1b', 'balcony_1'),
 ('bedroom_1b', 'kitchen_1'),
 ('bedroom_1b', 'store_1'),
 ('bedroom_1b', 'entry_1'),
 ('bedroom_1b', 'veranda_1'),
 ('bedroom_1b', 'dining_1'),
 ('bedroom_1b', 'study_1'),
 ('toilets_1', 'livingroom_1'),
 ('toilets_1', 'bedroom_1a'),
 ('toilets_1', 'bedroom_1b'),
 ('toilets_1', 'serventroom_1'),
 ('toilets_1', 'balcony_1'),
 ('toilets_1', 'kitchen_1'),
 ('toilets_1', 'store_1'),
 ('toilets_1', 'entry_1'),
 ('toilets_1', 'veranda_1'),
 ('toilets_1', 'dining_1'),
 ('toilets_1', 'study_1'),
 ('serventroom_1', 'kitchen_1'),
 ('serventroom_1', 'entry_1'),
 ('serventroom_1', 'veranda_1'),
 ('serventroom_1', 'dining_1'),
 ('balcony_1', 'livingroom_1'),
 ('balcony_1', 'bedroom_1a'),
 ('balcony_1', 'bedroom_1b'),
 ('balcony_1', 'toilets_1'),
 ('balcony_1', 'serventroom_1'),
 ('balcony_1', 'kitchen_1'),
 ('balcony_1', 'store_1'),
 ('balcony_1', 'entry_1'),
 ('balcony_1', 'veranda_1'),
 ('balcony_1', 'dining_1'),
 ('balcony_1', 'study_1'),
 ('kitchen_1', 'livingroom_1'),
 ('kitchen_1', 'bedroom_1a'),
 ('kitchen_1', 'bedroom_1b'),
 ('kitchen_1', 'toilets_1'),
 ('kitchen_1', 'serventroom_1'),
 ('kitchen_1', 'balcony_1'),
 ('kitchen_1', 'store_1'),
 ('kitchen_1', 'entry_1'),
 ('kitchen_1', 'veranda_1'),
 ('kitchen_1', 'dining_1'),
 ('kitchen_1', 'study_1'),
 ('entry_1', 'livingroom_1'),
 ('entry_1', 'bedroom_1a'),
 ('entry_1', 'bedroom_1b'),
 ('entry_1', 'toilets_1'),
 ('entry_1', 'serventroom_1'),
 ('entry_1', 'balcony_1'),
 ('entry_1', 'kitchen_1'),
 ('entry_1', 'store_1'),
 ('entry_1', 'veranda_1'),
 ('entry_1', 'dining_1'),
 ('entry_1', 'study_1'),
 ('study_1', 'livingroom_1'),
 ('study_1', 'bedroom_1a'),
 ('study_1', 'bedroom_1b'),
 ('study_1', 'toilets_1'),
 ('study_1', 'serventroom_1'),
 ('study_1', 'balcony_1'),
 ('study_1', 'kitchen_1'),
 ('study_1', 'store_1'),
 ('study_1', 'entry_1'),
 ('study_1', 'veranda_1'),
 ('study_1', 'dining_1'),
 ('livingroom_2', 'bedroom_2b'),
 ('livingroom_2', 'bedroom_2a'),
 ('livingroom_2', 'toilets_2'),
 ('livingroom_2', 'serventroom_2'),
 ('livingroom_2', 'balcony_2'),
 ('livingroom_2', 'kitchen_2'),
 ('livingroom_2', 'store_2'),
 ('livingroom_2', 'entry_2'),
 ('livingroom_2', 'veranda_2'),
 ('livingroom_2', 'dining_2'),
 ('livingroom_2', 'study_2'),
 ('bedroom_2b', 'livingroom_2'),
 ('bedroom_2b', 'bedroom_2a'),
 ('bedroom_2b', 'toilets_2'),
 ('bedroom_2b', 'serventroom_2'),
 ('bedroom_2b', 'balcony_2'),
 ('bedroom_2b', 'kitchen_2'),
 ('bedroom_2b', 'store_2'),
 ('bedroom_2b', 'entry_2'),
 ('bedroom_2b', 'veranda_2'),
 ('bedroom_2b', 'dining_2'),
 ('bedroom_2b', 'study_2'),
 ('bedroom_2a', 'livingroom_2'),
 ('bedroom_2a', 'bedroom_2b'),
 ('bedroom_2a', 'toilets_2'),
 ('bedroom_2a', 'serventroom_2'),
 ('bedroom_2a', 'balcony_2'),
 ('bedroom_2a', 'kitchen_2'),
 ('bedroom_2a', 'store_2'),
 ('bedroom_2a', 'entry_2'),
 ('bedroom_2a', 'veranda_2'),
 ('bedroom_2a', 'dining_2'),
 ('bedroom_2a', 'study_2'),
 ('toilets_2', 'livingroom_2'),
 ('toilets_2', 'bedroom_2b'),
 ('toilets_2', 'bedroom_2a'),
 ('toilets_2', 'serventroom_2'),
 ('toilets_2', 'balcony_2'),
 ('toilets_2', 'kitchen_2'),
 ('toilets_2', 'store_2'),
 ('toilets_2', 'entry_2'),
 ('toilets_2', 'veranda_2'),
 ('toilets_2', 'dining_2'),
 ('toilets_2', 'study_2'),
 ('serventroom_2', 'kitchen_2'),
 ('serventroom_2', 'store_2'),
 ('serventroom_2', 'entry_2'),
 ('serventroom_2', 'veranda_2'),
 ('serventroom_2', 'dining_2'),
 ('serventroom_2', 'study_2'),
 ('balcony_2', 'livingroom_2'),
 ('balcony_2', 'bedroom_2b'),
 ('balcony_2', 'bedroom_2a'),
 ('balcony_2', 'toilets_2'),
 ('balcony_2', 'serventroom_2'),
 ('balcony_2', 'kitchen_2'),
 ('balcony_2', 'store_2'),
 ('balcony_2', 'entry_2'),
 ('balcony_2', 'veranda_2'),
 ('balcony_2', 'dining_2'),
 ('balcony_2', 'study_2'),
 ('kitchen_2', 'livingroom_2'),
 ('kitchen_2', 'bedroom_2b'),
 ('kitchen_2', 'bedroom_2a'),
 ('kitchen_2', 'toilets_2'),
 ('kitchen_2', 'serventroom_2'),
 ('kitchen_2', 'balcony_2'),
 ('kitchen_2', 'store_2'),
 ('kitchen_2', 'entry_2'),
 ('kitchen_2', 'veranda_2'),
 ('kitchen_2', 'dining_2'),
 ('kitchen_2', 'study_2'),
 ('entry_2', 'livingroom_2'),
 ('entry_2', 'bedroom_2b'),
 ('entry_2', 'bedroom_2a'),
 ('entry_2', 'toilets_2'),
 ('entry_2', 'serventroom_2'),
 ('entry_2', 'balcony_2'),
 ('entry_2', 'kitchen_2'),
 ('entry_2', 'store_2'),
 ('entry_2', 'veranda_2'),
 ('entry_2', 'dining_2'),
 ('entry_2', 'study_2'),
 ('study_2', 'balcony_2'),
 ('study_2', 'kitchen_2'),
 ('study_2', 'store_2'),
 ('study_2', 'entry_2'),
 ('study_2', 'veranda_2'),
 ('study_2', 'dining_2'),
 ('livingroom_3', 'bedroom_3b'),
 ('livingroom_3', 'bedroom_3a'),   
 ('livingroom_3', 'toilets_3'),    
 ('livingroom_3', 'serventroom_3'),
 ('livingroom_3', 'balcony_3'),    
 ('livingroom_3', 'kitchen_3'),    
 ('livingroom_3', 'store_3'),      
 ('livingroom_3', 'entry_3'),      
 ('livingroom_3', 'veranda_3'),    
 ('livingroom_3', 'dining_3'),     
 ('livingroom_3', 'study_3'),      
 ('bedroom_3b', 'livingroom_3'),   
 ('bedroom_3b', 'bedroom_3a'),     
 ('bedroom_3b', 'toilets_3'),      
 ('bedroom_3b', 'serventroom_3'),  
 ('bedroom_3b', 'balcony_3'),      
 ('bedroom_3b', 'kitchen_3'),      
 ('bedroom_3b', 'store_3'),        
 ('bedroom_3b', 'entry_3'),        
 ('bedroom_3b', 'veranda_3'),      
 ('bedroom_3b', 'dining_3'),       
 ('bedroom_3b', 'study_3'),
 ('bedroom_3a', 'livingroom_3'),
 ('bedroom_3a', 'bedroom_3b'),
 ('bedroom_3a', 'toilets_3'),
 ('bedroom_3a', 'serventroom_3'),
 ('bedroom_3a', 'balcony_3'),
 ('bedroom_3a', 'kitchen_3'),
 ('bedroom_3a', 'store_3'),
 ('bedroom_3a', 'entry_3'),
 ('bedroom_3a', 'veranda_3'),
 ('bedroom_3a', 'dining_3'),
 ('bedroom_3a', 'study_3'),
 ('toilets_3', 'livingroom_3'),
 ('toilets_3', 'bedroom_3b'),
 ('toilets_3', 'bedroom_3a'),
 ('toilets_3', 'serventroom_3'),
 ('toilets_3', 'balcony_3'),
 ('toilets_3', 'kitchen_3'),
 ('toilets_3', 'store_3'),
 ('toilets_3', 'entry_3'),
 ('toilets_3', 'veranda_3'),
 ('toilets_3', 'dining_3'),
 ('toilets_3', 'study_3'),
 ('serventroom_3', 'kitchen_3'),
 ('serventroom_3', 'store_3'),
 ('serventroom_3', 'entry_3'),
 ('serventroom_3', 'veranda_3'),
 ('serventroom_3', 'dining_3'),
 ('kitchen_3', 'livingroom_3'),
 ('kitchen_3', 'bedroom_3b'),
 ('kitchen_3', 'bedroom_3a'),
 ('kitchen_3', 'toilets_3'),
 ('kitchen_3', 'serventroom_3'),
 ('kitchen_3', 'balcony_3'),
 ('kitchen_3', 'store_3'),
 ('kitchen_3', 'entry_3'),
 ('kitchen_3', 'veranda_3'),
 ('kitchen_3', 'dining_3'),
 ('kitchen_3', 'study_3'),
 ('entry_3', 'livingroom_3'),
 ('entry_3', 'bedroom_3b'),
 ('entry_3', 'bedroom_3a'),
 ('entry_3', 'toilets_3'),
 ('entry_3', 'serventroom_3'),
 ('entry_3', 'balcony_3'),
 ('entry_3', 'kitchen_3'),
 ('entry_3', 'store_3'),
 ('entry_3', 'veranda_3'),
 ('entry_3', 'dining_3'),
 ('entry_3', 'study_3'),
 ('study_3', 'livingroom_3'),
 ('study_3', 'bedroom_3b'),
 ('study_3', 'bedroom_3a'),
 ('study_3', 'toilets_3'),
 ('study_3', 'serventroom_3'),
 ('study_3', 'balcony_3'),
 ('study_3', 'kitchen_3'),
 ('study_3', 'store_3'),
 ('study_3', 'entry_3'),
 ('study_3', 'veranda_3'),
 ('study_3', 'dining_3'),
 ('entry_4', 'entry_5'),
 ('entry_4', 'entry_6'),
 ('entry_4', 'stair'),
 ('entry_4', 'lobby'),
 ('entry_5', 'entry_4'),
 ('entry_5', 'entry_6'),
 ('entry_5', 'stair'),
 ('entry_5', 'lobby'),
 ('entry_6', 'entry_4'),
 ('entry_6', 'entry_5'),
 ('entry_6', 'stair'),
 ('entry_6', 'lobby'),
 ('stair', 'entry_4'),
 ('stair', 'entry_5'),
 ('stair', 'entry_6'),
 ('stair', 'lobby'),
 ('lobby', 'entry_4'),
 ('lobby', 'entry_5'),
 ('lobby', 'entry_6'),
 ('lobby', 'stair')
 ]