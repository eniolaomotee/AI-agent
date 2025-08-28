import os

def get_files_info(working_directory, directory = "."):
    base_dir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(base_dir, directory))
    
    # Check if the target path is within the base directory
    if not target_path.startswith(base_dir):
        return f"Error: Cannot list {directory} as it is outside the permitted working directory."
    
    if not os.path.isdir(target_path):
        return f"Error: {directory} is not a valid directory."
    try:
        content = []
        for item in os.listdir(target_path):
            full_path = os.path.join(target_path, item)
            is_dir = os.path.isdir(full_path)
            size = os.path.getsize(full_path) if not is_dir else 0
            content.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")
        
        return "\n".join(content)
    except Exception as e:
        return f"Error listing files: {e}"
    

