
# PLATEAUデータの利用 (コマンドライン)

## CityGMLからGeoJSON/CityJSONを生成

### GeoJSON

`plateaukit generate-geojson` コマンドを使用して、PLATEAU CityGML から <a href="https://gis-oer.github.io/gitbook/book/materials/web_gis/GeoJSON/GeoJSON.html" target="_blank">GeoJSON</a> を生成することができます。

```bash title="例: 建造物 (bldg) データからLOD0/1相当のGeoJSONを生成"
plateaukit generate-geojson --dataset plateau-tokyo23ku -t bldg /tmp/tokyo23ku-bldg.json
```

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [139.759939, 35.658638, 11.195],
            [139.759957, 35.658628, 11.195],
            [139.75997, 35.658642, 11.195],
            [139.759971, 35.658643, 11.195],
            [139.759999, 35.658676, 11.195],
            [139.759997, 35.658677, 11.195],
            [139.759986, 35.658683, 11.195],
            [139.760003, 35.658703, 11.195],
            [139.759813, 35.658813, 11.195],
            [139.759783, 35.658778, 11.195],
            [139.759826, 35.658718, 11.195],
            [139.759857, 35.6587, 11.195],
            [139.759848, 35.65869, 11.195],
            [139.759866, 35.65868, 11.195],
            [139.759939, 35.658638, 11.195]
          ]
        ]
      },
      "properties": {
        "id": "BLD_1afa2b8d-ad6c-41f8-85a8-2c482717e5a5",
        "measuredHeight": 11.0
      }
    },
    // ...
  ]
}
```

### CityJSON

`plateaukit generate-cityjson` コマンドを使用して、PLATEAU CityGML から <a href="https://www.cityjson.org/" target="_blank">CityJSON</a> を生成することができます。(現在 LOD1 をサポート)

```bash title="例: 建造物 (bldg) データからLOD1相当のCityJSONを生成"
plateaukit generate-cityjson --dataset plateau-tokyo23ku /tmp/tokyo23ku-bldg.city.json
```

```json
{
  "type": "CityJSON",
  "version": "2.0",
  "extensions": {},
  "transform": { "scale": [1.0, 1.0, 1.0], "translate": [0.0, 0.0, 0.0] },
  "metadata": {
    "referenceSystem": "https://www.opengis.net/def/crs/EPSG/0/3857"
  },
  "CityObjects": {
    "BLD_fc50c7d9-76ac-4576-bfbd-f37c74410928": {
      "type": "Building",
      "geometry": [
        {
          "type": "Solid",
          "lod": "1",
          "boundaries": [
            [
              [[0, 1, 2, 3, 4, 5, 6, 7]],
              [[0, 7, 8, 9]],
              [[7, 6, 10, 8]],
              [[6, 5, 11, 10]],
              [[5, 4, 12, 11]],
              [[4, 3, 13, 12]],
              [[3, 2, 14, 13]],
              [[2, 1, 15, 14]],
              [[1, 0, 9, 15]],
              [[9, 8, 10, 11, 12, 13, 14, 15]]
            ]
          ]
        }
      ]
    },
    // ...
  }
}
```

```bash title="例: ファイルを指定"
plateaukit generate-cityjson ./udx/bldg/53395548_bldg_6697_2_op.gml /tmp/53395548_bldg_6697_2_op.city.json
```

## CityGMLから属性情報を抽出

> TODO: ドキュメントの整備
