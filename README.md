# PlateauKit

[![PyPI](https://img.shields.io/pypi/v/plateaukit.svg)](https://pypi.org/project/plateaukit/)
<!-- [![PyPI downloads](https://img.shields.io/pypi/dm/plateaukit.svg)](https://pypistats.org/packages/plateaukit) -->

> Python library and converter for 3D city models by MLIT Project PLATEAU

国土交通省PLATEAU 3D都市モデルのPythonライブラリおよび変換ツール (WIP)

**ドキュメント Documentation:** <https://ozekik.github.io/plateaukit/>

## 特徴 Features

- [x] PLATEAUデータセットのインストール・管理
- [x] 並列処理でのデータ変換
- [x] citygml-tools / citygml4j (Java) に依存せずCityJSONを生成 (一部)
- [ ] JupyterLab / Jupyer Notebookでの3D都市モデル表示 (LOD1/2)

## PlateauKitのインストール Install

```sh
pip install plateaukit
```

## コマンドライン Command-line

### PLATEAUデータをインストール/アンインストール

#### 利用可能な都市モデルの一覧を表示

```sh
plateaukit install --list
```

#### 都市モデルをダウンロード・インストール

```sh
# (方法1) 東京都23区のデータをダウンロードして追加
plateaukit install plateau-tokyo23ku

# (方法2) 事前にダウンロード済みの東京都23区のデータを追加 (CityGML)
plateaukit install plateau-tokyo23ku --local ./13100_tokyo23-ku_2020_citygml_3_2_op/ --format citygml
```

```sh
# 追加済みのデータの一覧を表示
plateaukit list
```

#### 都市モデルをアンインストール

```sh
# 東京都23区のデータをアンインストール
plateaukit uninstall plateau-tokyo23ku
```

### PLATEAU CityGMLからCityJSON/GeoJSONを生成

```sh
# 建造物 (bldg) データからLOD0/1相当のGeoJSONを生成
plateaukit generate-geojson --dataset plateau-tokyo23ku -t bldg /tmp/tokyo23ku-bldg.json
```

```sh
# 建造物 (bldg) データからLOD0/1/2相当のCityJSONを生成 (データセット指定未対応、ファイル単位)
plateaukit generate-cityjson ./udx/bldg/53395548_bldg_6697_2_op.gml /tmp/53395548_bldg_6697_2_op.cityjson
```

### PLATEAU CityGMLから属性情報を抽出

> TODO: ドキュメントの整備

## ライブラリ Library

> TODO: ドキュメントの整備

## ロードマップ Roadmap

- [ ] ドキュメントの整備
- [ ] データセットの軽量版のバンドルを提供
- [ ] ファイル分割の平均化
- [ ] テストの作成

## その他のツール・ライブラリ Alternatives

- [plateaupy](https://github.com/AcculusSasao/plateaupy)
  - [rhenerose/plateaupy](https://github.com/rhenerose/plateaupy)
- [raokiey/plateau-geo-tools](https://github.com/raokiey/plateau-geo-tools)
