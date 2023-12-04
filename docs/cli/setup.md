
# PLATEAUデータの追加と削除 (CLI)

## 利用可能な都市モデルの一覧を表示

利用可能な都市モデルの一覧を表示するには、`plateaukit list` コマンドを使用します。

```bash
plateaukit list
```

??? note "現在の都市一覧 (最新版のみ)"

    |                   id                   |       name       | version |                                    homepage                                   |
    |:--------------------------------------:|:----------------:|:-------:|:-----------------------------------------------------------------------------:|
    |                  all                   |     (全都市)     |         |                                                                               |
    |     plateau-01100-sapporo-shi-2020     |   北海道札幌市   |   2020  |     https://www.geospatial.jp/ckan/dataset/plateau-01100-sapporo-shi-2020     |
    |   plateau-01639-sarabetsu-mura-2022    |   北海道更別村   |   2022  |    https://www.geospatial.jp/ckan/dataset/plateau-01639-sarabetsu-mura-2022   |
    |     plateau-01205-muroran-shi-2022     |   北海道室蘭市   |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-01205-muroran-shi-2022     |
    |      plateau-02208-mutsu-shi-2022      |   青森県むつ市   |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-02208-mutsu-shi-2022      |
    |     plateau-03201-morioka-shi-2022     |   岩手県盛岡市   |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-03201-morioka-shi-2022     |
    |     plateau-04100-sendai-shi-2022      |   宮城県仙台市   |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-04100-sendai-shi-2022     |
    |      plateau-07204-iwaki-shi-2020      |  福島県いわき市  |   2020  |      https://www.geospatial.jp/ckan/dataset/plateau-07204-iwaki-shi-2020      |
    |    plateau-07203-koriyama-city-2020    |   福島県郡山市   |   2020  |    https://www.geospatial.jp/ckan/dataset/plateau-07203-koriyama-city-2020    |
    |    plateau-07205-shirakawa-shi-2020    |   福島県白河市   |   2020  |    https://www.geospatial.jp/ckan/dataset/plateau-07205-shirakawa-shi-2020    |
    |   plateau-07212-minamisouma-shi-2022   |  福島県南相馬市  |   2022  |   https://www.geospatial.jp/ckan/dataset/plateau-07212-minamisouma-shi-2022   |
    |     plateau-08234-hokota-shi-2022      |   茨城県鉾田市   |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-08234-hokota-shi-2022     |
    |     plateau-08220-tsukuba-shi-2022     |  茨城県つくば市  |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-08220-tsukuba-shi-2022     |
    |   plateau-09201-utsunomiya-shi-2020    |  栃木県宇都宮市  |   2020  |    https://www.geospatial.jp/ckan/dataset/plateau-09201-utsunomiya-shi-2020   |
    |      plateau-10203-kiryu-shi-2020      |   群馬県桐生市   |   2020  |      https://www.geospatial.jp/ckan/dataset/plateau-10203-kiryu-shi-2020      |
    |   plateau-10207-tatebayashi-shi-2020   |   群馬県館林市   |   2020  |   https://www.geospatial.jp/ckan/dataset/plateau-10207-tatebayashi-shi-2020   |
    |    plateau-11202-kumagaya-shi-2020     |   埼玉県熊谷市   |   2020  |     https://www.geospatial.jp/ckan/dataset/plateau-11202-kumagaya-shi-2020    |
    |     plateau-11100-saitama-shi-2022     | 埼玉県さいたま市 |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-11100-saitama-shi-2022     |
    |      plateau-11224-toda-shi-2022       |   埼玉県戸田市   |   2022  |       https://www.geospatial.jp/ckan/dataset/plateau-11224-toda-shi-2022      |
    |      plateau-11230-niiza-shi-2020      |   埼玉県新座市   |   2020  |      https://www.geospatial.jp/ckan/dataset/plateau-11230-niiza-shi-2020      |
    |     plateau-11238-hasuda-shi-2022      |   埼玉県蓮田市   |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-11238-hasuda-shi-2022     |
    |   plateau-11326-moroyama-machi-2020    |  埼玉県毛呂山町  |   2020  |    https://www.geospatial.jp/ckan/dataset/plateau-11326-moroyama-machi-2020   |
    |     plateau-12217-kashiwa-shi-2020     |    千葉県柏市    |   2020  |     https://www.geospatial.jp/ckan/dataset/plateau-12217-kashiwa-shi-2020     |
    |     plateau-12210-mobara-shi-2022      |   千葉県茂原市   |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-12210-mobara-shi-2022     |
    |     plateau-12221-yachiyo-shi-2022     |  千葉県八千代市  |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-12221-yachiyo-shi-2022     |
    |         plateau-tokyo23ku-2022         |    東京都23区    |   2022  |         https://www.geospatial.jp/ckan/dataset/plateau-tokyo23ku-2022         |
    |   plateau-13229-nishitokyo-shi-2022    |  東京都西東京市  |   2022  |    https://www.geospatial.jp/ckan/dataset/plateau-13229-nishitokyo-shi-2022   |
    |    plateau-13201-hachioji-shi-2022     |  東京都八王子市  |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-13201-hachioji-shi-2022    |
    | plateau-13213-higashimurayama-shi-2020 |  東京都東村山市  |   2020  | https://www.geospatial.jp/ckan/dataset/plateau-13213-higashimurayama-shi-2020 |
    |    plateau-14130-kawasaki-shi-2022     |  神奈川県川崎市  |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-14130-kawasaki-shi-2022    |
    |   plateau-14150-sagamihara-shi-2020    | 神奈川県相模原市 |   2020  |    https://www.geospatial.jp/ckan/dataset/plateau-14150-sagamihara-shi-2020   |
    |    plateau-14382-hakone-machi-2020     |  神奈川県箱根町  |   2020  |     https://www.geospatial.jp/ckan/dataset/plateau-14382-hakone-machi-2020    |
    |    plateau-14201-yokosuka-shi-2020     | 神奈川県横須賀市 |   2020  |     https://www.geospatial.jp/ckan/dataset/plateau-14201-yokosuka-shi-2020    |
    |    plateau-14100-yokohama-shi-2022     |  神奈川県横浜市  |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-14100-yokohama-shi-2022    |
    |     plateau-15100-niigata-shi-2022     |   新潟県新潟市   |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-15100-niigata-shi-2022     |
    |      plateau-17206-kaga-shi-2022       |   石川県加賀市   |   2022  |       https://www.geospatial.jp/ckan/dataset/plateau-17206-kaga-shi-2022      |
    |    plateau-17201-kanazawa-shi-2020     |   石川県金沢市   |   2020  |     https://www.geospatial.jp/ckan/dataset/plateau-17201-kanazawa-shi-2020    |
    |       plateau-20209-ina-shi-2020       |   長野県伊那市   |   2020  |       https://www.geospatial.jp/ckan/dataset/plateau-20209-ina-shi-2020       |
    |      plateau-20204-okaya-shi-2022      |   長野県岡谷市   |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-20204-okaya-shi-2022      |
    |      plateau-20217-saku-shi-2022       |   長野県佐久市   |   2022  |       https://www.geospatial.jp/ckan/dataset/plateau-20217-saku-shi-2022      |
    |      plateau-20214-chino-shi-2022      |   長野県茅野市   |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-20214-chino-shi-2022      |
    |    plateau-20202-matsumoto-shi-2020    |   長野県松本市   |   2020  |    https://www.geospatial.jp/ckan/dataset/plateau-20202-matsumoto-shi-2020    |
    |      plateau-21201-gifu-shi-2022       |   岐阜県岐阜市   |   2022  |       https://www.geospatial.jp/ckan/dataset/plateau-21201-gifu-shi-2022      |
    |    plateau-21211-minokamo-shi-2022     | 岐阜県美濃加茂市 |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-21211-minokamo-shi-2022    |
    |      plateau-19201-kofu-shi-2022       |   山梨県甲府市   |   2022  |       https://www.geospatial.jp/ckan/dataset/plateau-19201-kofu-shi-2022      |
    |      plateau-22205-atami-shi-2022      |   静岡県熱海市   |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-22205-atami-shi-2022      |
    |       plateau-22222-izu-shi-2022       |   静岡県伊豆市   |   2022  |       https://www.geospatial.jp/ckan/dataset/plateau-22222-izu-shi-2022       |
    |    plateau-22225-izunokuni-shi-2022    | 静岡県伊豆の国市 |   2022  |    https://www.geospatial.jp/ckan/dataset/plateau-22225-izunokuni-shi-2022    |
    |       plateau-22208-ito-shi-2022       |   静岡県伊東市   |   2022  |       https://www.geospatial.jp/ckan/dataset/plateau-22208-ito-shi-2022       |
    |      plateau-22211-iwata-shi-2022      |   静岡県磐田市   |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-22211-iwata-shi-2022      |
    |    plateau-22223-omaezaki-shi-2022     |  静岡県御前崎市  |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-22223-omaezaki-shi-2022    |
    |      plateau-22344-oyama-cho-2022      |   静岡県小山町   |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-22344-oyama-cho-2022      |
    |    plateau-22213-kakegawa-shi-2020     |   静岡県掛川市   |   2020  |     https://www.geospatial.jp/ckan/dataset/plateau-22213-kakegawa-shi-2020    |
    |     plateau-22302-kawazu-cho-2022      |   静岡県河津町   |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-22302-kawazu-cho-2022     |
    |     plateau-22325-kannami-cho-2022     |   静岡県函南町   |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-22325-kannami-cho-2022     |
    |    plateau-22224-kikugawa-city-2020    |   静岡県菊川市   |   2020  |    https://www.geospatial.jp/ckan/dataset/plateau-22224-kikugawa-city-2020    |
    |      plateau-22221-kosai-shi-2022      |   静岡県湖西市   |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-22221-kosai-shi-2022      |
    |     plateau-22215-gotenba-shi-2022     |  静岡県御殿場市  |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-22215-gotenba-shi-2022     |
    |    plateau-22100-shizuoka-shi-2022     |   静岡県静岡市   |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-22100-shizuoka-shi-2022    |
    |     plateau-22341-shimizu-cho-2022     |   静岡県清水町   |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-22341-shimizu-cho-2022     |
    |     plateau-22219-shimoda-shi-2022     |   静岡県下田市   |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-22219-shimoda-shi-2022     |
    |     plateau-22220-susono-shi-2022      |   静岡県裾野市   |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-22220-susono-shi-2022     |
    |    plateau-22342-nagaizumi-cho-2022    |   静岡県長泉町   |   2022  |    https://www.geospatial.jp/ckan/dataset/plateau-22342-nagaizumi-cho-2022    |
    |     plateau-22203-numazu-shi-2021      |   静岡県沼津市   |   2021  |      https://www.geospatial.jp/ckan/dataset/plateau-22203-numazu-shi-2021     |
    |   plateau-22301-higashiizu-cho-2022    |  静岡県東伊豆町  |   2022  |    https://www.geospatial.jp/ckan/dataset/plateau-22301-higashiizu-cho-2022   |
    |     plateau-22216-fukuroi-shi-2022     |   静岡県袋井市   |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-22216-fukuroi-shi-2022     |
    |      plateau-22210-fuji-shi-2022       |   静岡県富士市   |   2022  |       https://www.geospatial.jp/ckan/dataset/plateau-22210-fuji-shi-2022      |
    |     plateau-22214-fujieda-shi-2022     |   静岡県藤枝市   |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-22214-fujieda-shi-2022     |
    |   plateau-22207-fujinomiya-shi-2022    |  静岡県富士宮市  |   2022  |    https://www.geospatial.jp/ckan/dataset/plateau-22207-fujinomiya-shi-2022   |
    |   plateau-22226-makinohara-shi-2022    |  静岡県牧之原市  |   2022  |    https://www.geospatial.jp/ckan/dataset/plateau-22226-makinohara-shi-2022   |
    |     plateau-22206-mishima-shi-2022     |   静岡県三島市   |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-22206-mishima-shi-2022     |
    |    plateau-22304-minamiizu-cho-2022    |  静岡県南伊豆町  |   2022  |    https://www.geospatial.jp/ckan/dataset/plateau-22304-minamiizu-cho-2022    |
    |     plateau-22461-mori-machi-2022      |    静岡県森町    |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-22461-mori-machi-2022     |
    |      plateau-22212-yaizu-shi-2022      |   静岡県焼津市   |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-22212-yaizu-shi-2022      |
    |     plateau-22424-yoshida-cho-2022     |   静岡県吉田町   |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-22424-yoshida-cho-2022     |
    |      plateau-23212-anjo-shi-2020       |   愛知県安城市   |   2020  |       https://www.geospatial.jp/ckan/dataset/plateau-23212-anjo-shi-2020      |
    |     plateau-23202-okazaki-shi-2020     |   愛知県岡崎市   |   2020  |     https://www.geospatial.jp/ckan/dataset/plateau-23202-okazaki-shi-2020     |
    |     plateau-23206-kasugai-shi-2022     |  愛知県春日井市  |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-23206-kasugai-shi-2022     |
    |    plateau-23208-tsushima-shi-2020     |   愛知県津島市   |   2020  |     https://www.geospatial.jp/ckan/dataset/plateau-23208-tsushima-shi-2020    |
    |    plateau-23207-toyokawa-shi-2022     |   愛知県豊川市   |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-23207-toyokawa-shi-2022    |
    |     plateau-23100-nagoya-shi-2020      |  愛知県名古屋市  |   2020  |      https://www.geospatial.jp/ckan/dataset/plateau-23100-nagoya-shi-2020     |
    |     plateau-23230-nisshin-shi-2022     |   愛知県日進市   |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-23230-nisshin-shi-2022     |
    |     plateau-24212-kumano-shi-2022      |   三重県熊野市   |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-24212-kumano-shi-2022     |
    |    plateau-24202-yokkaichi-shi-2022    |  三重県四日市市  |   2022  |    https://www.geospatial.jp/ckan/dataset/plateau-24202-yokkaichi-shi-2022    |
    |      plateau-26100-kyoto-shi-2022      |   京都府京都市   |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-26100-kyoto-shi-2022      |
    |      plateau-27204-ikeda-shi-2020      |   大阪府池田市   |   2020  |      https://www.geospatial.jp/ckan/dataset/plateau-27204-ikeda-shi-2020      |
    |      plateau-27100-osaka-shi-2022      |   大阪府大阪市   |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-27100-osaka-shi-2022      |
    |    plateau-27221-kashiwara-shi-2022    |   大阪府柏原市   |   2022  |    https://www.geospatial.jp/ckan/dataset/plateau-27221-kashiwara-shi-2022    |
    |  plateau-27216-kawachinagano-shi-2022  | 大阪府河内長野市 |   2022  |  https://www.geospatial.jp/ckan/dataset/plateau-27216-kawachinagano-shi-2022  |
    |      plateau-27140-sakai-shi-2022      |    大阪府堺市    |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-27140-sakai-shi-2022      |
    |     plateau-27224-settsu-shi-2020      |   大阪府摂津市   |   2020  |      https://www.geospatial.jp/ckan/dataset/plateau-27224-settsu-shi-2020     |
    |    plateau-27207-takatsuki-shi-2020    |   大阪府高槻市   |   2020  |    https://www.geospatial.jp/ckan/dataset/plateau-27207-takatsuki-shi-2020    |
    |     plateau-27341-tadaoka-cho-2020     |   大阪府忠岡町   |   2020  |     https://www.geospatial.jp/ckan/dataset/plateau-27341-tadaoka-cho-2020     |
    |    plateau-27203-toyonaka-shi-2020     |   大阪府豊中市   |   2020  |     https://www.geospatial.jp/ckan/dataset/plateau-27203-toyonaka-shi-2020    |
    |      plateau-28225-asago-shi-2022      |   兵庫県朝来市   |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-28225-asago-shi-2022      |
    |    plateau-28210-kakogawa-shi-2020     |  兵庫県加古川市  |   2020  |     https://www.geospatial.jp/ckan/dataset/plateau-28210-kakogawa-shi-2020    |
    |      plateau-30422-taiji-cho-2021      |  和歌山県太地町  |   2021  |      https://www.geospatial.jp/ckan/dataset/plateau-30422-taiji-cho-2021      |
    |    plateau-30201-wakayama-shi-2022     | 和歌山県和歌山市 |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-30201-wakayama-shi-2022    |
    |     plateau-31201-tottori-shi-2020     |   鳥取県鳥取市   |   2020  |     https://www.geospatial.jp/ckan/dataset/plateau-31201-tottori-shi-2020     |
    |      plateau-34304-kaita-cho-2021      |   広島県海田町   |   2021  |      https://www.geospatial.jp/ckan/dataset/plateau-34304-kaita-cho-2021      |
    |      plateau-34202-kure-shi-2020       |    広島県呉市    |   2020  |       https://www.geospatial.jp/ckan/dataset/plateau-34202-kure-shi-2020      |
    |    plateau-34100-hirosima-shi-2022     |   広島県広島市   |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-34100-hirosima-shi-2022    |
    |    plateau-34207-fukuyama-shi-2020     |   広島県福山市   |   2020  |     https://www.geospatial.jp/ckan/dataset/plateau-34207-fukuyama-shi-2020    |
    |      plateau-34208-fuchu-shi-2022      |   広島県府中市   |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-34208-fuchu-shi-2022      |
    |    plateau-37201-takamatsu-shi-2022    |   香川県高松市   |   2022  |    https://www.geospatial.jp/ckan/dataset/plateau-37201-takamatsu-shi-2022    |
    |    plateau-38201-matsuyama-shi-2020    |   愛媛県松山市   |   2020  |    https://www.geospatial.jp/ckan/dataset/plateau-38201-matsuyama-shi-2020    |
    |     plateau-41423-omachi-cho-2022      |   佐賀県大町町   |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-41423-omachi-cho-2022     |
    |       plateau-41208-ogi-shi-2022       |   佐賀県小城市   |   2022  |       https://www.geospatial.jp/ckan/dataset/plateau-41208-ogi-shi-2022       |
    |    plateau-41424-kouhoku-machi-2022    |   佐賀県江北町   |   2022  |    https://www.geospatial.jp/ckan/dataset/plateau-41424-kouhoku-machi-2022    |
    |    plateau-41425-shiroisi-chou-2022    |   佐賀県白石町   |   2022  |    https://www.geospatial.jp/ckan/dataset/plateau-41425-shiroisi-chou-2022    |
    |      plateau-41206-takeo-shi-2022      |   佐賀県武雄市   |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-41206-takeo-shi-2022      |
    |     plateau-40205-iizuka-shi-2020      |   福岡県飯塚市   |   2020  |      https://www.geospatial.jp/ckan/dataset/plateau-40205-iizuka-shi-2020     |
    |      plateau-40225-ukiha-shi-2022      |  福岡県うきは市  |   2022  |      https://www.geospatial.jp/ckan/dataset/plateau-40225-ukiha-shi-2022      |
    |   plateau-40100-kitakyushu-shi-2020    |  福岡県北九州市  |   2020  |    https://www.geospatial.jp/ckan/dataset/plateau-40100-kitakyushu-shi-2020   |
    |     plateau-40203-kurume-shi-2020      |  福岡県久留米市  |   2020  |      https://www.geospatial.jp/ckan/dataset/plateau-40203-kurume-shi-2020     |
    |     plateau-40130-fukuoka-shi-2022     |   福岡県福岡市   |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-40130-fukuoka-shi-2022     |
    |    plateau-40220-munakata-shi-2020     |   福岡県宗像市   |   2020  |     https://www.geospatial.jp/ckan/dataset/plateau-40220-munakata-shi-2020    |
    |      plateau-43204-arao-shi-2020       |   熊本県荒尾市   |   2020  |       https://www.geospatial.jp/ckan/dataset/plateau-43204-arao-shi-2020      |
    |    plateau-43100-kumamoto-shi-2022     |   熊本県熊本市   |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-43100-kumamoto-shi-2022    |
    |     plateau-43206-tamana-shi-2020      |   熊本県玉名市   |   2020  |      https://www.geospatial.jp/ckan/dataset/plateau-43206-tamana-shi-2020     |
    |    plateau-43443-mashiki-machi-2020    |   熊本県益城町   |   2020  |    https://www.geospatial.jp/ckan/dataset/plateau-43443-mashiki-machi-2020    |
    |      plateau-44204-hita-shi-2020       |   大分県日田市   |   2020  |       https://www.geospatial.jp/ckan/dataset/plateau-44204-hita-shi-2020      |
    |     plateau-45203-nobeoka-shi-2022     |   宮崎県延岡市   |   2022  |     https://www.geospatial.jp/ckan/dataset/plateau-45203-nobeoka-shi-2022     |
    |      plateau-47201-naha-shi-2020       |   沖縄県那覇市   |   2020  |       https://www.geospatial.jp/ckan/dataset/plateau-47201-naha-shi-2020      |

