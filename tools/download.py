import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pytube import YouTube, Playlist
import threading
import requests
from PIL import Image, ImageTk
from io import BytesIO

class YouTubeDownloader(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("YouTube Downloader")
        self.geometry("800x600")
        self.resizable(False, False)
        
        self.create_widgets()
        
    def create_widgets(self):
        # URL input
        self.url_label = tk.Label(self, text="YouTube URL:")
        self.url_label.pack(pady=10)
        
        self.url_entry = tk.Entry(self, width=80)
        self.url_entry.pack(pady=10)
        
        self.fetch_button = ttk.Button(self, text="Fetch Video Details", command=self.fetch_video_details)
        self.fetch_button.pack(pady=5)
        
        # Stream selection
        self.stream_label = tk.Label(self, text="Available Streams:")
        self.stream_label.pack(pady=10)
        
        self.stream_listbox = tk.Listbox(self, width=80, height=10)
        self.stream_listbox.pack(pady=10)
        
        self.download_stream_button = ttk.Button(self, text="Download Selected Stream", command=self.download_selected_stream)
        self.download_stream_button.pack(pady=5)
        
        # Thumbnail
        self.thumbnail_label = tk.Label(self, text="Thumbnail:")
        self.thumbnail_label.pack(pady=10)
        
        self.thumbnail_canvas = tk.Canvas(self, width=320, height=180)
        self.thumbnail_canvas.pack(pady=10)
        
        self.download_thumbnail_button = ttk.Button(self, text="Download Thumbnail", command=self.download_thumbnail)
        self.download_thumbnail_button.pack(pady=5)
        
        # Playlist
        self.download_playlist_button = ttk.Button(self, text="Download Playlist", command=self.download_playlist)
        self.download_playlist_button.pack(pady=5)
        
    def fetch_video_details(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return
        
        try:
            youtube_video = YouTube(url)
            streams = youtube_video.streams.filter(progressive=True)
            self.stream_listbox.delete(0, tk.END)
            self.streams = []
            for i, stream in enumerate(streams):
                self.stream_listbox.insert(tk.END, f"{i}: {stream}")
                self.streams.append(stream)
            
            self.thumbnail_url = youtube_video.thumbnail_url
            response = requests.get(self.thumbnail_url)
            if response.status_code != 200:
                messagebox.showerror("Error", "Failed to fetch thumbnail")
                return
            
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((320, 180), Image.ANTIALIAS)
            self.thumbnail_image = ImageTk.PhotoImage(img)
            self.thumbnail_canvas.create_image(0, 0, anchor=tk.NW, image=self.thumbnail_image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch video details: {e}")
    
    def download_selected_stream(self):
        selection = self.stream_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a stream from the list")
            return
        
        stream_index = selection[0]
        stream = self.streams[stream_index]
        download_thread = threading.Thread(target=self.download_stream, args=(stream,))
        download_thread.start()
    
    def download_stream(self, stream):
        try:
            download_folder = filedialog.askdirectory()
            if not download_folder:
                return
            
            stream.download(output_path=download_folder)
            messagebox.showinfo("Success", "Video downloaded successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download video: {e}")
    
    def download_thumbnail(self):
        try:
            download_folder = filedialog.askdirectory()
            if not download_folder:
                return
            
            response = requests.get(self.thumbnail_url)
            if response.status_code != 200:
                messagebox.showerror("Error", "Failed to fetch thumbnail")
                return
            
            img_data = response.content
            with open(f"{download_folder}/thumbnail.jpg", "wb") as img_file:
                img_file.write(img_data)
            
            messagebox.showinfo("Success", "Thumbnail downloaded successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download thumbnail: {e}")
    
    def download_playlist(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return
        
        try:
            playlist = Playlist(url)
            download_thread = threading.Thread(target=self.download_playlist_videos, args=(playlist,))
            download_thread.start()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch playlist details: {e}")
    
    def download_playlist_videos(self, playlist):
        try:
            download_folder = filedialog.askdirectory()
            if not download_folder:
                return
            
            for video in playlist.videos:
                video.streams.first().download(output_path=download_folder)
            
            messagebox.showinfo("Success", "Playlist downloaded successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download playlist: {e}")

if __name__ == "__main__":
    app = YouTubeDownloader()
    app.mainloop()
