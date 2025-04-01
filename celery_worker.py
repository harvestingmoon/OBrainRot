from celery import Celery
import redis
import subprocess
import os

# Load environment variables
CELERY_QUEUE = os.getenv("CELERY_QUEUE", "default_queue")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "pyamqp://guest@rabbitmq//")

# Initialize Celery
celery = Celery(
    'long_task_worker',
    broker=CELERY_BROKER_URL,
    backend='redis://redis:6379/0'
)

# Redis client for storing task statuses
redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

@celery.task(bind=True)
def process_reddit_video(self, task_id, reddit_url, llm=False, scraped_url='texts/scraped_url.txt', 
                         output_pre='texts/processed_output.txt', final_output='texts/oof.txt', 
                         speech_final='audio/output_converted.wav', subtitle_path='texts/testing.ass', 
                         output_path='final/final.mp4', speaker_wav="assets/default.mp3", 
                         video_path='assets/subway.mp4'):
    
    redis_client.set(task_id, "PROCESSING")

    try:
        # Construct command
        command = f"python main.py --reddit_url '{reddit_url}' --llm {llm} --scraped_url '{scraped_url}'"
        command += f" --output_pre '{output_pre}' --final_output '{final_output}'"
        command += f" --speech_final '{speech_final}' --subtitle_path '{subtitle_path}'"
        command += f" --output_path '{output_path}' --speaker_wav '{speaker_wav}' --video_path '{video_path}'"

        # Execute `main()` in a subprocess
        subprocess.run(command, shell=True, check=True)

        # Save task result
        redis_client.set(task_id, f"COMPLETED: {output_path}")

    except subprocess.CalledProcessError:
        redis_client.set(task_id, "FAILED")

    return True
