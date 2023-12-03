# Based on https://www.geospatial.jp/ckan/dataset/plateau

# %%

city_list = [
    {
        "dataset_id": "plateau-01100-sapporo-shi-2020",
        "city_name": "北海道札幌市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-01100-sapporo-shi-2020",
        "citygml": "5236a116-35be-46ea-a4d0-e840cc7ab3ac",
        "3dtiles": "2306f36e-603e-4be2-8a51-afd4054c7e82",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-01639-sarabetsu-mura-2022",
        "city_name": "北海道更別村",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-01639-sarabetsu-mura-2022",
        "citygml": "35daef49-396e-4c21-9e5c-d602e3a1833b",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-01205-muroran-shi-2022",
        "city_name": "北海道室蘭市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-01205-muroran-shi-2022",
        "citygml": "92bd06f2-7421-4ab9-aeeb-d886887c8a3a",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-02208-mutsu-shi-2022",
        "city_name": "青森県むつ市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-02208-mutsu-shi-2022",
        "citygml": "5f780e16-816d-4239-a345-83c5c0fe8919",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-03201-morioka-shi-2022",
        "city_name": "岩手県盛岡市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-03201-morioka-shi-2022",
        "citygml": "94b62d49-9c3f-4826-8016-8a7816e075cd",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-04100-sendai-shi-2022",
        "city_name": "宮城県仙台市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-04100-sendai-shi-2022",
        "citygml": "a1f35479-9339-4b97-a416-ff120c138db5",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-07204-iwaki-shi-2020",
        "city_name": "福島県いわき市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-07204-iwaki-shi-2020",
        "citygml": "6400e9dc-3dd2-46ad-821f-9072122f44e0",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-07203-koriyama-city-2020",
        "city_name": "福島県郡山市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-07203-koriyama-city-2020",
        "citygml": "ddbc5880-d584-4ce1-bfeb-0f8f46f0135b",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-07205-shirakawa-shi-2020",
        "city_name": "福島県白河市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-07205-shirakawa-shi-2020",
        "citygml": "91c776c5-142a-456c-83d4-7915e8cdb9f6",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-07212-minamisouma-shi-2022",
        "city_name": "福島県南相馬市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-07212-minamisouma-shi-2022",
        "citygml": "2784b256-8649-4375-85d6-ca29ff6de3d6",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-08234-hokota-shi-2020",
        "city_name": "茨城県鉾田市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-08234-hokota-shi-2020",
        "citygml": "02b00898-7370-467e-be92-b7d8a5e00a5a",
        "version": "2020",
    },
    {
        "dataset_id": "plateau-08234-hokota-shi-2022",
        "city_name": "茨城県鉾田市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-08234-hokota-shi-2022",
        "citygml": "1ee20390-7283-47ac-8d74-8db868a136bc",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-08220-tsukuba-shi-2022",
        "city_name": "茨城県つくば市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-08220-tsukuba-shi-2022",
        "citygml": "81551ff2-1680-42a8-a27c-3c01e0bc80ce",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-09201-utsunomiya-shi-2020",
        "city_name": "栃木県宇都宮市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-09201-utsunomiya-shi-2020",
        "citygml": "caa24ca5-5999-4f22-9d8e-8efb9df2cd2c",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-10203-kiryu-shi-2020",
        "city_name": "群馬県桐生市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-10203-kiryu-shi-2020",
        "citygml": "b947726e-c869-4ab9-9483-081ede143038",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-10207-tatebayashi-shi-2020",
        "city_name": "群馬県館林市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-10207-tatebayashi-shi-2020",
        "citygml": "675c8180-e02f-4e5c-ba6c-fc1f47c0ea8f",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-11202-kumagaya-shi-2020",
        "city_name": "埼玉県熊谷市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-11202-kumagaya-shi-2020",
        "citygml": "531c5b69-98b1-4d9f-ad11-89b95c450779",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-11100-saitama-shi-2020",
        "city_name": "埼玉県さいたま市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-11100-saitama-shi-2020",
        "citygml": "114a6d9e-d991-4f19-b686-ebcf5b74719a",
        "version": "2020",
    },
    {
        "dataset_id": "plateau-11100-saitama-shi-2022",
        "city_name": "埼玉県さいたま市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-11100-saitama-shi-2022",
        "citygml": "fbbf84ed-a6a4-4179-8933-f7b144d8e320",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-11224-toda-shi-2022",
        "city_name": "埼玉県戸田市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-11224-toda-shi-2022",
        "citygml": "4550fe74-0eee-4d39-8e35-ddb88898a7a4",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-11230-niiza-shi-2020",
        "city_name": "埼玉県新座市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-11230-niiza-shi-2020",
        "citygml": "d128f7b5-f361-44dd-b28e-e83943a40837",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-11238-hasuda-shi-2022",
        "city_name": "埼玉県蓮田市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-11238-hasuda-shi-2022",
        "citygml": "9397dcb6-1441-4eb7-a803-011d1aea95a5",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-11326-moroyama-machi-2020",
        "city_name": "埼玉県毛呂山町",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-11326-moroyama-machi-2020",
        "citygml": "ccdb3ff1-d01b-4669-9d55-6b0ad6da4a33",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-12217-kashiwa-shi-2020",
        "city_name": "千葉県柏市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-12217-kashiwa-shi-2020",
        "citygml": "44e88796-ba94-43a8-b89a-6f41436b97e0",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-12210-mobara-shi-2022",
        "city_name": "千葉県茂原市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-12210-mobara-shi-2022",
        "citygml": "612cd74e-8ed2-41da-ae0c-d176a2322e6a",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-12221-yachiyo-shi-2022",
        "city_name": "千葉県八千代市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-12221-yachiyo-shi-2022",
        "citygml": "f3c84060-a65c-4d25-8d30-f57dbe9aa569",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-tokyo23ku",
        "city_name": "東京都23区",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-tokyo23ku",
        "citygml": "0bab2b7f-6962-41c8-872f-66ad9b40dcb1",
        "3dtiles": "7e2b3b8f-10e0-4f6a-99ec-8ebad021c0d0",
        "version": "2020",
    },
    {
        "dataset_id": "plateau-tokyo23ku-2022",
        "city_name": "東京都23区",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-tokyo23ku-2022",
        "citygml": "55c72dd0-32eb-4107-9526-71fc0af8d50f",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-13229-nishitokyo-shi-2022",
        "city_name": "東京都西東京市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-13229-nishitokyo-shi-2022",
        "citygml": "7b9c2815-e739-4a3d-88cb-66b26106d60b",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-13201-hachioji-shi-2020",
        "city_name": "東京都八王子市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-13201-hachioji-shi-2020",
        "citygml": "4c4fb49e-fcd5-43de-87a1-835aeec0a164",
        "version": "2020",
    },
    {
        "dataset_id": "plateau-13201-hachioji-shi-2022",
        "city_name": "東京都八王子市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-13201-hachioji-shi-2022",
        "citygml": "ef7d1a60-334d-44c6-98c8-e8409779e889",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-13213-higashimurayama-shi-2020",
        "city_name": "東京都東村山市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-13213-higashimurayama-shi-2020",
        "citygml": "4877a936-c244-468f-8bb1-3d3bfa606528",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-14130-kawasaki-shi-2020",
        "city_name": "神奈川県川崎市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-14130-kawasaki-shi-2020",
        "citygml": "51a8a702-03ee-45db-9136-3881daba2477",
        "version": "2020",
    },
    {
        "dataset_id": "plateau-14130-kawasaki-shi-2022",
        "city_name": "神奈川県川崎市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-14130-kawasaki-shi-2022",
        "citygml": "17d4084d-9fed-4194-bc1c-37de9f2a9c7a",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-14150-sagamihara-shi-2020",
        "city_name": "神奈川県相模原市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-14150-sagamihara-shi-2020",
        "citygml": "b910d62c-6a89-4b91-aaec-8a7596432139",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-14382-hakone-machi-2020",
        "city_name": "神奈川県箱根町",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-14382-hakone-machi-2020",
        "citygml": "d2a7c149-6519-40a6-a06d-9b6512304b23",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-14201-yokosuka-shi-2020",
        "city_name": "神奈川県横須賀市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-14201-yokosuka-shi-2020",
        "citygml": "31c6a382-f922-42d7-85e0-26ab2c6655ca",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-14100-yokohama-city-2020",
        "city_name": "神奈川県横浜市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-14100-yokohama-city-2020",
        "citygml": "ef70f915-2347-4b50-9008-46a6027bda4b",
        "version": "2020",
    },
    {
        "dataset_id": "plateau-14100-yokohama-shi-2022",
        "city_name": "神奈川県横浜市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-14100-yokohama-shi-2022",
        "citygml": "f4ba72a5-d693-4947-a6ed-547ca346c3c1",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-15100-niigata-shi-2020",
        "city_name": "新潟県新潟市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-15100-niigata-shi-2020",
        "citygml": "1ecc0b56-f9ab-4ab9-b70e-691698a9e4ee",
        "version": "2020",
    },
    {
        "dataset_id": "plateau-15100-niigata-shi-2022",
        "city_name": "新潟県新潟市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-15100-niigata-shi-2022",
        "citygml": "0b0d7ed2-ed57-41f4-b481-11e0454c71a9",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-17206-kaga-shi-2020",
        "city_name": "石川県加賀市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-17206-kaga-shi-2020",
        "citygml": "bf13fbef-e717-446d-a325-25f229e5248d",
        "version": "2020",
    },
    {
        "dataset_id": "plateau-17206-kaga-shi-2021",
        "city_name": "石川県加賀市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-17206-kaga-shi-2021",
        "citygml": "50b61a19-e6bd-437d-9cc1-88eb7042af78",
        "version": "2021",
    },
    {
        "dataset_id": "plateau-17206-kaga-shi-2022",
        "city_name": "石川県加賀市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-17206-kaga-shi-2022",
        "citygml": "dea2a59d-dede-42b9-bc4a-ed270eb3cdc4",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-17201-kanazawa-shi-2020",
        "city_name": "石川県金沢市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-17201-kanazawa-shi-2020",
        "citygml": "87b8b2de-fd92-4710-9f88-d6ccd8693be1",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-20209-ina-shi-2020",
        "city_name": "長野県伊那市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-20209-ina-shi-2020",
        "citygml": "fbaaced1-a87b-405a-aef5-ce1b36e812d8",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-20204-okaya-shi-2020",
        "city_name": "長野県岡谷市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-20204-okaya-shi-2020",
        "citygml": "fbd57aeb-6832-48d1-b5e1-163371d3de2b",
        "version": "2020",
    },
    {
        "dataset_id": "plateau-20204-okaya-shi-2022",
        "city_name": "長野県岡谷市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-20204-okaya-shi-2022",
        "citygml": "59775dd6-0d4b-468a-9581-5c995a5e8bda",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-20217-saku-shi-2022",
        "city_name": "長野県佐久市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-20217-saku-shi-2022",
        "citygml": "6bcf4ae5-86ce-4228-be3c-2f26652102f0",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-20214-chino-shi-2020",
        "city_name": "長野県茅野市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-20214-chino-shi-2020",
        "citygml": "3755ab32-a73d-429d-8583-869850c6053c",
        "version": "2020",
    },
    {
        "dataset_id": "plateau-20214-chino-shi-2022",
        "city_name": "長野県茅野市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-20214-chino-shi-2022",
        "citygml": "45ce6f76-5564-4799-8352-e6e8a7398d03",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-20202-matsumoto-shi-2020",
        "city_name": "長野県松本市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-20202-matsumoto-shi-2020",
        "citygml": "40591402-8363-4512-88ac-3d191a806e8d",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-21201-gifu-shi-2020",
        "city_name": "岐阜県岐阜市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-21201-gifu-shi-2020",
        "citygml": "a8f0da53-862a-4116-a53f-f81690a38d5c",
        "version": "2020",
    },
    {
        "dataset_id": "plateau-21201-gifu-shi-2022",
        "city_name": "岐阜県岐阜市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-21201-gifu-shi-2022",
        "citygml": "08e8f100-7827-4cfa-82e6-f4c8a9665793",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-21211-minokamo-shi-2022",
        "city_name": "岐阜県美濃加茂市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-21211-minokamo-shi-2022",
        "citygml": "3825d2f6-e1de-4e69-bda5-1621aeda2af3",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-19201-kofu-shi-2022",
        "city_name": "山梨県甲府市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-19201-kofu-shi-2022",
        "citygml": "8931fbf1-1873-4406-84da-85f2b1187fd6",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22205-atami-shi-2022",
        "city_name": "静岡県熱海市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22205-atami-shi-2022",
        "citygml": "23c6f893-209f-4ebd-a4be-8a8310f85396",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22222-izu-shi-2022",
        "city_name": "静岡県伊豆市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22222-izu-shi-2022",
        "citygml": "f1b756f2-ccce-4e05-a67e-43d542d7613b",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22225-izunokuni-shi-2022",
        "city_name": "静岡県伊豆の国市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22225-izunokuni-shi-2022",
        "citygml": "db3e4121-9342-4d6e-89ac-4cc376501374",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22208-ito-shi-2022",
        "city_name": "静岡県伊東市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22208-ito-shi-2022",
        "citygml": "6f4a97b6-64b6-474d-b28c-c8fb98d36937",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22211-iwata-shi-2022",
        "city_name": "静岡県磐田市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22211-iwata-shi-2022",
        "citygml": "3f9a656b-36b1-4d0f-b4e2-3a9da72d6c30",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22223-omaezaki-shi-2022",
        "city_name": "静岡県御前崎市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22223-omaezaki-shi-2022",
        "citygml": "0778768e-f2cd-4e67-b298-98a87188f360",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22344-oyama-cho-2022",
        "city_name": "静岡県小山町",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22344-oyama-cho-2022",
        "citygml": "f1a32827-15d1-4f3a-b130-23bc3a26c651",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22213-kakegawa-shi-2020",
        "city_name": "静岡県掛川市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22213-kakegawa-shi-2020",
        "citygml": "b6690396-44f5-46e4-90b2-9ba5ab00a388",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22302-kawazu-cho-2022",
        "city_name": "静岡県河津町",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22302-kawazu-cho-2022",
        "citygml": "02f2902f-e400-448d-8388-ddc5dcf1768b",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22325-kannami-cho-2022",
        "city_name": "静岡県函南町",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22325-kannami-cho-2022",
        "citygml": "53c7d344-c261-42b6-88d2-4ad32efd4c44",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22224-kikugawa-city-2020",
        "city_name": "静岡県菊川市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22224-kikugawa-city-2020",
        "citygml": "f2a8c891-73ff-40f8-a88a-d1415e5a8725",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22221-kosai-shi-2022",
        "city_name": "静岡県湖西市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22221-kosai-shi-2022",
        "citygml": "1c61303d-eebc-4699-9e96-519b38fee92f",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22215-gotenba-shi-2022",
        "city_name": "静岡県御殿場市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22215-gotenba-shi-2022",
        "citygml": "f2187864-6d63-499e-a526-76dcbd2413a7",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22100-shizuoka-shi-2022",
        "city_name": "静岡県静岡市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22100-shizuoka-shi-2022",
        "citygml": "6f0e8388-0dfe-4fcb-aadf-9f41cd26df65",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22341-shimizu-cho-2022",
        "city_name": "静岡県清水町",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22341-shimizu-cho-2022",
        "citygml": "f03efa32-d0ce-4689-932f-c88141849bac",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22219-shimoda-shi-2022",
        "city_name": "静岡県下田市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22219-shimoda-shi-2022",
        "citygml": "fda8a9e7-9443-4b0a-87c8-ce963f7eb716",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22220-susono-shi-2022",
        "city_name": "静岡県裾野市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22220-susono-shi-2022",
        "citygml": "7e21dc08-7651-4a5f-95c2-b4ddc30034e0",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22342-nagaizumi-cho-2022",
        "city_name": "静岡県長泉町",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22342-nagaizumi-cho-2022",
        "citygml": "7fea2135-bdee-40d2-811e-6c1c7e9eca2a",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22203-numazu-shi-2020",
        "city_name": "静岡県沼津市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22203-numazu-shi-2020",
        "citygml": "71b80915-1c17-4975-a8f2-c69871cee1f5",
        "version": "2020",
    },
    {
        "dataset_id": "plateau-22203-numazu-shi-2021",
        "city_name": "静岡県沼津市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22203-numazu-shi-2021",
        "citygml": "758fe63a-b20f-4d5d-817d-c35eac530143",
        "version": "2021",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22301-higashiizu-cho-2022",
        "city_name": "静岡県東伊豆町",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22301-higashiizu-cho-2022",
        "citygml": "407f7b68-0b25-407a-96b8-de176f746e94",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22216-fukuroi-shi-2022",
        "city_name": "静岡県袋井市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22216-fukuroi-shi-2022",
        "citygml": "864d2ca4-045f-490e-ba05-abcbceaeed5d",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22210-fuji-shi-2022",
        "city_name": "静岡県富士市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22210-fuji-shi-2022",
        "citygml": "00da73ef-4aa5-4a04-bd39-ee6bc96a87bd",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22214-fujieda-shi-2022",
        "city_name": "静岡県藤枝市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22214-fujieda-shi-2022",
        "citygml": "0967b2b0-f23b-4d25-85d6-cdc33f2c6b5e",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22207-fujinomiya-shi-2022",
        "city_name": "静岡県富士宮市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22207-fujinomiya-shi-2022",
        "citygml": "75aa2464-afea-44ae-abeb-bc6779895b7f",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22226-makinohara-shi-2022",
        "city_name": "静岡県牧之原市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22226-makinohara-shi-2022",
        "citygml": "3958611b-2ad3-4ce0-a21f-ea78fce3556c",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22206-mishima-shi-2022",
        "city_name": "静岡県三島市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22206-mishima-shi-2022",
        "citygml": "85ec9a31-5960-433e-b352-55928cc63480",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22304-minamiizu-cho-2022",
        "city_name": "静岡県南伊豆町",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22304-minamiizu-cho-2022",
        "citygml": "05d34943-457e-46c7-a890-a729e4658916",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22461-mori-machi-2022",
        "city_name": "静岡県森町",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22461-mori-machi-2022",
        "citygml": "943ccee9-6b92-45d9-b288-f2f3d3dd31ac",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22212-yaizu-shi-2022",
        "city_name": "静岡県焼津市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22212-yaizu-shi-2022",
        "citygml": "da88169b-3763-4065-9191-f75f6cb03726",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-22424-yoshida-cho-2022",
        "city_name": "静岡県吉田町",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-22424-yoshida-cho-2022",
        "citygml": "8d07cf7e-9fdb-4f4c-848c-77c62bcca52d",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-23212-anjo-shi-2020",
        "city_name": "愛知県安城市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-23212-anjo-shi-2020",
        "citygml": "2f3b2351-e7fd-4553-bd00-1424bb05964b",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-23202-okazaki-shi-2020",
        "city_name": "愛知県岡崎市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-23202-okazaki-shi-2020",
        "citygml": "481fde81-ee89-4e1d-a26e-44ec2719d46d",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-23206-kasugai-shi-2022",
        "city_name": "愛知県春日井市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-23206-kasugai-shi-2022",
        "citygml": "199e5bdd-4a2d-479c-8f1a-7d4d75770c10",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-23208-tsushima-shi-2020",
        "city_name": "愛知県津島市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-23208-tsushima-shi-2020",
        "citygml": "18613a1d-16eb-4aa5-aaff-08a40d1aab8b",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-23207-toyokawa-shi-2022",
        "city_name": "愛知県豊川市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-23207-toyokawa-shi-2022",
        "citygml": "809deb42-c22d-498c-afd9-be2249730899",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-23100-nagoya-shi-2020",
        "city_name": "愛知県名古屋市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-23100-nagoya-shi-2020",
        "citygml": "718bf496-7da7-4b7f-83c3-98dd4a8e3acb",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-23230-nisshin-shi-2022",
        "city_name": "愛知県日進市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-23230-nisshin-shi-2022",
        "citygml": "cee5a327-2a72-43ba-935d-4a4bedd86097",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-24212-kumano-shi-2022",
        "city_name": "三重県熊野市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-24212-kumano-shi-2022",
        "citygml": "a63fbbf5-ab09-40d7-9893-31280ee09386",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-24202-yokkaichi-shi-2022",
        "city_name": "三重県四日市市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-24202-yokkaichi-shi-2022",
        "citygml": "f3a2a85c-e1a8-40d8-8c70-c8be6f77ebfa",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-26100-kyoto-shi-2022",
        "city_name": "京都府京都市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-26100-kyoto-shi-2022",
        "citygml": "3da2e055-45a8-4212-bc0e-e769e5f58683",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-27204-ikeda-shi-2020",
        "city_name": "大阪府池田市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-27204-ikeda-shi-2020",
        "citygml": "8c1b439c-893c-435c-a850-7c91721ede63",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-27100-osaka-shi-2020",
        "city_name": "大阪府大阪市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-27100-osaka-shi-2020",
        "citygml": "de8fd635-f08c-4143-b22e-c145e695dc43",
        "version": "2020",
    },
    {
        "dataset_id": "plateau-27100-osaka-shi-2022",
        "city_name": "大阪府大阪市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-27100-osaka-shi-2022",
        "citygml": "63ba6765-6d33-4f44-9abb-3fa8000c2b3f",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-27221-kashiwara-shi-2022",
        "city_name": "大阪府柏原市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-27221-kashiwara-shi-2022",
        "citygml": "59662350-46eb-4549-a3b8-29227ad56b85",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-27216-kawachinagano-shi-2022",
        "city_name": "大阪府河内長野市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-27216-kawachinagano-shi-2022",
        "citygml": "9ae655e2-a0b5-4d8d-8ade-6405abfc2a8e",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-27140-sakai-shi-2022",
        "city_name": "大阪府堺市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-27140-sakai-shi-2022",
        "citygml": "549d1361-0f67-4ec9-86b8-9577d7684f0d",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-27224-settsu-shi-2020",
        "city_name": "大阪府摂津市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-27224-settsu-shi-2020",
        "citygml": "a4eaa3a3-8edc-49db-99f9-9815490cc5fe",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-27207-takatsuki-shi-2020",
        "city_name": "大阪府高槻市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-27207-takatsuki-shi-2020",
        "citygml": "d58a6a37-14dd-4584-a0eb-43c026e705e1",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-27341-tadaoka-cho-2020",
        "city_name": "大阪府忠岡町",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-27341-tadaoka-cho-2020",
        "citygml": "f425d011-2d9c-41e6-bb84-d02e5e4a4b04",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-27203-toyonaka-shi-2020",
        "city_name": "大阪府豊中市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-27203-toyonaka-shi-2020",
        "citygml": "25973afa-4fc8-4d4c-a3a6-f8b2b8efebec",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-28225-asago-shi-2022",
        "city_name": "兵庫県朝来市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-28225-asago-shi-2022",
        "citygml": "c0160066-1c17-4920-a88d-b7bca4443951",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-28210-kakogawa-shi-2020",
        "city_name": "兵庫県加古川市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-28210-kakogawa-shi-2020",
        "citygml": "8ec3a81f-5968-449d-8a65-08a1271bc3f2",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-30422-taiji-cho-2021",
        "city_name": "和歌山県太地町",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-30422-taiji-cho-2021",
        "citygml": "021bba37-7720-4eb4-9445-0626ffdbf23b",
        "version": "2021",
        "latest": True,
    },
    {
        "dataset_id": "plateau-30201-wakayama-shi-2022",
        "city_name": "和歌山県和歌山市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-30201-wakayama-shi-2022",
        "citygml": "33c59d3e-0840-4c24-9246-9b11abaedcb0",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-31201-tottori-shi-2020",
        "city_name": "鳥取県鳥取市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-31201-tottori-shi-2020",
        "citygml": "6f8355f0-0d2d-485c-b1c0-85ac9929dd8d",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-34304-kaita-cho-2021",
        "city_name": "広島県海田町",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-34304-kaita-cho-2021",
        "citygml": "b7f7ccc1-2008-4cde-8b71-cb673d2a073b",
        "version": "2021",
        "latest": True,
    },
    {
        "dataset_id": "plateau-34202-kure-shi-2020",
        "city_name": "広島県呉市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-34202-kure-shi-2020",
        "citygml": "9f10c73f-c073-40e5-ac14-e429c32c3b15",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-34100-hirosima-shi-2022",
        "city_name": "広島県広島市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-34100-hirosima-shi-2022",
        "citygml": "cd9cf494-84f7-4c59-af3d-ed47d9663dcf",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-34207-fukuyama-shi-2020",
        "city_name": "広島県福山市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-34207-fukuyama-shi-2020",
        "citygml": "b7076aa0-40de-4eab-a863-064ae600ff1d",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-34208-fuchu-shi-2022",
        "city_name": "広島県府中市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-34208-fuchu-shi-2022",
        "citygml": "733b4687-1a4e-415a-84a0-c98f44513814",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-37201-takamatsu-shi-2022",
        "city_name": "香川県高松市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-37201-takamatsu-shi-2022",
        "citygml": "48ac360d-6c98-43d6-aeec-9a7510ca53bb",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-38201-matsuyama-shi-2020",
        "city_name": "愛媛県松山市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-38201-matsuyama-shi-2020",
        "citygml": "6cfb40c0-875a-45ec-a0da-32157af8b15b",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-41423-omachi-cho-2022",
        "city_name": "佐賀県大町町",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-41423-omachi-cho-2022",
        "citygml": "2924c864-e79d-407d-9b38-845559733606",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-41208-ogi-shi-2022",
        "city_name": "佐賀県小城市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-41208-ogi-shi-2022",
        "citygml": "18a50707-b4e4-49ce-b1c3-388bbf569fa3",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-41424-kouhoku-machi-2022",
        "city_name": "佐賀県江北町",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-41424-kouhoku-machi-2022",
        "citygml": "1d3b5000-305c-4dc4-aebc-277cf225ff30",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-41425-shiroisi-chou-2022",
        "city_name": "佐賀県白石町",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-41425-shiroisi-chou-2022",
        "citygml": "f10717be-cd02-4f98-bb72-2c60cb43935c",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-41206-takeo-shi-2022",
        "city_name": "佐賀県武雄市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-41206-takeo-shi-2022",
        "citygml": "71f8ff13-95b7-4dd9-87ee-ffcfcbc32209",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-40205-iizuka-shi-2020",
        "city_name": "福岡県飯塚市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-40205-iizuka-shi-2020",
        "citygml": "34da8e32-7f3b-4a61-87da-2f55d6b563b2",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-40225-ukiha-shi-2022",
        "city_name": "福岡県うきは市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-40225-ukiha-shi-2022",
        "citygml": "ff501855-b467-4d90-9217-48173a469cc4",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-40100-kitakyushu-shi-2020",
        "city_name": "福岡県北九州市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-40100-kitakyushu-shi-2020",
        "citygml": "a393587f-b4bf-4cc9-b5c3-23bbe20572c9",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-40203-kurume-shi-2020",
        "city_name": "福岡県久留米市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-40203-kurume-shi-2020",
        "citygml": "66e8e343-05e8-4850-8cd6-c7c97c432f2e",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-40130-fukuoka-shi-2022",
        "city_name": "福岡県福岡市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-40130-fukuoka-shi-2022",
        "citygml": "f1fa5f41-b876-47bb-b54c-766f0657d1c0",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-40220-munakata-shi-2020",
        "city_name": "福岡県宗像市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-40220-munakata-shi-2020",
        "citygml": "345e8989-2cab-4e26-8174-a344d8ee1b5d",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-43204-arao-shi-2020",
        "city_name": "熊本県荒尾市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-43204-arao-shi-2020",
        "citygml": "f0345e11-2ef0-4600-9b23-402949e43c0f",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-43100-kumamoto-shi-2020",
        "city_name": "熊本県熊本市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-43100-kumamoto-shi-2020",
        "citygml": "211ac99a-b176-4f6a-ad7f-4d7d1d0dcf77",
        "version": "2020",
    },
    {
        "dataset_id": "plateau-43100-kumamoto-shi-2022",
        "city_name": "熊本県熊本市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-43100-kumamoto-shi-2022",
        "citygml": "05b3ba0d-2402-4ca4-99bb-a441323f3b9f",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-43206-tamana-shi-2020",
        "city_name": "熊本県玉名市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-43206-tamana-shi-2020",
        "citygml": "10b6f58a-dbff-4844-963a-c8780fb8bacd",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-43443-mashiki-machi-2020",
        "city_name": "熊本県益城町",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-43443-mashiki-machi-2020",
        "citygml": "a9cfbc79-c00f-4698-95fb-2b8f9a538f60",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-44204-hita-shi-2020",
        "city_name": "大分県日田市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-44204-hita-shi-2020",
        "citygml": "72cac244-9c3e-4ab4-afad-74ad0cc3ad80",
        "version": "2020",
        "latest": True,
    },
    {
        "dataset_id": "plateau-45203-nobeoka-shi-2022",
        "city_name": "宮崎県延岡市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-45203-nobeoka-shi-2022",
        "citygml": "2aca8a01-32e4-406f-a4c4-92f95b99a9c0",
        "version": "2022",
        "latest": True,
    },
    {
        "dataset_id": "plateau-47201-naha-shi-2020",
        "city_name": "沖縄県那覇市",
        "homepage": "https://www.geospatial.jp/ckan/dataset/plateau-47201-naha-shi-2020",
        "citygml": "59819ec2-c617-4508-9827-994cf7b4cae6",
        "version": "2020",
        "latest": True,
    },
]

