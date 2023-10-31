# [Application Name] ※要決定

## 概要

※要記入

## ローカル開発環境の構築手順

### 1. リポジトリをクローンする

```shell
git clone git@github.com:Hirakawa-Kaishi-Zemi/FastAPI.git
```

以降の手順は、プロジェクトディレクトリで行います。

```shell
cd /path/to/cloned/directory
```

### 2. 依存関係をインストールする

---

> ローカルにインストールされたグローバルなPythonインタプリタを使用する前に、
> プロジェクト固有の独立した Virtualenv 環境の利用を検討してください。\
> Virtualenv 環境は、ローカルコンピュータにインストールされたPythonとは別に、
> プロジェクトごとに独立した Python インタプリタ、サードパーティパッケージのバージョンを管理できる便利な機能です。

[Virtualenv](https://docs.python.org/ja/3/library/venv.html) を利用する場合は、以下の手順で作成・有効化を行います。

#### 仮想環境の作成

```shell
 # <venv> には仮想環境名を指定します。
 # (ex) python -m venv venv  -> `venv` という仮想環境を作成する
 
$ python -m venv <venv>
# or 
$ python3 -m venv <venv>
```

#### プラットフォーム別 仮想環境有効化

※ `<venv>` には作成した仮想環境名を指定してください

##### POSIX

- bash/zsh
    ```
    $ source <venv>/bin/activate
    ```

- PowerShell
    ```shell
    $ <venv>/bin/Activate.ps1
    ```

##### Windows

- cmd.exe
    ```shell
    C:\> <venv>\Scripts\activate.bat
    ```

- PowerShell
    ```shell
    PS C:\> <venv>\Scripts\Activate.ps1
    ```

---

依存関係にあるパッケージをインストールします。

```shell
pip install -r requirements.txt
```

ローカルのデータベースを作成します。

```shell
touch database.sqlite
```

> データベースファイル名は `.env` の `DB_DATABASE` で指定してください。 

### 3. API サーバーの起動

```shell
uvicorn main:app --reload
```

### 4. Fast API への理解

本プロジェクトは FastAPI を用いて開発されています。

さらなる情報は、[Fast API公式ドキュメント](https://fastapi.tiangolo.com/ja/#_3)を参照してください。
