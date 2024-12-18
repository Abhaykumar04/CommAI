# frontend.py
import gradio as gr
from backend import VerbaCommunicationCoach
import os


class VerbaConfidenceApp:
    def __init__(self):
        """Initialize the VerbaConfidenceApp with scenarios and coach"""
        # Define scenarios first before initializing the coach
        self.scenarios = [
            "Hotel Room Booking",
            "Restaurant Interaction", 
            "Retail Negotiation",
            "Job Interview Preparation",
            "Professional Introduction"
        ]
        
        self.scenario_descriptions = {
            "Hotel Room Booking": "Practice booking a hotel room, discussing amenities, and handling special requests",
            "Restaurant Interaction": "Practice making reservations, ordering food, and communicating with restaurant staff",
            "Retail Negotiation": "Practice negotiating prices, discussing product features, and making purchases",
            "Job Interview Preparation": "Practice common interview questions and professional responses",
            "Professional Introduction": "Practice introducing yourself in professional settings and networking events"
        }
        
        try:
            self.coach = VerbaCommunicationCoach()
        except Exception as e:
            print(f"Initialization Error: {str(e)}")
    
    def process_audio(self, audio, scenario):
        """
        Process audio input and generate analysis
        """
        if not audio:
            return "No audio provided", "Please record or upload audio", None
            
        if not scenario:
            return "No scenario selected", "Please select a scenario", None
            
        try:
            # Validate uploaded file
            if not os.path.exists(audio):
                return "Error: Invalid audio file path", "Audio file not found", None

            # Transcribe audio
            transcript = self.coach.transcribe_audio(audio)
            if "Error" in transcript:
                return transcript, "Transcription failed", None
            
            # Analyze communication
            analysis = self.coach.analyze_communication(transcript, scenario)
            if "Error" in analysis:
                return transcript, analysis, None
            
            # Generate audio feedback
            feedback_audio = self.coach.generate_feedback_audio(analysis)
            if not feedback_audio:
                return transcript, analysis, "Audio feedback generation failed"
            
            # Save feedback audio
            feedback_audio_path = "feedback_output.mp3"
            with open(feedback_audio_path, "wb") as audio_file:
                audio_file.write(feedback_audio)
            
            # Log interaction
            self.coach.log_interaction("demo_user", scenario, transcript, analysis)
            
            return transcript, analysis, feedback_audio_path
        
        except Exception as e:
            return f"Error Processing: {str(e)}", "Analysis failed", None
    
    def launch_app(self):
        """Create and configure Gradio interface"""
        with gr.Blocks(theme=gr.themes.Soft()) as demo:
            # Header
            gr.Markdown(
                """
                <div style="text-align: center;">
                <h1 style="font-weight: bold;">CommAI 🗣️</h1>
                <h3 style="font-weight: bold;">Improve your communication skills with AI-powered feedback</h3>
                </div>
                """
            )
            
            # Main interface
            with gr.Row():
                # Left column - Input
                with gr.Column():
                    scenario_dropdown = gr.Dropdown(
                        choices=self.scenarios,
                        label="Choose Scenario",
                        info="Select the type of interaction you want to practice"
                    )
                    
                    scenario_info = gr.Markdown()
                    
                    audio_input = gr.Audio(
                        sources=["microphone", "upload"],
                        type="filepath",
                        label="Record or Upload Your Speech",
                        interactive=True
                    )
                    
                    submit_btn = gr.Button(
                        "Analyze Communication",
                        variant="primary"
                    )

                    feedback_audio_output = gr.Audio(
                        label="AI Response",
                        type="filepath"
                    )
                
                # Right column - Output
                with gr.Column():
                    transcript_output = gr.Textbox(
                        label="Transcribed Speech",
                        lines=4,
                        interactive=False
                    )
                    
                    analysis_output = gr.Textbox(
                        label="Communication Analysis",
                        lines=8,
                        interactive=False
                    )
                    
                    
            # Event handlers
            def update_scenario_info(scenario):
                return self.scenario_descriptions.get(scenario, "")
            
            scenario_dropdown.change(
                fn=update_scenario_info,
                inputs=[scenario_dropdown],
                outputs=[scenario_info]
            )
            
            submit_btn.click(
                fn=self.process_audio,
                inputs=[audio_input, scenario_dropdown],
                outputs=[transcript_output, analysis_output, feedback_audio_output],
                api_name="analyze_communication"
            )
            
            # Footer
            gr.Markdown(
                """
                ### Tips for best results:
                - Speak clearly and at a normal pace
                - Use a quiet environment for recording
                - Keep responses concise and focused
                - Practice different scenarios regularly
                """
            )
        
        return demo

# Main execution
if __name__ == "__main__":
    try:
        app = VerbaConfidenceApp()
        demo = app.launch_app()
        demo.launch(
            share=True,
        )
    except Exception as e:
        print(f"Application Error: {str(e)}")
