import streamlit as st
import libtorrent as lt
import time

# Initialize session
ses = lt.session()
ses.listen_on(6881, 6891)
downloads = []

# Streamlit UI
st.title("Torrent Downloader")

# Input for magnet link
magnet_link = st.text_input("Enter Magnet Link Or Type Exit:")

if st.button("Add Magnet Link"):
    if magnet_link.lower() != "exit":
        params = {"save_path": "/content/drive/My Drive/Torrent"}
        downloads.append(lt.add_magnet_uri(ses, magnet_link, params))
        st.success("Magnet link added!")

# Display download progress
state_str = [
    "queued",
    "checking",
    "downloading metadata",
    "downloading",
    "finished",
    "seeding",
    "allocating",
    "checking fastresume",
]

if st.button("Start Download"):
    while downloads:
        for index, download in enumerate(downloads[:]):
            if not download.is_seed():
                s = download.status()
                st.write(
                    f"{download.name()} - {s.download_rate / 1000} kB/s - {state_str[s.state]}"
                )
                st.progress(s.progress)
            else:
                ses.remove_torrent(download)
                downloads.remove(download)
                st.success(f"{download.name()} complete")
        time.sleep(1)
