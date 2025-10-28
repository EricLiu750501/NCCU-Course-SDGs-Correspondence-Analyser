# CollegeScale Directory Overview

This directory contains scripts and data related to the classification and analysis of university courses against the United Nations Sustainable Development Goals (SDGs) using Large Language Models (LLMs).

## Analysis (圖表皆在 [/plot](https://github.com/EricLiu750501/NCCU-Course-SDGs-Correspondence-Analyser/tree/3036f96c8f52bf2831a127db79b260ee5f9fb646/src/CollegeScale/plots))

### 分群
根據 https://www.nccu.edu.tw/p/426-1000-55.php?Lang=zh-tw 做學院分群

### SDG覆蓋率 (SDG Coverage)
設定一個分數閾值（例如 final_score > 6.99）來定義「此課程與該SDG相關」。    
統計全校有多少「比例」課程與 至少一個 SDG 相關。

e.g 商院覆蓋率
![image](https://github.com/EricLiu750501/NCCU-Course-SDGs-Correspondence-Analyser/blob/c68a0291042dfdd16ace16d67ca8fdc028ab4c04/src/CollegeScale/plots/College_of_Commerce_(508_courses)_Courses_per_SDG_Percentage_Gemini-2.5-pro.png)
file: *_Courses_per_SDG_Percentage_Gemini-2.5-pro.png

### 平均分數
統計學院平均分數

e.g 法學院平均分數
![image](https://github.com/EricLiu750501/NCCU-Course-SDGs-Correspondence-Analyser/blob/c68a0291042dfdd16ace16d67ca8fdc028ab4c04/src/CollegeScale/plots/Gemini-2.5-pro_College_of_Law_avg_scores.png)
file: *_avg_scores.png

### WordCloud
提取 evidence 欄位 製作 WordCloud 看 LLM 是基於哪些關鍵詞來給出高分的。也可知道課程中哪些詞會代表該SDGs

e.g. 
![image](https://github.com/EricLiu750501/NCCU-Course-SDGs-Correspondence-Analyser/blob/c68a0291042dfdd16ace16d67ca8fdc028ab4c04/src/CollegeScale/plots/WordCloud_Industry%2C_Innovation_and_Infrastructure_Gemini-2.5-pro.png)
file: WordCloud_*

### Top 10 Courses for SDG
--- Top 10 Courses for SDG: No Poverty (Gemini-2.5-pro) ---
| Rank | Course ID | Course Name | Department | Score | Course URL |
|------|-----------|-------------|------------|-------|------------|
| 1    | 651343001 | 社會保險法專題研究（一）                                     | 法律碩一法律博一法律碩二法律博二                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=651343&gop=00&s=1.html) |
| 2    | 651B90001 | 社會法名著選讀     | 法律碩一法律博一法律碩二法律博二                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=651B90&gop=00&s=1.html) |
| 3    | 266941001 | 所得稅問題       | 應社碩一應社碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=266941&gop=00&s=1.html) |
| 4    | ZU1868001 | 永續發展商業模式：選擇、實施與最佳案例分析 | 創國學三創國學四                                                                                            | 9.50 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=ZU1868&gop=00&s=1.html) |
| 5    | 264101001 | 社會政策與社會立法專題 | 社工碩一社工碩二                                                                                            | 9.50 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=264101&gop=00&s=1.html) |
| 6    | 252699001 | 全球化與東亞福利國家  | 政治碩一政治博一政治碩二政治博二                                                                                  | 9.50 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=252699&gop=00&s=1.html) |
| 7    | 862950001 | 國際合作專題 – 農業、經濟與貿易議題 | 國研碩一國研碩二                                                                                            | 9.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=862950&gop=00&s=1.html) |
| 8    | 266910001 | 發展援助專題      | 應社碩一應社碩二                                                                                            | 9.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=266910&gop=00&s=1.html) |
| 9    | 261924001 | 發展援助專題      | 國發碩一國發博一國發碩二國發博二                                                                                  | 9.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=261924&gop=00&s=1.html) |
| 10   | 926848001 | 發展援助專題      | 亞太碩一亞太碩二                                                                                            | 9.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=926848&gop=00&s=1.html) |

