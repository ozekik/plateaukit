# PlateauKit + PlateauLab

[![PyPI](https://img.shields.io/pypi/v/plateaukit.svg)](https://pypi.org/project/plateaukit/)
<!-- [![PyPI downloads](https://img.shields.io/pypi/dm/plateaukit.svg)](https://pypistats.org/packages/plateaukit) -->

> Python library and utility for programming 3D city models by MLIT Project PLATEAU

PlateauKit は、<a href="https://www.mlit.go.jp/plateau/" target="_blank">国土交通省PLATEAUプロジェクト</a>の3D都市モデルを利用するためのPythonライブラリおよび変換ツールです。

PlateauLab は、<a href="https://jupyter.org" target="_blank">JupyterLab / Jupyter Notebook</a>上でPLATEAU都市モデルを扱うコーディング環境を実現するためのPythonライブラリです。 現在はPlateauKitの一部として提供しています。

**ドキュメント Documentation:** <https://ozekik.github.io/plateaukit/>

<div><video controls src="https://github.com/ozekik/plateaukit/assets/32771324/ea02df34-82f9-462a-b2e7-3f71dd3201ea" muted="false"></video></div>

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
- [ ] [ipydeck](https://github.com/ozekik/ipydeck)への移行
- [ ] JupyterLiteサポート
- [ ] 標高データの可視化
- [ ] LOD2サポート (WIP)

## その他のツール・ライブラリ Alternatives

- [Awesome PLATEAU](https://japan-opendata.github.io/awesome-plateau/)

### Python

- [plateaupy](https://github.com/AcculusSasao/plateaupy)
  - [rhenerose/plateaupy](https://github.com/rhenerose/plateaupy)
- [plateau-geo-tools](https://github.com/raokiey/plateau-geo-tools)

### その他

- Blender: [Plateau-Blender-Importer](https://github.com/nneri-hin/Plateau-Blender-Importer)
- Unreal Engine: [PLATEAU-SDK-for-Unreal](https://github.com/Project-PLATEAU/PLATEAU-SDK-for-Unreal)
- Unity: [PLATEAU-SDK-for-Unity](https://github.com/Project-PLATEAU/PLATEAU-SDK-for-Unity)

## ライセンス License

MIT License

PLATEAUデータセットの利用については、[国土交通省 Project PLATEAU](https://www.mlit.go.jp/plateau/site-policy/) の利用規約に従ってください。
