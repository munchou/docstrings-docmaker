"""munchou 2025

"""


import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


color_background = "#1e1e1e"
color_class_title = "#4ec9b0"
color_function_def = "#4c86b6"
color_function_title = "#dcdcaa"
color_docstrings = "#ce9178"


def get_functions_name(filename, split_file, filespath):
    has_docstrings = False
    has_class = False
    file_name = f"""<div id="{filespath}-{filename[:-3]}"><b><u style="color:{color_function_def};">{filename[:-3].upper()}.py</u></b></div>\n"""
    file_content = ""
    class_tab = ""
    u = 0

    menu_sub = ""

    while u != len(split_file):
        function_docstring = ""
        line = split_file[u].strip()
        if line.startswith("class "):
            has_class = True
            class_title = line[6:].replace(":", "")
            if "(" in line:
                class_title = line[6:].split("(")[0]
            class_tab = "margin-left:1rem;"
            u += 1
            continue

        elif line.startswith("def "):
            function_name = line[4:].split("(")[0]
            if not split_file[u+1].strip().startswith('"""'):
                function_docstring = "<i>no docstrings</i>"
                u += 1
            else: # start of triple quote
                has_docstrings = True
                i = 1

                if '"""' in split_file[u+1].strip()[3:]:
                    function_docstring += f"{split_file[u+i].strip()[3:-3]}<br>\n"
                
                else:
                    function_docstring += f"{split_file[u+i].strip()[3:]}<br>\n"
                    i += 1
                    while True:
                        if '"""' in split_file[u+i].strip(): # What follows is to avoid adding commentaries after the quote, if any                            
                            current_line = split_file[u+i].strip()
                            s = 0
                            while True:
                                if current_line[s] == '"':
                                    try:
                                        if current_line[s+1] == current_line[s+2] == '"':
                                            break
                                    except Exception:
                                        pass
                                s += 1
                            function_docstring += f"{current_line[:s]}<br>\n"
                            i += 1
                            break

                        else:
                            function_docstring += f"{split_file[u+i].strip()}<br>\n"
                            i += 1

                u += i

            if has_docstrings and has_class:
                file_content += f'<div style="margin-left:1rem; color:{color_class_title}">{class_title}</div>'
                file_content += f'<div style="{class_tab}"><li style="margin-left:1rem; color: {color_function_title};"><b><color style="color: {color_function_title};">{function_name}</color></b><br>\n<div style="margin-left:1rem; color:{color_docstrings};">{function_docstring}</li><br></div></div>\n\n'
                has_class = False
            elif has_docstrings and not has_class:
                file_content += f'<div style="{class_tab}"><li style="margin-left:1rem; color: {color_function_title};"><b><color style="color: {color_function_title};">{function_name}</color></b><br>\n<div style="margin-left:1rem; color:{color_docstrings};">{function_docstring}</li><br></div></div>\n\n'
            has_docstrings = False

        else:
            u += 1
    
    if file_content != "":
        final_content = file_name
        final_content += file_content
        menu_sub += f'<div style="color:{color_function_def}; margin-left:1.5rem;">- <a style="color:{color_function_def};" href="#{filespath}-{filename[:-3]}">{filename[:-3]}</a></div>\n'
    else:
        final_content = ""

    return menu_sub, final_content


def check_files(dir_path, filespath, python_files):
    final_content = ""
    menu_subs = ""

    for file in python_files:
        with open(f"{dir_path}{filespath}/{file}") as python_file:
            try:
                split_file = python_file.read().splitlines()
                # print(filespath, "->", file)
                menu_sub, file_content = get_functions_name(file, split_file, filespath.split("/")[-1])
            except Exception as e:
                # print(f"Error in splitting lines of file {filespath}/{file}")
                # print(e)
                continue

        menu_subs += menu_sub
        final_content += file_content
    return menu_subs, final_content

folders_dic = {}