--- Top 10 Courses for SDG: Zero Hunger (Gemini-2.5-pro) ---
| Rank | Course ID | Course Name | Department | Score | Course URL |
|------|-----------|-------------|------------|-------|------------|
| 1    | 923893001 | 農地、共用資源與農村發展專題研究 | 地政專一地政專二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=923893&gop=00&s=1.html) |
| 2    | 862950001 | 國際合作專題 – 農業、經濟與貿易議題 | 國研碩一國研碩二                                                                                            | 9.50 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=862950&gop=00&s=1.html) |
| 3    | 153482001 | 東亞農業史專題     | 歷史碩一歷史博一歷史碩二歷史博二                                                                                  | 9.50 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=153482&gop=00&s=1.html) |
| 4    | 158702001 | 東亞農業史專題     | 台史碩一台史博一台史碩二台史博二                                                                                  | 9.50 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=158702&gop=00&s=1.html) |
| 5    | 041176001 | 風土、餐桌與台灣史   | 歷史系        | 8.50 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=041176&gop=00&s=1.html) |
| 6    | 207761001 | 土地重劃                                                     | 地二土管地二土資                                                                                            | 8.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=207761&gop=00&s=1.html) |
| 7    | 267937001 | 原住民族空間規劃    | 原碩專一原碩專二原碩專三原碩專四                                                                                  | 8.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=267937&gop=00&s=1.html) |
| 8    | ZU1873001 | 創新與全球發展     | 創國學二創國學三創國學四                                                                                       | 8.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=ZU1873&gop=00&s=1.html) |
| 9    | 261103001 | 永續發展        | 國發碩一國發碩二                                                                                            | 8.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=261103&gop=00&s=1.html) |
| 10   | 158902001 | 日治時期台灣經濟發展專題                                     | 台史碩一台史博一台史碩二台史博二                                                                                  | 7.50 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=158902&gop=00&s=1.html) |

--- Top 10 Courses for SDG: Good Health and Well-being (Gemini-2.5-pro) ---
| Rank | Course ID | Course Name | Department | Score | Course URL |
|------|-----------|-------------|------------|-------|------------|
| 1    | 002337011 | 體育[男女合班]—羽球中級 | 體育         | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=002337&gop=01&s=1.html) |
| 2    | ZU1009001 | 全球衛生治理      | 創國學三創國學四                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=ZU1009&gop=00&s=1.html) |
| 3    | 002346001 | 體育[男女合班]—鐵人三項初級                                 | 體育         | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=002346&gop=00&s=1.html) |
| 4    | 090106001 | 健康與生活       | 教務處通識教育中心  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=090106&gop=00&s=1.html) |
| 5    | 002115001 | 體育[女]—羽球中級                                           | 體育         | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=002115&gop=00&s=1.html) |
| 6    | 002384001 | 體育[男女合班]—桌球高級 | 體育         | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=002384&gop=00&s=1.html) |
| 7    | 043021001 | 探索遺傳特性      | 神科所        | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=043021&gop=00&s=1.html) |
| 8    | 913930001 | 讀者諮詢與書目療法   | 圖資專二                                                                                                 | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=913930&gop=00&s=1.html) |
| 9    | 002312001 | 體育[男]—男體適能                                           | 體育         | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=002312&gop=00&s=1.html) |
| 10   | 002368021 | 體育[男女合班]—定向越野 | 體育         | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=002368&gop=02&s=1.html) |

