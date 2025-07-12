import streamlit as st
import os
import shutil
import zipfile
from pathlib import Path
import mimetypes
import datetime
import pandas as pd
from typing import List, Dict

# Set page config
st.set_page_config(
    page_title="File Explorer",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_path' not in st.session_state:
    st.session_state.current_path = os.getcwd()
if 'selected_files' not in st.session_state:
    st.session_state.selected_files = []

def get_file_info(file_path: str) -> Dict:
    """Get detailed information about a file or directory"""
    try:
        stat = os.stat(file_path)
        return {
            'name': os.path.basename(file_path),
            'path': file_path,
            'size': stat.st_size,
            'modified': datetime.datetime.fromtimestamp(stat.st_mtime),
            'is_dir': os.path.isdir(file_path),
            'extension': os.path.splitext(file_path)[1] if not os.path.isdir(file_path) else '',
            'type': 'Directory' if os.path.isdir(file_path) else mimetypes.guess_type(file_path)[0] or 'Unknown'
        }
    except Exception as e:
        return None

def format_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    return f"{size_bytes:.2f} {size_names[i]}"

def list_directory(path: str) -> List[Dict]:
    """List all files and directories in the given path"""
    try:
        items = []
        if os.path.exists(path):
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                info = get_file_info(item_path)
                if info:
                    items.append(info)
        return sorted(items, key=lambda x: (not x['is_dir'], x['name'].lower()))
    except PermissionError:
        st.error(f"Permission denied: Cannot access {path}")
        return []
    except Exception as e:
        st.error(f"Error listing directory: {str(e)}")
        return []

def create_new_file(path: str, filename: str, content: str = ""):
    """Create a new file"""
    try:
        file_path = os.path.join(path, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        st.success(f"File '{filename}' created successfully!")
        return True
    except Exception as e:
        st.error(f"Error creating file: {str(e)}")
        return False

def create_new_directory(path: str, dirname: str):
    """Create a new directory"""
    try:
        dir_path = os.path.join(path, dirname)
        os.makedirs(dir_path, exist_ok=True)
        st.success(f"Directory '{dirname}' created successfully!")
        return True
    except Exception as e:
        st.error(f"Error creating directory: {str(e)}")
        return False

def delete_item(path: str):
    """Delete a file or directory"""
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        st.success(f"'{os.path.basename(path)}' deleted successfully!")
        return True
    except Exception as e:
        st.error(f"Error deleting item: {str(e)}")
        return False

def rename_item(old_path: str, new_name: str):
    """Rename a file or directory"""
    try:
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        os.rename(old_path, new_path)
        st.success(f"Renamed to '{new_name}' successfully!")
        return True
    except Exception as e:
        st.error(f"Error renaming item: {str(e)}")
        return False

def copy_item(src_path: str, dst_path: str):
    """Copy a file or directory"""
    try:
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)
        st.success(f"Copied successfully!")
        return True
    except Exception as e:
        st.error(f"Error copying item: {str(e)}")
        return False

def search_files(path: str, query: str, search_in_content: bool = False) -> List[Dict]:
    """Search for files matching the query"""
    results = []
    try:
        for root, dirs, files in os.walk(path):
            # Search in directory names
            for dir_name in dirs:
                if query.lower() in dir_name.lower():
                    dir_path = os.path.join(root, dir_name)
                    info = get_file_info(dir_path)
                    if info:
                        results.append(info)
            
            # Search in file names
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if query.lower() in file_name.lower():
                    info = get_file_info(file_path)
                    if info:
                        results.append(info)
                
                # Search in file content (for text files)
                elif search_in_content and file_name.endswith(('.txt', '.py', '.js', '.html', '.css', '.md', '.json')):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if query.lower() in content.lower():
                                info = get_file_info(file_path)
                                if info:
                                    results.append(info)
                    except:
                        pass
    except Exception as e:
        st.error(f"Error during search: {str(e)}")
    
    return results

# Main App
def main():
    st.title("📁 File Explorer")
    st.markdown("---")
    
    # Sidebar for navigation and operations
    with st.sidebar:
        st.header("Navigation")
        
        # Current path display
        st.text_input("Current Path", value=st.session_state.current_path, key="path_input")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📂 Home"):
                st.session_state.current_path = os.path.expanduser("~")
                st.rerun()
        
        with col2:
            if st.button("⬆️ Parent"):
                parent = os.path.dirname(st.session_state.current_path)
                if parent != st.session_state.current_path:
                    st.session_state.current_path = parent
                    st.rerun()
        
        # Quick navigation
        st.subheader("Quick Access")
        if st.button("🗂️ Documents"):
            st.session_state.current_path = os.path.join(os.path.expanduser("~"), "Documents")
            st.rerun()
        
        if st.button("📥 Downloads"):
            st.session_state.current_path = os.path.join(os.path.expanduser("~"), "Downloads")
            st.rerun()
        
        if st.button("🖼️ Pictures"):
            st.session_state.current_path = os.path.join(os.path.expanduser("~"), "Pictures")
            st.rerun()
        
        st.markdown("---")
        
        # File operations
        st.header("File Operations")
        
        # Create new file
        with st.expander("📄 Create New File"):
            new_filename = st.text_input("File Name", placeholder="example.txt")
            new_file_content = st.text_area("File Content (optional)", height=100)
            if st.button("Create File"):
                if new_filename:
                    create_new_file(st.session_state.current_path, new_filename, new_file_content)
                    st.rerun()
        
        # Create new directory
        with st.expander("📁 Create New Directory"):
            new_dirname = st.text_input("Directory Name", placeholder="New Folder")
            if st.button("Create Directory"):
                if new_dirname:
                    create_new_directory(st.session_state.current_path, new_dirname)
                    st.rerun()
        
        # Upload file
        with st.expander("📤 Upload File"):
            uploaded_file = st.file_uploader("Choose a file", type=None)
            if uploaded_file is not None:
                try:
                    file_path = os.path.join(st.session_state.current_path, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error uploading file: {str(e)}")
    
    # Main content area
    # Search functionality
    st.header("🔍 Search Files")
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        search_query = st.text_input("Search for files and folders", placeholder="Enter search term...")
    
    with col2:
        search_in_content = st.checkbox("Search in content")
    
    with col3:
        search_button = st.button("Search")
    
    if search_button and search_query:
        st.subheader(f"Search Results for: '{search_query}'")
        search_results = search_files(st.session_state.current_path, search_query, search_in_content)
        
        if search_results:
            for item in search_results:
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    icon = "📁" if item['is_dir'] else "📄"
                    st.write(f"{icon} {item['name']}")
                with col2:
                    st.write(format_size(item['size']) if not item['is_dir'] else "-")
                with col3:
                    st.write(item['modified'].strftime("%Y-%m-%d %H:%M"))
                with col4:
                    if st.button("Open", key=f"open_{item['path']}"):
                        if item['is_dir']:
                            st.session_state.current_path = item['path']
                            st.rerun()
                        else:
                            st.info(f"File: {item['path']}")
        else:
            st.info("No files found matching your search.")
    
    st.markdown("---")
    
    # Directory listing
    st.header(f"📂 Current Directory: {os.path.basename(st.session_state.current_path)}")
    
    items = list_directory(st.session_state.current_path)
    
    if items:
        # Create a DataFrame for better display
        df_data = []
        for item in items:
            df_data.append({
                'Name': f"{'📁' if item['is_dir'] else '📄'} {item['name']}",
                'Size': format_size(item['size']) if not item['is_dir'] else '-',
                'Modified': item['modified'].strftime("%Y-%m-%d %H:%M"),
                'Type': item['type']
            })
        
        df = pd.DataFrame(df_data)
        
        # Display items with operations
        for i, item in enumerate(items):
            col1, col2, col3, col4, col5, col6, col7 = st.columns([3, 1, 1, 1, 1, 1, 1])
            
            with col1:
                icon = "📁" if item['is_dir'] else "📄"
                if st.button(f"{icon} {item['name']}", key=f"item_{i}"):
                    if item['is_dir']:
                        st.session_state.current_path = item['path']
                        st.rerun()
                    else:
                        st.info(f"Selected: {item['name']}")
            
            with col2:
                st.write(format_size(item['size']) if not item['is_dir'] else "-")
            
            with col3:
                st.write(item['modified'].strftime("%Y-%m-%d"))
            
            with col4:
                if st.button("✏️", key=f"rename_{i}", help="Rename"):
                    st.session_state[f"rename_mode_{i}"] = True
            
            with col5:
                if st.button("📋", key=f"copy_{i}", help="Copy"):
                    st.session_state[f"copy_source"] = item['path']
                    st.success(f"Copied {item['name']} to clipboard")
            
            with col6:
                if st.button("📥", key=f"download_{i}", help="Download") and not item['is_dir']:
                    try:
                        with open(item['path'], 'rb') as f:
                            st.download_button(
                                label=f"Download {item['name']}",
                                data=f,
                                file_name=item['name'],
                                key=f"download_btn_{i}"
                            )
                    except Exception as e:
                        st.error(f"Error downloading file: {str(e)}")
            
            with col7:
                if st.button("🗑️", key=f"delete_{i}", help="Delete"):
                    if st.session_state.get(f"confirm_delete_{i}", False):
                        delete_item(item['path'])
                        st.rerun()
                    else:
                        st.session_state[f"confirm_delete_{i}"] = True
                        st.warning("Click again to confirm deletion")
            
            # Rename functionality
            if st.session_state.get(f"rename_mode_{i}", False):
                new_name = st.text_input(f"New name for {item['name']}", value=item['name'], key=f"rename_input_{i}")
                col_rename1, col_rename2 = st.columns(2)
                with col_rename1:
                    if st.button("Save", key=f"save_rename_{i}"):
                        if new_name and new_name != item['name']:
                            rename_item(item['path'], new_name)
                            st.session_state[f"rename_mode_{i}"] = False
                            st.rerun()
                
                with col_rename2:
                    if st.button("Cancel", key=f"cancel_rename_{i}"):
                        st.session_state[f"rename_mode_{i}"] = False
                        st.rerun()
        
        # Paste operation
        if 'copy_source' in st.session_state:
            st.markdown("---")
            if st.button("📋 Paste Here"):
                source = st.session_state.copy_source
                filename = os.path.basename(source)
                destination = os.path.join(st.session_state.current_path, filename)
                copy_item(source, destination)
                del st.session_state.copy_source
                st.rerun()
    
    else:
        st.info("This directory is empty or cannot be accessed.")
    
    # Footer
    st.markdown("---")
    st.markdown("**File Explorer** - Built with Streamlit")

if __name__ == "__main__":
    main()