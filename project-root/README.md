# Project Overview

This project is designed to provide an integrated platform for educational content, including a chatbot for assistance, video lectures, and study materials in the form of notes and flashcards. The project is structured into several components, each serving a specific purpose.

## Project Structure

- **chatbot/**: Contains the chatbot functionality.
  - **backend/**: Backend code implemented using Python with frameworks like Flask or FastAPI. This includes routing, models, and business logic.
  - **frontend/**: User interface for the chatbot, including HTML, CSS, and JavaScript files for an interactive experience.
  - **tests/**: Testing files for both backend and frontend components, including unit tests and integration tests.

- **lecture_videos/**: Contains video lecture materials.
  - **scripts/**: Generated lecture scripts summarizing the content of the video lectures.
  - **audio/**: Narration files in audio formats (e.g., MP3, WAV) used for the video lectures.
  - **videos/**: Final MP4 videos of the completed lectures.
  - **code/**: Automation scripts for text-to-speech (TTS), video processing (Wav2Lip), and video editing (MoviePy).

- **notes_flashcards/**: Contains study materials.
  - **notes/**: Text notes summarizing key concepts, in markdown or plain text format.
  - **flashcards/**: Question-and-answer cards for study or review.
  - **code/**: Generator scripts for creating flashcards or notes from text files.

- **common/**: Shared resources across the project.
  - **assets/**: Shared assets such as logos, CSS files, and icons.
  - **templates/**: HTML templates for rendering views in the application.
  - **static/**: Static files like JavaScript and CSS used in the frontend.
  - **api/**: API endpoints that integrate features from different components of the project.

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd project-root
   ```

2. **Install dependencies**:
   - For the chatbot backend, navigate to the `chatbot/backend` directory and install the required Python packages.
   - For the frontend, ensure that all necessary JavaScript libraries are included.

3. **Run the application**:
   - Start the backend server.
   - Open the frontend in a web browser.

4. **Testing**:
   - Navigate to the `chatbot/tests` directory and run the test suite to ensure all components are functioning correctly.

## Usage Guidelines

- Access the chatbot through the designated frontend interface.
- View lecture videos and listen to audio narrations in the `lecture_videos/videos` and `lecture_videos/audio` directories.
- Utilize notes and flashcards for study purposes, found in the `notes_flashcards` directory.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.