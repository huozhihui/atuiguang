from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


@app.route('/')
def main():
    return render_template('main/index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=2000)