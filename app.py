from flask import Flask, render_template, jsonify
from diff_match_patch import diff_match_patch
import html
import re

app = Flask(__name__)

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.read()

def convert_markdown_to_html(text):
    """Convert markdown headers to HTML"""
    lines = text.split('\n')
    html_lines = []
    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
        if line.startswith('###'):
            html_lines.append(f'<h3>{line.lstrip("#").strip()}</h3>')
        elif line.startswith('##'):
            html_lines.append(f'<h2>{line.lstrip("#").strip()}</h2>')
        elif line.startswith('#'):
            html_lines.append(f'<h1>{line.lstrip("#").strip()}</h1>')
        elif line.startswith('-') or line.startswith('*'):
            html_lines.append(f'<p class="bullet-point">{line[1:].strip()}</p>')
        else:
            html_lines.append(f'<p>{line}</p>')
    return '\n'.join(html_lines)

def extract_text_content(text):
    """Modified to work with text instead of file"""
    content = []
    lines = text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue

        # Check for headers (###, ##, #)
        if line.startswith('###'):
            content.append((line.lstrip('#').strip(), 'h3', False, ''))
        elif line.startswith('##'):
            content.append((line.lstrip('#').strip(), 'h2', False, ''))
        elif line.startswith('#'):
            content.append((line.lstrip('#').strip(), 'h1', False, ''))
        # Check for bullet points
        elif line.startswith('•') or line.startswith('-') or line.startswith('*'):
            content.append((line[1:].strip(), 'p', True, '•'))
        else:
            content.append((line, 'p', False, ''))

    return content

def compare_text_word_by_word(text1, text2):
    """
    Compare texts using Google's diff-match-patch library
    """
    dmp = diff_match_patch()
    diffs = dmp.diff_main(text1, text2)
    dmp.diff_cleanupSemantic(diffs)

    result = []
    for op, text in diffs:
        if not text:
            continue

        if op == 0:  # Equal
            result.append(html.escape(text))
        elif op == -1:  # Deletion
            result.append(f'<span class="removed">{html.escape(text)}</span>')
        elif op == 1:  # Addition
            result.append(f'<span class="added">{html.escape(text)}</span>')

    return ' '.join(result)

def compare_documents(doc1, doc2):
    """Modified to work with text instead of files"""
    content1 = extract_text_content(doc1)
    content2 = extract_text_content(doc2)

    html_content = ""

    for i in range(max(len(content1), len(content2))):
        if i < len(content1) and i < len(content2):
            text1, style1, is_bullet1, bullet_char1 = content1[i]
            text2, style2, is_bullet2, bullet_char2 = content2[i]

            compared_text = compare_text_word_by_word(text1, text2)

            if (is_bullet1 or is_bullet2) and style1.startswith('p'):
                html_content += f'<{style1} class="bullet-point">{compared_text}</{style1}>'
            else:
                html_content += f'<{style1}>{compared_text}</{style1}>'
        elif i < len(content1):
            text1, style1, is_bullet1, bullet_char1 = content1[i]
            if is_bullet1 and style1.startswith('p'):
                html_content += f'<{style1} class="bullet-point"><span class="removed">{html.escape(text1)}</span></{style1}>'
            else:
                html_content += f'<{style1}><span class="removed">{html.escape(text1)}</span></{style1}>'
        else:
            text2, style2, is_bullet2, bullet_char2 = content2[i]
            if is_bullet2 and style2.startswith('p'):
                html_content += f'<{style2} class="bullet-point"><span class="added">{html.escape(text2)}</span></{style2}>'
            else:
                html_content += f'<{style2}><span class="added">{html.escape(text2)}</span></{style2}>'

    return html_content

# Read documents from files
documents = {
    "1": read_file(r'C:\Users\Name\Document\#\01.txt'),
    "2": read_file(r'C:\Users\Name\Document\#\02.txt'),
    "3": read_file(r'C:\Users\Name\Document\#\03.txt'),
    "4": read_file(r'C:\Users\Name\Document\#\04.txt'),
    "5": read_file(r'C:\Users\Name\Document\#\05.txt')
}

# Updated prompts
prompts = {
    "1": "1. Your Prompt 01",
    "2": "2. Your Prompt 02",
    "3": "3. Your Prompt 03",
    "4": "4. Your Prompt 04",
    "5": "5. Your Prompt 05"
}

@app.route('/')
def index():
    return render_template('index.html', prompts=prompts)

@app.route('/get_content/<int:tab_id>')
def get_content(tab_id):
    if tab_id == 1:
        converted_content = convert_markdown_to_html(documents["1"])
        return jsonify({'content': converted_content, 'type': 'single'})
    elif 1 < tab_id <= 5:
        doc1 = documents[str(tab_id-1)]
        doc2 = documents[str(tab_id)]
        comparison = compare_documents(doc1, doc2)
        return jsonify({'content': comparison, 'type': 'comparison'})
    else:
        return jsonify({'error': 'Invalid tab ID'})

if __name__ == '__main__':
    app.run(debug=True)
