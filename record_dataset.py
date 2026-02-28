import os
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

DURATION = 3  # seconds

def get_supported_samplerate():
    device_info = sd.query_devices(kind='input')
    print("\nUsing microphone:", device_info['name'])
    return int(device_info['default_samplerate'])

def record_samples(class_name, num_samples):
    folder = f"data/{class_name}"
    os.makedirs(folder, exist_ok=True)

    SAMPLE_RATE = get_supported_samplerate()
    print("Using Sample Rate:", SAMPLE_RATE)

    for i in range(num_samples):
        input(f"\nPress ENTER to record sample {i+1} for {class_name}...")
        print("Recording...")

        audio = sd.rec(
            int(DURATION * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype='float32'
        )
        sd.wait()

        audio = np.squeeze(audio)

        filename = f"{folder}/{class_name}_{i+1}.wav"
        write(filename, SAMPLE_RATE, audio)

        print(f"Saved: {filename}")

if __name__ == "__main__":
    print("Voice Dataset Recorder\n")

    record_samples("class0", 5)
    record_samples("class1", 5)

    print("\nRecording complete!")
    