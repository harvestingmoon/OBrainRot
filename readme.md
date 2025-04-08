# Open Brain Rot 
![Logo](images/logo.jpg) 
<Created with Imagen 3>


### So i got extremely bored over the holidays and decided to just make a fun project to see if its possible to automate the kind of content i was seeing on TikTok

## A simple brain rot generator just by inserting your reddit url

### UI Interface
![UI Interface](images/ui.png)

To facilitate and make things easier to create videos, I have created a web interface.


## Example
[![Watch the video](images/thumbnail.png)](https://youtube.com/shorts/CRhbay8YvBg)


## Features

### Custom Image and Audio Assets:

**Image Overlays:**

To add your own image overlays, follow these steps:

1.  Create a new folder inside the `assets/` directory. Choose a descriptive name for your folder (e.g., `my_overlays`).

2.  Place your image files into this new folder. For optimal display, aim for images around 512 x 512 pixels in size. Common image formats like PNG and JPG are supported.

3.  Open the `main.py` file.

4.  Locate the `asset_name` variable.

5.  Replace the existing value of `asset_name` with the name of the folder you created in step 1 (e.g., if your folder is `my_overlays`, set `asset_name = "my_overlays"`).

**Audio Samples:**

To use custom audio samples:

1.  Place your audio files directly into the `assets/` directory. Common audio formats like MP3 and WAV are likely supported.

2.  Open the `main.py` file.

3.  Locate the relevant audio configuration (the specific variable name might vary depending on your code).

4.  Update the audio configuration to point to your audio file name.

**Pre-loaded Assets:**

For your convenience, four "brain rot" character images are already included in the `assets/` directory. You can use these directly by setting the `asset_name` in `main.py` to one of the following (case-sensitive):

* `trump`
* `spongebob`
* `lebron`
* `griffin`


## How it works 

### High Level Diagram
![Diagram](images/diagram.png)

### Switch
Deciding if its a thread or an actual link based on the link provided, if it is a thread it will go through a filter via VADER and llama 3.3 70b via sentiment analysis to see which thread to select, else it would enter directly into scraping.

### Scraping 
Simple webscraping using Reddit's open source API, to collect the title and story based off the reddit website

### Voice Translation:
Using Coqui's xTTSv2 (which is super lightweight , portable and accurate), I converted the text into audio. Coqui's TTS audio also allows you to use sample audios, so I used the common-man's TikTok audio. 

### Pre-processing:
Removal of certain punctuations, special characters via RegEx before we carry out force alignment.

### On Force Alignment: 
The most important step to generate the video was the alignment between audio and text in order to get the subtitle. This was achieved using forced alignment. In this, we used wav2vec2 and base it all on Motu Hira's tutorial on Forced alignment with Wav2Vec2. It uses a frame-wise label probality from the audio (that is the voice that we generated), creates a trellis matrix representing the probability of labels aligned per time step before using the most likely path from the trellis matrix.

### ffpmeg Magic:
Once we got the audio, video sample as well as the timestamp text (which is in .ass format btw), we can then generate the video using some simple ffmpeg magic. 

### Image Overlay
This is a new algorithm that basically imposes images on the video feed. So for every sentence that was spoken, it would then feed another image. The algorithm used was suprisingly more complex as it looks, involving aligning with time stamp and knowing when to switch between each new sentence structure.

``` video_generator.py ```

## How to run it

**Option 1: Local Installation**

All are important scripts within this, each deliberately separated so that it can be easier to include any upgrades in the future (and what not)

### Pre-requisites:
1. PyTorch (with CUDA 12.4)
2. Coqui TTS ([Link](https://github.com/coqui-ai/TTS))
3. FFMpeg ([Link](https://www.ffmpeg.org/))

Afterwards, just run the script 

```bash
python server.py
````

and you are good to go\!

Take note, when turning on the reddit link thread,


it will prompt for Groq API Key which can be acquired when you sign up as a Groq member. I will look into integrated other LLMs or creating your own heuristics too in the future :).

**Option 2: Docker Installation (Recommended)**

This project now includes a Dockerfile for easier setup.

### Prerequisites:

1.  Docker installed on your system.

### Steps:

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/harvestingmoon/OBrainRot.git
    cd OBrainRot
    ```

2.  **Build the Docker Image:**

    ```bash
    docker build -t obrainrot:latest .
    ```

3.  **Run the Docker Container:**

    ```bash
    docker run -it -p 8000:5000 obrainrot:latest /bin/bash
    ```

    This command will:

      * Run a container in interactive mode (`-it`).
      * Map port 8000 on your host machine to port 5000 in the container (`-p 8000:5000`).
      * Start a bash shell inside the container.

4.  **Edit the Reddit Link:**
    Inside the container's bash shell, navigate to the project directory and edit the Reddit link in `main.py` using a text editor like `nano` or `vim`.

5.  **Run the Script:**

    ```bash
    python3 main.py
    ```

    **Note:** Currently, `server.py` is not functioning correctly within the Docker environment.

## Others:

### Are there any future updates?

So far , yes there are but it is to hopefully create website or gradio to make this more user friendly, and to hopefully create more brain rot videos in the future (i am looking at OpenSora but no plans as of now)

## Thanks:

I would like to thank Motu Hira for creating this tutorial on Forced Alignment using Wav2Vec2. Without this, the subtitles would not be able to work (the original plan was to use CMUSphinx but the lack of community support made it difficult for me to work with)

Here is the original Tutorial if anyone is interested:

[Link](https://pytorch.org/audio/main/tutorials/forced_alignment_tutorial.html)

