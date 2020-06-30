import json
from src.google_cloud.cloud_data_process import StorageData
from flask import Flask, render_template, request
from settings import SERVER_HOST, SERVER_PORT

app = Flask(__name__)
cloud_process = StorageData()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/extract', methods=['POST'])
def success():
    if request.method == 'POST':
        dir_url = request.form['dir_url']
        cloud_process.process_cloud_data(thread_id=0, dir_url=dir_url)

        return "success"


@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        data = {
            'process': cloud_process.progress,
            'upload_files': cloud_process.ret_file,
            'progress_bar': cloud_process.state
        }

        cloud_process.ret_file = []
        response = json.dumps(data)
        return response


if __name__ == '__main__':

    # app.run(debug=True, host=SERVER_HOST, port=SERVER_PORT)
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