--- Top 10 Courses for SDG: Quality Education (Gemini-2.5-pro) ---
| Rank | Course ID | Course Name | Department | Score | Course URL |
|------|-----------|-------------|------------|-------|------------|
| 1    | 171911001 | 教育政策專題（二）   | 教政碩一教政碩二教政碩三                                                                                       | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=171911&gop=00&s=1.html) |
| 2    | 509007001 | 初級法文語法                                                 | 歐文法一                                                                                                 | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=509007&gop=00&s=1.html) |
| 3    | 159002001 | 文學研究方法論                                               | 台文碩二                                                                                                 | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=159002&gop=00&s=1.html) |
| 4    | 509017001 | 中級法文語法                                                 | 歐文法二                                                                                                 | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=509017&gop=00&s=1.html) |
| 5    | 032001311 | 大學英文（一）                                               | 外文中        | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=032001&gop=31&s=1.html) |
| 6    | 551846001 | 課程規劃與教材評估之研究                                     | 英文碩一英博教一英文碩二英博教二                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=551846&gop=00&s=1.html) |
| 7    | 354715001 | 書報討論                                                     | 統計博一統計博二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=354715&gop=00&s=1.html) |
| 8    | 651B91001 | 工程法論文專題研討   | 法律碩一法律博一法律碩二法律博二                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=651B91&gop=00&s=1.html) |
| 9    | 300785001 | 服務學習專業課程－指南服務團－社會服務與學習（一） | 商院學士                                                                                                 | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=300785&gop=00&s=1.html) |
| 10   | 501069111 | 寫作與閱讀（三）    | 英文二甲英文二乙                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=501069&gop=11&s=1.html) |

--- Top 10 Courses for SDG: Gender Equality (Gemini-2.5-pro) ---
| Rank | Course ID | Course Name | Department | Score | Course URL |
|------|-----------|-------------|------------|-------|------------|
| 1    | 103230001 | 性別與近代西方世界的形成 | 歷史二                                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=103230&gop=00&s=1.html) |
| 2    | 041175001 | 台灣電影與文學中的性別 | 台文所        | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=041175&gop=00&s=1.html) |
| 3    | 652151001 | 勞動法         | 法科碩一法科碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=652151&gop=00&s=1.html) |
| 4    | 464934001 | 性別與傳播科技     | 傳播碩一傳播碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=464934&gop=00&s=1.html) |
| 5    | 042217001 | AI、性別與勞動    | 勞工所        | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=042217&gop=00&s=1.html) |
| 6    | 153522001 | 近代中國性別史專題   | 歷史碩一歷史博一歷史碩二歷史博二                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=153522&gop=00&s=1.html) |
| 7    | 651314001 | 法社會學專題研究（二）                                       | 法律碩一法律博一法律碩二法律博二                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=651314&gop=00&s=1.html) |
| 8    | ZM1885001 | 女性影像與新媒體    | 全創碩一全創碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=ZM1885&gop=00&s=1.html) |
| 9    | 401120001 | 進階新聞報導與族群／性別／階級 | 新聞三                                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=401120&gop=00&s=1.html) |
| 10   | 042126001 | 同志文學在東亞                                               | 台文所        | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=042126&gop=00&s=1.html) |

