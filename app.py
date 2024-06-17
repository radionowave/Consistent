import gradio as gr
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predictions', methods=['POST'])
def handle_predictions():
    data = request.get_json()
    prompt = data['input']['prompt']
    # Виконайте необхідні операції з даними
    
    # Приклад відповіді
    response = {'result': f'Ви надіслали наступний проmpт: {prompt}'}
    return jsonify(response)

def run_local_server():
    app.run(host='localhost', port=8000, debug=True)

def predict(request: gr.Request, *args, progress=gr.Progress(track_tqdm=True)):
    prompt = args[0]
    
    headers = {'Content-Type': 'application/json'}
    payload = {"input": {"prompt": prompt}}
    
    try:
        response = requests.post("http://localhost:8000/predictions", headers=headers, json=payload)
        
        if response.status_code == 200:
            json_response = response.json()
            result = json_response["result"]
            return result
        else:
            raise gr.Error(f"The submission failed! Error: {response.status_code}")
    
    except Exception as e:
        raise gr.Error(f"An error occurred: {e}")

title = "Demo for consistent-character cog image by fofr"
description = "Create images of a given character in different poses • running cog image by fofr"

css="""
#col-container{
    margin: 0 auto;
    max-width: 1400px;
    text-align: left;
}
"""
with gr.Blocks(css=css) as app:
    with gr.Column(elem_id="col-container"):
        gr.HTML(f"""
        <h2 style="text-align: center;">Consistent Character Workflow</h2>
        <p style="text-align: center;">{description}</p>
        """)

        prompt = gr.Textbox(label="Prompt")
        output = gr.Textbox(label="Output")
        submit_btn = gr.Button("Submit")

    submit_btn.click(fn=predict, inputs=[prompt], outputs=[output])

if __name__ == '__main__':
    run_local_server()
    app.queue().launch()