# import json

# # print(json.dumps(city_list, ensure_ascii=False, indent=2))

# # %%
# import requests

# resp = requests.get("https://www.geospatial.jp/ckan/dataset/plateau")

# # %%
# import re
# from lxml import html

# # print(resp.text)

# root = html.fromstring(resp.text)
# el = root.find_class("embedded-content")[0]
# content = html.tostring(el, encoding="unicode")
# content = content.replace("\n", "")
# # print(content)

# m_all = re.findall(r"strong>(.*?)</strong>(.*?)<p><", content) # TODO: include last one!
# m_all = m_all[3:]

# # print(len(m), m)

# result = []

# for pref_name, pref_part in m_all:
#     # if pref_name == "茨城県":
#     #     print(pref_name, pref_part)
#     m_cities = re.findall(
#         r'<a href="https://www.geospatial.jp/ckan/dataset/(.*?)" title="(.*?)(\d\d\d\d)">.*?</a>',
#         pref_part,
#     )
#     # print(pref_name)
#     # print(m_cities)

#     for dataset_id, name, year in m_cities:
#         result.append(
#             {
#                 "dataset_id": dataset_id,
#                 "city_name": pref_name + name,
#                 "homepage": f"https://www.geospatial.jp/ckan/dataset/{dataset_id}",
#                 # "citygml": None,
#                 # "3dtiles": None,
#             }
#         )

