import os
import sys
import subprocess

import pandas as pd
import streamlit as st



from main import organize_files
from undo import undo_last_organization
from config.settings import get_source_folder, ORGANIZED_FOLDERS, DUPLICATE_FOLDER, LOG_FILE_PATH


def _read_logs():
    if not os.path.exists(LOG_FILE_PATH):
        return "Log file not found yet."

    try:
        with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Failed to read log file: {e}"



def build_folder_dataframe(folder_name):
    folder_path = get_folder_path(folder_name)
    os.makedirs(folder_path, exist_ok=True)

    rows = []

    for item in os.listdir(folder_path):

        # Hide internal files
        if item in [".gitkeep", ".DS_Store"]:
            continue

        item_path = os.path.join(folder_path, item)

        if os.path.isfile(item_path):


            extension = os.path.splitext(item)[1]

            if extension == "":
                extension = "No Extension"

            size_kb = round(os.path.getsize(item_path) / 1024, 2)

            rows.append({
                "File Name": item,
                "Extension": extension,
                "Size KB": size_kb,
                "Folder": folder_name,
                "Path": os.path.abspath(item_path)
            })

    df = pd.DataFrame(
        rows,
        columns=[
            "File Name",
            "Extension",
            "Size KB",
            "Folder",
            "Path"
        ]
    )

    return df




def get_folder_path(folder_name: str) -> str:
    base_folder = get_source_folder()

    if folder_name == "Main Folder":
        return base_folder

    return os.path.join(base_folder, folder_name)


def open_file(file_path):
    if not file_path:
        return False, "Please select a file."

    file_path = os.path.abspath(file_path)

    if not os.path.exists(file_path):
        return False, "File not found."

    if not os.path.isfile(file_path):
        return False, "Invalid file."

    try:
        if sys.platform == "darwin":
            subprocess.Popen(["open", file_path])
        elif sys.platform == "win32":
            os.startfile(file_path)
        else:
            subprocess.Popen(["xdg-open", file_path])

        return True, "Opened successfully."

    except Exception as error:
        return False, f"Unable to open file: {error}"



def calculate_file_hash(file_path: str) -> str:
    import hashlib

    hash_md5 = hashlib.md5()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()


def find_related_duplicates(selected_path: str):
    if not selected_path:
        return []

    selected_path = os.path.abspath(selected_path)

    if not os.path.exists(selected_path):
        return []

    if not os.path.isfile(selected_path):
        return []

    try:
        selected_hash = calculate_file_hash(selected_path)
    except Exception:
        return []

    # Scan all organizer folders including Duplicates and Main
    base_folder = get_source_folder()
    rel_folders = [
        "",
        "Documents",
        "Images",
        "Audio",
        "Videos",
        "Archives",
        "Code",
        "Others",
        DUPLICATE_FOLDER,
    ]

    related = []

    for rel in rel_folders:
        folder_path = os.path.join(base_folder, rel) if rel else base_folder
        if not os.path.exists(folder_path):
            continue

        for root, dirs, files in os.walk(folder_path):
            for item in files:
                if item in [".gitkeep", ".DS_Store"]:
                    continue

                item_path = os.path.join(root, item)
                if not os.path.isfile(item_path):
                    continue

                try:
                    if calculate_file_hash(item_path) == selected_hash:
                        related.append(os.path.abspath(item_path))
                except Exception:
                    continue

    # Ensure unique results
    return sorted(set(related))


def delete_file(file_path: str):
    if not file_path:
        return False, "No file selected."

    file_path = os.path.abspath(file_path)

    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"

    if not os.path.isfile(file_path):
        return False, "Selected path is not a file."

    if os.path.basename(file_path) in [".gitkeep", ".DS_Store"]:
        return False, "Internal file cannot be deleted."

    try:
        os.remove(file_path)
        return True, "File deleted successfully."

    except Exception as error:
        return False, f"Unable to delete file(s): {error}"





def rename_file(file_path: str, new_name: str):
    if not file_path:
        return False, "No file selected."

    file_path = os.path.abspath(file_path)

    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"

    if not new_name.strip():
        return False, "Please enter a new file name."

    if os.path.basename(file_path) in [".gitkeep", ".DS_Store"]:
        return False, "Internal file cannot be renamed."

    # Preserve extension of the selected file
    original_base, original_ext = os.path.splitext(os.path.basename(file_path))
    _, new_ext = os.path.splitext(new_name.strip())

    target_ext = original_ext
    if new_ext:
        target_ext = new_ext

    # If user typed only name without extension, keep original extension
    final_name = new_name.strip()
    if not new_ext:
        final_name = final_name + target_ext

    related = find_related_duplicates(file_path)

    if not related:
        return False, "No related duplicates found to rename."

    try:
        # First validate all destination paths to avoid partial renames
        destinations = []
        for path in related:
            folder_path = os.path.dirname(path)
            dest = os.path.abspath(os.path.join(folder_path, final_name))
            destinations.append((path, dest))

        for _, dest in destinations:
            # Allow renaming to same path
            if os.path.exists(dest):
                if all(src != dest for src, _ in destinations):
                    return False, "A file with this name already exists."

        # Rename
        for src, dest in destinations:
            if os.path.abspath(src) != dest:
                os.rename(src, dest)

        return True, "File renamed successfully."

    except Exception as error:
        return False, f"Unable to rename related files: {error}"