def check_path(user_path, folders_dic, folders_to_skip):
    for dirpath, dirnames, filenames in os.walk(user_path):
        dir_files = []

        # print("current:", dirpath)

        # if folders_to_skip:
            # print("SKIP FOLDERS:", folders_to_skip)
            # if dirpath[len(user_path)+1:].startswith(tuple(folders_to_skip)):
            # for folder in folders_to_skip:
            #     if folder in dirpath:
                    # print("Skipping", dirpath)
                    # continue

        # if dirnames:
        #     dirnames.sort()
        #     print("dirnames:", dirnames)
        #     for dirname in dirnames:
        #         print(f"  Subdirectory: {dirname}")

        for filename in filenames:
            if filename.endswith(".py") and filename != "docstrings-docmaker.py":
                if not any(folder.strip() in dirpath for folder in folders_to_skip):
                    # print("filepath:", dirpath, "->", filename)
                    dir_files.append(filename)

        folders_dic[dirpath[len(user_path):]] = dir_files

def menu():
    while True:
        clear_screen()
        print("Project's name / Project's full path / Folders to skip (if any)\n")

        project_name_input = input("Project's name: ")
        full_path_input = input("Project's full path (leave blank if at the root): ")
        output_path_input = input("Generated HTML output path (blank = same folder as where the script is run): ")
        while True:
            add_folders_input = input("\n\tAdd folders to skip (Y/N)? ").lower()
            if add_folders_input not in ["y", "n"]:
                continue
            if add_folders_input == "n":
                folders_to_skip = None
                break
            else:
                folders_to_skip = []
                while True:
                    folders_to_skip_input = input("\tAdd a folder to skip: ")
                    if not folders_to_skip_input == "":
                        folders_to_skip.append(folders_to_skip_input)
                    print("Folder(s) that will be skipped:", folders_to_skip)
                    while True:
                        add_folder_again_input = input("\tAdd one more (Y/N)? ").lower()
                        if not add_folder_again_input in ["y", "n"]:
                            continue
                        break
                    if add_folder_again_input == "y":
                        continue
                    break

            break

        dir_path = "./" if full_path_input == "" else full_path_input
        output_path_input = "/home/munchou/Python-projects/docstrings-docmaker"
        if output_path_input != "" and not output_path_input.endswith("/"):
            output_path_input += "/"

        clear_screen()
        project_name_input = "ZUPAsswordz Manager"
        dir_path = "/home/munchou/Python-projects/zupasswords-manager"
        # output_path_input = "/home/munchou/Python-projects"
        folders_to_skip = [".buildozer", "_env", "_saved-files"]

        print("\tSUMMARY\n")
        print(f"Project's name: {project_name_input}")
        print(f"Project's full path: {dir_path}")
        print(f"Generated HTML output path: {output_path_input}")
        print(f"Folders to skip: {folders_to_skip}\n")

        while True:
            confirm_answers = input("Confirm (Y/N): ").lower()
            if confirm_answers not in ["y", "n"]:
                continue
            break

        if confirm_answers == "n":
            continue

        break

    check_path(dir_path, folders_dic, folders_to_skip)
    return project_name_input, dir_path, output_path_input

        
project_name, dir_path, output_path = menu()
# check_path(dir_path, folders_dic, folders_to_skip)

menu_content = '<div style="left: 10px; margin: 0; padding: 0; width: 300px; position: fixed; height: 100%; overflow: auto; border: 1px solid;">\n'
menu_content += f'<div style="color:{color_function_def}; text-align: center; text-decoration: underline;"><b>{project_name}</b></div><br>\n'

file_content = ""
for filespath in folders_dic:
    if folders_dic[filespath]:
        folders_dic[filespath].sort()
        # print(f"{filespath}: {folders_dic[filespath]}\n")
        menu_content_sub, file_content_sub = check_files(dir_path, filespath, folders_dic[filespath])
        if menu_content_sub != "":
            menu_content += f'''<li style="color:{color_function_def};">{"<i>project's root</i>" if filespath == "" else filespath}</li>\n'''
        menu_content += menu_content_sub
        file_content += file_content_sub


output_file = open(f"{output_path}{project_name}_docstrings.html", "w")

output_file.write(f"""<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{project_name} DocStrings</title>
        <link href="code_highlights.css" rel="stylesheet">
    </head>
<body style="margin-left: 315px; background-color: {color_background};">

""")

menu_content += '<br>\n</div>\n'
output_file.write(menu_content)
output_file.write(file_content)
output_file.write("</body>\n</html>")

output_file.close()

print("DONE")