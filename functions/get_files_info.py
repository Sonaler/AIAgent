import os

def get_files_info(working_directory, directory="."):

    files_list = []
    string_to_return = ""
    try:
        path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(path, directory))
        valid_full_path = os.path.commonpath([path, full_path]) == path

        if not valid_full_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        
        for item in os.listdir(full_path):
            curr_file = {}
            item_path = os.path.join(full_path, item)
            curr_file["name"] = item
            curr_file["size"] = os.stat(item_path).st_size
            curr_file["is_dir"] = os.path.isdir(item_path)
            files_list.append(curr_file)
        
        for item in files_list:
            string_to_return += f"- {item["name"]}: file_size={item["size"]}, is_dir={item["is_dir"]}\n"
        
        return string_to_return
    except Exception as e:
        return f"Error: {e}"