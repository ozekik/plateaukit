
# PLATEAUデータの追加/削除 (コマンドライン)

## 利用可能な都市モデルの一覧を表示

```bash
plateaukit install --list
```

??? note "一覧"

    |                   id                   |         name         |                                    homepage                                   |
    |----------------------------------------|----------------------|-------------------------------------------------------------------------------|
    |                  all                   |       (全都市)       |                                                                               |
    |           plateau-tokyo23ku            |      東京都23区      |            https://www.geospatial.jp/ckan/dataset/plateau-tokyo23ku           |
    |     plateau-01100-sapporo-shi-2020     |     北海道札幌市     |     https://www.geospatial.jp/ckan/dataset/plateau-01100-sapporo-shi-2020     |
    |    plateau-07203-koriyama-city-2020    |     福島県郡山市     |    https://www.geospatial.jp/ckan/dataset/plateau-07203-koriyama-city-2020    |
    |      plateau-07204-iwaki-shi-2020      |    福島県いわき市    |      https://www.geospatial.jp/ckan/dataset/plateau-07204-iwaki-shi-2020      |
    |    plateau-07205-shirakawa-shi-2020    |     福島県白河市     |    https://www.geospatial.jp/ckan/dataset/plateau-07205-shirakawa-shi-2020    |
    |     plateau-08234-hokota-shi-2020      |     茨城県鉾田市     |      https://www.geospatial.jp/ckan/dataset/plateau-08234-hokota-shi-2020     |
    |   plateau-09201-utsunomiya-shi-2020    |    栃木県宇都宮市    |    https://www.geospatial.jp/ckan/dataset/plateau-09201-utsunomiya-shi-2020   |
    |      plateau-10203-kiryu-shi-2020      |     群馬県桐生市     |      https://www.geospatial.jp/ckan/dataset/plateau-10203-kiryu-shi-2020      |
    |   plateau-10207-tatebayashi-shi-2020   |     群馬県館林市     |   https://www.geospatial.jp/ckan/dataset/plateau-10207-tatebayashi-shi-2020   |
    |            plateau-saitama             |   埼玉県さいたま市   |             https://www.geospatial.jp/ckan/dataset/plateau-saitama            |
    |    plateau-11202-kumagaya-shi-2020     |     埼玉県熊谷市     |     https://www.geospatial.jp/ckan/dataset/plateau-11202-kumagaya-shi-2020    |
    |      plateau-11230-niiza-shi-2020      |     埼玉県新座市     |      https://www.geospatial.jp/ckan/dataset/plateau-11230-niiza-shi-2020      |
    |   plateau-11326-moroyama-machi-2020    |    埼玉県毛呂山町    |    https://www.geospatial.jp/ckan/dataset/plateau-11326-moroyama-machi-2020   |
    |     plateau-12217-kashiwa-shi-2020     |      千葉県柏市      |     https://www.geospatial.jp/ckan/dataset/plateau-12217-kashiwa-shi-2020     |
    |   plateau-13201-hachioji-shi-m-2020    | 東京都八王子市南大沢 |    https://www.geospatial.jp/ckan/dataset/plateau-13201-hachioji-shi-m-2020   |
    | plateau-13213-higashimurayama-shi-2020 |    東京都東村山市    | https://www.geospatial.jp/ckan/dataset/plateau-13213-higashimurayama-shi-2020 |
    |    plateau-14100-yokohama-city-2020    |    神奈川県横浜市    |    https://www.geospatial.jp/ckan/dataset/plateau-14100-yokohama-city-2020    |
    |    plateau-14130-kawasaki-shi-2020     |    神奈川県川崎市    |     https://www.geospatial.jp/ckan/dataset/plateau-14130-kawasaki-shi-2020    |
    |   plateau-14150-sagamihara-shi-2020    |   神奈川県相模原市   |    https://www.geospatial.jp/ckan/dataset/plateau-14150-sagamihara-shi-2020   |
    |    plateau-14201-yokosuka-shi-2020     |   神奈川県横須賀市   |     https://www.geospatial.jp/ckan/dataset/plateau-14201-yokosuka-shi-2020    |
    |    plateau-14382-hakone-machi-2020     |    神奈川県箱根町    |     https://www.geospatial.jp/ckan/dataset/plateau-14382-hakone-machi-2020    |
    |     plateau-15100-niigata-shi-2020     |     新潟県新潟市     |     https://www.geospatial.jp/ckan/dataset/plateau-15100-niigata-shi-2020     |
    |    plateau-17201-kanazawa-shi-2020     |     石川県金沢市     |     https://www.geospatial.jp/ckan/dataset/plateau-17201-kanazawa-shi-2020    |
    |         plateau-17206-kaga-shi         |     石川県加賀市     |         https://www.geospatial.jp/ckan/dataset/plateau-17206-kaga-shi         |
    |    plateau-20202-matsumoto-shi-2020    |     長野県松本市     |    https://www.geospatial.jp/ckan/dataset/plateau-20202-matsumoto-shi-2020    |
    |      plateau-20204-okaya-shi-2020      |     長野県岡谷市     |      https://www.geospatial.jp/ckan/dataset/plateau-20204-okaya-shi-2020      |
    |       plateau-20209-ina-shi-2020       |     長野県伊那市     |       https://www.geospatial.jp/ckan/dataset/plateau-20209-ina-shi-2020       |
    |      plateau-20214-chino-shi-2020      |     長野県茅野市     |      https://www.geospatial.jp/ckan/dataset/plateau-20214-chino-shi-2020      |
    |      plateau-21201-gifu-shi-2020       |     岐阜県岐阜市     |       https://www.geospatial.jp/ckan/dataset/plateau-21201-gifu-shi-2020      |
    |        plateau-22203-numazu-shi        |     静岡県沼津市     |        https://www.geospatial.jp/ckan/dataset/plateau-22203-numazu-shi        |
    |    plateau-22213-kakegawa-shi-2020     |     静岡県掛川市     |     https://www.geospatial.jp/ckan/dataset/plateau-22213-kakegawa-shi-2020    |
    |    plateau-22224-kikugawa-city-2020    |     静岡県菊川市     |    https://www.geospatial.jp/ckan/dataset/plateau-22224-kikugawa-city-2020    |
    |     plateau-23100-nagoya-shi-2020      |    愛知県名古屋市    |      https://www.geospatial.jp/ckan/dataset/plateau-23100-nagoya-shi-2020     |
    |     plateau-23202-okazaki-shi-2020     |     愛知県岡崎市     |     https://www.geospatial.jp/ckan/dataset/plateau-23202-okazaki-shi-2020     |
    |    plateau-23208-tsushima-shi-2020     |     愛知県津島市     |     https://www.geospatial.jp/ckan/dataset/plateau-23208-tsushima-shi-2020    |
    |      plateau-23212-annjo-shi-2020      |     愛知県安城市     |      https://www.geospatial.jp/ckan/dataset/plateau-23212-annjo-shi-2020      |
    |      plateau-27100-osaka-shi-2020      |     大阪府大阪市     |      https://www.geospatial.jp/ckan/dataset/plateau-27100-osaka-shi-2020      |
    |    plateau-27203-toyonaka-shi-2020     |     大阪府豊中市     |     https://www.geospatial.jp/ckan/dataset/plateau-27203-toyonaka-shi-2020    |
    |      plateau-27204-ikeda-shi-2020      |     大阪府池田市     |      https://www.geospatial.jp/ckan/dataset/plateau-27204-ikeda-shi-2020      |
    |    plateau-27207-takatsuki-shi-2020    |     大阪府高槻市     |    https://www.geospatial.jp/ckan/dataset/plateau-27207-takatsuki-shi-2020    |
    |     plateau-27224-settsu-shi-2020      |     大阪府摂津市     |      https://www.geospatial.jp/ckan/dataset/plateau-27224-settsu-shi-2020     |
    |     plateau-27341-tadaoka-cho-2020     |     大阪府忠岡町     |     https://www.geospatial.jp/ckan/dataset/plateau-27341-tadaoka-cho-2020     |
    |    plateau-28210-kakogawa-shi-2020     |    兵庫県加古川市    |     https://www.geospatial.jp/ckan/dataset/plateau-28210-kakogawa-shi-2020    |
    |     plateau-31201-tottori-shi-2020     |     鳥取県鳥取市     |     https://www.geospatial.jp/ckan/dataset/plateau-31201-tottori-shi-2020     |
    |      plateau-34202-kure-shi-2020       |      広島県呉市      |       https://www.geospatial.jp/ckan/dataset/plateau-34202-kure-shi-2020      |
    |    plateau-34207-fukuyama-shi-2020     |     広島県福山市     |     https://www.geospatial.jp/ckan/dataset/plateau-34207-fukuyama-shi-2020    |
    |    plateau-38201-matsuyama-shi-2020    |     愛媛県松山市     |    https://www.geospatial.jp/ckan/dataset/plateau-38201-matsuyama-shi-2020    |
    |   plateau-40100-kitakyushu-shi-2020    |    福岡県北九州市    |    https://www.geospatial.jp/ckan/dataset/plateau-40100-kitakyushu-shi-2020   |
    |     plateau-40203-kurume-shi-2020      |    福岡県久留米市    |      https://www.geospatial.jp/ckan/dataset/plateau-40203-kurume-shi-2020     |
    |     plateau-40205-iizuka-shi-2020      |     福岡県飯塚市     |      https://www.geospatial.jp/ckan/dataset/plateau-40205-iizuka-shi-2020     |
    |    plateau-40220-munakata-shi-2020     |     福岡県宗像市     |     https://www.geospatial.jp/ckan/dataset/plateau-40220-munakata-shi-2020    |
    |    plateau-43100-kumamoto-shi-2020     |     熊本県熊本市     |     https://www.geospatial.jp/ckan/dataset/plateau-43100-kumamoto-shi-2020    |
    |      plateau-43204-arao-shi-2020       |     熊本県荒尾市     |       https://www.geospatial.jp/ckan/dataset/plateau-43204-arao-shi-2020      |
    |     plateau-43206-tamana-shi-2020      |     熊本県玉名市     |      https://www.geospatial.jp/ckan/dataset/plateau-43206-tamana-shi-2020     |
    |    plateau-43443-mashiki-machi-2020    |     熊本県益城町     |    https://www.geospatial.jp/ckan/dataset/plateau-43443-mashiki-machi-2020    |
    |      plateau-44204-hita-shi-2020       |     大分県日田市     |       https://www.geospatial.jp/ckan/dataset/plateau-44204-hita-shi-2020      |
    |      plateau-47201-naha-shi-2020       |     沖縄県那覇市     |       https://www.geospatial.jp/ckan/dataset/plateau-47201-naha-shi-2020      |

