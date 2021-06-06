import os
import cv2
import copy
import time
import json
from pprint import pprint
import numpy as np
import streamlit as st
from PIL import ImageColor
# import coco_annotation_parser as annot_parse # type:ignore
import SessionState #type:ignore
import circulation_skeletonizer as circ_skeleton #type:ignore
import connectivity_sets as connect_set #type:ignore
import common_utils as cmnutils #type:ignore
import coco_json_generator as coco_json #type:ignore

EXPORT_FLAG = False
COLOR_CODE_RGB_JSON = "color_code_RGB.json"

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_title="Arch App",page_icon=":control_knobs:",layout="wide",initial_sidebar_state="auto")

with st.sidebar.beta_expander(label='Expand to import file or select folder', expanded=True):
    with st.form(key="_form_upload_annotation"):
        annotation_file = st.file_uploader("Import Annotation File", type=['json'], key='_file_uploader_json')
        dir_name_list = [dir for dir in os.listdir() if os.path.isdir(dir) and not (dir.startswith('.') or dir.startswith('__'))]
        dir_name_list.insert(0, "Select_Folder")
        annotated_image_dir = st.selectbox(label="Select Folder", options=dir_name_list, index=0)
        st.form_submit_button(label='Submit')

with st.sidebar.beta_expander(label="Runtime Debug Messages", expanded=True):
    rt_msg_form = st.form(key="rt_msg")
    rt_msg_form.form_submit_button(label='Refresh')

# @st.cache(suppress_st_warning=True)
def send_runtime_msg(msg='', msg_identifier='', msg_type='info', msg_ttl=1):
    msg_placeholder = rt_msg_form.empty()
    if msg_type == 'info':
        msg_placeholder.info(f'{msg}:{msg_identifier}')
    elif msg_type == 'warn':
        msg_placeholder.warning(f'{msg}:{msg_identifier}')
    elif msg_type == 'error':
        msg_placeholder.error(f'{msg}:{msg_identifier}')
    time.sleep(0.5)
    msg_placeholder.empty()

@st.cache(suppress_st_warning=True)
def get_categories_color_dict(categories_json_data):
    send_runtime_msg(msg='Caching:Cache Miss', msg_identifier='categories_color_dict', msg_type='info', msg_ttl=1)
    _categories_color_dict = {}
    for category_ in categories_json_data:
        hex_clr = category_['color']
        rgb_clr = ImageColor.getcolor(hex_clr, "RGB")
        bgr_clr = rgb_clr[::-1]
        _rgb_clr = list(rgb_clr)
        _bgr_clr = list(bgr_clr)
        _rgb_clr.append(255)
        _bgr_clr.append(255)
        rgba_clr = tuple(_rgb_clr)
        bgra_clr = tuple(_bgr_clr)
        clr_format_dict = {'HEX':hex_clr,'RGB':rgb_clr,'BGR':bgr_clr,'RGBA':rgba_clr,'BGRA':bgra_clr}
        _categories_color_dict.update({category_['name']:clr_format_dict})
    return _categories_color_dict

@st.cache(suppress_st_warning=True)
def get_file_json_data_info(_annotation_file):
    send_runtime_msg(msg='Cache Miss', msg_identifier='file_json_data_info', msg_type='info', msg_ttl=1)
    # with open(_annotation_file_name, 'r') as _annotation_file:
    # _annotation_file = json.load(_annotation_file)    
    # _annotation_json_file_info = _annotation_file.name #_annotation_file.__dict__
    _annotation_json_file_data = json.load(_annotation_file)
    return  _annotation_json_file_data#, _annotation_json_file_info

@st.cache(suppress_st_warning=True)
def init_annotation_data(_annotation_json_file_data):
    send_runtime_msg(msg='Cache Miss', msg_identifier='init_annotation_data', msg_type='info', msg_ttl=1)
    _images_json_data = _annotation_json_file_data['images']
    _categories_json_data = _annotation_json_file_data['categories']
    _annotations_json_data = _annotation_json_file_data['annotations']
    return _images_json_data, _categories_json_data, _annotations_json_data