--- Top 10 Courses for SDG: Clean Water and Sanitation (Gemini-2.5-pro) ---
| Rank | Course ID | Course Name | Department | Score | Course URL |
|------|-----------|-------------|------------|-------|------------|
| 1    | 923882001 | 永續與共享城市     | 地政專一地政專二                                                                                            | 9.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=923882&gop=00&s=1.html) |
| 2    | 045063001 | 自主學習專題：3D建模與原型製作－從概念到創造 | 教務處通識教育中心  | 9.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=045063&gop=00&s=1.html) |
| 3    | 254759001 | 蓋婭政治與戰時生態學  | 社會碩一社會碩二                                                                                            | 8.50 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=254759&gop=00&s=1.html) |
| 4    | 204783001 | 蓋婭政治與戰時生態學  | 社會三社會四                                                                                              | 8.50 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=204783&gop=00&s=1.html) |
| 5    | 921817001 | 財政與貨幣政策     | 行管碩一行國防一行領導一行管碩二行國防二行領導二                                                                        | 8.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=921817&gop=00&s=1.html) |
| 6    | ZU1875001 | 蓋婭政治與戰時生態學  | 創國學三創國學四                                                                                            | 8.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=ZU1875&gop=00&s=1.html) |
| 7    | 202819001 | 國際環境與能源專題   | 政治三政治四                                                                                              | 8.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=202819&gop=00&s=1.html) |
| 8    | 261867001 | 自然資源與再生能源   | 國發碩一國發博一國發碩二國發博二                                                                                  | 8.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=261867&gop=00&s=1.html) |
| 9    | 259665001 | 亞洲主權：人類學視角  | 民族碩一民族博一民族碩二                                                                                       | 7.50 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=259665&gop=00&s=1.html) |
| 10   | 041133011 | 近代臺灣歷史與人物   | 台史所        | 7.50 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=041133&gop=01&s=1.html) |

--- Top 10 Courses for SDG: Affordable and Clean Energy (Gemini-2.5-pro) ---
| Rank | Course ID | Course Name | Department | Score | Course URL |
|------|-----------|-------------|------------|-------|------------|
| 1    | 252685001 | 國際環境與能源專題   | 政治碩一政治碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=252685&gop=00&s=1.html) |
| 2    | ZM1887001 | 科技社會與文化     | 全創碩一全創碩二全創碩三                                                                                       | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=ZM1887&gop=00&s=1.html) |
| 3    | 205915001 | 能源經濟管理導論    | 財政三甲財政三乙財政四甲財政四乙                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=205915&gop=00&s=1.html) |
| 4    | 255824001 | 能源經濟管理導論    | 財政碩一財政碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=255824&gop=00&s=1.html) |
| 5    | 202819001 | 國際環境與能源專題   | 政治三政治四                                                                                              | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=202819&gop=00&s=1.html) |
| 6    | 926854001 | 國際環境與能源專題   | 亞太碩一亞太碩二亞太碩三                                                                                       | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=926854&gop=00&s=1.html) |
| 7    | 258720001 | 環境與資源經濟學（二）：能源經濟與政策 | 經濟碩一經濟博一經濟碩二經濟博二                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=258720&gop=00&s=1.html) |
| 8    | 261867001 | 自然資源與再生能源   | 國發碩一國發博一國發碩二國發博二                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=261867&gop=00&s=1.html) |
| 9    | 358904011 | 產險專題研究      | 風管碩一風管博一風管碩二風管博二                                                                                  | 9.50 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=358904&gop=01&s=1.html) |
| 10   | 363016001 | 低碳時代企業永續發展研討 | 企研碩一企研碩二                                                                                            | 9.50 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=363016&gop=00&s=1.html) |

--- Top 10 Courses for SDG: Decent Work and Economic Growth (Gemini-2.5-pro) ---
| Rank | Course ID | Course Name | Department | Score | Course URL |
|------|-----------|-------------|------------|-------|------------|
| 1    | 264873001 | 遷移與發展       | 社工碩一社工博一社工碩二社工博二                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=264873&gop=00&s=1.html) |
| 2    | 506863001 | 商務日語１       | 日文三                                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=506863&gop=00&s=1.html) |
| 3    | 351704001 | 國際經濟法       | 國貿碩一國貿碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=351704&gop=00&s=1.html) |
| 4    | 261872001 | 全球化經濟下的勞動與工作 | 國發碩一國發博一國發碩二國發博二                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=261872&gop=00&s=1.html) |
| 5    | ZC0936001 | 尋找心中的創業家    | X實驗學士                                                                                                | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=ZC0936&gop=00&s=1.html) |
| 6    | 000218011 | 總體經濟學                                                   | 經濟系        | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=000218&gop=01&s=1.html) |
| 7    | 651343001 | 社會保險法專題研究（一）                                     | 法律碩一法律博一法律碩二法律博二                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=651343&gop=00&s=1.html) |
| 8    | 652151001 | 勞動法         | 法科碩一法科碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=652151&gop=00&s=1.html) |
| 9    | 202842001 | 政治學實習                                                   | 政治三政治四                                                                                              | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=202842&gop=00&s=1.html) |
| 10   | 305009001 | 人力資源管理                                                 | 企管二甲企管二乙                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=305009&gop=00&s=1.html) |

