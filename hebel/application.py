#!flask/bin/python
import json
from flask import Flask, Response
from hebel.flaskrun import flaskrun
from hebel.apis.rest_api import apis
from hebel.frontend.views import frontend

# アプリケーションのインスタンス生成
app = application = Flask(__name__)

# ログテスト
app.logger.debug('app start')
app.logger.error('app start')
app.logger.info('app start')


# blueprintをアプリケーションに登録
app.register_blueprint(frontend)
app.register_blueprint(apis)

# views
@app.route('/', methods=['GET'])
def apis_get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)

@app.route('/', methods=['POST'])
def apis_post():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
    
    
    
if __name__ == '__main__':
    flaskrun(app)
