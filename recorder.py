import threading
import pyaudio


class AudioRecorder(threading.Thread):
    # arg queue: Queue, record_length: int length of time to record, sample_rate: int, frames_per_buffer: int
    def __init__(self, queue, record_length=15, sample_rate=44100, frames_per_buffer=1024):
        threading.Thread.__init__(self)
        self.queue = queue
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.record_length = record_length
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=frames_per_buffer)
        
    # put last 100 frames into queue
    def run(self):
        while True:
            # 1024 is the number of frames per buffer
            # 44100 is the sample rate
            # To record x seconds of audio, we need to read 44100 * x samples. 
            # Since we are reading 1024 samples per buffer, we need to read 44100 * x / 1024 buffers in total.
            for i in range(0, int(44100 / 1024 * self.record_length)):
                data = self.stream.read(1024)
                self.frames.append(data)
            self.queue.put(self.frames)
            self.frames = []
    
    # shutdown stream
    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    
def record_audio(queue):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    frames = []
    while True:
        data = stream.read(1024)
        frames.append(data)
        if len(frames) == 100:
            queue.put(data)
            frames = []