# PlateauKit

[![PyPI](https://img.shields.io/pypi/v/plateaukit.svg)](https://pypi.org/project/plateaukit/)
[![PyPI downloads](https://img.shields.io/pypi/dm/plateaukit.svg)](https://pypistats.org/packages/plateaukit)

PlateauKit は <a href="https://www.mlit.go.jp/plateau/" target="_blank">国土交通省 Project PLATEAU</a> の3D都市モデルを扱うための変換ツールおよび Python ライブラリです。<br />
[JupyterLab / Jupyter Notebook](https://jupyter.org/)上で3D都市モデルを扱うための [PlateauLab](lab/index.md) ライブラリも同梱しています。

- [ブラウザで試す (試験版)](/plateaukit/jupyterlite/notebooks/?path=demo.ipynb)

<!-- <figure markdown="span">
  ![landing image](./assets/landing.png){ width="320" }
</figure> -->

<div><video controls src="assets/sample2-web.mp4" muted="false"></video></div>

## 機能 Features

- [x] PLATEAUデータセットのインストール・管理
- [x] GeoJSON / CityJSONへの変換
    - Java製の外部ライブラリ (citygml4j, citygml-tools) 非依存
    - 並列処理に対応 (変換速度の向上)
    - 圧縮ファイルのまま変換可能 (省容量)
- [x] JupyterLab / Jupyer Notebookでの3D都市モデル表示 (LOD1/2)

## インストール Installation

```bash
pip install plateaukit
```

- [PlateauKitのインストール](install.md)を参照

<div style="margin-bottom:10rem"></div>
