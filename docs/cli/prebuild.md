
# 都市モデルデータの事前ビルド (CLI)

PlateauKit では、都市モデルのデータを事前に変換してデータベース化しておくことで、その後の利用時に高速にデータの読み込みや変換を行うことができます (事前ビルド)。

デフォルトでは、インストール時に建築物のデータ (LOD0/1) のみが事前ビルドされます。
道路や橋梁など、他の種類のデータも利用する場合は、[都市モデルをインストール](prebuild.md)後、`plateaukit prebuild` コマンドを利用して再度事前ビルドすることができます。

事前ビルドするデータの種類は `-t` オプションで指定します。
現時点で事前ビルドに対応しているデータの種類は以下の通りです。

- `bldg`: 建築物 (LOD0/1/2)
- `tran`: 道路
- `brid`: 橋梁

ただし、含まれているデータの種類は各都市モデルのデータセットによって異なります。
各都市モデルが提供するデータの種類については、都市モデルをインストール後、[`plateaukit info` コマンド](info.md)を利用して確認してください。

```bash title="例: 建築物 (`bldg`) と道路 (`tran`) のデータを事前ビルド"
plateaukit prebuild plateau-14382-hakone-machi-2020 -t bldg -t tran
```

<div class="result" markdown>

```bash title="実行例"
$ plateaukit prebuild plateau-14382-hakone-machi-2020 -t bldg -t tran
Generating GeoJSONSeq files: bldg Done ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Generating GeoJSONSeq files: tran Done ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Generating CityJSONSeq files: bldg Done ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Generating CityJSONSeq files: tran Done ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Writing Parquet files... Done
```

</div>

!!! warning ""
    サイズが大きいデータセットは処理に時間がかかる場合があります。
