# rebuilding force alignment using a wav2vec model 
# Force alignment script is based off PyTorch tutorial on force alignment

import torch 
import torchaudio 
from dataclasses import dataclass
import IPython
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# likely need to edit the transcript for this
def format_text(input_text):
    # Split the input text into words
    words = input_text.split()
    
    # Join the words with '|' and add leading and trailing '|'
    formatted_text = '|' + '|'.join(words) + '|'
    return formatted_text


## Step 1: Getting class label probability (1)

def class_label_prob(SPEECH_FILE):
    bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
    model = bundle.get_model().to(device)
    labels = bundle.get_labels()
    with torch.inference_mode():
        waveform, _ = torchaudio.load(SPEECH_FILE)
        emissions, _ = model(waveform.to(device))
        emissions = torch.log_softmax(emissions, dim=-1)

    emission = emissions[0].cpu().detach()
    return (bundle,waveform,labels, emission)


# Step 2: Getting the trellis: represents the probability of transcript labels
# occuring at each time frame

def trellis_algo(labels, ts, emission, blank_id=0):
    dictionary = {c: i for i, c in enumerate(labels)}
    transcript = format_text(ts)
    tokens = []
    for c in transcript:
        if c in dictionary:
            tokens.append(dictionary[c])
        else:
            tokens.append(0)
   # tokens = [dictionary[c] for c in transcript else '-'] 

        

    if not tokens:
        raise ValueError("Tokens list is empty. Check the input text and labels.")

    num_frame = emission.size(0)
    num_tokens = len(tokens)

    trellis = torch.zeros((num_frame, num_tokens))
    trellis[1:, 0] = torch.cumsum(emission[1:, blank_id], 0)
    trellis[0, 1:] = -float("inf")
    trellis[-num_tokens + 1 :, 0] = float("inf")

    for t in range(num_frame - 1):
        trellis[t + 1, 1:] = torch.maximum(
            trellis[t, 1:] + emission[t, blank_id],
            trellis[t, :-1] + emission[t, tokens[1:]],
        )
    return trellis, emission, tokens

# Step 3: most likely path using backtracking algorithm
@dataclass
class Point:
    token_index: int
    time_index: int
    score: float

def backtrack(trellis, emission, tokens, blank_id=0):
    t, j = trellis.size(0) - 1, trellis.size(1) - 1

    path = [Point(j, t, emission[t, blank_id].exp().item())]
    while j > 0:
        # Should not happen but just in case
        assert t > 0

        # 1. Figure out if the current position was stay or change
        # Frame-wise score of stay vs change
        p_stay = emission[t - 1, blank_id]
        p_change = emission[t - 1, tokens[j]]

        # Context-aware score for stay vs change
        stayed = trellis[t - 1, j] + p_stay
        changed = trellis[t - 1, j - 1] + p_change

        # Update position
        t -= 1
        if changed > stayed:
            j -= 1

        # Store the path with frame-wise probability.
        prob = (p_change if changed > stayed else p_stay).exp().item()
        path.append(Point(j, t, prob))

    # Now j == 0, which means, it reached the SoS.
    # Fill up the rest for the sake of visualization
    while t > 0:
        prob = emission[t - 1, blank_id].exp().item()
        path.append(Point(j, t - 1, prob))
        t -= 1

    return path[::-1]



# Step 4: Path segmentation
@dataclass
class Segment:
    label: str
    start: int
    end: int
    score: float

    def __repr__(self):
        return f"{self.label}\t({self.score:4.2f}): [{self.start:5d}, {self.end:5d})"

    @property
    def length(self):
        return self.end - self.start


def merge_repeats(path, transcript):
    i1, i2 = 0, 0
    segments = []
    while i1 < len(path):
        while i2 < len(path) and path[i1].token_index == path[i2].token_index:
            i2 += 1
        score = sum(path[k].score for k in range(i1, i2)) / (i2 - i1)
        segments.append(
            Segment(
                transcript[path[i1].token_index],
                path[i1].time_index,
                path[i2 - 1].time_index + 1,
                score,
            )
        )
        i1 = i2
    return segments


# Merge segments into words (each part also showcases the corresponding framerate)
# Merge words
def merge_words(segments, separator="|"):
    words = []
    i1, i2 = 0, 0
    while i1 < len(segments):
        if i2 >= len(segments) or segments[i2].label == separator:
            if i1 != i2:
                segs = segments[i1:i2]
                word = "".join([seg.label for seg in segs])
                score = sum(seg.score * seg.length for seg in segs) / sum(seg.length for seg in segs)
                words.append(Segment(word, segments[i1].start, segments[i2 - 1].end, score))
            i1 = i2 + 1
            i2 = i1
        else:
            i2 += 1
    return words


## Formatting portion, ensures that the time adheres to .ASS format
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours:01}:{minutes:02}:{seconds:05.2f}"

def display_segment(bundle, trellis, word_segments,waveform, i):
    ratio = waveform.size(1) / trellis.size(0)
    word = word_segments[i]
    x0 = int(ratio * word.start)
    x1 = int(ratio * word.end)
    start_time = x0 / bundle.sample_rate
    end_time = x1 / bundle.sample_rate
    formatted_start_time = format_time(start_time)
    formatted_end_time = format_time(end_time)
    print(f"{word.label} ({word.score:.2f}): {formatted_start_time} - {formatted_end_time} sec")
    segment = waveform[:, x0:x1]
    return (word.label, formatted_start_time, formatted_end_time)


# this portion converts it into ASS file format
def convert_timing_to_ass(timing_info, output_path):
    # Create the ASS file content
    ass_content = """[Script Info]
; Script generated by Python script
Title: Default ASS file
ScriptType: v4.00+
PlayResX: 384
PlayResY: 288
ScaledBorderAndShadow: yes
YCbCr Matrix: None

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,24,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,1,0,5,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    # Add each word with its timing as a dialogue event in the ASS file
    for word, start_time, end_time in timing_info:
        ass_content += f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{word}\n"

    # Write the ASS file content to the output file
    with open(output_path, 'w') as file:
        file.write(ass_content)