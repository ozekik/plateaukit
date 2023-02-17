# PlateauKit

> Python library and converter for 3D city models by MLIT Project PLATEAU

国土交通省PLATEAU 3D都市モデルのPythonライブラリおよび変換ツール (WIP)

## 特徴 Features

- [x] 並列処理でのデータ変換
- [x] citygml-tools / citygml4j (Java) に依存せずCityJSONを生成 (一部)
- [ ] JupyterLab / Jupyer Notebookでの3D都市モデル表示 (LOD1/2)

## インストール Install

```sh
pip install plateaukit
```

## コマンドライン Command-line

### PLATEAUデータをダウンロード

#### 利用可能な都市モデルの一覧を表示

```sh
plateaukit install --list
```

#### 都市モデルをダウンロード・インストール

```sh
# 東京都23区のデータをダウンロードして追加
plateaukit install plateau-tokyo23ku
```

```sh
# ダウンロード済みの東京都23区のデータを追加 (CityGML)
plateaukit install plateau-tokyo23ku --local ./13100_tokyo23-ku_2020_citygml_3_2_op/ --format citygml
```

```sh
# 追加済みのデータの一覧を表示
plateaukit list
```

### PLATEAU CityGMLからCityJSON/GeoJSONを生成

```sh
# 建造物 (bldg) データからLOD0/1相当のGeoJSONを生成
plateaukit generate-geojson /tmp/tokyo23ku-bldg.json --dataset plateau-tokyo23ku -t bldg
```

```sh
# 建造物 (bldg) データからLOD0/1/2相当のCityJSONを生成 (データセット指定未対応)
plateaukit generate-cityjson ./udx/bldg/53395548_bldg_6697_2_op.gml /tmp/53395548_bldg_6697_2_op.cityjson
```

### PLATEAU CityGMLから属性情報を抽出

> TODO: ドキュメントの整備

## ロードマップ Roadmap

- [ ] ドキュメントの整備
- [ ] データセットの軽量版のバンドルを提供
- [ ] ファイル分割の平均化

## その他の選択肢 Alternatives

- [plateaupy](https://github.com/AcculusSasao/plateaupy)
  - [rhenerose/plateaupy](https://github.com/rhenerose/plateaupy)
