import streamlit as st
from handlers.url_validator import URLValidator
from handlers.youtube_downloader import YouTubeDownloader
from handlers.file_handler import FileHandler
from handlers.ui_handler import UIHandler
import concurrent.futures
import time

def initialize_session_state():
    if 'download_state' not in st.session_state:
        st.session_state.download_state = {
            'progress': 0,
            'status': '',
            'completed': False,
            'started': False,
            'zip_path': None
        }

def download_audio_wrapper(args):
    i, video_url, temp_dir, audio_format, audio_quality = args
    downloader = YouTubeDownloader()
    downloader.download_audio(video_url, temp_dir, audio_format, audio_quality)
    return i

def main():
    st.title('YouTube Audio Downloader')

    initialize_session_state()

    ui = UIHandler()
    url = ui.get_url_input()
    audio_format = ui.get_audio_format()
    audio_quality = ui.get_audio_quality()

    progress_bar = st.progress(st.session_state.download_state['progress'])
    status_text = st.empty()
    status_text.text(st.session_state.download_state['status'])

    if st.button('Download') and not st.session_state.download_state['started']:
        validator = URLValidator()
        if not validator.is_valid_youtube_url(url):
            st.error('Please enter a valid YouTube URL.')
        else:
            st.session_state.download_state['started'] = True
            st.session_state.download_state['completed'] = False
            st.session_state.download_state['progress'] = 0
            st.session_state.download_state['status'] = 'Starting download...'

    if st.session_state.download_state['started'] and not st.session_state.download_state['completed']:
        downloader = YouTubeDownloader()
        file_handler = FileHandler()

        with file_handler.create_temp_directory() as temp_dir:
            video_urls = downloader.get_video_urls(url)
            total_videos = len(video_urls)

            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                futures = [executor.submit(download_audio_wrapper, (i, video_url, temp_dir, audio_format, audio_quality)) 
                           for i, video_url in enumerate(video_urls, 1)]
                
                completed = 0
                for future in concurrent.futures.as_completed(futures):
                    completed += 1
                    st.session_state.download_state['progress'] = completed / total_videos
                    st.session_state.download_state['status'] = f'Downloaded {completed} of {total_videos} videos'
                    progress_bar.progress(st.session_state.download_state['progress'])
                    status_text.text(st.session_state.download_state['status'])
                    time.sleep(0.1)  # Prevent excessive updates

            st.session_state.download_state['status'] = 'Creating zip file...'
            status_text.text(st.session_state.download_state['status'])
            zip_path = file_handler.create_zip_file(temp_dir)
            
            st.session_state.download_state['status'] = 'Download complete!'
            st.session_state.download_state['completed'] = True
            st.session_state.download_state['zip_path'] = zip_path

        progress_bar.progress(1.0)
        status_text.text(st.session_state.download_state['status'])

    if st.session_state.download_state['completed'] and st.session_state.download_state['zip_path']:
        ui.display_download_button(st.session_state.download_state['zip_path'])
        if ui.download_clicked():
            file_handler = FileHandler()
            file_handler.remove_file(st.session_state.download_state['zip_path'])
            st.session_state.download_state['started'] = False
            st.session_state.download_state['completed'] = False
            st.session_state.download_state['zip_path'] = None

    ui.display_instructions()

if __name__ == "__main__":
    main()