--- Top 10 Courses for SDG: Industry, Innovation and Infrastructure (Gemini-2.5-pro) ---
| Rank | Course ID | Course Name | Department | Score | Course URL |
|------|-----------|-------------|------------|-------|------------|
| 1    | 652885001 | 專利實務        | 法科碩一法科碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=652885&gop=00&s=1.html) |
| 2    | 364106001 | 科技與創新管理     | 科博產二                                                                                                 | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=364106&gop=00&s=1.html) |
| 3    | 300859001 | 供應鏈管理實務     | 商院碩士                                                                                                 | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=300859&gop=00&s=1.html) |
| 4    | 355532001 | 科技與創新管理     | 企博產二                                                                                                 | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=355532&gop=00&s=1.html) |
| 5    | 933855001 | 中小企業創新      | 國營碩一國營碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=933855&gop=00&s=1.html) |
| 6    | 364041001 | 科技管理與智慧財產理論研討（三） | 科博學二科博學三                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=364041&gop=00&s=1.html) |
| 7    | ZM1903001 | 影音媒體創新與互動科技 | 全創碩一全創碩二全創碩三                                                                                       | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=ZM1903&gop=00&s=1.html) |
| 8    | ZU1026001 | 設計思維        | 創國學三創國學四                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=ZU1026&gop=00&s=1.html) |
| 9    | 306016031 | 資訊系統專案設計                                             | 資管三甲資管三乙                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=306016&gop=03&s=1.html) |
| 10   | 363884001 | 智能供應鏈：趨勢與運用 | 企研碩一企研碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=363884&gop=00&s=1.html) |

--- Top 10 Courses for SDG: Reduced Inequalities (Gemini-2.5-pro) ---
| Rank | Course ID | Course Name | Department | Score | Course URL |
|------|-----------|-------------|------------|-------|------------|
| 1    | 264873001 | 遷移與發展       | 社工碩一社工博一社工碩二社工博二                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=264873&gop=00&s=1.html) |
| 2    | 202829001 | 多元文化與移民政治   | 政治三政治四                                                                                              | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=202829&gop=00&s=1.html) |
| 3    | 267938001 | 環境規劃與治理     | 原碩專一原碩專二原碩專三原碩專四                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=267938&gop=00&s=1.html) |
| 4    | 651343001 | 社會保險法專題研究（一）                                     | 法律碩一法律博一法律碩二法律博二                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=651343&gop=00&s=1.html) |
| 5    | ZU1859001 | 移民工研究實作     | 創國學三創國學四                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=ZU1859&gop=00&s=1.html) |
| 6    | 208026001 | 勞動經濟學       | 經濟三甲經濟三乙經濟四甲經濟四乙                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=208026&gop=00&s=1.html) |
| 7    | 205062001 | 租稅法（一）      | 財政四甲財政四乙                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=205062&gop=00&s=1.html) |
| 8    | 042217001 | AI、性別與勞動    | 勞工所        | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=042217&gop=00&s=1.html) |
| 9    | 651B80001 | 人性尊嚴的歷史與法律解釋 | 法律碩一法律碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=651B80&gop=00&s=1.html) |
| 10   | 264925001 | 優勢觀點社會工作    | 社工碩一社工博一社工碩二社工博二                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=264925&gop=00&s=1.html) |

