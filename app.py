import streamlit as st
import os
import tempfile
import time
import libtorrent as lt
from urllib.parse import urlparse

st.set_page_config(
    page_title="Torrent Downloader",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Torrent Downloader")

# Initialize session state
if 'downloads' not in st.session_state:
    st.session_state.downloads = []
if 'ses' not in st.session_state:
    st.session_state.ses = lt.session()
    st.session_state.ses.listen_on(6881, 6891)

# Create a temporary directory for downloads
temp_download_path = tempfile.gettempdir()

def add_magnet(magnet_link):
    try:
        params = {
            'save_path': temp_download_path,
            'storage_mode': lt.storage_mode_t(2),
        }
        handle = lt.add_magnet_uri(st.session_state.ses, magnet_link, params)
        st.session_state.downloads.append(handle)
        return True
    except Exception as e:
        st.error(f"Error adding magnet link: {str(e)}")
        return False

def format_size(size_bytes):
    """Format size in bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0

# Sidebar
with st.sidebar:
    st.header("ℹ️ Information")
    st.info("""
    This is a simple torrent downloader.
    
    **Features:**
    - Magnet link support
    - Download progress tracking
    - Temporary file storage
    
    **Note:** Files are temporarily stored and will be lost after session ends.
    """)

# Main interface
col1, col2 = st.columns([2, 1])

with col1:
    magnet_link = st.text_input("🔗 Enter Magnet Link:", 
                               placeholder="magnet:?xt=urn:btih:...")
    
    if st.button("➕ Add Download", use_container_width=True):
        if magnet_link:
            if add_magnet(magnet_link):
                st.success("Magnet link added successfully!")
        else:
            st.warning("Please enter a magnet link")

# Download status and progress
if st.session_state.downloads:
    st.header("📥 Downloads")
    
    state_str = [
        "Queued", "Checking", "Downloading Metadata",
        "Downloading", "Finished", "Seeding",
        "Allocating", "Checking Resume Data"
    ]
    
    for i, handle in enumerate(st.session_state.downloads[:]):
        try:
            if handle.status().has_metadata:
                info = handle.get_torrent_info()
                
                # Create unique keys for each download's progress bar
                progress_key = f"progress_{i}"
                status_key = f"status_{i}"
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text(f"📦 {info.name()}")
                with col2:
                    if st.button("❌ Remove", key=f"remove_{i}"):
                        st.session_state.ses.remove_torrent(handle)
                        st.session_state.downloads.remove(handle)
                        st.rerun()
                
                status = handle.status()
                
                # Progress bar
                progress = status.progress * 100
                st.progress(progress, text=f"Progress: {progress:.2f}%")
                
                # Status information
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.text(f"Status: {state_str[status.state]}")
                with col2:
                    download_rate = status.download_rate / 1024
                    st.text(f"Speed: {download_rate:.2f} KB/s")
                with col3:
                    total_size = format_size(info.total_size())
                    st.text(f"Size: {total_size}")
                
                st.divider()
                
        except Exception as e:
            st.error(f"Error updating torrent status: {str(e)}")
            continue
        
        time.sleep(0.1)  # Small delay to prevent excessive CPU usage

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Made with ❤️ by Your Name</p>
    </div>
    """, 
    unsafe_allow_html=True
) 