# import json

# print(json.dumps(result, ensure_ascii=False, indent=2))


# # %%

# # diff1 = {x["dataset_id"] for x in city_list} - {x["dataset_id"] for x in result}
# diff2 = {x["dataset_id"] for x in result} - {x["dataset_id"] for x in city_list}
# diff2

# # %%
# from time import sleep

# final_result = []

# for city in result:
#     if city["dataset_id"] not in diff2:
#         city = next(x for x in city_list if x["dataset_id"] == city["dataset_id"])
#         final_result.append(city)
#         continue
#     resp = requests.get(city["homepage"])
#     text = resp.text # .replace("\n", "")

#     ms = re.findall(r'<a class="heading" href=".*?/resource/(.*?)" title="(CityGML.*?)">', text)

#     for i, m in enumerate(ms):
#         print(i, m)

#     if len(ms) == 1:
#         city["citygml"] = ms[take][0]
#         final_result.append(city)
#         sleep(1)
#         continue

#     take = int(input("Which one? "))
#     city["citygml"] = ms[take][0]

#     final_result.append(city)

# print(json.dumps(final_result, ensure_ascii=False, indent=2))
# # for city in city_list:
# #     print({"dataset_id": re.match("https://www.geospatial.jp/ckan/dataset/(.*)", city[1]).group(1), "city_name": city[0], "homepage": city[1]}, ",")

# # for city in city_list:
# #     print(
# #         f'"{city["dataset_id"]}": {{ "city_name": "{city["city_name"]}", "homepage": "{city["homepage"]}"}},'
# #     )

# # %%

# import re

# new_city_list = []

# for city in city_list:
#     try:
#         dataset_id = city["dataset_id"]
#         m = re.match(r".*-(\d\d\d\d)", dataset_id)
#         year = m.group(1)
#         city["version"] = year
#     except:
#         print(city)
#         year = input("year:")
#         city["version"] = year

#     new_city_list.append(city)


# new_city_list

# # %%

# new_city_list = []

# for city in city_list:
#     if [x["city_name"] for x in city_list].count(city["city_name"]) == 1:
#         city["latest"] = True
#     else:
#         cities = [x for x in city_list if x["city_name"] == city["city_name"]]
#         latest_year = max([int(x["version"]) for x in cities])
#         if city["version"] == str(latest_year):
#             city["latest"] = True

#     new_city_list.append(city)


# new_city_list
