import pandas as pd
from prophet import Prophet
from google.colab import files

# 1. データの読み込み
file_path = '/訪日外国人_加工データ.csv'
df_processed = pd.read_csv(file_path)

# 日付形式の整形
df_processed['Month_num'] = df_processed['Month'].str.replace('月', '').astype(int)
df_processed['Date'] = pd.to_datetime(df_processed['Year'].astype(str) + '-' + df_processed['Month_num'].astype(str) + '-01')

# 2. 「総計」データの作成
df_total_sum = df_processed.groupby('Date')['Visitors'].sum().reset_index()
df_total_sum['Country'] = '総計'

# 3. 予測対象のトップ10 ＋ 総計
target_countries = ['総計', '中国', '韓国', '台湾', '香港', '米国', 'タイ', '豪州', 'フィリピン', 'シンガポール', 'ベトナム']

all_forecasts = []

print(f"{len(target_countries)}件の市場の予測を開始します...\n")

for country in target_countries:
    print(f"▶ {country} の分析を実行中...")

    # 対象データの抽出
    if country == '総計':
        df_target = df_total_sum.copy()
    else:
        df_target = df_processed[df_processed['Country'] == country].copy()

    # 【手順③】元データから「コロナ期間も含む本物の合計値」を取り出す
    df_actual_sum = df_target[['Date', 'Visitors']].copy()
    df_actual_sum.columns = ['ds', 'Actual_Sum']

    # Prophet形式に変換
    df_prophet = df_target[['Date', 'Visitors']].copy()
    df_prophet.columns = ['ds', 'y']

    # 【手順②】コロナ期間（2020年〜2022年）を「空（None）」にする
    df_prophet.loc[(df_prophet['ds'] >= '2020-01-01') & (df_prophet['ds'] <= '2022-12-31'), 'y'] = None

    # モデルの作成と学習
    model = Prophet(yearly_seasonality=True, interval_width=0.8)
    model.fit(df_prophet)

    # 2027年末までの未来の枠を作成（25ヶ月分）
    future = model.make_future_dataframe(periods=25, freq='MS')
    forecast = model.predict(future)

    # 【手順①＆②】AIの予測結果と本物の実績を結合 (how='left')
    df_final = pd.merge(forecast, df_actual_sum, on='ds', how='left')

    # 【追加処理】予測値(yhat)をベースに「Combined_Line」を作成し、過去分をすべて「本物の数字(Actual_Sum)」で上書き
    # これにより「過去の実績〜未来の予測」が綺麗に繋がった1本の線になります
    df_final['Combined_Line'] = df_final['yhat']
    mask_past = df_final['Actual_Sum'].notna() # 実績データが存在する全期間
    df_final.loc[mask_past, 'Combined_Line'] = df_final['Actual_Sum']

    # コロナ期間フラグを追加（Tableauでの色分け用）
    df_final['Is_Corona_Period'] = df_final['ds'].apply(
        lambda x: 1 if '2020-01-01' <= str(x) <= '2022-12-31' else 0
    )

    # カラム名をTableau用に整理
    df_tableau = df_final[[
        'ds', 'yhat', 'Actual_Sum', 'Combined_Line',
        'yhat_lower', 'yhat_upper', 'trend', 'Is_Corona_Period'
    ]].copy()

    df_tableau.columns = [
        'Date',             # 日付
        'Ideal_Forecast',   # AIが計算した理想の推移（yhat）
        'Raw_Actual_Sum',   # 元データの実績合計
        'Combined_Line',    # 【メイン】実績と予測を一本に繋いだ線
        'Forecast_Lower',   # 予測の下限
        'Forecast_Upper',   # 予測の上限
        'Base_Trend',       # 長期的な成長トレンド
        'Is_Corona_Period'  # コロナ期間かどうかの判定（0 or 1）
    ]

    # ★追加：Tableauのフィルターで切り替えるための「国名」列
    df_tableau['Country'] = country

    all_forecasts.append(df_tableau)

# 4. 全国の結果を1つに統合
df_final_all = pd.concat(all_forecasts, ignore_index=True)

# カラムの並び順を綺麗に整える（CountryをDateの隣に配置）
cols = ['Date', 'Country', 'Ideal_Forecast', 'Raw_Actual_Sum', 'Combined_Line', 'Forecast_Lower', 'Forecast_Upper', 'Base_Trend', 'Is_Corona_Period']
df_final_all = df_final_all[cols]

# 5. CSVとして保存
output_file = 'japan_tourism_top10_analysis_final_2027.csv'
df_final_all.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n✅ 全国のCSV作成完了: {output_file}")

# 6. ファイルをローカルPCにダウンロード
files.download(output_file)

# 2021年4月のデータをチラ見して検証（総計のデータ）
print("\n--- 総計の2021年4月のデータ（検証） ---")
print(df_final_all[(df_final_all['Country'] == '総計') & (df_final_all['Date'] == '2021-04-01')])
