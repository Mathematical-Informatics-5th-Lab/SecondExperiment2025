# SecondExperiment2025
2025年度の数理情報工学実験第二  

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
