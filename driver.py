from config import *
from rrt import rrt
import rrt as module_rrt
import drawing
import utils
from time import sleep,time
import pygame as pg
# import driver
import utils
import json
from time import sleep,time
from itertools import combinations, combinations_with_replacement, permutations
from pprint import pprint
import sim_code_sub_id as sim_sub_id
import os

os.environ["SDL_VIDEODRIVER"] = "dummy"

# drawing.recorder = False

def drive(_start_pos, _goal_pos, _permute_name, reg_lst, path_line_clr, RUN_FLG):

    pg.init()
    # programIcon = pg.image.load(ICON_FILE)
    pg.display.set_caption(f"The main window {_permute_name}")
    # pg.display.set_icon(programIcon)
    drawing.screen = pg.display.set_mode((WIDTH, HEIGHT))
    drawing.render_region_on_obs_surf(drawing.obstaclesSurface, reg_lst)
    drawing.goalPos = _goal_pos
    drawing.startPos = _start_pos

    module_rrt.RENDER_RRT_EDGE = False
    
    while RUN_FLG:
        
        drawing.clearEdgesPool()
        tree = rrt(drawing.startPos, drawing.goalPos, drawing.obstaclesSurface)
        if tree:  # A path was found:
            drawing.drawPath(tree, path_line_clr)
        drawing.update()
        sleep(3)
        RUN_FLG = False
    # drawing.clearTree()
    retun_str = f'permute_name:{_permute_name},frame_counter:{drawing.frame_counter},frame_tracker:{drawing.frame_tracker}'
    return drawing.master_pts_lst


master_data_logger = {}

sub_id_dict = sim_sub_id.sub_id_dict
_perm_lst = sim_sub_id._perm_lst

circulation_file = "_circulation.json"
connectivity_file = "_connectivity.json"

def file_writter(file_data):
    with open("master_data_logger.json", "w") as outfile:
        json.dump(file_data, outfile)

# def json_accum_point():
with open(connectivity_file, 'r') as annotation_file:
    json_file_data = json.load(annotation_file)

# print(json_file_data)

mast_lst = []
for id, seg in json_file_data.items():
    tmp_lst = []
    for elem in seg:
        tmp_lst.append((elem[0], elem[1]))
    mast_lst.append(tmp_lst)
# pprint(mast_lst)

with open(circulation_file, 'r') as _annotation_file:
    json_file_data_all = json.load(_annotation_file)

# print(json_file_data_all)

cntr_lst = []
cntr_lst_dict = {}
for ids, segs in json_file_data_all.items():    
    poly_lst = []
    sub_ids = int(ids.split("_")[1])
    # print(ids, sub_ids)
    for elem in segs:
        poly_lst.append((elem[0], elem[1]))
    center = utils.get_center_of_poly(poly_lst)

    for vals in sub_id_dict:        
        if sub_id_dict[vals] == str(sub_ids):
            # print(sub_id_dict[vals], sub_ids)
            x_crd = center[0]
            y_crd = center[1]
            cntr_lst_dict.update({vals:(x_crd, y_crd)})
            # print(ids,ids.split("_")[1],(x_crd, y_crd))

# pprint(cntr_lst_dict)

final_pem_pairs = []
for _pem_pers in _perm_lst:
    # print(cntr_lst_dict[_pem_pers[0]], cntr_lst_dict[_pem_pers[1]])
    _tmp_lst = []
    for el in _pem_pers:
        _tmp_lst.append(cntr_lst_dict[el])
    final_pem_pairs.append(_tmp_lst)

reg_lst = mast_lst
pairs_list = final_pem_pairs

no_of_hopes = 1
for pairs in pairs_list:
    grp_path_line_clr = utils.get_random_color()
    idx = pairs_list.index(pairs)
    get_pair = _perm_lst[idx]
    stpr = pairs[0]
    endpr = pairs[1]

    stpr_x = stpr[0]
    stpr_y = stpr[1]
    endpr_x = endpr[0]
    endpr_y = endpr[1]
    
    # if get_pair[0] == "stairs" or get_pair[0] == "lift":
    # if get_pair[0].split("_")[0] == "entry" or get_pair[1].split("_")[0] == "entry":
    # if get_pair[0].split("_")[0] == "entry":        
    #     if get_pair[0].split("_")[-1] == "T":
    #         stpr_y += 30
    #     else:  
    #         stpr_y -= 30          

    # if get_pair[1].split("_")[0] == "entry":
    #     if get_pair[1].split("_")[-1] == "T":
    #         endpr_y += 30
    #     else:
    #         endpr_y -= 30

    endpr = tuple([endpr_x, endpr_y])
    stpr = tuple([stpr_x, stpr_y])  

    for i in range(no_of_hopes):
        tic = time() 
        _response_ =""       
        print(f'perm_{idx}_{i}_{get_pair[0]}-->{get_pair[1]}')
        print(f'original points : {pairs} | new points : {stpr, endpr}')                
        _response_ = drive(stpr, endpr, f'perm_{idx}_{i}_{get_pair[0]}-->{get_pair[1]}', reg_lst, grp_path_line_clr, True)
        toc = time()-tic
        sleep(0.01)
        master_data_logger.update({f'{get_pair[0]}-->{get_pair[1]}':_response_})    
        print(master_data_logger)

file_writter(master_data_logger)

