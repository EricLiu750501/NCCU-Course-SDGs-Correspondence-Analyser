✦ 好的，這是一份根據您提供的專案結構與需求所產出的技術實作細節報告。報告內容分析了 CollegeScale 目錄下的程式碼，並推斷其運作邏輯與架構。

  ---

  SDG 課程文本分類系統（LLM-based）技術實作報告

  版本：1.0
  日期：2025年10月15日

  ---

  摘要

  本報告旨在詳細闡述基於大型語言模型（LLM）的聯合國永續發展目標（SDG）課程文本分類系統的技術實作細節。系統透過指令行介面（CLI）接收課程資
  料，利用 LLM（如 Gemini 或 GPT）進行內容分析與 SDG 
  關聯性評分，最終產出結構化的分類結果與統計圖表。本文將從系統架構、資料流程、核心模組、環境設定、未來擴展與優化建議等面向進行深入剖析。

  ---

  一、系統總體架構與資料流說明

  1.1 系統架構

  本系統為一個模組化的批次處理架構，主要由四個核心部分組成：

   1. 指令行介面 (CLI): 作為使用者互動的入口，負責接收輸入資料路徑、模型類型、處理參數（如閾值）等指令。推測由 LLM_Discussions.py 和 
      analyze.py 中的 argparse 或類似模組實現。
   2. LLM 互動模組 (`LLM_Discussions.py`): 核心處理單元，負責讀取課程資料，根據 system_prompts.py 中的範本生成對應的 Prompt，並呼叫外部 LLM 
      API（Gemini/GPT）進行分析。
   3. 資料分析與後處理模組 (`analyze.py`): 負責讀取 LLM 產生的原始 JSON 結果，進行資料彙整、平均分數計算、根據指定閾值過濾 SDG 項目，並利用 
      matplotlib 等函式庫生成視覺化圖表。
   4. 資料儲存:
       * 輸入資料: 課程資訊，以 JSON 格式儲存（例如 College_of_Commerce.json）。
       * 原始輸出: LLM 對單一課程的分析結果，以獨立 JSON 檔案形式儲存於 result/ 目錄下。
       * 統計結果: 經過 analyze.py 處理後的彙總資料，儲存為 gemini_avg.json 或 gpt_avg.json。
       * 視覺化圖表: 最終分析結果的長條圖，儲存為 .png 檔案。

  1.2 資料流

  系統的主要資料處理流程可以透過以下文字流程圖表示：

    1 [CLI 輸入]
    2     |
    3     | (例如: python LLM_Discussions.py --input College_of_Commerce.json)
    4     v
    5 [讀取課程文本] (從指定的 .json 檔案讀取課程名稱、描述等)
    6     |
    7     v
    8 [Prompt 格式化] (使用 system_prompts.py 中的模板，將課程資訊填入)
    9     |
   10     v
   11 [呼叫 LLM API] (將格式化後的 Prompt 發送至 Gemini 或 GPT 模型)
   12     |
   13     v
   14 [產生原始 SDG 分類結果] (LLM 回傳包含 SDG 編號、分數、理由的 JSON 字串)
   15     |
   16     v
   17 [儲存原始結果] (將每門課程的分析結果存為一個獨立的 .json 檔案於 result/ 目錄)
   18     |
   19     | (執行第二階段分析: python analyze.py --threshold 0.8)
   20     v
   21 [批次讀取與分析] (analyze.py 讀取 result/ 目錄下的所有 .json 檔案)
   22     |
   23     v
   24 [結果過濾與彙整] (根據 threshold 過濾低分 SDG，並計算各 SDG 的平均分數)
   25     |
   26     v
   27 [儲存統計結果與圖表] (將彙總數據存為 _avg.json，並生成 _avg_scores.png 圖表)
   28     |
   29     v
   30 [結束]

  ---

  二、主要模組與 API

  2.1 使用的 API

  根據檔案名稱 gemini_avg.json 和 gpt_avg.json 推斷，本系統同時整合了兩種 LLM API：

   1. Google Gemini API:
       * 請求格式: 通常是向 Gemini API 端點發送一個包含 contents 的 JSON 物件。contents 中包含一個或多個 parts，其中 text 欄位即為我們的 
         Prompt。
       * 回應格式: API 回應一個 JSON 物件，其 candidates[0].content.parts[0].text 中包含模型生成的文字。本系統預期此文字是一個可被解析的 
         JSON 字串。

   2. OpenAI GPT API:
       * 請求格式: 向 OpenAI API 的 chat/completions 端點發送請求，messages 陣列中包含 role ("system", "user") 與 content。system content 
         用於設定角色，user content 包含主要指令與課程文本。
       * 回應格式: API 回應一個 JSON 物件，其 choices[0].message.content 中包含模型生成的文字，同樣預期為一個可解析的 JSON 字串。

  2.2 自定義模組功能

   * `LLM_Discussions.py`
       * 功能: 驅動 LLM 分析流程的主程式。它遍歷輸入的課程清單，為每門課程呼叫 LLM API，並將結果儲存。
       * 輸入: 課程資料檔案路徑 (e.g., --input College_of_Commerce.json)、目標 LLM 模型 (e.g., --model gemini)。
       * 輸出: 在 result/ 目錄下生成多個 JSON 檔案，檔名與課程代碼對應。

   * `system_prompts.py`
       * 功能: 儲存系統所使用的 Prompt 模板。這是一個設定檔或函式庫，提供標準化的指令結構，確保 LLM 在一致的引導下進行分析。
       * 輸入: 無（作為常數或函式被其他模組引用）。
       * 輸出: 格式化後的 Prompt 字串。

   * `analyze.py`
       * 功能: 進行結果的後處理與統計分析。它讀取 result/ 中的所有原始數據，計算每個 SDG 的平均分數，並生成最終的彙總報告與圖表。
       * 輸入: 原始結果目錄路徑 (e.g., --input_dir result/)、分數閾值 (e.g., --threshold 0.8)。
       * 輸出: 彙總後的 JSON 檔案 (e.g., gemini_avg.json) 與視覺化圖表 (e.g., Gemini-2.5-flash_avg_scores.png)。

  2.3 模組相依性

   * LLM_Discussions.py 相依於 system_prompts.py 來獲取 Prompt 模板。
   * analyze.py 相依於 LLM_Discussions.py 的輸出結果（result/ 目錄下的檔案）。
   * 兩個主要執行檔都相依於外部函式庫，如 google-generativeai, openai, pandas, matplotlib。

  ---

  三、資料處理流程

  3.1 資料前處理與格式化

  系統的核心在於將非結構化的課程文本轉換為 LLM 能夠理解並處理的結構化 Prompt。

   1. 讀取資料: 從輸入的 College_of_Commerce.json 檔案中讀取課程陣列。每個課程物件包含 課程名稱、授課教師、課程描述 等欄位。
   2. Prompt 生成: 系統從 system_prompts.py 取得模板，並將課程的具體資訊填入。

  Pseudocode 範例:

    1 # system_prompts.py
    2 SDG_PROMPT_TEMPLATE = """
    3 作為一個永續發展目標（SDG）分類專家，請根據以下課程資訊，評估其與 17 項 SDGs 的關聯性。
    4 請以 1 到 10 分進行評分，10 分表示高度相關。
    5 僅輸出與課程最相關的 3 到 5 個 SDG。
    6 請以嚴格的 JSON 格式陣列輸出，每個物件包含 "SDG" (編號)、"score" (分數) 和 "reasoning" (理由)。
    7 
    8 課程名稱: {course_name}
    9 課程描述: {course_description}
   10 
   11 JSON 輸出:
   12 """
   13 
   14 # LLM_Discussions.py
   15 def format_prompt_for_course(course_data):
   16     prompt = SDG_PROMPT_TEMPLATE.format(
   17         course_name=course_data['課程名稱'],
   18         course_description=course_data['課程說明']
   19     )
   20     return prompt

  3.2 Threshold 過濾與後處理

  LLM 的原始輸出經過 analyze.py 進行後處理，以提取有意義的洞見。

   1. 資料彙整: 程式遍歷 result/ 目錄，讀取所有 JSON 檔案，將每個檔案中的 SDG 評分結果彙整到一個集中的資料結構中（例如 Pandas DataFrame）。
   2. 分數計算: 對於每個 SDG（1 到 17），計算其在所有課程中出現的平均分數。
   3. Threshold 過濾: 系統會套用一個由 CLI 參數 --threshold 指定的閾值。只有平均分數高於此閾值的 SDG 
      項目會被視為與該學院課程主題高度相關，並保留在最終結果中。

  計算方式範例:

  假設 SDG 7 在三門課程中的得分分別為 8, 9, 5，則其原始平均分為 (8+9+5)/3 = 7.33。
  若 threshold 設為 8.0，則 SDG 7 在最終統計中可能會被過濾掉（取決於過濾邏輯是作用於單次評分還是平均分，此處假設作用於平均分）。從檔名 
  gemini_avg.json 推斷，過濾應作用於計算後的平均分數。

  ---

  四、CLI 運作邏輯

  系統的執行分為兩個主要步驟，均透過 CLI 進行。

   1. 第一步：執行 LLM 分析
       * 命令: python CollegeScale/LLM_Discussions.py --input <INPUT_JSON> --model <MODEL_NAME>
       * 解析: CLI 解析 --input 和 --model 參數。
       * 執行: 程式讀取指定的輸入檔案，並根據指定的模型名稱（gemini 或 gpt）初始化對應的 API 客戶端。接著，它會遍歷所有課程，生成 
         Prompt，呼叫 API，並將結果存入 result/ 目錄。

   2. 第二步：執行結果分析與視覺化
       * 命令: python CollegeScale/analyze.py --input_dir <RESULT_DIR> --threshold <VALUE>
       * 解析: CLI 解析 --input_dir 和 --threshold 參數。
       * 執行: 程式讀取指定目錄下的所有分析結果，執行彙整、計算平均分、過濾和視覺化等後處理步驟，最終生成統計檔案和圖表。

  具體執行範例:

   1 # 步驟一: 使用 Gemini 模型對商學院所有課程進行 SDG 分類
   2 python CollegeScale/LLM_Discussions.py --input CollegeScale/College_of_Commerce.json --model gemini
   3 
   4 # 步驟二: 分析 result/ 目錄下的結果，僅保留平均分高於 0.8 (假設分數被正規化) 的 SDG
   5 python CollegeScale/analyze.py --input_dir CollegeScale/result/ --threshold 0.8

  ---

  五、環境設定與重現步驟

  要重現本研究的完整流程，請遵循以下步驟：

   1. 建立虛擬環境:
   1     python3 -m venv venv
   2     source venv/bin/activate

   2. 安裝依賴套件:
      建立 requirements.txt 檔案，內容如下：

   1     google-generativeai
   2     openai
   3     pandas
   4     matplotlib
   5     numpy
   6     tqdm # 用於顯示進度條，提升體驗
      執行安裝：
   1     pip install -r requirements.txt

   3. 設定 API 金鑰:
      將您的 API 金鑰設定為環境變數。這是保護金鑰安全的最佳實踐。
   1     export GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
   2     export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"

   4. 準備輸入資料:
      確保 CollegeScale/College_of_Commerce.json 等課程資料檔案存在且路徑正確。

   5. 執行完整流程:

   1     # 執行 SDG 分類
   2     python CollegeScale/LLM_Discussions.py --input CollegeScale/College_of_Commerce.json --model gemini
   3 
   4     # 執行結果分析
   5     python CollegeScale/analyze.py --input_dir CollegeScale/result/ --threshold 0.8

  ---

  六、擴展應用與未來延伸

  6.1 擴展應用

  本系統的核心是將任意文本對應到 SDG 框架，此能力可廣泛應用於：

   * ESG 報告分析: 自動分析企業發布的 ESG（環境、社會、治理）報告，評估其聲明的行動與各項 SDG 的一致性。
   * 永續政策文本分析: 分析政府或國際組織的政策文件，快速標記其內容涉及的 SDG 領域，便於政策評估與比較。
   * 學術論文分類: 自動將學術研究論文根據其內容對應到相關的 SDG，加速跨學科的永續發展研究整合。
   * 新聞媒體監控: 監控全球新聞，自動標記與 SDG 相關的報導，用於追蹤特定永續發展議題的公眾關注度。

  6.2 架構延伸可能性

   * 整合向量資料庫 (Vector Database):
       * 將所有課程文本或分析過的文本進行 Embedding，存入 Pinecone、ChromaDB 等向量資料庫。
       * 可實現 語意搜尋（例如，搜尋「所有關於潔淨能源的課程」）與 RAG (Retrieval-Augmented Generation)，讓 LLM 
         在分析時能參考最相關的既有資料，提升準確性與一致性。
   * 多語言支援:
       * 在 Prompt 中加入指令，要求 LLM 直接處理不同語言的文本，或在呼叫 LLM 前增加一個翻譯模組。
   * 互動式視覺化儀表板:
       * 使用 Streamlit、Dash 或 Flask/React 建立一個 Web UI，讓使用者可以上傳檔案、動態調整 
         threshold、篩選不同學院的結果，並即時查看互動式圖表。
   * 模型微調 (Fine-tuning):
       * 收集一批由專家手動標記的「課程-SDG」資料集，對開源 LLM（如 Llama 3, Mistral）進行微調，可能以更低的成本達到更高的分類準確度。

  ---

  七、優化建議

   * 運算效能:
       * 非同步處理: LLM_Discussions.py 中的 API 呼叫是典型的 I/O 密集型操作。改用 asyncio 和 aiohttp 
         進行非同步呼叫，可以大幅縮短處理大量課程所需的總時間。
       * 批次請求: 若 API 支援，將多個請求合併為一個批次請求，減少網路延遲。

   * 資料處理效率:
       * 快取機制: 對於內容未變更的課程，可以建立快取機制（例如使用檔案 hash 作為 key），避免重複呼叫 API，節省成本與時間。
       * 統一的 CLI 入口: 將 LLM_Discussions.py 和 analyze.py 的功能整合成單一主程式 main.py，並使用 main.py classify 和 main.py analyze 
         等子命令，提升 CLI 使用體驗。

   * 模型準確度:
       * Few-shot Prompting: 在 Prompt 中提供 1-2 個高品質的分類範例（"few-shot"），可以引導 LLM 產出更符合期望格式與品質的結果。
       * 思維鏈 (Chain-of-Thought): 在 Prompt 中要求 LLM "先思考，再評分"，明確列出其判斷某課程與某 SDG 
         相關的邏輯鏈，有助於提升評分的準確性與可解釋性。

   * CLI 使用體驗:
       * 進度條: 在 LLM_Discussions.py 的迴圈中加入 tqdm 進度條，讓使用者能即時了解處理進度。
       * 更豐富的輸出: 在 CLI 執行結束後，除了儲存檔案外，可以直接在終端機印出排名前三的 SDG 及其平均分數，提供即時回饋。

