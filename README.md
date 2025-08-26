# SecondExperiment2025
2025年度の数理情報工学実験第二  

## 新機能: 1総通の電報形式対応
このバージョンでは、モールス信号による電報形式の音声生成に対応しました。

### 機能概要
- **TelegraphGen**: モールス符号による音声信号生成
- **対応文字**: A-Z, 0-9 (36文字)
- **制御パラメータ**: 
  - `speed`: モールス信号速度 (5-25 WPM)
  - `frequency`: 信号周波数 (400-1200 Hz) 
  - `character`: 送信文字選択
- **UI表示**: ゲーム画面で "Telegraph (電報)" として表示

### 技術仕様
- Paris標準タイミング準拠
- リアルタイム音声生成
- 既存の PulseGen, SineGen と同様にランダム選択対象

## 実行手順
1. 以下の「[leapcを使えるようにするsetup](#leapcを使えるようにするsetup)」を実行

1. wsl or macに応じて以下を実行

    - wslを使っている場合は、「[wslでusbを認識する方法](#wslでusbを認識する方法)」を実行

    - macを使っている場合は、 `brew install portaudio` を実行

1. poetryをセットアップ
```
poetry install --no-root
```

1. 以下で main を実行
```
poetry run python src/main.py
```


## leapcを使えるようにするsetup
poetryのversionが2以上であることを仮定します. (`poetry --version` で確認してください.)

1. leapc-python-bindingsサブモジュールをインストール
```
git submodule update --init --recursive
```

2. leapc-cffiの設定
```
poetry run python -m build leapc-python-bindings/leapc-cffi
poetry run pip install leapc-python-bindings/leapc-cffi/dist/leapc_cffi-0.0.1.tar.gz
```

3. poetryのinstall
```
poetry install --no-root
```

4. 実行できるか確認
```
poetry run python leapc-python-bindings/examples/tracking_event_example.py
```

## wslでusbを認識する方法
1. usbipd-winをインストールする(powershellで実行)  
```
winget install usbipd
```
2. usbの一覧を表示する(管理者権限のpowershellで実行)  
```
usbipd list
```
出力例：
```
BUSID  VID:PID    DEVICE                                                        STATE
1-6    2b7e:c757  FHD Webcam, IR Camera                                         Not shared
1-13   2936:1206  Ultraleap                                                     Not shared
```  
3. wslにusbをシェアできるようにする(管理者権限のpowershellで実行)  
```
usbipd bind --busid {BUSID}
```
上の{BUSID}にはUltraleapが接続されているBUSIDを入力してください. (2.の出力例から言えば1-13)  
なお、1度実行すればその後USBを接続し直してもこの操作をやり直す必要はありません. (2.でusbの一覧を表示したときにSTATEがSharedになっていれば大丈夫)

4. wslにusbをアタッチ(管理者権限のpowershellで実行)  
```
usbipd attach --wsl --busid {BUSID}
```

5. wslにusbがアタッチされていることを確認する(wslのターミナルで実行)
```
lsusb
```
