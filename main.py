from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
import configparser


# 视频切割函数
def video_cut(file_path, file_path_save, start=0, end=None):
    try:
        video_data = VideoFileClip(file_path)
        video_new = video_data.subclip(start, end)
        video_new.write_videofile(file_path_save, audio_codec="aac")
        video_data.reader.close()
        return True
    except Exception as e:
        print("视频分割失败：", str(e))
        return False


def merge_videos(video_files, output_path):
    """
    合并多个视频文件为一个视频文件

    :param video_files: 要合并的视频文件路径列表
    :param output_path: 合并后的视频文件路径
    :return: 合并成功返回True，否则返回False
    """
    try:
        # 用VideoFileClip读取所有视频
        video_clips = [VideoFileClip(v) for v in video_files]

        # 取第一个视频的音频轨道
        #audio = video_clips[0].audio

        # 使用concatenate_videoclips函数将所有视频合并
        final_clip = concatenate_videoclips(video_clips)

        # 将音频轨道添加到合并后的视频中
        #final_clip = final_clip.set_audio(audio)

        # 保存合并后的视频
        final_clip.write_videofile(output_path,audio_codec="aac")
        return True
    except Exception as e:
        print("视频合并失败：", str(e))
        return False


if __name__ == "__main__":

    cf = configparser.ConfigParser()
    cf.read("config.ini")  # 读取配置文件，如果写文件的绝对路径，就可以不用os模块
    secs = cf.sections()

    for s in secs:
        file = cf.get(s, "file")
        cut_name = cf.get(s, "cut_name")
        num = cf.get(s, "num")
        num = int(num)  # 切割数量
        merge = cf.get(s, "merge")
        merge_name = cf.get(s, "merge_name")
        header = cf.get(s, "header")
        footer = cf.get(s, "footer")
        video_data = VideoFileClip(file)
        print('视频时长：' + str(video_data.duration))
        part_time = video_data.duration / num  # 计算平均长度
        for x in range(num):
            path_out = cut_name + str(x) + '.mp4'
            cut_res = video_cut(file, path_out, start=x * part_time, end=(x + 1) * part_time)
            # 定义要合并的视频文件名
            if cut_res:
                print('生成视频：' + path_out)
                if merge == 'yes':
                    video_files = [path_out]
                    # 定义合并后的视频文件名
                    if header:
                        video_files.insert(0, header)
                    if footer:
                        video_files.append(footer)

                    merge_output_path = merge_name + str(x) + '.mp4'
                    # 调用合并函数
                    if merge_videos(video_files, merge_output_path):
                        print("合并视频："+merge_output_path)
                    else:
                        print("合并失败："+merge_output_path)
            else:
                print('生成失败：' + path_out)