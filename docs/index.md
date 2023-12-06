# PlateauKit

[![PyPI](https://img.shields.io/pypi/v/plateaukit.svg)](https://pypi.org/project/plateaukit/)
<!-- [![PyPI downloads](https://img.shields.io/pypi/dm/plateaukit.svg)](https://pypistats.org/packages/plateaukit) -->

PlateauKit は、<a href="https://www.mlit.go.jp/plateau/" target="_blank">国土交通省 Project PLATEAU</a> の3D都市モデルを扱うためのオープンソース Python ライブラリおよび変換ツールです。

![landing image](./assets/landing.png)

## 機能 Features

- [x] PLATEAUデータセットのインストール・管理
- [x] GeoJSONやCityJSONへの変換
    - Java製の外部ライブラリ (citygml4j, citygml-tools) に依存しません
    - 並列処理の実装により変換速度を向上
- [x] JupyterLab / Jupyer Notebookでの3D都市モデル表示 (LOD1)

## インストール Installation

```bash
pip install plateaukit
```

- [PlateauKitのインストール](install.md)を参照

## ライセンス License

MIT License

<div style="margin-bottom:10rem"></div>