--- Top 10 Courses for SDG: Sustainable Cities and Communities (Gemini-2.5-pro) ---
| Rank | Course ID | Course Name | Department | Score | Course URL |
|------|-----------|-------------|------------|-------|------------|
| 1    | 926864001 | 永續發展與都市政治   | 亞太碩一亞太碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=926864&gop=00&s=1.html) |
| 2    | 205850001 | 永續發展與企業社會責任 | 財政三甲財政三乙財政四甲財政四乙                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=205850&gop=00&s=1.html) |
| 3    | Z23941001 | 永續發展與都市政治   | 創國碩士                                                                                                 | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=Z23941&gop=00&s=1.html) |
| 4    | 207959001 | 規劃實務（一）實習   | 地二土資                                                                                                 | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=207959&gop=00&s=1.html) |
| 5    | 207726001 | 住宅研究與資料科學   | 地三土管                                                                                                 | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=207726&gop=00&s=1.html) |
| 6    | 921814001 | 社會企業專題      | 行管碩一行國防一行領導一行管碩二行國防二行領導二                                                                        | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=921814&gop=00&s=1.html) |
| 7    | 207056001 | 地圖學                                                       | 地二土測                                                                                                 | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=207056&gop=00&s=1.html) |
| 8    | 207737001 | 都市更新與容積代金估價實務 | 地四土管                                                                                                 | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=207737&gop=00&s=1.html) |
| 9    | 257709001 | 土地利用法專題研究   | 地政碩一地政博一地政碩二地政博二                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=257709&gop=00&s=1.html) |
| 10   | 090121001 | 風土、生活與產業    | 教務處通識教育中心  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=090121&gop=00&s=1.html) |

--- Top 10 Courses for SDG: Responsible Consumption and Production (Gemini-2.5-pro) ---
| Rank | Course ID | Course Name | Department | Score | Course URL |
|------|-----------|-------------|------------|-------|------------|
| 1    | 300011001 | 企業倫理與永續發展   | 商院碩士                                                                                                 | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=300011&gop=00&s=1.html) |
| 2    | 205850001 | 永續發展與企業社會責任 | 財政三甲財政三乙財政四甲財政四乙                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=205850&gop=00&s=1.html) |
| 3    | 000361051 | 企業倫理與社會責任   | 企管系        | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=000361&gop=05&s=1.html) |
| 4    | 208027001 | 環境經濟學       | 經濟三甲經濟三乙經濟四甲經濟四乙                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=208027&gop=00&s=1.html) |
| 5    | 205849001 | 循環經濟和永續發展   | 財政三甲財政三乙財政四甲財政四乙                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=205849&gop=00&s=1.html) |
| 6    | 255832001 | 循環商業模式      | 財政碩一財政碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=255832&gop=00&s=1.html) |
| 7    | 364766001 | 永續、創新與商業模式  | 科智碩1A科智碩2A                                                                                          | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=364766&gop=00&s=1.html) |
| 8    | 651B59001 | 公司治理與ESG    | 法律碩一法律碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=651B59&gop=00&s=1.html) |
| 9    | 300011011 | 企業倫理與永續發展   | 商院碩士                                                                                                 | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=300011&gop=01&s=1.html) |
| 10   | 000361041 | 企業倫理與社會責任   | 企管系        | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=000361&gop=04&s=1.html) |

