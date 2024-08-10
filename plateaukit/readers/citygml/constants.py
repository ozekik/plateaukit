from plateaukit.constants import default_nsmap

# NOTE: https://www.mlit.go.jp/plateau/file/libraries/doc/plateau_doc_0002_ver03.pdf#page=60
data_type_display_names_v3 = {
    "bldg": {
        "ja": "建築物",
    },
    "tran": {
        "ja": "交通（道路）",
    },
    "rwy": {
        "ja": "交通（鉄道）",
    },
    "trk": {
        "ja": "交通（徒歩道）",
    },
    "squr": {
        "ja": "交通（広場）",
    },
    "wwy": {
        "ja": "交通（航路）",
    },
    "luse": {
        "ja": "土地利用",
    },
    "fld": {
        "ja": "洪水浸水想定区域",
    },
    "tnm": {
        "ja": "津波浸水想定",
    },
    "htd": {
        "ja": "高潮浸水想定区域",
    },
    "ifld": {
        "ja": "内水浸水想定区域",
    },
    "lsld": {
        "ja": "土砂災害警戒区域",
    },
    "urf": {
        "ja": "都市計画決定情報",
    },
    "brid": {
        "ja": "橋梁",
    },
    "tun": {
        "ja": "トンネル",
    },
    "cons": {
        "ja": "その他の構造物",
    },
    "frn": {
        "ja": "都市設備",
    },
    "ubld": {
        "ja": "地下街",
    },
    "veg": {
        "ja": "植生",
    },
    "dem": {
        "ja": "地形",
    },
    "wtr": {
        "ja": "水部",
    },
    "area": {
        "ja": "区域",
    },
    "gen": {
        "ja": "汎用都市オブジェクト",
    },
    "app": {
        "ja": "アピアランス",
    },
}

# NOTE: https://www.mlit.go.jp/plateau/file/libraries/doc/plateau_doc_0001_ver02.pdf#page=336
# NOTE: https://www.mlit.go.jp/plateau/file/libraries/doc/plateau_doc_0002_ver02.pdf#page=61
data_type_display_names = data_type_display_names_v2 = {
    "bldg": {
        "ja": "建築物",
    },
    # NOTE: brid is not defined in the specification
    "brid": {
        "ja": "橋梁",
    },
    "tran": {
        "ja": "道路",
    },
    "urf": {
        "ja": "都市計画決定情報",
    },
    "luse": {
        "ja": "土地利用",
    },
    "fld": {
        "ja": "洪水浸水想定区域",
    },
    "tnm": {
        "ja": "津波浸水想定",
    },
    "lsld": {
        "ja": "土砂災害警戒区域",
    },
    "htd": {
        "ja": "高潮浸水想定区域",
    },
    "ifld": {
        "ja": "内水浸水想定区域",
    },
    "frn": {
        "ja": "都市設備",
    },
    "veg": {
        "ja": "植生",
    },
    "dem": {
        "ja": "起伏",
    },
}

tag_display_names = {
    "gml:name": {
        "ja": "名称",
    },
    "gml:description": {
        "ja": "説明",
    },
    "gml:boundedBy": {
        "ja": "範囲",
    },
    "core:creationDate": {
        "ja": "作成日",
    },
    "bldg:class": {
        "ja": "分類",
    },
    "bldg:usage": {
        "ja": "用途",
    },
    "bldg:measuredHeight": {
        "ja": "計測高さ",
    },
    "bldg:storeysAboveGround": {
        "ja": "地上階数",
    },
    "bldg:storeysBelowGround": {
        "ja": "地下階数",
    },
    "bldg:lod0RoofEdge": {
        "ja": "lod0屋根面",
    },
    "bldg:lod0FootPrint": {
        "ja": "lod0接地面",
    },
    "bldg:lod1Solid": {
        "ja": "lod1立体",
    },
    "bldg:lod2Solid": {
        "ja": "lod2立体",
    },
    "bldg:lod3Solid": {
        "ja": "lod3立体",
    },
    "bldg:address": {
        "ja": "住所",
    },
    "bldg:boundedBy": {
        "ja": "境界面",
    },
    "bldg:outerBuildingInstallation": {
        "ja": "建物付属物",
    },
    "bldg:consistsOfBuildingPart": {
        "ja": "建物部品",
    },
    "tran:function": {
        "ja": "機能",
    },
    "dem:reliefComponent": {
        "ja": "地形構成要素",
    },
    "uro:buildingDataQualityAttribute": {
        "ja": "データ品質",
    },
    "uro:buildingDetailAttribute": {
        "ja": "建物利用現況",
    },
    "uro:buildingIDAttribute": {
        "ja": "建物識別情報",
    },
    "uro:buildingDisasterRiskAttribute": {
        "ja": "災害リスク",
    },
}
