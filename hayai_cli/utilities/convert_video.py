import subprocess
from tqdm import tqdm
import re
from pathlib import Path

def convert_secs(text):
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
def convert_video(file_location: str, format = ".mp4"):
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
    desc = file_location + " to " + format
    pbar = tqdm(total=duration,leave=True,desc=desc)
    for line in iter(ffmpeg_process.stdout.readline,''):
        if line:
            time = re.search(r"\btime=\b",line)
            if time:
                start_time = time.span()[-1]
                time_as_float = convert_secs(line[start_time:start_time + 11])
                if time_as_float < duration:
                    pbar.n = time_as_float
                else:
                    pbar.n= duration

                pbar.refresh()

    pbar.close()
    return_code = ffmpeg_process.poll()
    print("return code",return_code)
    #if(return_code and return_code ==0):
    if not return_code:
        print("unlinking")
        Path.unlink(Path(file_location))

