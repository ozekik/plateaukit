# PlateauKit + PlateauLab

[![PyPI](https://img.shields.io/pypi/v/plateaukit.svg)](https://pypi.org/project/plateaukit/)
[![build](https://github.com/ozekik/plateaukit/actions/workflows/ci.yaml/badge.svg)](https://github.com/ozekik/plateaukit/actions/workflows/ci.yaml)
[![Coverage Status](https://codecov.io/gh/ozekik/plateaukit/branch/master/graph/badge.svg)](https://codecov.io/gh/ozekik/plateaukit)
[![PyPI downloads](https://img.shields.io/pypi/dm/plateaukit.svg)](https://pypistats.org/packages/plateaukit)

> Python library and utility for programming 3D city models by MLIT Project PLATEAU

**PlateauKit** は、<a href="https://www.mlit.go.jp/plateau/" target="_blank">国土交通省PLATEAUプロジェクト</a>の3D都市モデルを利用するための変換ツールおよびPythonライブラリです。

**PlateauLab** は、<a href="https://jupyter.org" target="_blank">JupyterLab / Jupyter Notebook</a>上でPLATEAU都市モデルを扱うコーディング環境を実現するためのPythonライブラリです。 現在はPlateauKitの一部として提供しています。

- **ドキュメント Documentation:** <https://ozekik.github.io/plateaukit/>
<!-- - **ブラウザで試す (試験版) Try in Your Browser (Experimental):** <https://ozekik.github.io/plateaukit/jupyterlite/notebooks/?path=demo.ipynb> -->

## 目次 Table of Contents

- [機能 Features](#機能-features)
- [インストール Installation](#インストール-installation)
- [活用事例・紹介 Use Cases & Mentions](#活用事例紹介-use-cases--mentions)
- [ロードマップ Roadmap](#ロードマップ-roadmap)
- [その他のツール・ライブラリ Alternatives](#その他のツールライブラリ-alternatives)
- [発表資料 Presentations](#発表資料-presentations)
- [クレジット Credits](#クレジット-credits)
- [ライセンス License](#ライセンス-license)

## 機能 Features

- [x] PLATEAUデータセットのインストール・管理
- [x] GeoJSON / CityJSONへの変換
    - Java製の外部ライブラリ (citygml4j, citygml-tools) 非依存
    - 並列処理に対応 (変換速度の向上)
    - 圧縮ファイルのまま変換可能 (省容量)
- [x] JupyterLab / Jupyer Notebookでの3D都市モデル表示 (LOD1/2)

<div><video controls src="https://github.com/ozekik/plateaukit/assets/32771324/ea02df34-82f9-462a-b2e7-3f71dd3201ea" muted="false"></video></div>

## インストール Installation

```sh
pip install 'plateaukit[all]'
```

- 詳細は[PlateauKitのインストール](https://ozekik.github.io/plateaukit/install/)を参照

## 活用事例・紹介 Use Cases & Mentions

PlateauKit + PlateauLab を開発の一部などでお使いいただいている事例やご紹介いただいている事例です。
事例の追加・修正は[Issues](https://github.com/ozekik/plateaukit/issues)または[Pull Requests](https://github.com/ozekik/plateaukit/pulls)からお知らせください。

- **[PythonでPLATEAUのデータを手軽に扱ってみる](https://youtu.be/D1JMQfmGwpg?si=tlSnFmwtkDPJPGd4&t=11949) (ぴっかりん ([@raokiey](https://github.com/raokiey)) 氏)** FOSS4G 2024 Japan コアデイ
  - <https://github.com/raokiey/foss4g_2024_japan_general_presentation_25>
- **[AIまちづくりファシリテーター](https://protopedia.net/prototype/6072) (チーム シャキシャキ)** 🏆**グランプリ**, PLATEAU Hack Challenge 2024 in Tokyo
- **[PLATEAUを利用した名古屋市の犯罪マップと類似領域検索](https://www.mlit-data.jp/#/ShowcaseDetail?id=Showcase18) (向 直人氏)** 🏆**国土交通データプラットフォーム特別賞**, アーバンデータチャレンジ2023 with 土木学会インフラデータチャレンジ2023

## ロードマップ Roadmap

- [x] ドキュメントの整備
- [x] 最小限のテストの整備
- [x] [ipydeck](https://github.com/ozekik/ipydeck)対応
- [x] JupyterLiteサポート
- [x] LOD2サポート
- [ ] 標高データのサポート・可視化
- [ ] 軽量版データセットの提供
- [ ] テストの拡充
- [ ] 変換の高速化

## その他のツール・ライブラリ Alternatives

- [Awesome PLATEAU](https://japan-opendata.github.io/awesome-plateau/)

### Python

- [plateaupy](https://github.com/AcculusSasao/plateaupy) (Open3D/Blender)
  - [rhenerose/plateaupy](https://github.com/rhenerose/plateaupy)
- [plateau-geo-tools](https://github.com/raokiey/plateau-geo-tools) (GeoJSON)

### その他

- Blender: [Plateau-Blender-Importer](https://github.com/nneri-hin/Plateau-Blender-Importer)
- Unreal Engine: [PLATEAU SDK for Unreal](https://github.com/Project-PLATEAU/PLATEAU-SDK-for-Unreal)
- Unity: [PLATEAU SDK for Unity](https://github.com/Project-PLATEAU/PLATEAU-SDK-for-Unity)

## 発表資料 Presentations

- **[PlateauKit + PlateauLabによる都市空間プログラミング](https://www.mlit.go.jp/plateau/file/events/doc/20240528_dxkaigi_Ozeki-shi.pdf)** まちづくりDX全国会議 presented by 国土交通省都市局[↗](https://www.mlit.go.jp/plateau/journal/j061/)
- **[PlateauKit + PlateauLab](https://speakerdeck.com/toshiseisaku/no-dot-4-plateaukit-plus-plateaulab)** PLATEAU AWARD 2023[↗](https://www.mlit.go.jp/plateau-next/2023/award/)

## クレジット Credits

- `tests/fixtures/30422_taiji-cho_2021_citygml_2_op.zip`, `tests/fixtures/30422_taiji-cho_city_2021_citygml_4_op.zip`: PLATEAUデータセット ([国土交通省 Project PLATEAU](https://www.mlit.go.jp/plateau/site-policy/), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ja))

## ライセンス License

MIT License

PLATEAUデータセットの利用については、[国土交通省 Project PLATEAU](https://www.mlit.go.jp/plateau/site-policy/) の利用規約に従ってください。
