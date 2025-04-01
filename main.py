from scraping import *
from audio import * 
from force_alignment import * 
from dict import * 
from video_generator import * 
from search import *
import os
from dotenv import load_dotenv
load_dotenv()
def main(reddit_url, llm  = False, scraped_url = 'texts/scraped_url.txt', output_pre = 'texts/processed_output.txt', \
          final_output = 'texts/oof.txt',speech_final = 'audio/output_converted.wav', subtitle_path = 'texts/testing.ass', \
            output_path = 'final/final.mp4',speaker_wav="assets/default.mp3", video_path = 'assets/subway.mp4'):
    print("L1: SCRAPING RIGHT NOW")
    if not llm:
        map_request = scrape(reddit_url)
    else:
        print("Using LLM to determine best thread to scrape")
        print("-------------------")
        reddit_scrape = scrape_llm(reddit_url)
        text = vader(reddit_scrape)
        api = os.getenv('GROQ_API_KEY')
        map_request= groq(text, api) 
    print(map_request)
    save_map_to_txt(map_request,scraped_url)
    # ## AUDIO CONVERSION 
    print("L2: AUDIO CONVERSION NOW (TAKES THE LONGEST)")
    audio(scraped_url, speaker_wav = speaker_wav)
    convert_audio('audio/output.wav',speech_final)
    
    # IMPORTANT PRE PROCESSING STUFF 
    process_text(scraped_url, output_pre)
    process_text_section2(output_pre, final_output)

    with open(final_output, 'r') as file: 
        text = file.read().strip()
    
    # A BUNCH OF HARDCORE FORCED ALIGNMENT FORMATTING
    print("L3: FORCE ALIGNMENT")
    transcript = format_text(text)
    bundle, waveform, labels, emission1 = class_label_prob(speech_final)
    trellis,emission,tokens = trellis_algo(labels,text,emission1)
    path = backtrack(trellis, emission, tokens)
    segments = merge_repeats(path, transcript)
    word_segments = merge_words(segments)
    timing_list = []
    for (i, word) in enumerate(word_segments):
        timing_list.append((display_segment(bundle, trellis, word_segments, waveform, i)))
    
    # FINAL VIDEO
    print("L4: VIDEO GENERATION")
    convert_timing_to_ass(timing_list, subtitle_path)

    ## Finally, we need to generate the brain rot video tself
    add_subtitles_and_overlay_audio(video_path,speech_final, subtitle_path, output_path)
    print("DONE! SAVED AT " + output_path)

if __name__ == "__main__":
    main("https://www.reddit.com/r/confession/comments/1ja2f08/i_am_exploiting_my_employer_and_i_have_never_been/", llm = False)