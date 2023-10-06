import threading
import pyaudio
import wave


class AudioRecorder(threading.Thread):
    # arg queue: Queue, record_length: int length of time to record, sample_rate: int, frames_per_buffer: int
    def __init__(self, queue, record_length=5, sample_rate=44100, frames_per_buffer=102, audio_path = "audio/recording.wav"):
        threading.Thread.__init__(self)
        self.queue = queue
        self.audio_path = audio_path
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
            #self.save_audio()
            self.frames = []
    
    # shutdown stream
    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    # save audio file
    def save_audio(self):
        with wave.open(self.audio_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))
            