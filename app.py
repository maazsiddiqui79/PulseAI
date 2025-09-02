import os
import google.generativeai as genai
from flask import Flask, render_template, request ,url_for ,redirect
import markdown
# --- Flask App Initialization ---
app = Flask(__name__)

# --- Gemini API Configuration ---
# It's recommended to set your API key as an environment variable
# for security, but we'll place it here for simplicity.
# Example: genai.configure(api_key=os.environ["GEMINI_API_KEY"])
try:
    genai.configure(api_key="AIzaSyB_IrxoSLL02QCRQffSgCRQT-s8xnr7mxE")
    model = genai.GenerativeModel('gemini-2.5-flash')
    chat = model.start_chat(history=[])

except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    model = None
    
def get_genai_response(q):
    instructions = "You are an expert AI assistant. Provide comprehensive, accurate, and straightforward answers. Get directly to the point, avoid jargon, and use clear formatting for steps or lists when necessary."            
    # Combine your instructions with the user's input
    full_prompt = instructions + q
    response = model.generate_content(full_prompt)
    generated_text = response.text
    print(generated_text)
    return generated_text

# --- App Routes ---
generated_text = ""
user_prompt = ""
@app.route('/', methods=['GET', 'POST'])
def index():
    global generated_text 
    global user_prompt
    """
    Handles both displaying the form and processing the prompt.
    """

    if request.method == 'POST':
        user_prompt = request.form.get('prompt', '')
        if model and user_prompt:
            try:
                # Generate content using the Gemini model
                generated_text = markdown.markdown(get_genai_response(q=user_prompt))
            except Exception as e:
                # Handle potential API errors gracefully
                generated_text = f"An error occurred: {e}"
        elif not model:
            generated_text = "Gemini API is not configured. Please check your API key | Model is Absent"
            
        elif not user_prompt:
            generated_text = "User_Promt was absent "
        return redirect(url_for('index'))

    # Render the main page, passing the generated text and original prompt
    return render_template('index.html', generated_text=generated_text, user_prompt=user_prompt)

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True)