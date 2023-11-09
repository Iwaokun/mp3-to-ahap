import json
import numpy as np
from pydub import AudioSegment
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

def create_ahap_from_audio(audio_file_path, ahap_file_path):
    # MP3 ファイルを読み込み
    audio = AudioSegment.from_mp3(audio_file_path)

    # フレームレートとチャンネル数を取得
    framerate = audio.frame_rate
    n_channels = audio.channels

    # データを numpy 配列に変換
    waveform = np.array(audio.get_array_of_samples())

    # ステレオの場合は片方のチャンネルのみを使用
    if n_channels == 2:
        waveform = waveform[::2]

    # 波形データの正規化
    waveform_normalized = waveform / np.max(np.abs(waveform))

    # ピーク検出
    peaks, _ = find_peaks(waveform_normalized, height=0.5) # 高さの閾値を0.5に設定

    # ピークの時間を計算（秒単位）
    peak_times = peaks / framerate

    # AHAPファイルの基本構造を定義
    ahap_data = {
        "Version": 1,
        "Pattern": []
    }

    # 各ピークに対して触覚イベントを追加
    for peak_time in peak_times:
        event = {
            "Event": {
                "Time": peak_time,
                "EventType": "HapticTransient",
                "EventParameters": [
                    {"ParameterID": "HapticIntensity", "ParameterValue": 1.0},
                    {"ParameterID": "HapticSharpness", "ParameterValue": 1.0}
                ]
            }
        }
        ahap_data["Pattern"].append(event)

    # JSONデータをAHAPファイルとして保存
    with open(ahap_file_path, 'w') as file:
        json.dump(ahap_data, file, indent=2)

# 使用例
audio_file = 'sound.mp3' # ここに音ファイルのパスを指定
ahap_file = 'haptic_pattern.ahap' # 生成されるAHAPファイルの名前
create_ahap_from_audio(audio_file, ahap_file)