## 都市モデルをダウンロード・追加

一覧のIDを指定して都市モデルをダウンロード・追加します。

```bash title="例1: 東京都23区のデータをダウンロードして追加"
plateaukit install plateau-tokyo23ku
```

```bash title="例2: 事前にダウンロード済みの東京都23区のデータを追加 (CityGML)"
plateaukit install plateau-tokyo23ku --local ./13100_tokyo23-ku_2020_citygml_3_2_op/ --format citygml
```

```title="実行例 (例1)"
$ plateaukit install plateau-tokyo23ku
Downloading as: /.../plateaukit/13100_tokyo23-ku_2020_citygml_3_2_op.zip
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4.18G/4.18G [03:18<00:00, 14.1MB/s]
Saved: {
  "data": {
    "plateau-tokyo23ku": {
      "citygml": "/.../plateaukit/13100_tokyo23-ku_2020_citygml_3_2_op.zip"
    }
  }
}
```

新規にダウンロードする場合、データの保存場所はデフォルトでは以下の通りです:

- macOS: `/Users/<username>/Library/Application Support/plateaukit/`
- Windows: `C:\\Users\<username>\AppData\Local\plateaukit\`
- Linux: `/home/<username>/.local/share/plateaukit/`

ダウンロード済みのデータを追加する場合は (`--local` オプション)、そのファイルパスが参照されます。

## 追加済みのデータの一覧を表示

```bash
plateaukit list
```

## 都市モデルを削除

```bash title="例: 東京都23区のデータを削除"
plateaukit uninstall plateau-tokyo23ku
```