def render_folder_tab(tab_title: str, folder_rel_path: str):
    folder_path = get_folder_path(tab_title)
    df = build_folder_dataframe(tab_title)



    if df.empty:
        st.info(f"No files in {tab_title}.")
        return



    st.dataframe(
        df[["File Name", "Extension", "Size KB", "Folder"]],
        use_container_width=True,
        hide_index=True,
    )


    st.markdown("### File Actions")

    folder_name = tab_title

    selected_file_name = st.selectbox(
        "Select a file",
        options=["-- Select File --"] + df["File Name"].tolist(),
        key=f"select_file_{folder_name}",
    )


    if selected_file_name == "-- Select File --":
        selected_path = None
    else:
        selected_path = os.path.abspath(
            os.path.join(folder_path, selected_file_name)
        )

    col1, col2, col3 = st.columns(3)


    with col1:
        if st.button(
            "Open",
            key=f"open_button_{folder_name}",
            use_container_width=True,
        ):
            if selected_path is None:
                st.warning("Please select a file.")
            else:
                success, message = open_file(selected_path)
                if success:
                    st.success(f"{selected_file_name} opened.")
                else:
                    st.error(message)

    with col2:
        new_name = st.text_input(
            "New file name",
            value=(selected_file_name if selected_path is not None else ""),
            key=f"rename_input_{folder_name}",
            placeholder="e.g. report_final.txt",
        )


        if st.button(
            "Rename",
            key=f"rename_button_{folder_name}",
            use_container_width=True,
        ):
            if selected_path is None:
                st.warning("Please select a file.")
            else:
                success, message = rename_file(selected_path, new_name)
                if success:
                    st.success(f"{selected_file_name} renamed.")
                else:
                    st.error(message)

    with col3:
        confirm_delete = st.checkbox(
            "Confirm delete",
            key=f"confirm_delete_{folder_name}",
        )

        if st.button(
            "Delete",
            key=f"delete_button_{folder_name}",
            use_container_width=True,
        ):
            if selected_path is None:
                st.warning("Please select a file.")
            elif not confirm_delete:
                st.warning("Please confirm delete first.")
            else:
                success, message = delete_file(selected_path)
                if success:
                    st.success(message)
                else:
                    st.error(message)








def main():
    st.set_page_config(page_title="Smart File Organizer", layout="wide")

    source_folder = get_source_folder()
    os.makedirs(source_folder, exist_ok=True)

    if "_refresh_token" not in st.session_state:
        st.session_state["_refresh_token"] = 0

    # Sidebar
    with st.sidebar:
        st.title("Smart File Organizer")
        st.caption("Working folder")
        st.code(source_folder)

        st.write("Folder counts")
        for rel in ["", "Documents", "Images", "Audio", "Videos", "Archives", "Code", "Others", DUPLICATE_FOLDER]:
            folder_path = os.path.join(source_folder, rel) if rel else source_folder
            count = len([n for n in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, n))]) if os.path.exists(folder_path) else 0
            label = "Main Folder" if rel == "" else rel
            st.metric(label, count)

    st.title("Smart File Organizer")

    colA, colB, colC = st.columns([1, 1, 1])

    with colA:
        st.subheader("Create File")
        file_name = st.text_input(
            "File name with extension",
            placeholder="example: notes.txt",
            key="create_file_name",
        )

        if st.button("Create File", key="create_empty", use_container_width=True):
            if not file_name.strip():
                st.warning("Please enter a file name.")
            else:
                base_folder = source_folder
                file_path = os.path.join(base_folder, file_name.strip())

                if os.path.exists(file_path):
                    st.error("File already exists.")
                else:
                    # Create any file extension as a blank placeholder (OS will decide how to open it).
                    # For binary-like extensions, this will still create a 0-byte/empty placeholder, which is acceptable.
                    with open(file_path, "w", encoding="utf-8"):
                        pass

                    st.success("Created successfully.")
                    st.session_state["_refresh_token"] += 1




    with colB:
        st.subheader("Add File")
        uploaded = st.file_uploader("Upload a file to Main Folder", key="file_uploader")
        if uploaded is not None:
            dest = os.path.join(source_folder, uploaded.name)
            if os.path.exists(dest):
                st.warning("A file with the same name already exists in Main Folder.")
            else:
                with open(dest, "wb") as f:
                    f.write(uploaded.getbuffer())
                st.session_state["_refresh_token"] += 1
                st.success(f"Added {uploaded.name}")

    with colC:
        st.subheader("Actions")
        organize_col, undo_col, refresh_col = st.columns(3)

        with organize_col:
            if st.button("Organize Files", key="organize_btn", use_container_width=True):
                organize_files()
                st.session_state["_refresh_token"] += 1
                st.rerun()

        with undo_col:
            if st.button("Undo Last Organization", key="undo_btn", use_container_width=True):
                undo_last_organization()
                st.session_state["_refresh_token"] += 1
                st.rerun()

        with refresh_col:
            if st.button("Refresh", key="refresh_btn", use_container_width=True):
                st.session_state["_refresh_token"] += 1


    with st.expander("Logs", expanded=False):
        st.text(_read_logs())

    folder_names = [
        "Main Folder",
        "Documents",
        "Images",
        "Audio",
        "Videos",
        "Archives",
        "Code",
        "Others",
        "Duplicates",
    ]

    if "current_tab" not in st.session_state:
        st.session_state.current_tab = "Main Folder"

    selected_tab = st.radio(
        "Folders",
        folder_names,
        horizontal=True,
        key="current_tab",
    )

    # Force rerender on refresh
    _ = st.session_state["_refresh_token"]

    folder_rel_map = {
        "Main Folder": "",
        "Documents": "Documents",
        "Images": "Images",
        "Audio": "Audio",
        "Videos": "Videos",
        "Archives": "Archives",
        "Code": "Code",
        "Others": "Others",
        "Duplicates": DUPLICATE_FOLDER,
    }

    render_folder_tab(selected_tab, folder_rel_map[selected_tab])



if __name__ == "__main__":
    main()

