
  ---

   # SDG 課程文本分類系統
   
   本專案為一項大學專題研究，旨在開發一個自動化系統，利用大型語言模型（Large Language Models, 
   LLMs）分析大學課程文本，並將其對應至聯合國 17 項永續發展目標（Sustainable Development Goals, SDGs）。
   
   ## 專案簡介
   
   此系統的核心功能是讀取課程的描述、目標、大綱等文本資料，透過 LLM（如 Google Gemini 或 OpenAI GPT 
   系列模型）進行語意分析，最終產出該課程與各項 SDG 指標的關聯性評分與分析依據。
   
   本研究目標在於：
   1.  **自動化標註**：取代傳統人工閱讀與分類的繁瑣流程，快速、大規模地為課程標註 SDG 屬性。
   2.  **量化評估**：提供一套可量化的數據，幫助學術機構評估其課程設計在永續發展教育中的貢獻。
   3.  **提升可見性**：協助學生、研究人員或校務管理者快速找到與特定 SDG 目標相關的課程。
   
   此系統不僅有助於推動大學的永續發展教育，也能作為未來 ESG（環境、社會、公司治理）或相關政策文本分析的技術基礎。
   
   ## 系統架構與資料流
   
   本系統由多個 Python 模組構成，整體資料流如下：
   
   1.  **啟動與參數傳遞**：使用者透過命令列介面（CLI）啟動 `main.py`，傳入目標課程網站 URL、API 金鑰等參數。
   2.  **資料抓取**：系統根據 URL 抓取網頁內容，並解析出課程的標題、描述、授課教師等結構化資訊。（*註：爬蟲邏輯由 `grepHtml.py` 
   等模組處理，此處不詳述*）
   3.  **提示詞生成**：`genPrompt.py` 模組接收課程資訊，並將其嵌入一個預先設計的提示詞模板（Prompt Template）中。此模板會引導 LLM 
   進行 SDG 分析並以指定的 JSON 格式回傳結果。
   4.  **LLM API 呼叫**：`main.py` 將生成好的提示詞發送至指定的 LLM API（例如 Gemini API）。
   5.  **結果解析與過濾**：`CourseAnalyze.py` 模組接收 LLM 回傳的 JSON 字串，進行解析、驗證，並根據預設的 `threshold`
   （閾值）過濾掉關聯性較低的 SDG 結果。
   6.  **資料儲存**：處理完成的結構化數據（包含課程資訊與其對應的 SDG 分類）最終被儲存為 JSON 檔案，供後續分析使用。
   7.  **參考資料**：`CollegeScale/` 目錄下的 JSON 檔案提供學院、科系的參考資料，可作為爬取範圍或資料擴充的依據。
  graph TD
      A[使用者 CLI] -- 參數 --> B(main.py);
      B -- URL --> C{資料抓取模組};
      C -- 課程文本 --> D(genPrompt.py);
      D -- 生成 Prompt --> B;
      B -- API Request --> E{LLM API (Gemini/OpenAI)};
      E -- JSON Response --> F(CourseAnalyze.py);
      F -- 清理與過濾 --> B;
      B -- 儲存 --> G[結果 JSON 檔案];
      H(CollegeScale/*.json) -.-> C;
    
    ## 模組與功能說明
    
    | 檔案/目錄         | 功能說明
    |
    | ----------------- | 
    -------------------------------------------------------------------------------------------------------------------------------
    ---- |
    | `main.py`         | **主控流程與 CLI 介面**：作為系統的進入點，負責解析命令列參數（如 `--url`, `--api_key`
    ），串接爬蟲、提示詞生成、API 呼叫與結果分析等模組，控制整體執行流程。 |
    | `genPrompt.py`    | **提示詞生成器**：定義了與 LLM 
    互動的提示詞模板。它會將單一課程的文本資料（如課程名稱、簡介）填入模板，生成一個結構化的指令，要求 LLM 輸出特定格式的 JSON 
    結果。 |
    | `CourseAnalyze.py`| **模型輸出解析器**：專門處理 LLM 回傳的 JSON 字串。其功能包括：解析 JSON、驗證格式、根據 
    `relevance_score` 進行閾值過濾，並將最終符合條件的 SDG 分類結果進行整合。 |
    | `CollegeScale/`   | **學院與課程參考資料**：此目錄存放各學院的課程清單或科系結構的 JSON 
    檔案。這些檔案主要作為爬取目標的參考，或用於後續資料的擴充與驗證，而非直接參與 LLM 分析。 |
    
    ## LLM 與 API 呼叫
    
    系統透過標準的 API 请求與大型語言模型進行互動。
    
    *   **API 互動**：使用 `google.generativeai` 或 `openai` 等 Python 套件庫，將 `genPrompt.py` 生成的提示詞作為請求內容發送。
    *   **請求格式**：請求的核心是一個精心設計的提示詞，要求模型扮演學術分析專家，並回傳一個包含 SDG 
    索引、關聯性分數（1-10）和分析理由的 JSON 物件。
    *   **API Key**：為了安全起見，API 金鑰（API Key）應設定為環境變數，或透過安全的命令列參數傳入，避免硬編碼在程式碼中。
    *   **錯誤處理**：程式碼中包含 `try...except` 區塊，用於捕捉 API 
    請求過程中可能發生的網路錯誤、認證失敗或模型輸出格式錯誤等異常，確保系統的穩定性。
    
    ## 資料處理與評估機制
    
    #### 文本處理
    在送入 LLM 前，系統會從爬取的 HTML 
    中提取關鍵文本欄位，如「課程目標」、「課程大綱」、「授課內容」等，並將其串接成一段完整的上下文，作為分析的基礎。
    
    #### Threshold 過濾機制
    LLM 的輸出並非百分之百精確，有時會給出關聯性很低的分類。為了提升結果的可靠性，`CourseAnalyze.py` 
    中實作了一個閾值（Threshold）過濾機制。
    
    -   **用途**：只保留 `relevance_score`（關聯性分數）高於特定閾值的 SDG 分類結果。例如，若閾值設為 `5.0`
    ，則任何低於此分數的配對都會被捨棄。
    -   **設定**：此閾值可在程式中調整，以平衡結果的「召回率」與「精確率」。較高的閾值會產出更少但更精準的結果。
    
    #### 演算法 Pseudocode
    以下為 `CourseAnalyze.py` 中核心過濾邏輯的偽代碼：
  function analyze_and_filter(llm_output_json, threshold):
      // 1. 解析 LLM 回傳的 JSON 字串
      sdg_results = parse_json(llm_output_json)

      // 2. 建立一個新的列表來存放過濾後的結果
      filtered_results = []

      // 3. 遍歷每一個 SDG 分類結果
      for each mapping in sdg_results:
          // 4. 檢查關聯性分數是否高於閾值
          if mapping.relevance_score >= threshold:
              // 5. 若高於閾值，則保留此結果
              add mapping to filtered_results

      // 6. 回傳高品質的分類結果
      return filtered_results

    
    ## 執行流程與使用方式
    
    #### 1. 安裝依賴
    首先，請確保您已安裝 Python 3.8+。接著，安裝本專案所需的套件：
  pip install -r requirements.txt

    *(註：請自行建立 `requirements.txt` 檔案，包含 `google-generativeai`, `openai` 等必要套件)*
    
    #### 2. 設定 API 金鑰
    建議將您的 LLM API 金鑰設定為環境變數，以策安全。
    
    **For Gemini API:**
  export GEMINI_API_KEY="YOUR_API_KEY_HERE"
    
    **For OpenAI API:**
  export OPENAI_API_KEY="YOUR_API_KEY_HERE"
    
    #### 3. 執行指令
    使用 `courseCrawl/main.py` 來啟動分析流程。
    
    **範例命令：**
  python courseCrawl/main.py \
      --url "https://example.edu/course_catalog/2024" \
      --output "output/sdg_analysis_results.json" \
      --api_key "YOUR_API_KEY_HERE"  # 如果未設定環境變數，可由此傳入

  *   `--url`: 欲分析的課程目錄網址。
  *   `--output`: 結果輸出的檔案路徑。
  *   `--api_key`: 您的 API 金鑰（可選，若已設定環境變數）。
  
  ## 延伸應用與改進方向
  
  #### 延伸應用
  *   **ESG 報告分析**：修改提示詞與解析邏輯，用於分析企業的 ESG 或永續報告書，評估其與 SDG 的對應程度。
  *   **學術論文分類**：將本系統應用於學術資料庫，自動為論文標註相關的 SDG 領域。
  *   **政策文件稽核**：分析政府或非營利組織的政策文件，檢視其內容是否符合永續發展精神。
  
  #### 技術改進方向
  *   **非同步處理（Asynchronous Processing）**：目前的 API 呼叫為同步阻塞式。未來可改用 `asyncio`
  ，實現非同步呼叫，大幅提升處理大量課程時的效率。
  *   **快取機制（Caching）**：對於已經分析過的課程，可將其結果存入快取資料庫（如 Redis），避免重複呼叫 API，節省時間與成本。
  *   **多模型比較與整合**：引入多個不同的 LLM（如 Gemini, GPT, 
  Claude），對同一課程進行分析，並比較或整合其結果，以提升分析的穩定性與準確度。
  *   **使用者介面（UI）**：開發一個簡單的 Web UI，讓使用者能更方便地輸入網址、調整參數，並視覺化地查看分析結果。
  
  ## 授權與貢獻
  
  *   **作者**: [請填寫您的姓名或團隊名稱]
  *   **開發環境**: Python 3.12, Google Gemini API, OpenAI API
  *   **授權**: 本專案採用 [MIT License](https://opensource.org/licenses/MIT) 授權。
  
  歡迎對本專案提出建議或貢獻！