## 都市モデルをダウンロード・追加

都市モデルをダウンロード・追加するには、都市モデルのIDを指定して `plateaukit install` コマンドを実行します。

```bash title="例: 東京都23区のデータをダウンロードして追加"
plateaukit install plateau-tokyo23ku
```

<div class="result" markdown>

```bash title="実行例"
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

</div>

または、事前にデータをダウンロードしておき、`--local` オプションにファイルを指定して追加することもできます。

```bash title="例: 事前にダウンロード済みの東京都23区のデータを追加 (CityGML)"
plateaukit install plateau-tokyo23ku --local ./13100_tokyo23-ku_2020_citygml_3_2_op/ --format citygml
```

!!! note ""
    都市モデルのデータを新規にダウンロードする場合、データの保存場所はデフォルトでは以下の通りです:

    - macOS: `/Users/<username>/Library/Application Support/plateaukit/`
    - Windows: `C:\\Users\<username>\AppData\Local\plateaukit\`
    - Linux: `/home/<username>/.local/share/plateaukit/`

    `--local` オプションを使ってダウンロード済みのデータを追加する場合は、そのファイルパスへの参照が追加されます。（ファイルはコピーされません）


## 追加済みのデータの一覧を表示

追加済みのデータの一覧を表示するには、`plateaukit list --local` コマンドを使用します。

```bash
plateaukit list --local
```

## 都市モデルの削除

追加済みの都市モデルのデータを削除するには、`plateaukit uninstall` コマンドを使用します。

```bash
plateaukit uninstall plateau-tokyo23ku # 東京都23区のデータを削除
```
