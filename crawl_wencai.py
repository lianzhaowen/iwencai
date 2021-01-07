from copy import deepcopy
import requests
import pandas as pd


headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': '1',
        #   'If-Modified-Since': 'Thu, 11 Jan 2018 07:05:01 GMT',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}

headers_wc = deepcopy(headers)
headers_wc["Referer"] = "http://www.iwencai.com/unifiedwap/unified-wap/result/get-stock-pick"
headers_wc["Host"] = "www.iwencai.com"
headers_wc["X-Requested-With"] = "XMLHttpRequest"

Question_url = "http://www.iwencai.com/unifiedwap/unified-wap/result/get-stock-pick"


def QA_fetch_get_stock_daily(trade_date, fields):
    pass


def crawl_data_from_wencai(trade_date, fields):
    """通过问财接口抓取数据
    
    Arguments:
        trade_date {[type]} -- [description]
        fields {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    payload = {
        # 查询问句
        "question": "{},{},上市日期<={}".format(trade_date, ",".join(fields), trade_date),
        # 返回查询记录总数 
        "perpage": 5000,
        "query_type": "stock"
    }

    try:
        response = requests.get(Question_url, params=payload, headers=headers_wc)

        if response.status_code == 200:
            json = response.json()
            df_data = pd.DataFrame(json["data"]["data"])
            # 规范返回的columns，去掉[xxxx]内容
            df_data.columns = [col.split("[")[0] for col in df_data.columns]
            # 筛选查询字段，非查询字段丢弃
            df = df_data[fields]
            # 增加列, 交易日期 code 设置索引
            return df.assign(trade_date=trade_date, code=df["股票代码"].apply(lambda x: x[0:6])).set_index("trade_date", drop=False)
        else:
            print("连接访问接口失败")           
    except Exception as e:
        print(e)


if __name__ == "__main__":
    df = crawl_data_from_wencai("2021-1-1", ["股票简称", "股票代码", "市盈率(pe)", "市净率(pb)"])
    print(df)
    df.to_excel("output.xlsx")
