# CollegeScale Directory Overview

This directory contains scripts and data related to the classification and analysis of university courses against the United Nations Sustainable Development Goals (SDGs) using Large Language Models (LLMs).

## Analysis

### 分群
根據 https://www.nccu.edu.tw/p/426-1000-55.php?Lang=zh-tw 做學院分群

### SDG覆蓋率 (SDG Coverage)
設定一個分數閾值（例如 final_score > 6.99）來定義「此課程與該SDG相關」。    
統計全校有多少「比例」課程與 至少一個 SDG 相關。

file: *_Courses_per_SDG_Percentage_Gemini-2.5-pro.png

### 平均分數
統計學院平均分數

file: *_avg_scores.png

### WordCloud
提取 evidence 欄位 製作 WordCloud 看 LLM 是基於哪些關鍵詞來給出高分的。也可知道課程中哪些詞會代表該SDGs
