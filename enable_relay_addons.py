import bpy
import addon_utils
# import time
import sys, os, time
from bpy.types import Operator

def change_addon_key_value(change_dir):
    bpy.context.preferences.view.use_translate_interface = False
    for dir_list in change_dir:
        keymaps = bpy.context.window_manager.keyconfigs['Blender addon'].keymaps
        for ks_name , ks_data in keymaps.items():
            if ks_name == dir_list[0][0]:
                list_keymaps = []
                for id_name , id_data in ks_data.keymap_items.items():
                    if id_name == dir_list[0][1] and id_data.name == dir_list[0][2]:
                            list_keymaps.append(id_data)
                for data in list_keymaps:
                    for value in dir_list[1]:
                        setattr(data, value[0], value[1]) 
                        # print(value[0], value[1])
                    if dir_list[2] != None:
                        for prop in dir_list[2]:
                                setattr(data.properties,prop[0],prop[1])
                list_keymaps.clear()
    bpy.context.preferences.view.use_translate_interface = True

class Enable_Pie_Menu_Relay_Addons(Operator):
    bl_idname = "pie.enable_relay_addons"
    bl_label = "Enable Addons"
    bl_description = "一键打开常用内置插件"
    bl_options = {"REGISTER","UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        addon_utils.modules_refresh()
        addons_list =[]
        for mod in addon_utils.modules():
            addons_list.append(mod.__name__)

        user_path = bpy.utils.resource_path('USER') 
        config_path = os.path.join(user_path, "config")

        if sys.platform == "win32":
            assets_sync = r'D:/OneDrive/Sync/Blender/Assets Sync'
            assets_local = r'F:/Assets/Blender Assets'
        join = os.path.join

        addons_officials_list ={
        # 官方&社区      #  addon_name : [[addon_settings],[addon_keys]]
            'curve_tools' : [[],[]],
            'add_curve_extra_objects':[[],[]],
            'curve_simplify':[[],[]],
            'add_mesh_BoltFactory':[[],[]],
            'add_mesh_extra_objects':[[],[]],
            'development_edit_operator':[[],[]],
            'development_icon_get':[[],[]],
            'amaranth':[[('use_frame_current',False),
                        ('use_scene_refresh',False),
                        ('use_file_save_reload',False),
                        ('use_timeline_extra_info',False),
                        ('use_layers_for_render',False),
                        ],[]], 
            'space_view3d_copy_attributes':[[],[]],
            'materials_utils':[[],[(['3D View','wm.call_menu','Material Utilities'],[('value','CLICK'),('ctrl',True)],[])]],
            'object_print3d_utils':[[],[]],
            'mesh_f2':[[],[(['Mesh','mesh.f2','Make Edge/Face'],[('value','CLICK')],[])]],
            'mesh_looptools':[[],[]],
            'mesh_snap_utilities_line':[[],[]],
            'mesh_tiny_cad':[[],[]],
            'node_presets':[[('search_path',join(assets_sync,'Nodes Presets'))],[]], # addon path
            'node_wrangler':[[],[]],
            'object_boolean_tools':[[],[(['Object Mode','wm.call_menu','Bool Tool'],[('value','CLICK')],[])]], # key
            'magic_uv':[[],[]],
            'io_import_images_as_planes':[[],[]],
            'space_view3d_modifier_tools':[[],[]],
            'sun_position':[[],[]],
            'object_edit_linked':[[],[]],
            'mesh_tools':[[],[]],
            'mesh_inset':[[],[]],
            'io_import_dxf':[[],[]],
            'io_export_dxf':[[],[]],

        # 第三方
            'Bagapie': [[],[(['3D View','bagapie.duplicatelinkedgroup','Duplicate Linked Group'],[('active',False)],[]),
                            (['3D View','bagapie.duplicategroup','Duplicate Group'],[('active',False)],[]),
                            ]], # key alt N
            'slcad_transform': [[],[]],
            # EsayLight
            'EsayLight': [[('ies_library_path',join(assets_sync,'IES'))],[]], # ies lib path
            # HDRI
            'hdri_maker': [[('hdri_maker_library',join(assets_local,'HDRI MAKER LIBRARY'))],[]],
            # QuickSnap
            'quicksnap': [[('auto_check_update',False)],[
                (['3D View','object.quicksnap','QuickSnap Tool'],[('value','CLICK'),('type','G'),('shift',False)],[])]],
            # Simple Tabs
            'simple-tabs': [[('startup_delay',1)],[]], # 导入json设置
            'slcad_transform': [[],[]],
            'extra_lights': [[],[]],
            # Photographer
            'photographer': [[('hdri_lib_path',join(assets_sync,'Custom HDRI'))],
                            [(['3D View','wm.call_menu_pie','Photographer Camera Pie'],[('value','CLICK_DRAG')],[])]],
            # Object Asset Wizard
            'object_asset_wizard': [[('root',join(assets_sync,'Blender Assets Wizard'))],[]],
            'BMAX_Connector': [[],[]],
            'sketchup_importer': [[],[]],
            # Super IO
            'super_io': [[('force_unicode',True),('cpp_obj_importer',True),
                            ('cpp_obj_exporter',True),('extend_export_menu',True)],
                        [
                        (['3D View','wm.super_import','Super Import'],[('value','CLICK')],[]),
                        (['3D View','wm.super_export','Super Export'],[('value','CLICK'),('type','E')],[]),
                        (['Node Editor','wm.super_import','Super Import'],[('value','CLICK')],[]),
                        (['Node Editor','wm.super_export','Super Export'],[('value','CLICK'),('type','E')],[]),
                        (['Image Generic','wm.super_export','Super Export'],[('value','CLICK'),('type','E')],[]),
                        (['File Browser','wm.super_import','Super Import'],[('value','CLICK')],[]),
                        (['File Browser','wm.super_export','Super EXport'],[('value','CLICK'),('type','E')],[]),
                        ]],
            'Synchronize Workspaces': [[],[]],
            'EasyPBR': [[('lib_path',join(assets_sync,'Easy_PBR_library'))],[]], # keys 未更改
            'EdgeFlow': [[],[]],
            'slide_edge': [[],[]],
            'straight_skeleton': [[],[]],
            'face_cutter': [[],[]],
            'bend_face': [[],[]],
            # Niche Loops
            'niche-loops': [[],[]],
            'round_inset': [[],[]],
            'Seer Adjacent Selection': [[],[]],
            # Smart Fill
            'smart_fill': [[('mouse_wheel',True)],[
                (['Mesh','mesh.mesh.smart_fill_popup','Smart Fill Popup'],[('value','CLICK')],[]),
                (['Mesh','mesh.edge_face_add','Make Edge/Face'],[('value','CLICK')],[]),
            ]],
            'smart_loop_toolkit': [[],[]],
            #----Nodes----
            'BB_Nodes': [[],[]],
            'colormate': [[],[]],
            'ETK_core': [[],[]],
            'Node_kit': [[('nodes_path',join(assets_sync,'NodeKit_Library'))],[]],
            'node_pie': [[],[(['Node Editor','wm.call_menu_pie','Node pie'],[('value','CLICK_DRAG')],[])]],
            'uber_compositor': [[],[]],
            'b3dsdf': [[],[]],
            'wxz_nodes_presets': [[],[]],
            # Drop It
            'drop_it': [[],[
                (['3D View','object.drop_it','Drop It'],[('value','CLICK')],[])
                ]],
            'NGon Loop Select': [[],[
                (['Mesh','ls.select','Loop Select'],[('value','CLICK')],[]),
                ]],
            'OCD': [[],[]],
            # IQ lib
            'botaniq_full': [[('botaniq_path',join(assets_local,'botaniq_full'))],[]],
            # 'traffiq_full': [[('traffiq_path',join(assets_local,'traffiq_full'))],[]],
            'leafig': [[],[]],
            'Text_input': [[],[]],
            'atomic_data_manager': [[('enable_missing_file_warning',False),('enable_support_me_popup',False),
                                        ('enable_pie_menu_ui',False),('auto_check_update',False),],[]],
            'QOL_Select_Contiguous': [[],[]],
            # TexTools
            'TexTools_1_5': [[],[]],
            'UvSquares': [[],[]],
            'distributeobjects': [[],[]],
            # Friendly Povit
            'scpo': [[],[
                (['3D View','friendly.pivot','Friendly: SCPO'],[('value','CLICK'),('ctrl',True)],[]),
                (['Image','friendly.pivot2d','Friendly: SCPO2D'],[('value','CLICK'),('ctrl',True)],[])]],
            'lattice_helper': [[],[]],
            'viewport_timeline_scrub': [[],[]]
        }

        addon_disable_list = [
            'io_anim_bvh',
            'io_mesh_ply',
            # 'mesh_f2',
        ]

        # ads_lis_dir = addons_officials_list.update(addons_thirds_list)
        # 打开插件并设置
        for addon_name ,addon_change in addons_officials_list.items():
            if addon_name in addons_list:
                if addon_utils.check(addon_name)[0] == False:
            #  # check addon is enabled
                    try:
                        bpy.ops.preferences.addon_enable(module = addon_name)
                        time.sleep(1)
                        bpy.ops.preferences.addon_refresh()
                        print(addon_name,'is enabled')
                    except:
                        print(addon_name,'is enable error')
                if addon_change[0]:
                    for pref_change in addon_change[0]:
                        setattr(context.preferences.addons[addon_name].preferences, pref_change[0], pref_change[1])
                if addon_change[1]:
                    change_addon_key_value(addon_change[1])
        # 关闭插件
        for disable in addon_disable_list:
            if disable in addons_list and addon_utils.check(disable)[0] == True:
                bpy.ops.preferences.addon_disable(module = disable)

        # 部分插件其他设置
        bpy.ops.simpletabs.import_settings(filepath=r"D:/OneDrive/Sync/Blender/Blender_Mapping/config/simpletabs_prefs.json")

        return {"FINISHED"}

def register():
    bpy.utils.register_class(Enable_Pie_Menu_Relay_Addons)

def unregister():
    bpy.utils.unregister_class(Enable_Pie_Menu_Relay_Addons)

if __name__ == "__main__":
    register()