# PlateauKit

[![PyPI](https://img.shields.io/pypi/v/plateaukit.svg)](https://pypi.org/project/plateaukit/)
<!-- [![PyPI downloads](https://img.shields.io/pypi/dm/plateaukit.svg)](https://pypistats.org/packages/plateaukit) -->

> Python library and converter for 3D city models by MLIT Project PLATEAU

PlateauKit は、<a href="https://www.mlit.go.jp/plateau/" target="_blank">国土交通省PLATEAUプロジェクト</a> 3D都市モデルを利用するためのPythonライブラリおよび変換ツールです。(WIP)

**ドキュメント Documentation:** <https://ozekik.github.io/plateaukit/>

## 機能 Features

- [x] PLATEAUデータセットのインストール・管理
- [x] GeoJSONへの変換
- [x] CityJSONへの変換 (citygml-tools / citygml4j 非依存)
- [x] データ変換の並列処理
- [ ] JupyterLab / Jupyer Notebookでの3D都市モデル表示 (LOD1/2)

## インストール Installation

```sh
pip install plateaukit
```

## ロードマップ Roadmap

- [ ] ドキュメントの整備
- [ ] データセットの軽量版のバンドルを提供
- [ ] ファイル分割の平均化
- [ ] テストの作成

## その他のツール・ライブラリ Alternatives

### Python

- [plateaupy](https://github.com/AcculusSasao/plateaupy)
  - [rhenerose/plateaupy](https://github.com/rhenerose/plateaupy)
- [plateau-geo-tools](https://github.com/raokiey/plateau-geo-tools)

### その他の言語

- [PLATEAU-SDK-for-Unreal](https://github.com/Project-PLATEAU/PLATEAU-SDK-for-Unreal)
- [PLATEAU-SDK-for-Unity](https://github.com/Project-PLATEAU/PLATEAU-SDK-for-Unity)
