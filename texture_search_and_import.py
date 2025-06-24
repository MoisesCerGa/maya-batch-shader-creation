from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.api.OpenMaya as om
import maya.cmds as cmds

import time

import os

import maya.OpenMayaUI as omui1

def maya_main_window():
    main_window_ptr = omui1.MQtUtil.mainWindow()
    
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class MyLineEdit(QtWidgets.QLineEdit):
    
    enter_pressed = QtCore.Signal(str)
    
    def keyPressEvent(self, e):
        super(MyLineEdit, self).keyPressEvent(e)
        
        if e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
            self.enter_pressed.emit("Enter Key Pressed")


class ShaderCreation(QtWidgets.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super(ShaderCreation, self).__init__(parent)
        
        self.setWindowTitle("Create Shaders from Textures by MoisesCG")
        self.setMinimumWidth(200)
        self.setMinimumHeight(200)
        
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        self.apply_styles() 
        
        self.possible_names = []
        
        
    def create_widgets(self):
        self.lineedit = QtWidgets.QLineEdit() 
        self.instructions = QtWidgets.QLabel(
            "Hitting the 'Create' button will search for textures that have the name given inside of it, "
            "assign the shader to the selected objects, and connect the correct one based on naming conventions. "
            "The naming conventions are as follows:\n"
            "BC -> Base Color; R -> Roughness; M -> Metallic; Transmission -> Transmission; "
            "N -> Normal; Displacement -> Displacement; AO -> AO."
        )
        self.ok_btn = QtWidgets.QPushButton("Search")
        self.cancel_btn = QtWidgets.QPushButton("Close")
        
        self.toggle_button = QtWidgets.QToolButton(text="Modify Naming Conventions")
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(True)

        
        self.base_color_lineedit = QtWidgets.QLineEdit("BaseColor")
        self.roughness_lineedit = QtWidgets.QLineEdit("Roughness")
        self.metalic_lineedit = QtWidgets.QLineEdit("Metallic")
        self.transmission_lineedit = QtWidgets.QLineEdit("Transmission")
        self.normal_lineedit = QtWidgets.QLineEdit("Normal")
        self.displacement_lineedit = QtWidgets.QLineEdit("Height")
        self.ambientoclusion_lineedit = QtWidgets.QLineEdit("AO")
        
        self.naming_mode = QtWidgets.QComboBox()
        self.naming_mode.addItems(["Prefix", "Suffix"])
        
        self.preview_label = QtWidgets.QLabel("mtl_'name'")
        self.preview_label_two = QtWidgets.QLabel("sG_'name'")
        

    def toggle(self):
        expanded = self.toggle_button.isChecked()
        self.content.setVisible(expanded)
        self.toggle_button.setArrowType(2 if expanded else 1)
        

    def create_layouts(self):
        """Creates a clean and structured layout for the UI."""
        
        main_layout = QtWidgets.QVBoxLayout(self)
        
        instructions_group = QtWidgets.QGroupBox("Quick Guide")
        instructions_layout = QtWidgets.QVBoxLayout()
        instructions_layout.setContentsMargins(10, 25, 10, 10) 
        
        instructions_list = [
            "-> Select the prefered naming convention of the created Mtl.",
            "-> Click 'Search' to find possible textures.",
            "-> Remove the shaders you don't want to create.",
            "-> Click 'Create' to create all shaders that are still on the list."
        ]
        
        for instruction in instructions_list:
            label = QtWidgets.QLabel(instruction)
            label.setStyleSheet("font-size: 16px; color: #F4C430;") 
            instructions_layout.addWidget(label)

        instructions_group.setLayout(instructions_layout)
        instructions_group.setStyleSheet("""
            font-size: 18px; padding: 10px; border: 1px solid #555;
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding-bottom: 12px; }
        """) 
        main_layout.addWidget(instructions_group)
        
        # ?? Naming Mode Section
        naming_mode_group = QtWidgets.QGroupBox("Created Mtl Naming Preview")
        naming_mode_layout = QtWidgets.QHBoxLayout()

        # Naming Mode ComboBox
        self.naming_mode.setStyleSheet("""
            font-size: 16px; padding: 5px; border: 1px solid #666; border-radius: 5px;
            background-color: #222; color: white;
        """)
        naming_mode_layout.addWidget(self.naming_mode)

        # Filename Preview (Aligned Left)
        preview_layout = QtWidgets.QVBoxLayout()
        self.preview_label.setAlignment(QtCore.Qt.AlignLeft)
        self.preview_label_two.setAlignment(QtCore.Qt.AlignLeft)

        self.preview_label.setStyleSheet("font-size: 14px; color: #E0E0E0; padding-left: 10px;")
        self.preview_label_two.setStyleSheet("font-size: 14px; font-weight: bold; color: #E0E0E0; padding-left: 10px;")

        preview_layout.addWidget(self.preview_label)
        preview_layout.addWidget(self.preview_label_two)

        # Add Preview to the Right of Naming Mode
        naming_mode_layout.addLayout(preview_layout)

        naming_mode_group.setLayout(naming_mode_layout)
        naming_mode_group.setStyleSheet("""
            font-size: 16px; padding: 10px; border: 1px solid #777;
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding-bottom: 8px; }
        """)

        main_layout.addWidget(naming_mode_group)
        
        self.content = QtWidgets.QWidget()
        
        main_layout.addWidget(self.toggle_button)
        
        self.content_layout = QtWidgets.QVBoxLayout(self.content)
        self.content.setLayout(self.content_layout)

        naming_group = QtWidgets.QGroupBox("Modify Naming Conventions")
        naming_layout = QtWidgets.QFormLayout()
        naming_layout.setContentsMargins(10, 25, 10, 10)
        
        naming_layout.addRow("Base Color:", self.base_color_lineedit)
        naming_layout.addRow("Roughness:", self.roughness_lineedit)
        naming_layout.addRow("Metallic:", self.metalic_lineedit)
        naming_layout.addRow("Transmission:", self.transmission_lineedit)
        naming_layout.addRow("Normal:", self.normal_lineedit)
        naming_layout.addRow("Displacement:", self.displacement_lineedit)
        naming_layout.addRow("Ambient Occlusion:", self.ambientoclusion_lineedit)
        
        naming_group.setLayout(naming_layout)
        naming_group.setStyleSheet("""
            font-size: 16px; padding: 10px;
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding-bottom: 8px; }
        """)
        
        self.content_layout.addWidget(naming_group)
        
        
        main_layout.addWidget(self.content)
        
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        
        main_layout.addStretch()
        main_layout.addLayout(btn_layout)
        
    def find_possible_names(self):
        self.possible_names = []
        
        suffixes_list = [
            self.base_color_lineedit.text(),
            self.roughness_lineedit.text(),
            self.metalic_lineedit.text(),
            self.transmission_lineedit.text(),
            self.normal_lineedit.text(),
            self.displacement_lineedit.text(),
            self.ambientoclusion_lineedit.text()
        ]
        
        project_path = cmds.workspace(q=True, rootDirectory=True) 
        textures_path = os.path.join(project_path, "sourceimages") 
        
        possible_extensions = [".png", ".jpg", ".jpeg", ".tga", ".exr", ".tiff"]
        
        for suffix_test in suffixes_list:
        
            for root, _, files in os.walk(textures_path):  
                for file in files:
                    file_name, ext = os.path.splitext(file)
                    if ext.lower() not in possible_extensions:
                        continue  

                    for suffix in suffixes_list:
                        if file_name.endswith(f"_{suffix}") or file_name.endswith(f"_{suffix}.1001"):
                            if file_name.endswith(".1001"):
                                possible_name_no_suffix = file_name.replace(f"_{suffix}.1001", "")
                            else:
                                possible_name_no_suffix = file_name.replace(f"_{suffix}", "")
                            
                            if possible_name_no_suffix not in self.possible_names:
                                self.possible_names.append(possible_name_no_suffix)
                            break  
                            
            
        if self.possible_names:
            print(self.possible_names)
            self.possible_names = PossibleNamesUI(self.possible_names).exec_()
            for name in self.possible_names:
                self.create_shaders(name)
                

        if not self.possible_names:
            om.MGlobal.displayWarning("No valid textures found in sourceimages.")
            return

    def create_connections(self):
        self.ok_btn.clicked.connect(self.find_possible_names)
        self.cancel_btn.clicked.connect(self.close)
        self.toggle_button.clicked.connect(self.toggle)
        self.naming_mode.currentTextChanged.connect(self.update_preview)

    def create_shaders(self, name):
        """
        Creates an Arnold aiStandardSurface material and a shading group, naming them 
        based on the provided name.
        """
        if not name.strip():
            om.MGlobal.displayError("No valid name provided for the shader.")
            return None


        # This is what should be changed if the namig convention is changed
        
        if self.naming_mode.currentText() == "Prefix":
            material_name = f"mtl_{name}"
            shading_group_name = f"sG_{name}"
        elif self.naming_mode.currentText() == "Suffix":
            material_name = f"{name}_mtl"
            shading_group_name = f"{name}_sG"

        if not cmds.objExists(material_name):
            material = cmds.shadingNode("aiStandardSurface", asShader=True, name=material_name)
        else:
            material = material_name
            om.MGlobal.displayWarning(f"Material '{material_name}' already exists. Using existing one.")

        if not cmds.objExists(shading_group_name):
            shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shading_group_name)
        else:
            shading_group = shading_group_name
            om.MGlobal.displayWarning(f"Shading Group '{shading_group_name}' already exists. Using existing one.")

        cmds.connectAttr(f"{material}.outColor", f"{shading_group}.surfaceShader", force=True)
        
        self.search_existing_textures(name, material, shading_group)

        om.MGlobal.displayInfo(f"Created Material: {material_name}, Shading Group: {shading_group_name}")
        return {"material": material, "shading_group": shading_group}
        
        
    def search_existing_textures(self, name, material, shading_group):
        """
        Searches for all relevant textures in the sourceimages folder,
        creates the necessary file texture nodes, applies color correction,
        and connects them to the aiStandardSurface shader.
        """
        project_path = cmds.workspace(q=True, rootDirectory=True)  
        textures_path = os.path.join(project_path, "sourceimages")  

        if not os.path.exists(textures_path):
            om.MGlobal.displayWarning("The sourceimages folder does not exist in the current project.")
            return

        texture_map = {
            self.base_color_lineedit.text(): ("baseColor", False, False), 
            self.roughness_lineedit.text(): ("specularRoughness", True, True),  
            self.metalic_lineedit.text(): ("metalness", True, True),  
            self.transmission_lineedit.text(): ("transmission", True, True),  
            self.normal_lineedit.text(): ("normalCamera", False, False),
            self.displacement_lineedit.text(): ("displacementShader", True, True),  
            self.ambientoclusion_lineedit.text(): ("ambientOcclusion", True, True)  
        }

        possible_extensions = [".png", ".jpg", ".jpeg", ".tga", ".exr", ".tiff"]
        connection_list = []
        no_texture_found_list = []
        
        number_of_operations = len(texture_map)  
        progress_dialog = QtWidgets.QProgressDialog("Waiting to process...", "Cancel", 0, number_of_operations, self)
        progress_dialog.setWindowTitle("Progress...")
        progress_dialog.setValue(0)
        progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        progress_dialog.show()

        QtCore.QCoreApplication.processEvents()
        
        texture_has_udims = False

        for i, (suffix, (attr, is_raw, use_red_channel)) in enumerate(texture_map.items(), start=1):
            texture_file = None

            for root, _, files in os.walk(textures_path): 
                for ext in possible_extensions:
                    texture_path = os.path.join(root, f"{name}_{suffix}{ext}")

                    if os.path.exists(texture_path):
                        texture_file = texture_path
                        break
                    else:
                        udim_texture_path = os.path.join(root, f"{name}_{suffix}.1001{ext}")
                        if os.path.exists(udim_texture_path):
                            texture_file = udim_texture_path
                            texture_has_udims = True  
                            break
                
                if texture_file: 
                    break


            if not texture_file:
                no_texture_found_list.append(f"No texture found for {suffix} or it isn't named as: {name}_{suffix}' in sourceimages.")
                continue  
                
            if progress_dialog.wasCanceled():
                break
                
            progress_dialog.setLabelText(f"Processing: {suffix} ({i}/{number_of_operations})")
            progress_dialog.setValue(i)
            QtCore.QCoreApplication.processEvents()  


            file_node = cmds.shadingNode("file", asTexture=True, name=f"{name}_{suffix}_file")
            cmds.setAttr(f"{file_node}.fileTextureName", texture_file, type="string")

            if is_raw:
                cmds.setAttr(f"{file_node}.colorSpace", "Raw", type="string")
                cmds.setAttr(f"{file_node}.alphaIsLuminance", 1)
            
            if texture_has_udims:
                cmds.setAttr(f"{file_node}.uvTilingMode", 3)

            place2d = cmds.shadingNode("place2dTexture", asUtility=True, name=f"{name}_{suffix}_place2d")
            cmds.connectAttr(f"{place2d}.outUV", f"{file_node}.uvCoord", force=True)
            cmds.connectAttr(f"{place2d}.outUvFilterSize", f"{file_node}.uvFilterSize", force=True)

            cmds.connectAttr(f"{place2d}.coverage", f"{file_node}.coverage")
            cmds.connectAttr(f"{place2d}.translateFrame", f"{file_node}.translateFrame")
            cmds.connectAttr(f"{place2d}.rotateFrame", f"{file_node}.rotateFrame")
            cmds.connectAttr(f"{place2d}.mirrorU", f"{file_node}.mirrorU")
            cmds.connectAttr(f"{place2d}.mirrorV", f"{file_node}.mirrorV")
            cmds.connectAttr(f"{place2d}.stagger", f"{file_node}.stagger")
            cmds.connectAttr(f"{place2d}.wrapU", f"{file_node}.wrapU")
            cmds.connectAttr(f"{place2d}.wrapV", f"{file_node}.wrapV")
            cmds.connectAttr(f"{place2d}.repeatUV", f"{file_node}.repeatUV")
            cmds.connectAttr(f"{place2d}.offset", f"{file_node}.offset")
            cmds.connectAttr(f"{place2d}.rotateUV", f"{file_node}.rotateUV")
            cmds.connectAttr(f"{place2d}.noiseUV", f"{file_node}.noiseUV")

            

            output_attr = "outColor" if not use_red_channel else "outColorR"



            if suffix == self.normal_lineedit.text():
                normal_node = cmds.shadingNode("aiNormalMap", asUtility=True, name=f"{name}_normalMap")
                cmds.connectAttr(f"{file_node}.outColor", f"{normal_node}.input", force=True)
                cmds.connectAttr(f"{normal_node}.outValue", f"{material}.normalCamera", force=True)

            elif suffix == self.displacement_lineedit.text():
                displacement_node = cmds.shadingNode("displacementShader", asShader=True, name=f"{name}_displacement")
                
                subtract_node = cmds.shadingNode("aiSubtract", asUtility=True, name=f"{name}_subtract")
                cmds.setAttr(f"{subtract_node}.input2R", 0.5)
                cmds.setAttr(f"{subtract_node}.input2G", 0.5)
                cmds.setAttr(f"{subtract_node}.input2B", 0.5)
                
                multiply_node = cmds.shadingNode("aiMultiply", asUtility=True, name=f"{name}_multiply")
                cmds.setAttr(f"{multiply_node}.input2R", 1.0)
                cmds.setAttr(f"{multiply_node}.input2G", 1.0)
                cmds.setAttr(f"{multiply_node}.input2B", 1.0)
                
                cmds.connectAttr(f"{file_node}.outColor", f"{subtract_node}.input1", force=True)
                cmds.connectAttr(f"{subtract_node}.outColor", f"{multiply_node}.input1", force=True)
                cmds.connectAttr(f"{multiply_node}.outColor", f"{displacement_node}.vectorDisplacement", force=True)
                cmds.connectAttr(f"{displacement_node}.displacement", f"{shading_group}.displacementShader", force=True)
            elif suffix ==  self.base_color_lineedit.text():
                color_correct = cmds.shadingNode("aiColorCorrect", asUtility=True, name=f"{name}_{suffix}_colorCorrect")
                cmds.connectAttr(f"{file_node}.{output_attr}", f"{color_correct}.input", force=True)
                cmds.connectAttr(f"{color_correct}.outColor", f"{material}.{attr}", force=True)
            elif suffix == self.roughness_lineedit.text():
                cmds.setAttr(f"{file_node}.alphaIsLuminance", 0)
                color_correct_rough = cmds.shadingNode("aiColorCorrect", asUtility=True, name=f"{name}_{suffix}_colorCorrect")
                cmds.connectAttr(f"{file_node}.outColor", f"{color_correct_rough}.input", force=True)
                cmds.connectAttr(f"{color_correct_rough}.outColorR", f"{material}.{attr}", force=True)
            else:
                
                cmds.connectAttr(f"{file_node}.outAlpha", f"{material}.{attr}", force=True)
                
            

            om.MGlobal.displayInfo(f"Connected {texture_file} to {material}.{attr} using {file_node}.{output_attr}")
            connection_list.append(f"Connected {name}_{suffix}{ext} to {material}'s {attr}")
            time.sleep(0.05)

        progress_dialog.close()
        
        self.show_connection_dialog(connection_list, no_texture_found_list)
    
    def apply_styles(self):
        """Applies custom styles to the UI."""
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 22px;
                border: 1px solid gray;
                border-radius: 5px;
                margin-top: 10px;
                padding: 15px;
            }
            QPushButton {
                padding: 8px;
                font-size: 20px;
                border-radius: 4px;
                background-color: #3B7D91;
                color: white;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
            #selectFilePathBtn {
                background-color: #D4A017;
                color: black;
                font-size: 18px;
                font-weight: bold;
            }
            QLabel {
                font-size: 20px;
                font-weight: bold;
            }
            QLineEdit {
                padding: 6px;
                font-size: 16px;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
            }
            QRadioButton {
                font-size: 20px;
                padding: 5px;
                border-radius: 10px;
                background-color: #E8F0FE;
            }
            QProgressDialog {
                background-color: #2A2A2A;
                color: white;
                border-radius: 10px;
                padding: 15px;
            }
            QProgressBar {
                border: 2px solid #3B3B3B;
                border-radius: 4px;
                background-color: #3B3B3B;
                height: 20px;
                text-align: center; 
                color: #FFD700;
                font-size: 16px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                border-radius: 6px;
                background-color: #4FA3D1;
            }
        """)
    
    def run_progress_test(self):
        number_of_operations = 7

        progress_dialog = QtWidgets.QProgressDialog("Waiting to process...", "Cancel", 0, number_of_operations, self)
        progress_dialog.setWindowTitle("Progress...")
        progress_dialog.setValue(0)
        progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        progress_dialog.show()

        QtCore.QCoreApplication.processEvents()
      
    def update_preview(self):
        if self.naming_mode.currentText() == "Prefix":
            self.preview_label.setText("mtl_'name'")
            self.preview_label_two.setText("sG_'name'")
        else:
            self.preview_label.setText("'name'_mtl")
            self.preview_label_two.setText("'name'_sG")
        
    def show_connection_dialog(self, connection_list, no_texture_found_list):
        """Displays a styled QDialog with the list of connected textures."""
        
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Texture Connection Report")
        dialog.setMinimumSize(550, 400)

        layout = QtWidgets.QVBoxLayout(dialog)
        
        title_label = QtWidgets.QLabel("Texture Connection Results")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #FFD700;") 
        layout.addWidget(title_label)
        
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: #2A2A2A; border: 1px solid #444; border-radius: 5px; padding: 5px;")
        
        scroll_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_widget)
        
        for no_texture in no_texture_found_list:
            conn_label = QtWidgets.QLabel(no_texture)
            conn_label.setStyleSheet(
                "background-color: #333333; color: brown; font-size: 16px; padding: 8px; border: 1px solid #555;"
                "border-radius: 4px; margin-bottom: 5px;"
            )
            conn_label.setWordWrap(True)
            scroll_layout.addWidget(conn_label)
            
        
        for connection in connection_list:
            conn_label = QtWidgets.QLabel(connection)
            conn_label.setStyleSheet(
                "background-color: #333333; color: #85A84F; font-size: 16px; padding: 8px; border: 1px solid #555;"
                "border-radius: 4px; margin-bottom: 5px;"
            )
            conn_label.setWordWrap(True)
            scroll_layout.addWidget(conn_label)
        
        
        
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
        
        close_btn = QtWidgets.QPushButton("Close")
        close_btn.setStyleSheet(
            "background-color: #3B7D91; color: white; font-size: 18px; padding: 8px; border-radius: 5px;"
        )
        close_btn.clicked.connect(dialog.accept)
        
        layout.addWidget(close_btn, alignment=QtCore.Qt.AlignCenter)
        
        dialog.show()
        
class PossibleNamesUI(QtWidgets.QDialog):
    def __init__(self, possible_names, parent=None):
        super(PossibleNamesUI, self).__init__(parent)
        
        self.setWindowTitle("Select Names to Keep")
        self.setMinimumSize(500, 400)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)  

        self.possible_names = possible_names  
        self.new_possible_names = list(possible_names) 

        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        self.apply_styles()

    def create_widgets(self):
        """Create UI elements."""
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.addItems(self.new_possible_names)
        self.list_widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)  

        self.remove_btn = QtWidgets.QPushButton("Remove Selected")
        self.confirm_btn = QtWidgets.QPushButton("Confirm")
        self.close_btn = QtWidgets.QPushButton("Cancel")

    def create_layouts(self):
        """Set up UI layout."""
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(QtWidgets.QLabel("Select names to remove:"))
        main_layout.addWidget(self.list_widget)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.remove_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.confirm_btn)
        btn_layout.addWidget(self.close_btn)

        main_layout.addLayout(btn_layout)

    def create_connections(self):
        """Connect UI elements to functions."""
        self.remove_btn.clicked.connect(self.remove_selected_items)
        self.confirm_btn.clicked.connect(self.confirm_selection)
        self.close_btn.clicked.connect(self.close_clicked)

    def remove_selected_items(self):
        """Remove selected items from the list."""
        selected_items = self.list_widget.selectedItems()
        for item in selected_items:
            self.new_possible_names.remove(item.text()) 
            self.list_widget.takeItem(self.list_widget.row(item)) 

    def confirm_selection(self):
        """Return the new list and close the dialog."""
        self.accept() 
        
    def close_clicked(self):
        self.close()

    def apply_styles(self):
        """Apply styles to the UI."""
        self.setStyleSheet("""
            QDialog {
                background-color: #2A2A2A;
                color: white;
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #FFD700;
            }
            QListWidget {
                font-size: 16px;
                border: 2px solid #D4A017;
                background-color: #3B3B3B;
                padding: 5px;
                border-radius: 5px;
                outline: none;
            }
            QListWidget::item {
                padding: 6px;
                margin: 2px;
                border-radius: 3px;
                background-color: #4E4E4E;
                color: white;
            }
            QListWidget::item:selected {
                background-color: #FF6347;
                color: black;
                font-weight: bold;
            }
            QPushButton {
                padding: 8px;
                font-size: 16px;
                border-radius: 5px;
                background-color: #3B7D91;
                color: white;
            }
            QPushButton:hover {
                background-color: #85A84F;
            }
            QPushButton:pressed {
                background-color: #6B8E23;
            }
        """)

    def exec_(self):
        """Execute the dialog and return the modified list."""
        result = super().exec_()
        if result == QtWidgets.QDialog.Accepted:
            return self.new_possible_names
        else:
            self.new_possible_names = []
            return self.new_possible_names
        return self.possible_names
    

def open_ui():
    try:
        test_dialog.close()
    except:
        pass
    shader_creation_dialog = ShaderCreation()
    shader_creation_dialog.show()