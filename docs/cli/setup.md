
# PLATEAUデータの追加と削除 (CLI)

## 利用可能な都市モデルの一覧を表示

利用可能な都市モデルの一覧を表示するには、`plateaukit list` コマンドを実行します。

```bash
plateaukit list
```

??? note "現在の都市一覧 (最新版のみ)"

    |                   id                   |                name                | version | spec |                                    homepage                                   |
    | :------------------------------------: | :--------------------------------: | :-----: | :--: | :---------------------------------------------------------------------------: |
    |     plateau-01100-sapporo-shi-2020     |            北海道札幌市            |   2020  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-01100-sapporo-shi-2020     |
    |   plateau-01639-sarabetsu-mura-2023    |            北海道更別村            |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-01639-sarabetsu-mura-2023   |
    |     plateau-01205-muroran-shi-2022     |            北海道室蘭市            |   2022  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-01205-muroran-shi-2022     |
    |      plateau-02208-mutsu-shi-2022      |            青森県むつ市            |   2022  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-02208-mutsu-shi-2022      |
    |     plateau-03201-morioka-shi-2023     |            岩手県盛岡市            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-03201-morioka-shi-2023     |
    |     plateau-04100-sendai-shi-2022      |            宮城県仙台市            |   2022  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-04100-sendai-shi-2022     |
    |      plateau-07204-iwaki-shi-2020      |           福島県いわき市           |   2020  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-07204-iwaki-shi-2020      |
    |    plateau-07203-koriyama-shi-2020     |            福島県郡山市            |   2020  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-07203-koriyama-shi-2020    |
    |    plateau-07205-shirakawa-shi-2020    |            福島県白河市            |   2020  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-07205-shirakawa-shi-2020    |
    |   plateau-07212-minamisouma-shi-2022   |           福島県南相馬市           |   2022  |  v3  |   https://www.geospatial.jp/ckan/dataset/plateau-07212-minamisouma-shi-2022   |
    |     plateau-08546-sakai-machi-2023     |             茨城県境町             |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-08546-sakai-machi-2023     |
    |     plateau-08234-hokota-shi-2022      |            茨城県鉾田市            |   2022  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-08234-hokota-shi-2022     |
    |     plateau-08220-tsukuba-shi-2023     |           茨城県つくば市           |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-08220-tsukuba-shi-2023     |
    |   plateau-09201-utsunomiya-shi-2023    |           栃木県宇都宮市           |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-09201-utsunomiya-shi-2023   |
    |      plateau-10203-kiryu-shi-2020      |            群馬県桐生市            |   2020  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-10203-kiryu-shi-2020      |
    |   plateau-10207-tatebayashi-shi-2020   |            群馬県館林市            |   2020  |  v3  |   https://www.geospatial.jp/ckan/dataset/plateau-10207-tatebayashi-shi-2020   |
    |    plateau-10201-maebashi-shi-2023     |            群馬県前橋市            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-10201-maebashi-shi-2023    |
    |    plateau-11214-kasukabe-shi-2023     |           埼玉県春日部市           |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-11214-kasukabe-shi-2023    |
    |      plateau-11210-kazo-shi-2023       |            埼玉県加須市            |   2023  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-11210-kazo-shi-2023      |
    |      plateau-11232-kuki-shi-2023       |            埼玉県久喜市            |   2023  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-11232-kuki-shi-2023      |
    |    plateau-11202-kumagaya-shi-2023     |            埼玉県熊谷市            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-11202-kumagaya-shi-2023    |
    |    plateau-11222-koshigaya-shi-2023    |            埼玉県越谷市            |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-11222-koshigaya-shi-2023    |
    |     plateau-11100-saitama-shi-2023     |          埼玉県さいたま市          |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-11100-saitama-shi-2023     |
    |    plateau-11246-shiraoka-shi-2023     |            埼玉県白岡市            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-11246-shiraoka-shi-2023    |
    |    plateau-11464-sugito-machi-2023     |            埼玉県杉戸町            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-11464-sugito-machi-2023    |
    |      plateau-11224-toda-shi-2022       |            埼玉県戸田市            |   2022  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-11224-toda-shi-2022      |
    |      plateau-11230-niiza-shi-2020      |            埼玉県新座市            |   2020  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-11230-niiza-shi-2020      |
    |     plateau-11238-hasuda-shi-2022      |            埼玉県蓮田市            |   2022  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-11238-hasuda-shi-2022     |
    |  plateau-11465-matsubushi-machi-2023   |            埼玉県松伏町            |   2023  |  v3  |   https://www.geospatial.jp/ckan/dataset/plateau-11465-matsubushi-machi-2023  |
    |   plateau-11442-miyashiro-machi-2023   |            埼玉県宮代町            |   2023  |  v3  |   https://www.geospatial.jp/ckan/dataset/plateau-11442-miyashiro-machi-2023   |
    |   plateau-11326-moroyama-machi-2020    |          埼玉県毛呂山町市          |   2020  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-11326-moroyama-machi-2020   |
    |     plateau-11234-yashio-shi-2023      |            埼玉県八潮市            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-11234-yashio-shi-2023     |
    |    plateau-11243-yoshikawa-shi-2023    |            埼玉県吉川市            |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-11243-yoshikawa-shi-2023    |
    |     plateau-12217-kashiwa-shi-2020     |             千葉県柏市             |   2020  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-12217-kashiwa-shi-2020     |
    |     plateau-12210-mobara-shi-2022      |            千葉県茂原市            |   2022  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-12210-mobara-shi-2022     |
    |     plateau-12221-yachiyo-shi-2022     |           千葉県八千代市           |   2022  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-12221-yachiyo-shi-2022     |
    |         plateau-13-tokyo-2023          | 東京都（建築モデル等を除く）          |   2023  |  v3  |          https://www.geospatial.jp/ckan/dataset/plateau-13-tokyo-2023         |
    |      plateau-tokyo-takeshiba-2023      | 東京都サンプルデータ（竹芝モデル） |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-tokyo-takeshiba-2023      |
    |      plateau-13121-adachi-ku-2023      |            東京都足立区            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-13121-adachi-ku-2023      |
    |     plateau-13118-arakawa-ku-2023      |            東京都荒川区            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-13118-arakawa-ku-2023     |
    |     plateau-13119-itabashi-ku-2023     |            東京都板橋区            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-13119-itabashi-ku-2023     |
    |     plateau-13123-edogawa-ku-2023      |           東京都江戸川区           |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-13123-edogawa-ku-2023     |
    |       plateau-13111-ota-ku-2023        |            東京都大田区            |   2023  |  v3  |        https://www.geospatial.jp/ckan/dataset/plateau-13111-ota-ku-2023       |
    |    plateau-13122-katsushika-ku-2023    |            東京都葛飾区            |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-13122-katsushika-ku-2023    |
    |       plateau-13117-kita-ku-2023       |             東京都北区             |   2023  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-13117-kita-ku-2023       |
    |       plateau-13108-koto-ku-2023       |            東京都江東区            |   2023  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-13108-koto-ku-2023       |
    |    plateau-13109-shinagawa-ku-2023     |            東京都品川区            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-13109-shinagawa-ku-2023    |
    |     plateau-13113-shibuya-ku-2023      |            東京都渋谷区            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-13113-shibuya-ku-2023     |
    |     plateau-13104-shinjuku-ku-2023     |            東京都新宿区            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-13104-shinjuku-ku-2023     |
    |     plateau-13115-suginami-ku-2023     |            東京都杉並区            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-13115-suginami-ku-2023     |
    |      plateau-13107-sumida-ku-2023      |            東京都墨田区            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-13107-sumida-ku-2023      |
    |     plateau-13112-setagaya-ku-2023     |           東京都世田谷区           |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-13112-setagaya-ku-2023     |
    |      plateau-13106-taito-ku-2023       |            東京都台東区            |   2023  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-13106-taito-ku-2023      |
    |       plateau-13102-chuo-ku-2023       |            東京都中央区            |   2023  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-13102-chuo-ku-2023       |
    |     plateau-13101-chiyoda-ku-2023      |           東京都千代田区           |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-13101-chiyoda-ku-2023     |
    |     plateau-13116-toshima-ku-2023      |            東京都豊島区            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-13116-toshima-ku-2023     |
    |      plateau-13114-nakano-ku-2023      |            東京都中野区            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-13114-nakano-ku-2023      |
    |      plateau-13120-nerima-ku-2023      |            東京都練馬区            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-13120-nerima-ku-2023      |
    |      plateau-13105-bunkyo-ku-2023      |            東京都文京区            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-13105-bunkyo-ku-2023      |
    |      plateau-13103-minato-ku-2023      |             東京都港区             |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-13103-minato-ku-2023      |
    |      plateau-13110-meguro-ku-2023      |            東京都目黒区            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-13110-meguro-ku-2023      |
    |    plateau-13207-akishima-shi-2023     |            東京都昭島市            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-13207-akishima-shi-2023    |
    |     plateau-13228-akiruno-shi-2023     |          東京都あきる野市          |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-13228-akiruno-shi-2023     |
    |    plateau-13308-okutama-machi-2023    |           東京都奥多摩町           |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-13308-okutama-machi-2023    |
    |       plateau-13205-ome-shi-2023       |            東京都青梅市            |   2023  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-13205-ome-shi-2023       |
    |     plateau-13221-kiyose-shi-2023      |            東京都清瀬市            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-13221-kiyose-shi-2023     |
    |    plateau-13215-kunitachi-shi-2023    |            東京都国立市            |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-13215-kunitachi-shi-2023    |
    |     plateau-13210-koganei-shi-2023     |           東京都小金井市           |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-13210-koganei-shi-2023     |
    |    plateau-13214-kokubunji-shi-2023    |           東京都国分寺市           |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-13214-kokubunji-shi-2023    |
    |     plateau-13211-kodaira-shi-2023     |            東京都小平市            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-13211-kodaira-shi-2023     |
    |      plateau-13219-komae-shi-2023      |            東京都狛江市            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-13219-komae-shi-2023      |
    |    plateau-13202-tachikawa-shi-2023    |            東京都立川市            |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-13202-tachikawa-shi-2023    |
    |      plateau-13224-tama-shi-2023       |            東京都多摩市            |   2023  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-13224-tama-shi-2023      |
    |      plateau-13208-chofu-shi-2023      |            東京都調布市            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-13208-chofu-shi-2023      |
    |   plateau-13229-nishitokyo-shi-2023    |           東京都西東京市           |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-13229-nishitokyo-shi-2023   |
    |    plateau-13201-hachioji-shi-2023     |           東京都八王子市           |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-13201-hachioji-shi-2023    |
    |     plateau-13227-hamura-shi-2023      |            東京都羽村市            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-13227-hamura-shi-2023     |
    |  plateau-13222-higashikurume-shi-2023  |          東京都東久留米市          |   2023  |  v3  |  https://www.geospatial.jp/ckan/dataset/plateau-13222-higashikurume-shi-2023  |
    | plateau-13213-higashimurayama-shi-2023 |           東京都東村山市           |   2023  |  v3  | https://www.geospatial.jp/ckan/dataset/plateau-13213-higashimurayama-shi-2023 |
    |  plateau-13220-higashiyamato-shi-2023  |           東京都東大和市           |   2023  |  v3  |  https://www.geospatial.jp/ckan/dataset/plateau-13220-higashiyamato-shi-2023  |
    |      plateau-13212-hino-shi-2023       |            東京都日野市            |   2023  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-13212-hino-shi-2023      |
    |    plateau-13305-hinode-machi-2023     |           東京都日の出町           |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-13305-hinode-machi-2023    |
    |    plateau-13307-hinohara-mura-2023    |            東京都檜原村            |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-13307-hinohara-mura-2023    |
    |      plateau-13218-fussa-shi-2023      |            東京都福生市            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-13218-fussa-shi-2023      |
    |      plateau-13206-fuchu-shi-2023      |            東京都府中市            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-13206-fuchu-shi-2023      |
    |     plateau-13209-machida-shi-2023     |            東京都町田市            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-13209-machida-shi-2023     |
    |    plateau-13303-mizuho-machi-2023     |            東京都瑞穂町            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-13303-mizuho-machi-2023    |
    |     plateau-13204-mitaka-shi-2023      |            東京都三鷹市            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-13204-mitaka-shi-2023     |
    |    plateau-13203-musashino-shi-2023    |           東京都武蔵野市           |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-13203-musashino-shi-2023    |
    | plateau-13223-musashimurayama-shi-2023 |          東京都武蔵村山市          |   2023  |  v3  | https://www.geospatial.jp/ckan/dataset/plateau-13223-musashimurayama-shi-2023 |
    |         plateau-tokyo23ku-2022         |          東京都東京都23区          |   2022  |  v2  |         https://www.geospatial.jp/ckan/dataset/plateau-tokyo23ku-2022         |
    |     plateau-14212-atsugi-shi-2023      |           神奈川県厚木市           |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-14212-atsugi-shi-2023     |
    |    plateau-14130-kawasaki-shi-2022     |           神奈川県川崎市           |   2022  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-14130-kawasaki-shi-2022    |
    |   plateau-14150-sagamihara-shi-2023    |          神奈川県相模原市          |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-14150-sagamihara-shi-2023   |
    |    plateau-14382-hakone-machi-2020     |           神奈川県箱根町           |   2020  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-14382-hakone-machi-2020    |
    |    plateau-14201-yokosuka-shi-2020     |          神奈川県横須賀市          |   2020  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-14201-yokosuka-shi-2020    |
    |    plateau-14100-yokohama-shi-2023     |           神奈川県横浜市           |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-14100-yokohama-shi-2023    |
    |     plateau-15222-joetsu-shi-2023      |            新潟県上越市            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-15222-joetsu-shi-2023     |
    |     plateau-15202-nagaoka-shi-2023     |            新潟県長岡市            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-15202-nagaoka-shi-2023     |
    |     plateau-15100-niigata-shi-2023     |            新潟県新潟市            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-15100-niigata-shi-2023     |
    |      plateau-17206-kaga-shi-2022       |            石川県加賀市            |   2022  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-17206-kaga-shi-2022      |
    |    plateau-17201-kanazawa-shi-2023     |            石川県金沢市            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-17201-kanazawa-shi-2023    |
    |       plateau-20209-ina-shi-2020       |            長野県伊那市            |   2020  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-20209-ina-shi-2020       |
    |      plateau-20204-okaya-shi-2022      |            長野県岡谷市            |   2022  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-20204-okaya-shi-2022      |
    |      plateau-20217-saku-shi-2022       |            長野県佐久市            |   2022  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-20217-saku-shi-2022      |
    |      plateau-20206-suwa-shi-2023       |            長野県諏訪市            |   2023  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-20206-suwa-shi-2023      |
    |      plateau-20214-chino-shi-2023      |            長野県茅野市            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-20214-chino-shi-2023      |
    |    plateau-20202-matsumoto-shi-2020    |            長野県松本市            |   2020  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-20202-matsumoto-shi-2020    |
    |      plateau-21201-gifu-shi-2023       |            岐阜県岐阜市            |   2023  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-21201-gifu-shi-2023      |
    |    plateau-21211-minokamo-shi-2022     |          岐阜県美濃加茂市          |   2022  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-21211-minokamo-shi-2022    |
    |      plateau-19201-kofu-shi-2023       |            山梨県甲府市            |   2023  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-19201-kofu-shi-2023      |
    |      plateau-22205-atami-shi-2023      |            静岡県熱海市            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-22205-atami-shi-2023      |
    |       plateau-22222-izu-shi-2023       |            静岡県伊豆市            |   2023  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-22222-izu-shi-2023       |
    |    plateau-22225-izunokuni-shi-2023    |          静岡県伊豆の国市          |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-22225-izunokuni-shi-2023    |
    |       plateau-22208-ito-shi-2023       |            静岡県伊東市            |   2023  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-22208-ito-shi-2023       |
    |      plateau-22211-iwata-shi-2023      |            静岡県磐田市            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-22211-iwata-shi-2023      |
    |    plateau-22223-omaezaki-shi-2023     |           静岡県御前崎市           |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-22223-omaezaki-shi-2023    |
    |      plateau-22344-oyama-cho-2023      |            静岡県小山町            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-22344-oyama-cho-2023      |
    |    plateau-22213-kakegawa-shi-2023     |            静岡県掛川市            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-22213-kakegawa-shi-2023    |
    |     plateau-22302-kawazu-cho-2023      |            静岡県河津町            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-22302-kawazu-cho-2023     |
    |    plateau-22429-kawanehon-cho-2023    |           静岡県川根本町           |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-22429-kawanehon-cho-2023    |
    |     plateau-22325-kannami-cho-2023     |            静岡県函南町            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-22325-kannami-cho-2023     |
    |    plateau-22224-kikugawa-shi-2023     |            静岡県菊川市            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-22224-kikugawa-shi-2023    |
    |      plateau-22221-kosai-shi-2023      |            静岡県湖西市            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-22221-kosai-shi-2023      |
    |     plateau-22215-gotenba-shi-2023     |           静岡県御殿場市           |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-22215-gotenba-shi-2023     |
    |    plateau-22100-shizuoka-shi-2022     |            静岡県静岡市            |   2022  |  v2  |     https://www.geospatial.jp/ckan/dataset/plateau-22100-shizuoka-shi-2022    |
    |     plateau-22209-shimada-shi-2023     |            静岡県島田市            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-22209-shimada-shi-2023     |
    |     plateau-22341-shimizu-cho-2023     |            静岡県清水町            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-22341-shimizu-cho-2023     |
    |     plateau-22219-shimoda-shi-2023     |            静岡県下田市            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-22219-shimoda-shi-2023     |
    |     plateau-22220-susono-shi-2023      |            静岡県裾野市            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-22220-susono-shi-2023     |
    |    plateau-22342-nagaizumi-cho-2023    |            静岡県長泉町            |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-22342-nagaizumi-cho-2023    |
    |    plateau-22306-nishiizu-cho-2023     |           静岡県西伊豆町           |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-22306-nishiizu-cho-2023    |
    |     plateau-22203-numazu-shi-2021      |            静岡県沼津市            |   2021  |  v2  |      https://www.geospatial.jp/ckan/dataset/plateau-22203-numazu-shi-2021     |
    |    plateau-22130-hamamatsu-shi-2023    |            静岡県浜松市            |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-22130-hamamatsu-shi-2023    |
    |   plateau-22301-higashiizu-cho-2023    |           静岡県東伊豆町           |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-22301-higashiizu-cho-2023   |
    |     plateau-22216-fukuroi-shi-2023     |            静岡県袋井市            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-22216-fukuroi-shi-2023     |
    |      plateau-22210-fuji-shi-2023       |            静岡県富士市            |   2023  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-22210-fuji-shi-2023      |
    |     plateau-22214-fujieda-shi-2023     |            静岡県藤枝市            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-22214-fujieda-shi-2023     |
    |   plateau-22207-fujinomiya-shi-2023    |           静岡県富士宮市           |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-22207-fujinomiya-shi-2023   |
    |   plateau-22226-makinohara-shi-2023    |           静岡県牧之原市           |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-22226-makinohara-shi-2023   |
    |    plateau-22305-matsuzaki-cho-2023    |            静岡県松崎町            |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-22305-matsuzaki-cho-2023    |
    |     plateau-22206-mishima-shi-2023     |            静岡県三島市            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-22206-mishima-shi-2023     |
    |    plateau-22304-minamiizu-cho-2023    |           静岡県南伊豆町           |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-22304-minamiizu-cho-2023    |
    |     plateau-22461-mori-machi-2023      |             静岡県森町             |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-22461-mori-machi-2023     |
    |      plateau-22212-yaizu-shi-2023      |            静岡県焼津市            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-22212-yaizu-shi-2023      |
    |     plateau-22424-yoshida-cho-2023     |            静岡県吉田町            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-22424-yoshida-cho-2023     |
    |      plateau-23212-anjo-shi-2020       |            愛知県安城市            |   2020  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-23212-anjo-shi-2020      |
    |     plateau-23202-okazaki-shi-2020     |            愛知県岡崎市            |   2020  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-23202-okazaki-shi-2020     |
    |     plateau-23206-kasugai-shi-2023     |           愛知県春日井市           |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-23206-kasugai-shi-2023     |
    |    plateau-23208-tsushima-shi-2020     |            愛知県津島市            |   2020  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-23208-tsushima-shi-2020    |
    |    plateau-23207-toyokawa-shi-2022     |            愛知県豊川市            |   2022  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-23207-toyokawa-shi-2022    |
    |     plateau-23211-toyota-shi-2023      |            愛知県豊田市            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-23211-toyota-shi-2023     |
    |    plateau-23201-toyohashi-shi-2023    |            愛知県豊橋市            |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-23201-toyohashi-shi-2023    |
    |     plateau-23100-nagoya-shi-2022      |           愛知県名古屋市           |   2022  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-23100-nagoya-shi-2022     |
    |     plateau-23230-nisshin-shi-2023     |            愛知県日進市            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-23230-nisshin-shi-2023     |
    |     plateau-24212-kumano-shi-2022      |            三重県熊野市            |   2022  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-24212-kumano-shi-2022     |
    |    plateau-24202-yokkaichi-shi-2022    |           三重県四日市市           |   2022  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-24202-yokkaichi-shi-2022    |
    |      plateau-26100-kyoto-shi-2023      |            京都府京都市            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-26100-kyoto-shi-2023      |
    |      plateau-27204-ikeda-shi-2020      |            大阪府池田市            |   2020  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-27204-ikeda-shi-2020      |
    |      plateau-27219-izumi-shi-2023      |            大阪府和泉市            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-27219-izumi-shi-2023      |
    |      plateau-27100-osaka-shi-2022      |            大阪府大阪市            |   2022  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-27100-osaka-shi-2022      |
    |    plateau-27221-kashiwara-shi-2022    |            大阪府柏原市            |   2022  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-27221-kashiwara-shi-2022    |
    |  plateau-27216-kawachinagano-shi-2023  |          大阪府河内長野市          |   2023  |  v3  |  https://www.geospatial.jp/ckan/dataset/plateau-27216-kawachinagano-shi-2023  |
    |      plateau-27140-sakai-shi-2022      |             大阪府堺市             |   2022  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-27140-sakai-shi-2022      |
    |     plateau-27224-settsu-shi-2020      |            大阪府摂津市            |   2020  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-27224-settsu-shi-2020     |
    |    plateau-27207-takatsuki-shi-2020    |            大阪府高槻市            |   2020  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-27207-takatsuki-shi-2020    |
    |     plateau-27341-tadaoka-cho-2020     |            大阪府忠岡町            |   2020  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-27341-tadaoka-cho-2020     |
    |    plateau-27203-toyonaka-shi-2020     |            大阪府豊中市            |   2020  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-27203-toyonaka-shi-2020    |
    |      plateau-28225-asago-shi-2022      |            兵庫県朝来市            |   2022  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-28225-asago-shi-2022      |
    |    plateau-28210-kakogawa-shi-2020     |           兵庫県加古川市           |   2020  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-28210-kakogawa-shi-2020    |
    |     plateau-28201-himeji-shi-2023      |            兵庫県姫路市            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-28201-himeji-shi-2023     |
    |      plateau-28215-miki-shi-2023       |            兵庫県三木市            |   2023  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-28215-miki-shi-2023      |
    |      plateau-30422-taiji-cho-2021      |           和歌山県太地町           |   2021  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-30422-taiji-cho-2021      |
    |    plateau-30201-wakayama-shi-2023     |          和歌山県和歌山市          |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-30201-wakayama-shi-2023    |
    |      plateau-33211-bizen-shi-2023      |            岡山県備前市            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-33211-bizen-shi-2023      |
    |   plateau-31204-sakaiminato-shi-2022   |            鳥取県境港市            |   2022  |  v3  |   https://www.geospatial.jp/ckan/dataset/plateau-31204-sakaiminato-shi-2022   |
    |     plateau-31201-tottori-shi-2020     |            鳥取県鳥取市            |   2020  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-31201-tottori-shi-2020     |
    |      plateau-31384-hiezu-son-2023      |           鳥取県日吉津村           |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-31384-hiezu-son-2023      |
    |     plateau-31202-yonago-shi-2023      |            鳥取県米子市            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-31202-yonago-shi-2023     |
    |      plateau-34304-kaita-cho-2021      |            広島県海田町            |   2021  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-34304-kaita-cho-2021      |
    |      plateau-34202-kure-shi-2020       |             広島県呉市             |   2020  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-34202-kure-shi-2020      |
    |    plateau-34203-takehara-shi-2023     |            広島県竹原市            |   2023  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-34203-takehara-shi-2023    |
    |    plateau-34100-hirosima-shi-2022     |            広島県広島市            |   2022  |  v2  |     https://www.geospatial.jp/ckan/dataset/plateau-34100-hirosima-shi-2022    |
    |    plateau-34207-fukuyama-shi-2020     |            広島県福山市            |   2020  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-34207-fukuyama-shi-2020    |
    |      plateau-34208-fuchu-shi-2022      |            広島県府中市            |   2022  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-34208-fuchu-shi-2022      |
    |     plateau-34209-miyoshi-shi-2022     |            広島県三次市            |   2022  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-34209-miyoshi-shi-2022     |
    |    plateau-36201-tokushima-shi-2023    |            徳島県徳島市            |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-36201-tokushima-shi-2023    |
    |     plateau-37206-sanuki-shi-2023      |           香川県さぬき市           |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-37206-sanuki-shi-2023     |
    |    plateau-37201-takamatsu-shi-2022    |            香川県高松市            |   2022  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-37201-takamatsu-shi-2022    |
    |      plateau-38215-toon-shi-2023       |            愛媛県東温市            |   2023  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-38215-toon-shi-2023      |
    |    plateau-38201-matsuyama-shi-2020    |            愛媛県松山市            |   2020  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-38201-matsuyama-shi-2020    |
    |     plateau-40205-iizuka-shi-2020      |            福岡県飯塚市            |   2020  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-40205-iizuka-shi-2020     |
    |      plateau-40225-ukiha-shi-2023      |           福岡県うきは市           |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-40225-ukiha-shi-2023      |
    |      plateau-40202-omuta-shi-2023      |           福岡県大牟田市           |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-40202-omuta-shi-2023      |
    |   plateau-40100-kitakyushu-shi-2020    |           福岡県北九州市           |   2020  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-40100-kitakyushu-shi-2020   |
    |     plateau-40203-kurume-shi-2020      |           福岡県久留米市           |   2020  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-40203-kurume-shi-2020     |
    |     plateau-40130-fukuoka-shi-2022     |            福岡県福岡市            |   2022  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-40130-fukuoka-shi-2022     |
    |    plateau-40220-munakata-shi-2020     |            福岡県宗像市            |   2020  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-40220-munakata-shi-2020    |
    |     plateau-41423-omachi-cho-2022      |            佐賀県大町町            |   2022  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-41423-omachi-cho-2022     |
    |       plateau-41208-ogi-shi-2022       |            佐賀県小城市            |   2022  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-41208-ogi-shi-2022       |
    |    plateau-41424-kouhoku-machi-2022    |            佐賀県江北町            |   2022  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-41424-kouhoku-machi-2022    |
    |    plateau-41425-shiroisi-chou-2022    |            佐賀県白石町            |   2022  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-41425-shiroisi-chou-2022    |
    |      plateau-41206-takeo-shi-2022      |            佐賀県武雄市            |   2022  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-41206-takeo-shi-2022      |
    |   plateau-40447-chikuzen-machi-2023    |            佐賀県筑前町            |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-40447-chikuzen-machi-2023   |
    |     plateau-42202-sasebo-shi-2022      |           長崎県佐世保市           |   2022  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-42202-sasebo-shi-2022     |
    |      plateau-43204-arao-shi-2020       |            熊本県荒尾市            |   2020  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-43204-arao-shi-2020      |
    |    plateau-43100-kumamoto-shi-2022     |            熊本県熊本市            |   2022  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-43100-kumamoto-shi-2022    |
    |     plateau-43206-tamana-shi-2023      |            熊本県玉名市            |   2023  |  v3  |      https://www.geospatial.jp/ckan/dataset/plateau-43206-tamana-shi-2023     |
    |    plateau-43443-mashiki-machi-2023    |            熊本県益城町            |   2023  |  v3  |    https://www.geospatial.jp/ckan/dataset/plateau-43443-mashiki-machi-2023    |
    |      plateau-44204-hita-shi-2020       |            大分県日田市            |   2020  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-44204-hita-shi-2020      |
    |     plateau-45203-nobeoka-shi-2022     |            宮崎県延岡市            |   2022  |  v3  |     https://www.geospatial.jp/ckan/dataset/plateau-45203-nobeoka-shi-2022     |
    |      plateau-47201-naha-shi-2020       |            沖縄県那覇市            |   2020  |  v3  |       https://www.geospatial.jp/ckan/dataset/plateau-47201-naha-shi-2020      |


## 都市モデルをダウンロード・追加

都市モデルをダウンロード・追加するには、都市モデルのIDを指定して `plateaukit install` コマンドを実行します。

!!! warning ""
    サイズが大きいデータセットではダウンロードに時間がかかる場合があります。

```bash title="例: 神奈川県箱根町のデータをダウンロードして追加"
plateaukit install plateau-14382-hakone-machi-2020
plateaukit install plateau-14382-hakone-machi-2020 -v  # 進捗の詳細を表示
```

<div class="result" markdown>

```bash title="実行例"
$ plateaukit install plateau-14382-hakone-machi-2020
Download file as: .../plateaukit/data/14382_hakone-machi_2020_citygml_5_op.zip
Downloading... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 127.4/127.4 MB 0:00:00
```

</div>

または、事前にデータをダウンロードしておき、`--local` オプションにファイルを指定して追加することもできます。

```bash title="例: 事前にダウンロード済みの東京都23区のデータを追加 (CityGML)"
plateaukit install plateau-tokyo23ku-2022 --local ./13100_tokyo23-ku_2022_citygml_1_2_op/ --format citygml
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
plateaukit uninstall plateau-tokyo23ku-2022 # 東京都23区のデータを削除
```
