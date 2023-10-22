import librosa
import itertools
from pydub import AudioSegment
from pydub.silence import detect_silence

# 데시벨(dB) 값을 실제 파형의 진폭 값으로 변환
def db_to_float(db, using_amplitude=True):
    db = float(db)

    if using_amplitude:
        return 10 ** (db / 20)
    else:  # using power
        return 10 ** (db / 10)
    

# 침묵 탐지
def detect_silence(audio_segment, min_silence_len=1000, silence_thresh=-16, seek_step=1):

    seg_len = len(audio_segment)

    if seg_len < min_silence_len:
        return []

    silence_thresh = db_to_float(silence_thresh) * audio_segment.max_possible_amplitude

    silence_starts = []

    last_slice_start = seg_len - min_silence_len
    slice_starts = range(0, last_slice_start + 1, seek_step)

    if last_slice_start % seek_step:
        slice_starts = itertools.chain(slice_starts, [last_slice_start])

    for i in slice_starts:
        audio_slice = audio_segment[i:i + min_silence_len]
        if audio_slice.rms <= silence_thresh:
            silence_starts.append(i)

    if not silence_starts:
        return []

    silent_ranges = []

    prev_i = silence_starts.pop(0)
    current_range_start = prev_i

    for silence_start_i in silence_starts:
        continuous = (silence_start_i == prev_i + seek_step)

        silence_has_gap = silence_start_i > (prev_i + min_silence_len)

        if not continuous and silence_has_gap:
            silent_ranges.append([current_range_start,
                                  prev_i + min_silence_len])
            current_range_start = silence_start_i
        prev_i = silence_start_i

    silent_ranges.append([current_range_start,
                          prev_i + min_silence_len])

    return silent_ranges


# 음성을 특정 dBFS로 전처리
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


# 비침묵 구간 탐지
def detect_nonsilent(audio_segment, min_silence_len=900, silence_thresh=-16, seek_step=1):

  silent_ranges = detect_silence(audio_segment, min_silence_len, silence_thresh, seek_step)
  len_seg = len(audio_segment)

  if not silent_ranges:
    print('침묵 구간이 존재하지 않음')
    return [[0, len_seg]]

  if silent_ranges[0][0] == 0 and silent_ranges[0][1] == len_seg:
    print('모든 구간이 침묵')
    return []

  prev_end_i = 0
  nonsilent_ranges = []
  for start_i, end_i in silent_ranges:
      nonsilent_ranges.append([prev_end_i, start_i])
      prev_end_i = end_i

  if end_i != len_seg:
      nonsilent_ranges.append([prev_end_i, len_seg])

  if nonsilent_ranges[0] == [0, 0]:
      nonsilent_ranges.pop(0)

  return nonsilent_ranges


# 원본 음성에서 침묵 구간을 뺀 음성 만듦
def only_voice(audio_file, min_silence_length = 900, silence_thresh=-16):

  non_silence_ranges = detect_nonsilent(audio_file, min_silence_len = min_silence_length, silence_thresh = silence_thresh)

  non_silence_start = audio_file[0][0]
  non_silence_end = audio_file[0][1]

  print(non_silence_start, non_silence_end)

  non_silence_audio_combined = AudioSegment.empty()

  for non_silence_range in non_silence_ranges:

    non_silence_audio = audio_file[non_silence_range[0]-300:non_silence_range[1]+300]
    non_silence_audio_combined += non_silence_audio

  return non_silence_audio_combined


# 작은 데시벨의 소음과 무음 잘라서 저장
def trim_audio_data(audio_files):

  trimmed_audio_data = []
  top_db=40

  for audio_file in audio_files:
    y, sr = librosa.load(audio_file, sr=16000)
    y_trimmed, idx  = librosa.effects.trim(y, top_db=top_db)

    start_idx, end_idx = idx[0], idx[1]

    trimmed_sound = y_trimmed[start_idx:end_idx]
    trimmed_audio_data.append(trimmed_sound)

  return trimmed_audio_data