@st.cache(suppress_st_warning=True)
def get_image_id_width_height(_images_json_data, _selected_image):
    send_runtime_msg(msg='Caching:Cache Miss', msg_identifier='image_id_width_height', msg_type='info', msg_ttl=1)
    id, width, height =  [(im_dict['id'],im_dict['width'],im_dict['height']) for im_dict in _images_json_data if im_dict['file_name'] == _selected_image][0]
    return id, width, height

# @st.cache(suppress_st_warning=True)
def get_id_poly_segmentation(annotations_json_data, selected_image_id, selected_categories, categories_id_name_dict):
    # send_runtime_msg(msg='Caching:Cache Miss', msg_identifier='id_poly_segmentation', msg_type='info', msg_ttl=1)
    annot_id_point_dict = {}
    for ant_dict in annotations_json_data:
        if ant_dict['image_id'] == selected_image_id: # to select img
            for cat in selected_categories:
                _id_name = categories_id_name_dict[ant_dict['category_id']]
                if _id_name == cat:
                    sub_id = ant_dict['id']
                    ant_dict_lst = ant_dict['segmentation']
                    for seg_lst in ant_dict_lst:
                        segment_data = seg_lst
                        x_coords = list(map(int, segment_data[::2]))
                        y_coords = list(map(int, segment_data[1::2]))
                        poly_coord = list(zip(x_coords, y_coords))
                        annot_id_point_dict.update({f'{_id_name}_{sub_id}_{ant_dict_lst.index(seg_lst)}':poly_coord})
    # pprint(annot_id_point_dict)
    return annot_id_point_dict

@st.cache(suppress_st_warning=True)
def get_categories_name_list(annotations_json_data, categories_id_name_dict, selected_image_id, _selected_process):
    send_runtime_msg(msg='Caching:Cache Miss', msg_identifier='categories_name_list', msg_type='info', msg_ttl=1)
    seg_id_name_cat_id = {}
    for ant_dict in annotations_json_data:
        if ant_dict['image_id'] == selected_image_id:
            _cat_id = ant_dict['category_id']
            _id_name = categories_id_name_dict[_cat_id]                
            seg_id_name_cat_id.update({_id_name:_cat_id}) #TODO {ant_dict['category_id']:'*'}
    seg_id_name_lst = list(seg_id_name_cat_id.keys())
    if _selected_process == "Circulation":
        remove_suggested_categories = ["wall"]
        suggested_default_list = list(set(seg_id_name_lst) - set(remove_suggested_categories))
    elif _selected_process == "Connectivity":
        suggested_default_list = ["wall", "parapet", "window", "entry"]
    else:
        suggested_default_list = seg_id_name_lst
    return seg_id_name_lst, suggested_default_list

# @st.cache(suppress_st_warning=True)
def render_selected_segmentations(src_surface, png_surface,segmentations, region_type, categories_color_dict, _selected_process):
    # send_runtime_msg(msg='Caching:Cache Miss', msg_identifier='render_selected_segmentations', msg_type='info', msg_ttl=1)
    for seg_id,seg_points in segmentations.items():   
        _cat_clr_BGR = categories_color_dict[seg_id.split('_')[0]]['BGR']  
        _cat_clr_BGRA = categories_color_dict[seg_id.split('_')[0]]['BGRA'] 
        if _selected_process == "Circulation":
            _cat_clr_BGR = (255,255,255)
            _cat_clr_BGRA = (255,255,255,255)            
        if region_type == 'Fill':
            poly_img = cv2.fillPoly(src_surface, np.array([seg_points]), color=_cat_clr_BGR) #lineType=cv2.LINE_AA
            poly_png = cv2.fillPoly(png_surface, np.array([seg_points]), color=_cat_clr_BGRA) #lineType=cv2.LINE_AA
        else:# region_type == 'Lines':
            poly_img = cv2.polylines(src_surface, np.array([seg_points]), True, _cat_clr_BGR, 1) #lineType=cv2.LINE_AA
            poly_png = cv2.polylines(png_surface, np.array([seg_points]), True, color=_cat_clr_BGRA) #lineType=cv2.LINE_AA)
    return poly_img, poly_png

