# GPT Notes

This is a project that records audio, transcribes the audio using OpenAI's Whisper API, and uses ChatGPT to take notes on the recorded text.

## Installation

To install the project, follow these steps:

1. Clone the repository to your local machine:

   ```
   git clone https://github.com/username/project.git
   ```

2. Install the required Python packages using pip:

   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory of your project and add your environment variables in the format `KEY=VALUE`. For example:

   ```
   OPENAI_API_KEY=1234567890abcdef
   ```

## Usage

To run the project, use the following command:

```
python main.py
```

This will start the audio recording and transcription process. The program will record audio data from the default input device using PyAudio, transcribe the audio data using OpenAI's API, and parse the resulting text using GPT. The response from GPT will be printed to the console.
