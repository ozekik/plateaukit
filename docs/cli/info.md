
# PLATEAUデータの情報を取得 (CLI)

## 都市モデルの詳細情報を表示

インストール済みの都市モデルの詳細情報を表示するには、`plateaukit info` コマンドを実行します。
データセットに含まれているデータの種類や属性の種類が取得できます。

```bash title="例: 大阪府大阪市のデータの詳細情報を表示"
plateaukit info plateau-27100-osaka-shi-2022
```

<div class="result" markdown>

```title="実行結果"
plateau-27100-osaka-shi-2022
https://www.geospatial.jp/ckan/dataset/plateau-27100-osaka-shi-2022
Name: 大阪府大阪市
Version: 2022
Installed Files:
  citygml: ~/Library/Application Support/plateaukit/data/27100_osaka-shi_2022_citygml_1_op.zip
  gpkg: ~/Library/Application Support/plateaukit/data/plateau-27100-osaka-shi-2022.gpkg
Data Types:
  建築物 (bldg): /27100_osaka-shi_2022_citygml_1_op/udx/bldg
  起伏 (dem): /27100_osaka-shi_2022_citygml_1_op/udx/dem
  洪水浸水想定区域 (fld): /27100_osaka-shi_2022_citygml_1_op/udx/fld
  都市設備 (frn): /27100_osaka-shi_2022_citygml_1_op/udx/frn
  高潮浸水想定区域 (htd): /27100_osaka-shi_2022_citygml_1_op/udx/htd
  土地利用 (luse): /27100_osaka-shi_2022_citygml_1_op/udx/luse
  津波浸水想定 (tnm): /27100_osaka-shi_2022_citygml_1_op/udx/tnm
  道路 (tran): /27100_osaka-shi_2022_citygml_1_op/udx/tran
  都市計画決定情報 (urf): /27100_osaka-shi_2022_citygml_1_op/udx/urf
  植生 (veg): /27100_osaka-shi_2022_citygml_1_op/udx/veg
Attributes:
  建築物 (bldg):
    measureAttribute (gen:measureAttribute)
    intAttribute (gen:intAttribute)
    区名 (gen:stringAttribute)
    町丁目名称 (gen:stringAttribute)
    分類 (bldg:class)
    用途 (bldg:usage)
    計測高さ (bldg:measuredHeight)
    地上階数 (bldg:storeysAboveGround)
    lod0接地面 (bldg:lod0FootPrint)
    lod1立体 (bldg:lod1Solid)
    データ品質 (uro:buildingDataQualityAttribute)
    建物利用現況 (uro:buildingDetailAttribute)
    災害リスク (uro:buildingDisasterRiskAttribute)
    建物識別情報 (uro:buildingIDAttribute)
    区番号 (uro:keyValuePairAttribute)
    住所コード (uro:keyValuePairAttribute)
    地上１階用途 (uro:keyValuePairAttribute)
    地上２階用途 (uro:keyValuePairAttribute)
    地下１階用途 (uro:keyValuePairAttribute)
    地上３階用途 (uro:keyValuePairAttribute)
    名称 (gml:name)
    地下２階用途 (uro:keyValuePairAttribute)
    作成日 (core:creationDate)
    lod2立体 (bldg:lod2Solid)
    境界面 (bldg:boundedBy)
    建物部品 (bldg:consistsOfBuildingPart)
    lod3立体 (bldg:lod3Solid)
  起伏 (dem):
    名称 (gml:name)
    作成日 (core:creationDate)
    lod (dem:lod)
    地形構成要素 (dem:reliefComponent)
  洪水浸水想定区域 (fld):
  都市設備 (frn):
    作成日 (core:creationDate)
    function (frn:function)
    lod3Geometry (frn:lod3Geometry)
    cityFurnitureDataQualityAttribute (uro:cityFurnitureDataQualityAttribute)
  高潮浸水想定区域 (htd):
  土地利用 (luse):
    作成日 (core:creationDate)
    class (luse:class)
    lod1MultiSurface (luse:lod1MultiSurface)
    landUseDetailAttribute (uro:landUseDetailAttribute)
  津波浸水想定 (tnm):
  道路 (tran):
    作成日 (core:creationDate)
    lod1MultiSurface (tran:lod1MultiSurface)
    roadDataQualityAttribute (uro:roadDataQualityAttribute)
    roadStructureAttribute (uro:roadStructureAttribute)
    機能 (tran:function)
    trafficArea (tran:trafficArea)
    auxiliaryTrafficArea (tran:auxiliaryTrafficArea)
    lod3MultiSurface (tran:lod3MultiSurface)
    lod2MultiSurface (tran:lod2MultiSurface)
  都市計画決定情報 (urf):
    function (urf:function)
    validFrom (urf:validFrom)
    validFromType (urf:validFromType)
    custodian (urf:custodian)
    notificationNumber (urf:notificationNumber)
    prefecture (urf:prefecture)
    city (urf:city)
    lod1MultiSurface (urf:lod1MultiSurface)
    名称 (gml:name)
    note (urf:note)
    areaClassification (urf:areaClassification)
    reasonForAreaClassification (urf:reasonForAreaClassification)
    usage (urf:usage)
    floorAreaRate (urf:floorAreaRate)
    maximumFloorAreaRate (urf:maximumFloorAreaRate)
    minimumFloorAreaRate (urf:minimumFloorAreaRate)
    maximumBuildingCoverageRate (urf:maximumBuildingCoverageRate)
    minimumBuildingArea (urf:minimumBuildingArea)
    useToBeInduced (urf:useToBeInduced)
    maximumBuildingHeight (urf:maximumBuildingHeight)
    setbackSize (urf:setbackSize)
    location (urf:location)
  植生 (veg):
    作成日 (core:creationDate)
    vegetationDataQualityAttribute (uro:vegetationDataQualityAttribute)
    class ({http://www.opengis.net/citygml/vegetation/2.0}class)
    height ({http://www.opengis.net/citygml/vegetation/2.0}height)
    lod3Geometry ({http://www.opengis.net/citygml/vegetation/2.0}lod3Geometry)
    averageHeight ({http://www.opengis.net/citygml/vegetation/2.0}averageHeight)
    lod3MultiSurface ({http://www.opengis.net/citygml/vegetation/2.0}lod3MultiSurface)
    lod2Geometry ({http://www.opengis.net/citygml/vegetation/2.0}lod2Geometry)
    lod2MultiSurface ({http://www.opengis.net/citygml/vegetation/2.0}lod2MultiSurface)
```

</div>
