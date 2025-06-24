import os
import shutil
import maya.cmds as cmds
import maya.mel as mel

def onMayaDroppedPythonFile(*args, **kwargs):
    _onMayaDropped()  

def get_maya_prefs_scripts_dir():
    maya_version = cmds.about(version=True) 
    maya_app_dir = cmds.internalVar(userAppDir=True)  
    prefs_dir = os.path.join(maya_app_dir, maya_version) 
    scripts_dir = os.path.join(prefs_dir, "scripts")

    if not os.path.exists(scripts_dir):
        os.makedirs(scripts_dir)
        print(f"Created directory: {scripts_dir}")
    else:
        print(f"Directory already exists: {scripts_dir}")
    
    return scripts_dir

def _onMayaDropped():
    
    source_path = os.path.dirname(__file__)  
    scripts_dir = get_maya_prefs_scripts_dir()
    tool_name = "texture_search_and_import.py"
    target_path = os.path.join(scripts_dir, tool_name)

    if not os.path.exists(target_path):
        shutil.copy2(os.path.join(source_path, tool_name), target_path)
        print(f"Tool installed to {target_path}")
    else:
        print(f"Tool already exists in {scripts_dir}.")

    for img_name in ["texture_import_shelf_icon.svg", "texture_import_shelf_icon.svg"]:
        source_img_path = os.path.join(source_path, img_name)
        target_img_path = os.path.join(scripts_dir, img_name)
        if os.path.exists(source_img_path):
            shutil.copy2(source_img_path, target_img_path)
            print(f"Copied {img_name} to {target_img_path}")
        else:
            print(f"Warning: {img_name} not found in source directory.")

    create_shelf_button()

def create_shelf_button():
    shelf_name = "MoisesTools"
    
    if cmds.shelfLayout(shelf_name, exists=True):
        cmds.deleteUI(shelf_name, layout=True)

    shelf_tab_layout = mel.eval('$tmpVar=$gShelfTopLevel')
    cmds.shelfLayout(shelf_name, parent=shelf_tab_layout)

    icon_path = os.path.join(cmds.internalVar(userAppDir=True), cmds.about(version=True), "scripts", "texture_import_shelf_icon.svg")

    cmds.shelfButton(
        parent=shelf_name,
        label="Texture Import",
        command=f'''
import texture_search_and_import

texture_search_and_import.open_ui()
''',
        image=icon_path,
        annotation="Open Texture Search and Import UI"
    )

    print(f"Shelf button added to {shelf_name}")
