from typing import Dict, List,  Optional
import requests
from m3u8 import loads, M3U8
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from tqdm import tqdm
import re
import subprocess
import os


class VideoDownloader:
    def __init__(self, num_threads: int = 4):
        self.num_threads: int = num_threads
        self.session: requests.Session = requests.Session()

    def close_session(self):
        self.session.close()

    def _download_segment(self, url: str, filename: str) -> None:
        retry_count = 0
        while retry_count < 5:
            try:
                response: requests.Response = self.session.get(url, stream=True, timeout=10)
                with open(filename, "wb") as f:
                    for data in response.iter_content(chunk_size=4096):
                        f.write(data)
                return 
            except requests.exceptions.Timeout:
                retry_count += 1
                print(f"Timeout error occurred. Retrying... (Attempt {retry_count})")
            except requests.exceptions.RequestException as e:
                print("Something has gone wrong skipping segment.")
                print(e)
                break

    def _download_hls(self, url: str,quality: Optional[str] = None,output_dir: str = ".",output_file_name: Optional[str] = None, start_segment: int = 0, end_segment: Optional[int] = None,) -> None:
            try:
                response: requests.Response = self.session.get(url)
                response.raise_for_status()
            except Exception as e:
                print("Encounter exception while fetching url playlist: ", e)
                return
            playlist: M3U8 = loads(response.text)
            playlists: List[Dict] = playlist.data["playlists"]
            if len(playlists) == 0:
                print("No playlists found!!")
                return
            quality_playlist: Optional[Dict] = None
            playlists = sorted(playlists, key=lambda k: int(k["stream_info"].get("resolution","0x0").split("x")[0]), reverse=True)
            quality_playlist = playlists[0]
            if quality is not None:
                for p in playlists:
                    resolution = p["stream_info"].get("resolution","0x0").split("x")[0]
                    if resolution == quality:
                        quality_playlist = p
                        break

            base_url: str = url.rsplit("/",1)[0] + "/"
            playlist_url: str = quality_playlist["uri"]
            if not  playlist_url.startswith("http"):
                playlist_url = base_url + playlist_url

            try:
                response = self.session.get(playlist_url)
                response.raise_for_status()
            except Exception as e:
                print("Encounter exception while fetching segments url: ", e)
                return

            segments = loads(response.text).data["segments"]
            base_url = playlist_url.rsplit("/",1)[0] + "/"
            if end_segment is None:
                end_segment = len(segments)
            if output_file_name is None:
                output_file_name = f"{quality}"

            output_dir = output_dir if os.path.exists(output_dir) else "."
            with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
                futures: List[Future] = []
                for i, segment in enumerate(segments[start_segment:end_segment]):
                    segment_url: str = segment["uri"]
                    if not  segment_url.startswith("http"):
                        segment_url = base_url + segment_url
                    filename: str = f"{output_file_name}_segment{i+start_segment:05}.ts"
                    filename = os.path.join(output_dir,filename)
                    future = executor.submit(self._download_segment, segment_url, filename)
                    futures.append(future)
                for  future in tqdm(as_completed(futures), total=len(futures), desc=f"Downloading {output_file_name} segments", unit="segment"):
                    pass
            self._combine_segments(segments_dir=output_dir,output_file_name= output_file_name)
            self._convert_video_format(os.path.join(output_dir,output_file_name + ".ts"))

    def _combine_segments(self,segments_dir: str, output_file_name: str):
        if not os.path.exists(segments_dir):
            return
        with open(os.path.join(segments_dir,output_file_name + ".ts"), "wb") as f:  
            segments_file_names = []
            for filename in os.listdir(segments_dir):
                segment_file_name = os.path.join(segments_dir,filename)
                if os.path.isfile(segment_file_name) and filename.startswith(f"{output_file_name}_segment"):
                    segments_file_names.append(segment_file_name)
            for filename in tqdm(sorted(segments_file_names),desc= f"Combining {output_file_name} segments"):
                with open(filename, "rb") as segment_file:
                    f.write(segment_file.read())
                if not filename.endswith(output_file_name + ".ts"):
                    os.remove(filename)

    def _download_mp4(self, url: str,output_dir: str = ".", output_file_name: Optional[str] = None) -> None:
        if output_file_name is None:
            output_file_name = f"{url.rsplit('/',1)[-1]}.mp4"
        output_dir = output_dir if os.path.exists(output_dir) else "."
        output_file_name = os.path.join(output_dir,output_file_name)
        try:
            response: requests.Response = self.session.get(url, stream=True)
            total_size: int = int(response.headers.get("content-length", 0))
            with open(output_file_name + ".mp4", "wb") as f:
                for data in tqdm(response.iter_content(chunk_size=4096),total= total_size,desc=f"Downloading {output_file_name}"):
                    f.write(data)
        except Exception as e:
            print("Something has gone Wrong failed to download mp4!!")

    def _string_time_to_int(self,text):
        if isinstance(text, float):
            num = str(text)
            nums = num.split('.')
        else:
            nums = text.split(':')
        if len(nums) == 2:
            st_sn = int(nums[0]) * 60 + float(nums[1])
            return int(st_sn)
        elif len(nums) == 3:
            st_sn = int(nums[0]) * 3600 + int(nums[1]) * 60 + float(nums[2])
            return int(st_sn)
        else:
            #raise ValueError("Not correct time")
            return -1
    def _convert_video_format(self,file_location: str, format = ".mp4"):
        if not os.path.exists(file_location) or file_location.endswith(format):
            return
        file_location_with_format = file_location.rsplit(".",1)[0] + format
        ffprobecmd = ["ffprobe", "-v","error","-show_entries" ,"format=duration","-of" ,"default=noprint_wrappers=1:nokey=1","-i", file_location]
        ffmpegcmd = ["ffmpeg","-y", "-v","quiet","-stats","-i", file_location,"-c","copy",file_location_with_format]
        ffprobe = subprocess.run(ffprobecmd,stdout=subprocess.PIPE,shell=False,universal_newlines=True)
        duration = float(ffprobe.stdout.rstrip())
        duration = int(duration)
        ffmpeg_process = subprocess.Popen(ffmpegcmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             universal_newlines=True
                             )
        if(ffmpeg_process.stdout is None):
            return
        desc = os.path.basename(file_location) + " to " + format
        pbar = tqdm(total=duration,leave=True,desc=desc)
        for line in iter(ffmpeg_process.stdout.readline,''):
            if line:
                time = re.search(r"\btime=\b",line)
                if time:
                    start_time = time.span()[-1]
                    time_as_int = self._string_time_to_int(line[start_time:start_time + 11])
                    if time_as_int < duration:
                        pbar.n = time_as_int
                    else:
                        pbar.n= duration

                    pbar.refresh()

        pbar.close()
        return_code = ffmpeg_process.poll()
        if not return_code:
            os.unlink(file_location)
        ffmpeg_process.stdout.close()

    def download_video(self, url, quality=None,output_dir: str= ".", output_file: Optional[str]=None, start_segment: int=0, end_segment: Optional[int]=None):
        if url.endswith('.m3u8'):
            self._download_hls(url,quality,output_dir,output_file)

        elif url.endswith('.mp4'):
            self._download_mp4(url,output_dir = output_dir,output_file_name=output_file)
        else:
            print("Unsupported video format")


