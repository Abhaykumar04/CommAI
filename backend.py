import os
import vertexai
from google.generativeai import GenerativeModel
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech
from google.cloud import firestore
import io
from datetime import datetime

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "GOOGLE_APPLICATION_CREDENTIALS_Path"


class VerbaCommunicationCoach:
    def __init__(self):
        """
        Initialize the communication coach with required clients
        """
        try:
            self.speech_client = speech.SpeechClient()
            self.tts_client = texttospeech.TextToSpeechClient()
            self.db = firestore.Client()
            vertexai.init()
            self.model = GenerativeModel("gemini-2.0-flash-exp")
            # self.safety_settings = [
            #     {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            #     {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            #     {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            #     {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            # ]
            
        except Exception as e:
            raise InitializationError(f"Failed to initialize services: {str(e)}")

    def transcribe_audio(self, audio_path):
        """
        Transcribe audio file to text

        Args:
            audio_path (str): Path to the audio file

        Returns:
            str: Transcribed text or error message
        """
        if not audio_path or not os.path.exists(audio_path):
            return "Error: Invalid or missing audio file path"

        try:
            # Read audio file
            with open(audio_path, "rb") as audio_file:
                content = audio_file.read()

            # Configure audio recognition
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
                language_code="en-US",
                enable_automatic_punctuation=True,
                use_enhanced=True,
                model="latest_long",
                audio_channel_count=1,
                enable_word_time_offsets=True
            )

            # Perform transcription
            response = self.speech_client.recognize(config=config, audio=audio)

            if not response.results:
                return "No speech detected in the audio"

            transcript = " ".join(result.alternatives[0].transcript for result in response.results)
            return transcript.strip()

        except Exception as e:
            return f"Error transcribing audio: {str(e)}"

    def analyze_communication(self, transcript, scenario):
        """
        Analyze communication using Gemini model

        Args:
            transcript (str): Transcribed text to analyze
            scenario (str): Context/scenario for the communication

        Returns:
            str: Analysis results or error message
        """
        if not transcript or not scenario:
            return "Error: Missing transcript or scenario"

        if len(transcript.strip()) < 10:
            return "Error: Transcript too short for meaningful analysis"

        try:
            # Create detailed prompt
            prompt = f"""
            As a professional communication coach, analyze the following conversation/response:

            Context:
            - Scenario: {scenario}
            - Transcript: {transcript}

            Provide a detailed analysis covering:
            1. Clarity and Effectiveness:

            2. Tone and Professionalism:

            3. Areas for Improvement:

            4. Example

            Format the response in a clear, structured manner with distinct sections and must be written in 4 points not more then it and do not bold the points.
            """

            # Generate analysis
            response = self.model.generate_content(
                prompt,
                # safety_settings=self.safety_settings,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 1024,
                }
            )

            if response and hasattr(response, 'text'):
                return response.text

            return "Error: No analysis generated"

        except Exception as e:
            return f"Error analyzing communication: {str(e)}"

    def generate_feedback_audio(self, text):
        """
        Convert analysis text to speech with sound postive gesture and just speak the 4th point

        Args:
            text (str): Text to convert to speech

        Returns:
            bytes: Audio content or error message
        """
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)

            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                name="en-US-Neural2-F",
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
            )

            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=0.95,
                pitch=0.0,
                volume_gain_db=0.0
            )

            response = self.tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )

            return response.audio_content

        except Exception as e:
            print(f"Error generating audio feedback: {str(e)}")
            return None

    def log_interaction(self, user_id, scenario, transcript, analysis):
        """
        Log interaction details to Firestore

        Args:
            user_id (str): User identifier
            scenario (str): Communication scenario
            transcript (str): Original transcript
            analysis (str): Generated analysis
        """
        try:
            doc_ref = self.db.collection('interactions').document()
            doc_ref.set({
                'user_id': user_id,
                'scenario': scenario,
                'transcript': transcript,
                'analysis': analysis,
                'timestamp': firestore.SERVER_TIMESTAMP,
                'session_date': datetime.now().strftime("%Y-%m-%d")
            })

        except Exception as e:
            print(f"Error logging interaction: {str(e)}")
            pass


class InitializationError(Exception):
    """Custom exception for initialization errors"""
    pass
