
# AWSでFlask(Python3)を使う方法


## 1. CodeStarでFlask(EC2)を作る

ElasticBeansTalkでもいいかも

## 2. CodeBuildを開いて,プロジェクトをpython2.7からpython3.6に変更

メンテナンスが進んでいないのか，デフォルトプロジェクトが2.7になってる.
Cloud9環境ではpython3の仮想環境を作るのがデフォルトなので，
Build時にエラーが出る場合がある．

## 3. cloud9で仮想環境構築

## 3.1 .gitignoreを作る

```
$ cd /home/ec2-user/environment/<yourproject>
$ curl https://www.gitignore.io/api/python > .gitignore
```

## 3.2 仮想環境構築

```

$ virtualenv -p python3 .venv
Running virtualenv with interpreter /usr/bin/python3
Using base prefix '/usr'
New python executable in /home/ec2-user/environment/<your-project>/.venv/bin/python3
Also creating executable in /home/ec2-user/environment/<your-project>/.venv/bin/python
Installing setuptools, pip, wheel...done.

$ source .venv/bin/activate
(.venv) nohara:~/environment/<your-project> (master) $ 

$ python -V
Python 2.7.14

(.venv) $ unalias python
(.venv) $ python -V
Python 3.6.5

```

## 3.3 テスト


```
(.venv) $ python setup.py pytest
(.venv) $ python setup.py install
```


## 3.4 念のために) version確認テストの追加

test_application.py

```py
import sys
import json
import pytest
from helloworld.application import application

@pytest.fixture
def client():
    return application.test_client()

def test_response(client):
    result = client.get()
    response_body = json.loads(result.get_data())
    assert result.status_code == 200
    assert result.headers['Content-Type'] == 'application/json'
    assert response_body['Output'] == 'Hello World'

# 追加
def test_version():
    assert sys.version_info.major == 3

```	

## 3.5. gitにアップロードする

```
cd /home/ec2-user/environment/<your-project>

git config --global user.name "T.Nohara"
git config --global user.email nohara@main.com

git add .
git commit -m "auto commit"
git push
```

## 4. 開発サーバー(Cloud9)でサーバーを立ち上げ，動作確認

## 4.1 ポートの開放

EC2を開き，開発しているCloud9のインスタンスを探す
aws-coud9-<project-name>-34164614341646416413413413
	みたいな名前があるはず．

インスタンスのセキュリティグループを開いて「インバウンド」にTCP:8000番ポートを開放する．

下のようなIPアドレスをコピーしておく

ec2-19-235-133-49.us-west-2.compute.amazonaws.com

## 4.2 開発サーバーの起動

```
(.venv) python helloworld/application.py --port 8000 --debug

```


## 4.3 Preview -> Configure Preview URLの設定

「Preview」 -> 「Configure Preview」 に以下のようにURLを入力

http://<IPアドレス>:<ポート番号>

http://ec2-19-235-133-49.us-west-2.compute.amazonaws.com:8000

これで「Preview」 -> Open Preview」 にてプレビューできる



## 5. プロジェクト名の変更

```
(.venv) nohara:~/environment/<your-project> (master) $ tree
.
├── appspec.yml
├── buildspec.yml
├── helloworld
│   ├── application.py
│   ├── flaskrun.py
│   ├── __init__.py
├── README.md
├── requirements.txt
├── scripts
│   ├── codestar_remote_access
│   ├── install_dependencies
│   ├── start_server
│   ├── stop_server
│   └── supervisord.conf
├── setup.py
├── template.yml
└── tests
    └── test_application.py

```

まずは現時点でテストが合格するか確認しておく

```
python setup.py pytest
```

具体的に変更するファイルは以下のとおり


```bash

ディレクトリ名の変更
/hellowold/ => /<your-project>/


ファイル名を変更
   files:
     - 'template.yml'
     - 'scripts/**/*'
-    - 'helloworld/**/*.py'
+    - '<your-project>/**/*.py'
     - 'appspec.yml'
     - 'requirements.txt'
     - 'setup.py'


/setup.py
 setup(
-    name='helloworld',
+    name='<your-project>',
     packages=find_packages(),
     include_package_data=True,
     install_requires=[

/tests/test_application.py
 import sys
 import json
 import pytest
-from helloworld.application import application
+from <your-project>.application import application
 


```


サイドテストして確認

```
python setup.py pytest
```

もし問題なければ，サーバーも再起動しましょう


```bash
// パッケージの再インストール
$ python setup.py install

// サーバーの再起動 (ファイル名を変えたので)
 $ python <your-project>/application.py --port 8000 --debug                              
 * Serving Flask app "application" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:8000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 203-144-628

```

もし問題なければ, git pushしましょう

## 6. Blueprintの環境構築


## 6.1 ディレクトリ構造の変更

```
.
├── <your-app>
│   ├── apis
│   │   ├── __init__.py
│   │   └── rest_api.py
│   ├── application.py
│   ├── flaskrun.py
│   ├── frontend
│   │   ├── __init__.py
│   │   └── views.py
│   ├── __init__.py
│   └── templates
│       └── frontend
│           ├── base.html
│           └── index.html
├── scripts
│   ├── codestar_remote_access
│   ├── install_dependencies
│   ├── start_server
│   ├── stop_server
│   └── supervisord.conf
└── tests
    └── test_application.py
├── appspec.yml
├── setup.py
├── template.yml
├── README.md
├── requirements.txt

```