--- Top 10 Courses for SDG: Climate Action (Gemini-2.5-pro) ---
| Rank | Course ID | Course Name | Department | Score | Course URL |
|------|-----------|-------------|------------|-------|------------|
| 1    | 090116001 | 氣候變遷與永續旅遊   | 教務處通識教育中心  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=090116&gop=00&s=1.html) |
| 2    | 358904011 | 產險專題研究      | 風管碩一風管博一風管碩二風管博二                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=358904&gop=01&s=1.html) |
| 3    | 205850001 | 永續發展與企業社會責任 | 財政三甲財政三乙財政四甲財政四乙                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=205850&gop=00&s=1.html) |
| 4    | 267938001 | 環境規劃與治理     | 原碩專一原碩專二原碩專三原碩專四                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=267938&gop=00&s=1.html) |
| 5    | Z23941001 | 永續發展與都市政治   | 創國碩士                                                                                                 | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=Z23941&gop=00&s=1.html) |
| 6    | 257737001 | 氣候變遷時期土地與環境法制專題研究 | 地政碩一地政博一地政碩二地政博二                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=257737&gop=00&s=1.html) |
| 7    | 207959001 | 規劃實務（一）實習   | 地二土資                                                                                                 | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=207959&gop=00&s=1.html) |
| 8    | 308848001 | ESG永續投資與綠色金融創新 | 風管三風管四                                                                                              | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=308848&gop=00&s=1.html) |
| 9    | 252685001 | 國際環境與能源專題   | 政治碩一政治碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=252685&gop=00&s=1.html) |
| 10   | 044120001 | 氣候變遷對社會韌性的挑戰 | 創國學院       | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=044120&gop=00&s=1.html) |

--- Top 10 Courses for SDG: Life Below Water (Gemini-2.5-pro) ---
| Rank | Course ID | Course Name | Department | Score | Course URL |
|------|-----------|-------------|------------|-------|------------|
| 1    | 652208001 | 全球治理與國際法    | 法科碩一法科碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=652208&gop=00&s=1.html) |
| 2    | 652200001 | 國際海洋法       | 法科碩一法科碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=652200&gop=00&s=1.html) |
| 3    | 207933001 | 海洋測量        | 地四土測                                                                                                 | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=207933&gop=00&s=1.html) |
| 4    | 601388001 | 全球治理與國際法    | 法律三甲法律三乙法律三丙法律四甲法律四乙法律四丙                                                                        | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=601388&gop=00&s=1.html) |
| 5    | 601666001 | 國際海洋法                                                   | 法律三甲法律三乙法律三丙法律四甲法律四乙法律四丙                                                                        | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=601666&gop=00&s=1.html) |
| 6    | 253815001 | 國際海洋法       | 外交碩一外交碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=253815&gop=00&s=1.html) |
| 7    | 961056001 | 國際法專題研究     | 法碩專一法碩專二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=961056&gop=00&s=1.html) |
| 8    | ZU1862001 | 海洋法－法律框架、國家實踐、及挑戰 | 創國學二創國學三創國學四                                                                                       | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=ZU1862&gop=00&s=1.html) |
| 9    | 090026001 | 探索海洋－從水岸到深海                                       | 教務處通識教育中心  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=090026&gop=00&s=1.html) |
| 10   | 651A24001 | 國際公法專題研究（四） | 法律碩一法律博一法律碩二法律博二                                                                                  | 9.50 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=651A24&gop=00&s=1.html) |

--- Top 10 Courses for SDG: Life on Land (Gemini-2.5-pro) ---
| Rank | Course ID | Course Name | Department | Score | Course URL |
|------|-----------|-------------|------------|-------|------------|
| 1    | 267938001 | 環境規劃與治理     | 原碩專一原碩專二原碩專三原碩專四                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=267938&gop=00&s=1.html) |
| 2    | 045025001 | 動物權：理論與實踐   | 歐文學系       | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=045025&gop=00&s=1.html) |
| 3    | 257737001 | 氣候變遷時期土地與環境法制專題研究 | 地政碩一地政博一地政碩二地政博二                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=257737&gop=00&s=1.html) |
| 4    | 207056001 | 地圖學                                                       | 地二土測                                                                                                 | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=207056&gop=00&s=1.html) |
| 5    | 041176001 | 風土、餐桌與台灣史   | 歷史系        | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=041176&gop=00&s=1.html) |
| 6    | 923893001 | 農地、共用資源與農村發展專題研究 | 地政專一地政專二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=923893&gop=00&s=1.html) |
| 7    | 044084001 | 動物與人類社會     | 台史所        | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=044084&gop=00&s=1.html) |
| 8    | 090111001 | 環境科學與環境保護   | 教務處通識教育中心  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=090111&gop=00&s=1.html) |
| 9    | ZC0938001 | 跨界專題：藝術永續實踐 | X實驗學士                                                                                                | 9.80 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=ZC0938&gop=00&s=1.html) |
| 10   | 551758001 | 英美浪漫主義的空間想像 | 英文碩一英博文一英文碩二英博文二                                                                                  | 9.50 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=551758&gop=00&s=1.html) |

