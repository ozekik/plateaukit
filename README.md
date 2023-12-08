# PlateauKit

[![PyPI](https://img.shields.io/pypi/v/plateaukit.svg)](https://pypi.org/project/plateaukit/)
<!-- [![PyPI downloads](https://img.shields.io/pypi/dm/plateaukit.svg)](https://pypistats.org/packages/plateaukit) -->

> Python library and converter for 3D city models by MLIT Project PLATEAU

PlateauKit は、<a href="https://www.mlit.go.jp/plateau/" target="_blank">国土交通省PLATEAUプロジェクト</a> 3D都市モデルを利用するためのPythonライブラリおよび変換ツールです。(WIP)

**ドキュメント Documentation:** <https://ozekik.github.io/plateaukit/>

## 機能 Features

- [x] PLATEAUデータセットのインストール・管理
- [x] GeoJSONやCityJSONへの変換
    - Java製の外部ライブラリ (citygml4j, citygml-tools) に依存しません
    - 並列処理の実装により変換速度を向上
- [x] JupyterLab / Jupyer Notebookでの3D都市モデル表示 (LOD1)

## インストール Installation

```sh
pip install plateaukit
```

## ロードマップ Roadmap

- [x] ドキュメントの整備
- [ ] データセットの軽量版のバンドルを提供
- [ ] ファイル分割の平均化
- [ ] テストの整備

## その他のツール・ライブラリ Alternatives

### Python

- [plateaupy](https://github.com/AcculusSasao/plateaupy)
  - [rhenerose/plateaupy](https://github.com/rhenerose/plateaupy)
- [plateau-geo-tools](https://github.com/raokiey/plateau-geo-tools)

### その他

- Blender: [Plateau-Blender-Importer](https://github.com/nneri-hin/Plateau-Blender-Importer)
- Unreal Engine: [PLATEAU-SDK-for-Unreal](https://github.com/Project-PLATEAU/PLATEAU-SDK-for-Unreal)
- Unity: [PLATEAU-SDK-for-Unity](https://github.com/Project-PLATEAU/PLATEAU-SDK-for-Unity)
