import os


def select_texture_folder():
    """
    Open a dialog for the user to select the texture folder(s).
    
    Returns:
        str: The selected folder path.
    """
    return hou.ui.selectFile(start_directory="$HIP",
                            title="Select Texture Folder(s)", 
                            file_type=hou.fileType.Directory,
                            multiple_select=True)
                            
def import_fbx_file(fbx_file):
    """
    Import the FBX file into the scene.
    
    Args:
        fbx_file (str): The path to the FBX file.
    """
    try:
        hou.hipFile.importFBX(fbx_file)
    except hou.OperationFailed as e:
        print("Error importing FBX file:", e)                            
                               

def connect_textures(material_node, texture_folder):
    """
    Connect textures to the Principled Shader node.
    
    Args:
        material_node (hou.Node): The Principled Shader node.
        texture_folder (str): The folder path containing textures.
    """
    try:
        texture_folder_expanded = hou.expandString(texture_folder)
        files = os.listdir(texture_folder_expanded)
        texture_files = []
        fbx_files = []
        
        for file in files:
            if file.endswith(("exr", "jpg", "png", "tga")):
                texture_files.append(file)
            elif file.endswith(("fbx", "obj")):
                fbx_files.append(file)
    
        for fbx_file in fbx_files:
            import_fbx_file(os.path.join(texture_folder_expanded, fbx_file))    
        
    except hou.OperationFailed as e:
        print("Error finding files:", e)
        return

    basecolor_parm = material_node.parm("basecolor_texture")
    roughness_parm = material_node.parm("rough_texture")
    normal_parm = material_node.parm("baseNormal_texture")
    occlusion_parm = material_node.parm("occlusion_texture")
    displacement_parm = material_node.parm("dispTex_texture")
    metallic_parm = material_node.parm("metallic_texture")
    emissive_parm = material_node.parm("emissive_texture")
    opacity_parm = material_node.parm("opacity_texture")
    
    if texture_files:
        for texture_file in texture_files:
                
            if "Albedo" in texture_file or "Base" in texture_file or "Color" in texture_file:
                basecolor_parm.set(texture_folder_expanded + texture_file)
                material_node.parm("basecolor_useTexture").set(True)
                
            elif "Roughness" in texture_file:
                roughness_parm.set(texture_folder_expanded + texture_file)
                material_node.parm("rough_useTexture").set(True)
                
            elif "Normal" in texture_file or "Bump" in texture_file:
                normal_parm.set(texture_folder_expanded + texture_file)
                material_node.parm("baseBumpAndNormal_enable").set(True)
                material_node.parm("baseNormal_flipY").set(True)
                
            elif "AO" in texture_file:
                occlusion_parm.set(texture_folder_expanded + texture_file)
                material_node.parm("occlusion_useTexture").set(True)
                
            elif "Displacement" in texture_file:
                displacement_parm.set(texture_folder_expanded + texture_file)
                material_node.parm("dispTex_enable").set(True)
                
            elif "Metalness" in texture_file or "Metallic" in texture_file:
                metallic_parm.set(texture_folder_expanded + texture_file)
                material_node.parm("metallic_useTexture").set(True)
                
            elif "Emissive" in texture_file:
                emissive_parm.set(texture_folder_expanded + texture_file)
                material_node.parm("emissive_useTexture").set(True)
                
            elif "Opacity" in texture_file:
                opacity_parm.set(texture_folder_expanded + texture_file)
                material_node.parm("opacity_useTexture").set(True)
                

def main():
    """
    Perform the main operation of connecting textures to a Principled Shader node.
    
    This function creates a Principled Shader node,
    prompts the user to select a texture folder,
    and then connects the textures from the selected folder to the Principled Shader node.
    If no texture folder is selected,
    it prints a message indicating that no folder was selected.
    After successful connection of textures,
    it displays a message to the user indicating success.
    """

    texture_folder = select_texture_folder()
    mat_name = texture_folder.split("/")[-2]
    mat_name = mat_name.replace(" ","_")
    material_node = hou.node("/mat").createNode("principledshader", node_name=mat_name)
        
    if not texture_folder:
        print("No texture folder was selected.")
        return
        
    else:
        connect_textures(material_node, texture_folder)
        hou.ui.displayMessage("Textures have been successfully connected!", 
                              severity=hou.severityType.Message)
                              
                              
main()