--- Top 10 Courses for SDG: Peace, Justice and Strong Institutions (Gemini-2.5-pro) ---
| Rank | Course ID | Course Name | Department | Score | Course URL |
|------|-----------|-------------|------------|-------|------------|
| 1    | 601155021 | 刑法（一）       | 法律一乙法律一丙                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=601155&gop=02&s=1.html) |
| 2    | 263825001 | 俄國政府與政治     | 俄羅碩一俄羅碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=263825&gop=00&s=1.html) |
| 3    | 461855001 | 數位顛覆、新聞媒體與公民 | 國傳碩一國傳碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=461855&gop=00&s=1.html) |
| 4    | 202839001 | 選舉文宣企劃      | 政治三政治四                                                                                              | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=202839&gop=00&s=1.html) |
| 5    | 202829001 | 多元文化與移民政治   | 政治三政治四                                                                                              | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=202829&gop=00&s=1.html) |
| 6    | 401140001 | 新興媒體與新聞     | 新聞三                                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=401140&gop=00&s=1.html) |
| 7    | 791025001 | 個人資料保護法     | 資安碩一資安碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=791025&gop=00&s=1.html) |
| 8    | 961227001 | 中國大陸投資法律制度與實務（三） | 法碩專一法碩專二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=961227&gop=00&s=1.html) |
| 9    | 042156001 | 中國大陸概論      | 東亞所        | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=042156&gop=00&s=1.html) |
| 10   | 252002001 | 比較政治        | 政治碩一政治碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=252002&gop=00&s=1.html) |

--- Top 10 Courses for SDG: Partnerships for the Goals (Gemini-2.5-pro) ---
| Rank | Course ID | Course Name | Department | Score | Course URL |
|------|-----------|-------------|------------|-------|------------|
| 1    | 862950001 | 國際合作專題 – 農業、經濟與貿易議題 | 國研碩一國研碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=862950&gop=00&s=1.html) |
| 2    | 351704001 | 國際經濟法       | 國貿碩一國貿碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=351704&gop=00&s=1.html) |
| 3    | 652208001 | 全球治理與國際法    | 法科碩一法科碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=652208&gop=00&s=1.html) |
| 4    | 205008001 | 所得稅理論與制度                                             | 財政三甲財政三乙財政四甲財政四乙                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=205008&gop=00&s=1.html) |
| 5    | 203896001 | 永續發展導論      | 外交一                                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=203896&gop=00&s=1.html) |
| 6    | 255823001 | 國際租稅法       | 財政碩一財政碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=255823&gop=00&s=1.html) |
| 7    | 151506001 | 東亞文化的共融與和平  | 中文碩一中文碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=151506&gop=00&s=1.html) |
| 8    | 253050001 | 國際組織        | 外交碩一外交博一外交碩二外交博二                                                                                  | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=253050&gop=00&s=1.html) |
| 9    | 921814001 | 社會企業專題      | 行管碩一行國防一行領導一行管碩二行國防二行領導二                                                                        | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=921814&gop=00&s=1.html) |
| 10   | 862888001 | 區域研究—歐盟國際關係研究 | 國研碩一國研碩二                                                                                            | 10.00 | [Link](https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=862888&gop=00&s=1.html) |
