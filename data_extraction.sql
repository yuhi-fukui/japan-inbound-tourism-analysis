-- Query 1: Count records by market
SELECT
  Market,
  COUNT(*) AS record_count
FROM `Inbound01.INB01`
GROUP BY Market
ORDER BY record_count DESC;


-- Query 2: Preview non-total records
SELECT *
FROM `Inbound01.INB01`
WHERE Market NOT LIKE '%計'
  AND Market != '総数'
LIMIT 1000;


-- Query 3: Get distinct market names
SELECT DISTINCT Market
FROM `Inbound01.INB01`
WHERE Market NOT LIKE '%計'
  AND Market != '総数';


-- Query 4: Create base country-level dataset
SELECT
  Year,
  Month,
  Market AS Country,
  Visitors,
  Growth_Rate,
  ROUND(Growth_Rate / 100, 3) AS Growth_Rate1
FROM `Inbound01.INB01`;


-- Query 5: Regional classification for analysis
SELECT
  Year,
  Month,
  CASE
    WHEN Market IN ('韓国', '中国', '台湾', '香港', 'マカオ', 'モンゴル') THEN '東アジア'
    WHEN Market IN ('タイ', 'シンガポール', 'マレーシア', 'インドネシア', 'フィリピン', 'ベトナム', 'インド', 'その他アジア') THEN '東南アジア・南アジア'
    WHEN Market IN ('英国', 'フランス', 'ドイツ', 'イタリア', 'ロシア', 'スペイン', 'スウェーデン', 'オランダ', 'スイス', 'ベルギー', 'フィンランド', 'ポーランド', 'デンマーク', 'ノルウェー', 'オーストリア', 'ポルトガル', 'アイルランド', 'その他ヨーロッパ') THEN 'ヨーロッパ'
    WHEN Market IN ('米国', 'カナダ', 'その他北アメリカ') THEN '北米'
    WHEN Market IN ('メキシコ', 'ブラジル', 'その他南アメリカ') THEN '中南米'
    WHEN Market IN ('豪州', 'ニュージーランド', 'その他オセアニア') THEN 'オセアニア'
    WHEN Market IN ('イスラエル', 'トルコ', 'GCC6か国') THEN '中東'
    ELSE 'その他'
  END AS Area_Name,
  Market AS Country,
  Visitors,
  ROUND(Growth_Rate / 100, 3) AS Growth_Rate
FROM `Inbound01.INB01`
WHERE Market NOT LIKE '%計'
  AND Market NOT IN (
    '総数',
    '無国籍・その他',
    '中東地域',
    '北欧地域'
  );
