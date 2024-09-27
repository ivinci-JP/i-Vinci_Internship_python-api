import csv
import pprint
import requests
import json

#inputファイルの読み込み
with open('jusyo.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    # 出力用のCSVファイルを作成
    with open('jusyocheck.csv', mode='w', newline='',encoding='utf-8') as output_file:

        #1件ずつ読み込み
        for row in csv_reader:
            
            #データを格納
            #csvの7番目の項目（郵便番号）を取得
            *_, input_addr = row[:7]

            #API実施
            url = "https://zipcloud.ibsnet.co.jp/api/search"
            payload = {"zipcode": input_addr}
            res = requests.get(url, params=payload)

            #APIの実行結果を変数に格納
            jsonData = res.json()

            #住所チェックのため、入力された都道府県市区町村を取得
            *_, input_ken = row[:8]
            *_, input_si = row[:9]
            *_, input_cyou = row[:10]

            #入力された都道府県市区町村を連結しては変数に格納
            input_full_address = str(input_ken) + str(input_si) + str(input_cyou) 

            #APIの返却結果がNoneじゃなかった場合
            if jsonData["results"] is not None:
            
                #responseの最初のJsonオブジェクトを取得
                results = jsonData["results"][0]
                
                #APIから返却された都道府県市区町村を連結して変数に格納
                res_full_address = results['address1'] + results['address2'] + results['address3']
    
                #入力された住所とAPIの実行結果を比較    
                if input_full_address != res_full_address:

                    #入力値をcsvに出力するために配列に格納
                    data = [row]

                    # CSVファイルにデータを書き込む
                    with open('jusyocheck.csv', mode='a', newline='') as output_file:
                        writer = csv.writer(output_file)
                        writer.writerows(data)
                    print(jsonData["status"])
                    print("入力された郵便番号または住所に誤りがあります")
                    print("入力された住所：" + input_full_address)
                    print("APIから返却された住所：" + res_full_address)

            #APIの返却結果がNoneだった場合
            else:
                #入力値をcsvに出力するために配列に格納
                data = [row]

                # CSVファイルにデータを書き込む
                with open('jusyocheck.csv', mode='a', newline='') as output_file:
                    writer = csv.writer(output_file)
                    writer.writerows(data)
                print(jsonData["status"])
                print("入力された郵便番号に誤りがあります")
#API