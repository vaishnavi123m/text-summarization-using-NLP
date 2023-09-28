from flask import Flask, render_template, request, send_file  # Import send_file to serve the PDF
from textsummary import summarizer, audio_to_text  # Import audio_to_text
import os
import pdfkit

app = Flask(__name__)

# Configure pdfkit to use wkhtmltopdf executable (replace 'path/to/wkhtmltopdf' with the actual path)
config = pdfkit.configuration(wkhtmltopdf='path/to/wkhtmltopdf')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyse', methods=['POST'])
def analyse():
    if request.method == 'POST':
        # Check if the user wants to upload an audio file
        if 'audio' in request.files:
            audio_file = request.files['audio']
            # Save the audio file temporarily and get its path
            audio_path = "temp_audio.wav"  # Adjust the file path as needed
            audio_file.save(audio_path)
            audio_text = audio_to_text(audio_path)
        else:
            audio_text = ""

        # Check if the user entered text manually in the form
        if 'rawtext' in request.form:
            rawtext = request.form['rawtext']
        else:
            rawtext = ""

        # Combine text and audio for summarization
        text_for_summarization = rawtext + " " + audio_text

        summary, original_txt, len_orig_txt, len_summary = summarizer(text_for_summarization)

        # Generate an HTML summary
        summary_html = f"<html><body>{summary}</body></html>"

        # Export to PDF
        pdfkit.from_string(summary_html, 'summary.pdf', configuration=config)

        # Serve the PDF to the user for download
        return send_file('summary.pdf', as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

