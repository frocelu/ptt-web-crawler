# ptt-web-crawler (PTT 網路版爬蟲) [![Build Status](https://travis-ci.org/david30907d/ptt-web-crawler.svg?branch=master)](https://travis-ci.org/david30907d/ptt-web-crawler)

特色

* 支援單篇及多篇文章抓取
* 過濾資料內空白、空行及特殊字元
* JSON 格式輸出
* 支援 Python 2.7 - 3.4

輸出 JSON 格式

    {
        "article_id": 文章 ID,
        "article_title": 文章標題 ,
        "author": 作者,
        "board": 板名,
        "content": 文章內容,
        "date": 發文時間,
        "ip": 發文位址,
        "message_conut": { # 推文
            "all": 總數,
            "boo": 噓文數,
            "count": 推文數-噓文數,
            "neutral": → 數,
            "push": 推文數
        },
        "messages": [ # 推文內容
            {
                "push_content": 推文內容,
                "push_ipdatetime": 推文時間及位址,
                "push_tag": 推/噓/→ ,
                "push_userid": 推文者 ID
            },
            ...
        ]
    }

### 安裝

    pip install PttWebCrawler


### cmd執行方式
    python -m PttWebCrawler -b 看板名稱 -i 起始索引 結束索引 (設為 -1 則自動計算最後一頁)
    python -m PttWebCrawler -b 看板名稱 -a 文章ID

* 範例
  `python -m PttWebCrawler -b PublicServan -i 100 200`

會爬取 PublicServan 板第 100 頁 (https://www.ptt.cc/bbs/PublicServan/index100.html) 到第 200 頁 (https://www.ptt.cc/bbs/PublicServan/index200.html) 的內容，輸出至 `PublicServan-100-200.json`

* 範例 `python -m PttWebCrawler -b PublicServan -a M.1413618360.A.4F0`

會爬取 PublicServan 板文章 ID 為 M.1413618360.A.4F0 (https://www.ptt.cc/bbs/PublicServan/M.1413618360.A.4F0.html) 的內容，輸出至 `PublicServan-M.1413618360.A.4F0.json`

### 進階使用

呼叫PttWebCrawler模組  
可以傳入`callback function`去parse標題和內文  
constructor的參數：  
  * board：要爬的版的英文名稱
  * iOrA：要爬第幾頁到第幾頁，就把這個參數設為`True`
    * start：起始頁
    * end：結束頁，自動推算該版的最後一頁請設定為-1
  * article_id：如果`iOrA`是`False`，就代表是只要爬一篇文章，那就要提供article_id給constructor

政黑板1~3頁：`PttWebCrawler('HatePolitics',True , start=1, end=3)`
政黑板M.1491187129.A.D11這篇文章：`PttWebCrawler('HatePolitics', False, article_id='M.1491187129.A.D11')`

1. 以Food版[此篇文章](https://www.ptt.cc/bbs/Food/M.1491130337.A.E8F.html)做示範：  
`contfunc`是一個處理content的函式  
使用者可以自行決定想要保留content的哪些內容  
`contfunc`回傳的value，會被儲存在json的`content`欄位  

  * 程式範例：  

    ```
    from PttWebCrawler import *
    import re

    def contfunc(string):
    	redundency = re.search('營業時間：(.+?)：',string).group(1).split()[-1]
    	needed = re.search('營業時間：(.+?)：',string).group(1).replace(redundency, '')
    	return {'營業時間':needed}

    PttWebCrawler('Food',False ,article_id='M.1491130337.A.E8F', contentCallback=contfunc)  
    ```

  * 結果：  

    ```
    {
      "article_id": "M.1491130337.A.E8F",
      "article_title": "[食記] 高雄 開動了 日本家庭料理 ~美味竹籠套餐",
      "author": "mapleleaves (摩那卡monaka)",
      "board": "Food",
      "content": {
      "營業時間": "週三~週日11:00~14:00 "
      },
      "date": "Sun Apr  2 18:52:13 2017",
      "ip": "111.254.96.218",
      "message_conut": {
      "all": 0,
      "boo": 0,
      "count": 0,
      "neutral": 0,
      "push": 0
      },
      "messages": []
    }
    ```
2. 以NCHU課程版示範：

  * 程式範例：

    ```
    from PttWebCrawler import *
    import re

    def contfunc(string):
      needed = re.search('用書(.+?)評分方式',string,re.S).group(1)
      return {'book':needed}

    def titlefunc(string):
      string = string.replace('[心得] ', '').split('/')
      genra = string[0]
      time = string[1]
      name = string[2]
      teacher = string[3]
      return {'genra':genra, 'time':time, 'name':name, 'teacher':teacher}

    PttWebCrawler('NCHU-Courses',False ,article_id='M.1484187071.A.6D8', contentCallback=contfunc, titleCallback=titlefunc)
    ```
  * 結果：

    ```
    {
      "article_id": "M.1484187071.A.6D8",
      "article_title": {
        "genra": "外系",
        "name": "電腦軟體應用",
        "tea  cher": "蔡子安",
        "time": "4234"
      },
      "content": {
        "book": " word/power point實力養成暨評量 (第一堂上課會有書商來賣書，真的比去敦煌買便宜很多，一手交錢一手交貨) "
      }
      ...
    }
    ```


### 測試
    python test.py

***

ptt-web-crawler is a crawler for the web version of PTT, the largest online community in Taiwan.

    usage: python -m PttWebCrawler [-h] -b BOARD_NAME (-i START_INDEX END_INDEX | -a ARTICLE_ID)
    optional arguments:
      -h, --help                  show this help message and exit
      -b BOARD_NAME               Board name
      -i START_INDEX END_INDEX    Start and end index
      -a ARTICLE_ID               Article ID

Output would be `BOARD_NAME-START_INDEX-END_INDEX.json` (or `BOARD_NAME-ID.json`)
