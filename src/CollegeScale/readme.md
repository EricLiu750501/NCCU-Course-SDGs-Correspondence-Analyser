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
