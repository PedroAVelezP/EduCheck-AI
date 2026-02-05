
# EduCheck-AI

EduCheck-AI is an advanced AI-powered platform designed to automatically evaluate student tests and quizzes, streamlining the grading process for educators and providing instant, detailed feedback for students.

## Features
- **Automated Grading:** Uses state-of-the-art AI models to assess open-ended and multiple-choice responses.
- **Customizable Evaluation:** Supports custom answer keys and flexible grading criteria.
- **Detailed Feedback:** Provides justifications and scoring for each answer, helping students understand their results.
- **User-Friendly Interface:** Intuitive Gradio-based web interface for easy data upload, review, and result export.
- **Seamless Integration:** Easily integrates with CSV files for batch processing of student responses.

## Project Structure
```
EduCheck-AI/
├── main.py                # Entry point for launching the application
├── default_interface.py   # Main user interface (Gradio)
├── debug_interface.py     # Debug/testing interface
├── utils.py               # Core logic for grading and data processing
├── ollama_manager.py      # Manages Ollama AI model server
├── calificar.py           # Standalone grading script
├── Files/                 # Folder for input/output CSV files
├── Notebooks/             # Jupyter notebooks and documentation
├── README.md              # Project documentation
├── LICENSE.txt            # License information
```


## Installation
1. **Clone this repository:**
	```bash
	git clone https://github.com/yourusername/EduCheck-AI.git
	cd EduCheck-AI
	```
2. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```
3. **(Optional) Set up Ollama:**
	- Download and install [Ollama](https://ollama.com/) for local LLM inference.
	- Make sure the Ollama server is running before grading.

## Usage
### Launch the Main Application
```bash
python main.py --preset default
```
### Launch the Debug Interface
```bash
python main.py --preset debug
```
### Workflow
1. **Upload CSV:** Use the interface to upload your student responses and answer key files.
2. **Select Answer Key:** Identify the row containing the correct answers.
3. **Review Data:** Preview and confirm the data before grading.
4. **Grade:** Start the grading process and review the results.
5. **Export:** Download the graded results as a CSV file.

For more details, see the in-app instructions and comments in the code.

## Requirements
- Python 3.8+
- gradio
- pandas
- numpy
- lightrag
- ollama (for local LLM inference)


## Contributing
We welcome contributions from the community! To contribute:
- Fork the repository and create your branch from `main`.
- Commit your changes with clear messages.
- Open a pull request describing your changes.
- For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License. See [LICENSE.txt](LICENSE.txt) for full details.
