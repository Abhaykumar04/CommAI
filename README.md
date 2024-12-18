# CommAI

CommAI is a voice assistant designed to help users improve their verbal communication skills through AI-powered practice and feedback. This README provides instructions for setting up and running the project.

![image](https://github.com/user-attachments/assets/9d695454-f520-40f9-bad3-766ef72d6753)


## Table of Contents

*   [Project Structure](#project-structure)
*   [Prerequisites](#prerequisites)
*   [Setup](#setup)
    *   [Environment Setup](#environment-setup)
    *   [Google Cloud Setup](#google-cloud-setup)
*   [Running the Application](#running-the-application)
*   [Code Overview](#code-overview)
    *   [Frontend (frontend.py)](#frontend-frontendpy)
    *   [Backend (backend.py)](#backend-backendpy)
*   [Contributing](#contributing)
*   [License](#license)

## Project Structure


## Prerequisites

1. **Python 3.8+:** Ensure you have Python 3.8 or a later version installed.
2. **Google Cloud Account:** A Google Cloud account with billing enabled.
3. **Google Cloud SDK:** Install the Google Cloud SDK. Follow the instructions here: [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)
4. **Service Account Key:**
    *   Create a service account in your Google Cloud project.
    *   Grant it the following roles:
        *   **Dialogflow API Client**
        *   **Cloud Datastore User**
        *   **Storage Admin**
        *   **Vertex AI User**
    *   Generate a JSON key file for the service account and download it.
    *   **Important:** Securely store this key file. Do not commit it to version control.

## Setup

### Environment Setup

1. **Clone the Repository:**

    ```bash
    git clone <repository_url>
    cd CommAI
    ```

2. **Create a Virtual Environment (Recommended):**

    ```bash
    python3 -m venv venv
    ```

3. **Activate the Virtual Environment:**

    *   **On Windows:**

        ```bash
        venv\Scripts\activate
        ```

    *   **On macOS/Linux:**

        ```bash
        source venv/bin/activate
        ```

4. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Google Cloud Setup

1. **Enable APIs:**
    *   Enable the following APIs in your Google Cloud project:
        *   **Cloud Speech-to-Text API**
        *   **Cloud Text-to-Speech API**
        *   **Cloud Firestore API**
        *   **Vertex AI API**

## Running the Application

1. **Execute the Frontend Script:**

    ```bash
    python frontend.py
    ```

2. **Access the Application:**
    *   The Gradio interface will launch in your default web browser.
    *   If it doesn't open automatically, look for the local URL printed in the console.
    *   You might get the sharing URL too, which you can use to share this application.

## Code Overview

### Frontend (`frontend.py`)

*   **Gradio Interface:** Creates the user interface using the `gradio` library.
*   **Scenario Handling:** Defines available scenarios and their descriptions.
*   **Audio Input:** Allows users to record or upload audio.
*   **Communication Analysis:** Sends audio and scenario data to the backend for processing.
*   **Feedback Display:** Presents the transcribed text, analysis results, and plays the generated audio feedback.

### Backend (`backend.py`)

*   **`VerbaCommunicationCoach` Class:**
    *   **`__init__`:** Initializes Google Cloud clients (Speech-to-Text, Text-to-Speech, Firestore) and the Vertex AI Gemini 1.5 Flash model.
    *   **`transcribe_audio`:** Transcribes audio to text using Google Cloud Speech-to-Text.
    *   **`analyze_communication`:** Analyzes the transcribed text based on the selected scenario using the Gemini model.
    *   **`generate_feedback_audio`:** Converts the analysis to speech using Google Cloud Text-to-Speech.
    *   **`log_interaction`:** Stores interaction data (user ID, scenario, transcript, analysis, timestamp) in Firestore.

## Contributing

Contributions are welcome! If you'd like to contribute to CommAI, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with clear, descriptive messages.
4. Push your branch to your forked repository.
5. Submit a pull request to the main repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. (You may need to add a LICENSE file to your repository).