def export_image(src_surface, png_surface, export_image_format, export_file_name, export_image_width, export_image_height, resize_export=False):
    if export_image_format == 'png':                
        _export_image = png_surface
    elif export_image_format == 'jpeg':
        _export_image = src_surface
    if resize_export:
        _export_image = cv2.resize(_export_image, (export_image_width, export_image_height))                
    cv2.imwrite(export_file_name, _export_image)
    return True

@st.cache(suppress_st_warning=True)
def get_coco_json_file_data(annot_file, annot_dir, annot_clr, annot_export):
    send_runtime_msg(msg='Caching:Cache Miss', msg_identifier='coco_json_file_data', msg_type='info', msg_ttl=1)
    if annotation_file:
        coco_json_file_data = get_file_json_data_info(annotation_file)
    elif annotated_image_dir != "Select_Folder":
        coco_json_file_data = coco_json.generate_coco(image_dir=annotated_image_dir, color_code=annot_clr, export_json=annot_export)
    return coco_json_file_data

def main(): #TODO split in to stage by stage functions and call def init_front_end_routine()
    
    if not annotation_file == None or annotated_image_dir != "Select_Folder":
        annotation_json_file_data = get_coco_json_file_data(annot_file=annotation_file, annot_dir=annotated_image_dir, annot_clr=COLOR_CODE_RGB_JSON, annot_export=False)    

        images_json_data, categories_json_data, annotations_json_data = init_annotation_data(annotation_json_file_data)
        categories_color_dict = get_categories_color_dict(categories_json_data)

        images_name = [img_name['file_name'] for img_name in images_json_data]
        selected_image = st.sidebar.selectbox("Select Plan", images_name, index=0)
        selected_image_id, selected_image_width, selected_image_height = get_image_id_width_height(images_json_data, selected_image)
        # st.write(f'selected : {selected_image} | Size : {selected_image_width} x {selected_image_height}')

        with st.sidebar.form(key="Processes"):
            selected_process = st.radio("Process",("Visualize",'Circulation','Connectivity')) #TODO 'Heatmap',
            st.form_submit_button(label="Select")

        with st.sidebar.form(key="Reg_Label_Bg"):
            clm_region, clm_label, clm_bg_clr, clm_st_im_fmt = st.beta_columns(4)
            with clm_region:
                draw_region = st.radio("Regions", ('Fill','Lines'))
            with clm_label:
                show_label = st.radio("Tag/Label", ('Yes','No'))
            with clm_bg_clr:
                bg_clr = st.radio("Background", ('Black','White'))
            with clm_st_im_fmt:
                st_im_fmt = st.radio("Format", ("BGR", "RGB"))

            st.form_submit_button(label='Update')     

        if selected_process == 'Connectivity':
            with st.sidebar.beta_expander(label='Marker Settings', expanded=False):
                with st.form(key="marker_setting"):
                    _marker, _marker_color = st.beta_columns([4,1])
                    with _marker:
                        selected_mrkr_asset = st.selectbox(label='Asset', options=['line','dot'], index=1)
                    with _marker_color:
                        st.text('')
                        asset_mrkr_clr = st.color_picker(label='Pick', value='#1b56c1')
                    st.form_submit_button(label="Select")

        #TODO add this section in to cache def
        categories_id_name_dict = {category_['id']:category_['name'] for category_ in categories_json_data}
        categories_name_list, default_categories_name_list = get_categories_name_list(annotations_json_data, categories_id_name_dict, selected_image_id, selected_process)
        selected_categories = st.multiselect(label='Select tag to view annotation', options=categories_name_list, default=default_categories_name_list)

        if len(selected_categories):
            png_img = np.zeros((selected_image_height, selected_image_width, 4))
            src_img = np.zeros((selected_image_height, selected_image_width, 3), np.uint8)

            if bg_clr == 'White':
                src_img[:] = (255,255,255)
            
            annot_id_point_dict = get_id_poly_segmentation(annotations_json_data, selected_image_id, selected_categories, categories_id_name_dict)
            poly_surface, png_surface = render_selected_segmentations(src_img, png_img, annot_id_point_dict, draw_region, categories_color_dict, selected_process)
            main_surface = poly_surface

            if selected_process == 'Circulation':

                img_closed = png_surface
                im_background = poly_surface

                skel_graph, skel_image = circ_skeleton.get_skeleton(img_closed, im_background)
                polar_plt, unique_angles, cumulative_sum = circ_skeleton.get_orientation_graph(skel_graph, skel_image) 

                main_surface = skel_image

            if selected_process == 'Connectivity':
                with open("temp_assets\_connectivity.json", "w") as outfile: 
                    json.dump(annot_id_point_dict, outfile)

            st.image(image=main_surface, caption=' ------- [ Visulization ] ------- ', channels=st_im_fmt)

            if selected_process == 'Circulation':
                st.write('polar plote ----')
                st.pyplot(image=polar_plt, caption=' ------- [ Polar Plot ] ------- ')
            
            with st.sidebar.beta_expander(label='Export Settings'):
                with st.form(key="Export_settings"):
                    resize_export = False
                    export_complete = False
                    export_image_width = st.number_input(label='Width', min_value=100, max_value=int(selected_image_width), value=int(selected_image_width))
                    export_image_height = st.number_input(label='Height', min_value=100, max_value=int(selected_image_height), value=int(selected_image_height))            
                    export_image_format = st.selectbox(label='Export image as', options=['png','jpeg'], index=1)
                    export_file_name = f'assets\{selected_image.split(".")[0]}_{export_image_width}_{export_image_height}.{export_image_format}'
                    if selected_image_width != export_image_width or selected_image_height != export_image_height:
                        resize_export = True
                    export_complete = export_image(main_surface, png_surface, export_image_format, export_file_name, export_image_width, export_image_height, resize_export)
                    if export_complete:
                        placeholder = st.empty()
                        placeholder.info('export complete')
                        time.sleep(1)
                        placeholder.info(f'{export_file_name}')
                        time.sleep(1)
                        placeholder.empty()
                        # EXPORT_FLAG = True
                    st.form_submit_button(label="Export")
        
            with st.sidebar.beta_expander(label='Experimental'):
                _tmp_w, _tmp_h = st.beta_columns(2)
                with _tmp_w:
                    st.text_input(label=f'Width (Max:{selected_image_width})', value=f'{export_image_width}', max_chars=len(str(selected_image_width)))
                with _tmp_h:
                    st.text_input(label=f'Height (Max:{selected_image_height})', value=f'{export_image_height}', max_chars=len(str(selected_image_height)))
                _tmp_f, _tmp_b = st.beta_columns([2,1])
                with _tmp_f:
                    st.selectbox(label='frmt', options=['png','jpg'])
                with _tmp_b:
                    st.markdown('')
                    st.text('')
                    st.button(label='Export_')

        with st.beta_expander(label='App Active Dictionary', expanded=False): 
            try:
                temp_info = {
                    "file name":selected_image,
                    "file width":selected_image_width,
                    "file height":selected_image_height,
                    "Current Process":selected_process, 
                    "Region":draw_region, 
                    "Show Label":show_label, 
                    "Background":bg_clr,
                    "selected_categories":selected_categories
                    }
                if EXPORT_FLAG:
                    temp_info.update({"Export":{
                        "width":export_image_width, 
                        "height":export_image_height, 
                        "format":export_image_format}})
            except Exception as e:
                temp_info = f"Exception : {e}"
            st.write(temp_info)
    
    else:
        st.info("To continue please :arrow_down:")
        st.info("Navigate to SideBar :arrow_forward: Import Annotation File :arrow_forward: Drag and drop | Browse files :arrow_forward: Click Import")
        st.markdown("OR")
        st.info("Navigate to SideBar :arrow_forward: Select Folder from Drop Down :arrow_forward: Click Import")        

if __name__ == "__main__":
    main()