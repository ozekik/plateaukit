
# PLATEAUデータの利用 (コマンドライン)

## PLATEAU CityGMLからGeoJSON/CityJSONを生成

`plateaukit generate-geojson` コマンドを使って、PLATEAU CityGMLから<a href="https://gis-oer.github.io/gitbook/book/materials/web_gis/GeoJSON/GeoJSON.html" target="_blank">GeoJSON</a>を生成することができます。

```bash title="例: 建造物 (bldg) データからLOD0/1相当のGeoJSONを生成"
plateaukit generate-geojson --dataset plateau-tokyo23ku -t bldg /tmp/tokyo23ku-bldg.json
```

また、`plateaukit generate-cityjson` コマンドを使って、PLATEAU CityGMLから<a href="https://www.cityjson.org/" target="_blank">CityJSON</a>を生成することができます。

```bash title="例: 建造物 (bldg) データからLOD0/1/2相当のCityJSONを生成 (データセット指定未対応、ファイル単位)"
plateaukit generate-cityjson ./udx/bldg/53395548_bldg_6697_2_op.gml /tmp/53395548_bldg_6697_2_op.cityjson
```

## PLATEAU CityGMLから属性情報を抽出

> TODO: ドキュメントの整備
