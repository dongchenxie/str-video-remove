import subprocess
import re
import os

def extract_timecodes(srt_file):
    """提取没有字幕的时间段"""
    timecode_pattern = r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})'
    timecodes = []
    with open(srt_file, 'r') as file:
        for line in file:
            match = re.search(timecode_pattern, line)
            if match:
                start, end = match.groups()
                start = start.replace(',', '.')
                end = end.replace(',', '.')
                timecodes.append((start, end))
    return timecodes

def get_non_subtitle_segments(timecodes, video_duration):
    """计算没有字幕的时间段"""
    segments = []
    current_start = '00:00:00.000'
    for start, end in timecodes:
        if current_start != start:
            segments.append((current_start, start))
        current_start = end
    if current_start != video_duration:
        segments.append((current_start, video_duration))
    return segments

def main():
    srt_file = './files/example.srt'
    video_file = './files/example.mp4'
    output_file_prefix = './files/output_part_'
    merged_output_file = './files/merged_output.mp4'

    # 获取视频时长
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_file], stdout=subprocess.PIPE, text=True)
    video_duration = result.stdout.strip()

    # 提取时间码并计算没有字幕的时间段
    timecodes = extract_timecodes(srt_file)
    segments = get_non_subtitle_segments(timecodes, video_duration)

    parts = []
    for i, (start, end) in enumerate(segments):
        # 裁剪没有字幕的视频片段
        output_file = f'{output_file_prefix}{i}.mp4'
        command = f'ffmpeg -i {video_file} -ss {start} -to {end} -c copy {output_file}'
        subprocess.run(command, shell=True)
        parts.append(output_file)

    # 创建filelist.txt
    filelist_path = './files/filelist.txt'
    with open(filelist_path, 'w') as f:
        for part in parts:
            f.write(f"file '{os.path.basename(part)}'\n")

    # 合并裁剪后的视频片段
    merge_command = f'ffmpeg -f concat -safe 0 -i {filelist_path} -c copy {merged_output_file}'
    subprocess.run(merge_command, shell=True)

if __name__ == '__main__':
    main()
