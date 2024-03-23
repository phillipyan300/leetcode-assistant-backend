import os
import openai
import time
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

# Upload file
print('Uploading file...')
file = openai.files.create(
    file=open("training.jsonl", "rb"),
    purpose='fine-tune'
)

print('File uploaded: ', file)

# Check if file is ready
print('Checking file status...')
while file.status != 'processed':
    time.sleep(10)
    file = openai.File.retrieve(file.id)
    print('File status:', file.status)

    # If file fails, print error and exit
    if file.status != 'processed':
        print('File failed:', file)
        exit(1)

# Create fine-tuning job
print('Creating fine-tuning job...')
job = openai.FineTuningJob.create(
    training_file=file.id, model="gpt-3.5-turbo")

print('Job created.')
print(job)

# Loop until status is succeeded. Print status every 60 seconds
while job.status != 'succeeded':
    time.sleep(10)
    job = openai.FineTuningJob.retrieve(job.id)
    print('Job status:', job.status)

    # If job fails, print error and exit
    if job.status != 'running' and job.status != 'succeeded':
        print('Job failed:', job)
        exit(1)

print('Job completed.')
print('Fine-tuned model:', job.fine_tuned_model)