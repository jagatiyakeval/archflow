from itertools import permutations
import common_utils as cmnutils #type:ignore
from pprint import pprint

#TODO adjcency logic is missing FIXIT

def get_pairs_from_point_dict(id_point_dict):
    ids_center_dict = {}
    ids_lst = []
    for ids,points in id_point_dict.items():
        ids_center = cmnutils.get_center_of_poly(points)
        ids_lst.append(ids)
        ids_center_dict.update({ids:ids_center})
    perm_of_ids_list = list(permutations(ids_lst, 2)) 
    pairs_per_ids_center = []
    for perm in  perm_of_ids_list:
        perm_indx = perm_of_ids_list.index(perm)
        pairs_per_ids_center.append({f'pair_{perm_indx}':{perm[0]:ids_center_dict[perm[0]],perm[1]:ids_center_dict[perm[1]]}})
    ids_lst.clear()
    ids_center_dict.clear()
    return pairs_per_ids_center