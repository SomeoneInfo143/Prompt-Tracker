# Prompt Tracker with Document Comparison

A Flask web application that tracks prompts and compares multiple versions of documents. The app features a side-by-side view of prompts and their corresponding documents, with a diff viewer that highlights changes between consecutive versions.

## Features

- Interactive prompt tracking with different versions
- Real-time document comparison between consecutive versions
- Markdown to HTML conversion for better readability
- Highlighted text differences (additions and deletions)
- Clean and responsive user interface
- Support for headers and bullet points

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/prompt-tracker.git
cd prompt-tracker
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install flask diff-match-patch
```

## Project Structure
```
prompt_tracker/
│
├── app.py                 # Main Flask application
├── static/
│   └── style.css         # CSS styles
├── templates/
│   └── index.html        # HTML template
└── documents/            # Your document files (create this folder)
    ├── v1.txt
    ├── v2.txt
    ├── v3.txt
    ├── v4.txt
    └── v5.txt
```

## Configuration

1. Open `app.py` and update the document paths in the `documents` dictionary:
```python
documents = {
    "1": read_file(r'path/to/your/v1.txt'),
    "2": read_file(r'path/to/your/v2.txt'),
    "3": read_file(r'path/to/your/v3.txt'),
    "4": read_file(r'path/to/your/v4.txt'),
    "5": read_file(r'path/to/your/v5.txt')
}
```

2. Customize the prompts in the `prompts` dictionary if needed.

## Usage

1. Run the application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

3. Use the interface:
   - Click prompts on the left sidebar to view different versions
   - Use the tabs at the top to navigate between versions
   - The first tab shows the original document
   - Subsequent tabs show comparisons between consecutive versions

## Document Format

Your text documents should use the following format:
- Use `#` for main headers
- Use `##` for subheaders
- Use `###` for sub-subheaders
- Use `-` or `*` for bullet points

Example:
```markdown
# Main Title
## Section 1
This is a paragraph.
- Bullet point 1
- Bullet point 2
### Subsection
More content here.
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask for the web framework
- diff-match-patch for the text comparison functionality
- Contributors and testers of the project

## Support

For support or questions, please open an issue in the GitHub repository.
