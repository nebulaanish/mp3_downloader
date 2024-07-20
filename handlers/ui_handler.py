import streamlit as st

class UIHandler:
    def get_url_input(self):
        return st.text_input('Enter YouTube URL (video or playlist):', '')

    def get_audio_format(self):
        audio_formats = ['opus', 'mp3', 'wav', 'aac']
        return st.selectbox('Select audio format:', audio_formats, index=0)

    def get_audio_quality(self):
        audio_qualities = ['64', '128', '192', '256', '320']
        return st.selectbox('Select audio quality (kbps):', audio_qualities, index=0)

    def display_download_button(self, zip_path):
        with open(zip_path, 'rb') as f:
            return st.download_button(
                label="Download ZIP file",
                data=f,
                file_name="youtube_audio.zip",
                mime="application/zip"
            )

    def download_clicked(self):
        return st.session_state.get('download_clicked', False)

    def display_instructions(self):
        st.markdown("""
        ### Instructions:
        1. Enter a YouTube video URL or a playlist URL.
        2. Select the desired audio format and quality.
        3. Click the 'Download' button.
        4. Wait for the process to complete.
        5. Click the 'Download ZIP file' button to get your audio files.

        Please respect copyright laws and YouTube's terms of service when using this application.
        """)