import random
import time
import os
from multiprocessing import Process
from kafka import KafkaProducer
import pandas as pd
import numpy as np

def load_texts_from_parquet(parquet_files):
    all_texts = []
    for file in parquet_files:
        # Load the parquet file into a DataFrame
        df = pd.read_parquet(file)

        # Assuming the text data is in a column named 'text'
        if 'question' in df.columns:
            texts = df['question'].values
            text_values = [obj['text'] for obj in texts]
            all_texts.extend(text_values)
        else:
            print(f"Column 'text' not found in {file}. Available columns: {df.columns}")

    return all_texts

def producer(texts, strong_rate_1, strong_duration_1, strong_rate_2, strong_duration_2, weak_rate, weak_duration):
    producer = KafkaProducer(bootstrap_servers=['ip_address:9092'])
    topic = "as_you_wish_name"
    print("Kafka producer started - Data ingestion to chroma_stream")

    try:
        while True:  # Infinite loop
            elapsed_time = 0

            while elapsed_time < strong_duration_1:
                start_time = time.time()
                messages_per_second = np.random.poisson(strong_rate_1)

                for _ in range(messages_per_second):
                    sentence = random.choice(texts)
                    print(f"Sending: {sentence}")
                    producer.send(topic, sentence.encode('utf-8'))

                elapsed_time += 1
                time.sleep(max(0, 1.0 - (time.time() - start_time)))

            phase_2_start = elapsed_time
            while elapsed_time < phase_2_start + strong_duration_2:
                start_time = time.time()
                messages_per_second = np.random.poisson(strong_rate_2)

                for _ in range(messages_per_second):
                    sentence = random.choice(texts)
                    print(f"Sending: {sentence}")
                    producer.send(topic, sentence.encode('utf-8'))

                elapsed_time += 1
                time.sleep(max(0, 1.0 - (time.time() - start_time)))

            phase_3_start = elapsed_time
            while elapsed_time < phase_3_start + weak_duration:
                start_time = time.time()
                messages_per_second = np.random.poisson(weak_rate)

                for _ in range(messages_per_second):
                    sentence = random.choice(texts)
                    print(f"Sending: {sentence}")
                    producer.send(topic, sentence.encode('utf-8'))

                elapsed_time += 1
                time.sleep(max(0, 1.0 - (time.time() - start_time)))

    finally:
        producer.close()

if __name__ == "__main__":
    # Phase 1: Idle distribution 1 (2000 messages over 30 seconds)
    strong_duration_1 = 30
    strong_rate_1 = 2000 / strong_duration_1  # Messages per second for phase 1

    # Phase 2: Idle distribution 2 (3000 messages over 20 seconds)
    strong_duration_2 = 20
    strong_rate_2 = 3000 / strong_duration_2  # Messages per second for phase 2

    # Phase 3: Burst distribution (5000 messages over 10 seconds)
    weak_duration = 10
    weak_rate = 5000 / weak_duration  # Messages per second for phase 3

    # Path to the directory containing the parquet files
    parquet_directory = "./parquet" # wget https://discos.sogang.ac.kr/file/data/parquet.tar

    # Get the list of parquet files in the directory
    parquet_files = [os.path.join(parquet_directory, file) for file in os.listdir(parquet_directory) if file.endswith(".parquet")]

    # Load and extract text data from the parquet files
    texts = load_texts_from_parquet(parquet_files)

    # Start the producer with the defined message pattern
    Process(target=producer, args=(texts, strong_rate_1, strong_duration_1, strong_rate_2, strong_duration_2, weak_rate, weak_duration)).start()

