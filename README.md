
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
   
   ### 1. [src/courseCrawl/main.py](https://github.com/EricLiu750501/NCCU-Course-SDGs-Correspondence-Analyser/blob/72e654946c3cd39f7aa30659b52f870960867969/src/courseCrawl/main.py)

   - 相關資料(輸入): [src/courseCrawl/CoursesList.csv](https://github.com/EricLiu750501/NCCU-Course-SDGs-Correspondence-Analyser/blob/72e654946c3cd39f7aa30659b52f870960867969/src/courseCrawl/CoursesList.csv) 根據課程年度、學期、ID 生成相對應的 Url
   
  - 使用 [Crawl4ai](https://github.com/unclecode/crawl4ai) 爬蟲，過濾不必要之資訊，生成 Markdown 格式
  
  - 相關資料(輸出): [src/courseCrawl/details](https://github.com/EricLiu750501/NCCU-Course-SDGs-Correspondence-Analyser/tree/72e654946c3cd39f7aa30659b52f870960867969/src/courseCrawl/details)
      
   
   ### 2. [src/courseCrawl/genPrompt.py](https://github.com/EricLiu750501/NCCU-Course-SDGs-Correspondence-Analyser/blob/72e654946c3cd39f7aa30659b52f870960867969/src/courseCrawl/genPrompt.py)
     
  - 相關資料(輸入): Step 1 之輸出 Markdown
  - User Prompt 生成要點 :
    - 角色： SDGs 專家、評審 等等
    - 明訂對應指標： `sdgs_targets`
    - 給分規定：高度、中度、低度相關，全憑 LLM 自身理解程度，抑或是可以明訂高中低度相關之具體規則
    - 課程輸入：Markdown
    - JSON format 具體明確規定 LLM 的輸出格式，且 LLM API 亦可規定，詳見後續 LLM API 環節  
    對應指標與JSON forma尤為重要，攸關後續分析
  
  - 相關資料(輸出): [src/courseCrawl/prompts](https://github.com/EricLiu750501/NCCU-Course-SDGs-Correspondence-Analyser/tree/72e654946c3cd39f7aa30659b52f870960867969/src/courseCrawl/prompts)
   
   ### 3. [src/CollegeScale/LLM_Discussions.py](https://github.com/EricLiu750501/NCCU-Course-SDGs-Correspondence-Analyser/blob/72e654946c3cd39f7aa30659b52f870960867969/src/CollegeScale/LLM_Discussions.py)
      
   - 相關資料（輸入）：Step 2 之輸出 User Prompt 與 Step 1 之輸出 Markdown
   - 多模型討論:
       - 模型: GPT, Gemini
       - Prompt [system_prompts.py](https://github.com/EricLiu750501/NCCU-Course-SDGs-Correspondence-Analyser/blob/72e654946c3cd39f7aa30659b52f870960867969/src/CollegeScale/system_prompts.py):
           - Answer 階段 System Prompt 要點:
               - 角色與限制: 扮演 SDG 分類專家，並嚴格規定只能使用課程資訊，不可憑空推斷。
               - 輸出格式: 強制要求輸出嚴格的 JSON 格式，並保持 17 個 SDG 的順序。
               - 評分標準:
                   - score: 0.001 到 10.0 之間，有明確證據才能給高分。
                   - reason: 需簡潔（<=30字）且必須引用課程內容的原文。
                   - evidence: 提供最多 3 條直接從課程內文摘錄的短句作為證據。
                   - evidence_type: 區分證據是 explicit (明確提及) 還是 inferred (間接推斷)。
                   - 若無證據，分數固定為 0.001。
           - Critique 階段 System Prompt 要點:
               - 角色與任務: 扮演模型 A 或 B，比較自己與對方的答案，並根據對方更有說服力的理由來修正自己的分數。
               - 輸出格式: 同樣嚴格要求 JSON。只輸出有被修正的 SDG 項目。
               - JSON 結構: 包含 critique (對雙方差異的總體評價) 和 revisions (紀錄每個修正項目的原始分數、對方分數、修正後分數及原因)。
               - 誠實原則: 強調如果對方分析更準確，應願意修正自己的分數。若無需修正，則明確說明。
           - Judge 階段 System Prompt 要點:
               - 角色與任務: 扮演公正的裁判，綜合雙方模型的原始答案和相互評論，為每個 SDG 決定最準確的分數。
               - 評分標準: 根據課程文本中的明確證據、推理品質以及與 SDG 定義的契合度來做判斷。
               - 輸出格式: 輸出包含所有 17 個 SDG 的最終裁決 JSON。
               - JSON 結構: 每個 SDG 包含 final_score (最終分數)、source (分數來源，如 model_a, revised_b 等)、reasoning (裁決理由) 及 
                 model_comparison (彙整雙方所有分數以供追溯)。
               - 公正原則: 強調不可系統性地偏袒任一模型。
       - 討論流程 (LLM_Discussions.py):
          每一階段皆可開 Multi-thread
           - 獨立回答 (Answer) : GPT 與 Gemini 根據 system_prompt 各自生成結果。
           - 相互討論 (Mutual Critique) : GPT 參考 Gemini 的 Answer 進行 critique；Gemini 也參考 GPT 的 Answer 進行 
             critique。此階段會附上原始的課程 Markdown 作為參考基準。
           - 評論 (Judge) : 綜合前兩步產生的 4 份結果 (GPT Answer, Gemini Answer, GPT Critique, Gemini Critique)，分別交給 GPT Judge 和 
             Gemini Judge 進行最終裁決。（事後證明結果差異不大，表示雙方討論有共識）
   - 相關資料（輸出）：[src/CollegeScale/result](https://github.com/EricLiu750501/NCCU-Course-SDGs-Correspondence-Analyser/tree/72e654946c3cd39f7aa30659b52f870960867969/src/CollegeScale/result)
       - 最終每個課程會生成一個 JSON 檔案，包含以上討論過程中的 6 項結果。

     
  ### 4. 最終輸出分析 [src/CollegeScale/result](https://github.com/EricLiu750501/NCCU-Course-SDGs-Correspondence-Analyser/tree/72e654946c3cd39f7aa30659b52f870960867969/src/CollegeScale/result)
  #### gpt_answer 和 gemini_answer

  這兩者的結構完全相同。它們都是一個物件，其中：
   * 鍵 (key)：是 17 個永續發展目標的名稱，例如 "No Poverty", "Zero Hunger" 等。
   * 值 (value)：是一個物件，包含以下四個欄位：
       * reason (字串): 解釋給予該分數的原因。
       * score (數字): 對該 SDG 的評分 (介於 0.001 到 10 之間)。
       * evidence (陣列): 一個包含文字證據的陣列，用來支持評分。
       * evidence_type (字串): 證據的類型，例如 "none" (無證據), "explicit" (明確的), 或 "inferred" (推斷的)。

  #### gpt_critique 和 gemini_critique

  這兩者的結構也相同。它們都是一個物件，包含：
   * critique (字串): 對另一方模型分析的總體文字評論。
   * revisions (物件): 一個物件，記錄了評論後決定修正的 SDG 項目。
       * 如果沒有需要修正的項目，這個物件會是空的 ({})。
       * 如果需要修正，其鍵為 SDG 名稱，值為一個包含修正細節的物件，例如：
           * your_original: 自己模型的原始分數。
           * model_b_score: 另一模型的原始分數。
           * your_revised: 自己模型修正後的分數。
           * reason: 修正分數的理由。

  #### gpt_judge_final 和 gemini_judge_final

  這兩者的結構也相同，代表最終的裁決。它們都是一個物件，其中：
   * 鍵 (key)：是 17 個永續發展目標的名稱。
   * 值 (value)：是一個物件，包含以下四個欄位：
       * final_score (數字): 該 SDG 的最終決定分數。
       * source (字串): 最終分數的來源，例如 "model_a" (來自模型A), "model_b" (來自模型B), 或 "revised_a" (來自模型A的修正版)。
       * reasoning (字串): 解釋為何選擇該分數作為最終決定的理由。
       * model_comparison (物件): 一個物件，詳細記錄了兩個模型在評分過程中的原始分數和修正後的分數，方便追蹤比較。


  #### 如何分析 
  1. [範例](https://github.com/EricLiu750501/NCCU-Course-SDGs-Correspondence-Analyser/blob/72e654946c3cd39f7aa30659b52f870960867969/src/CollegeScale/analyze.py) : 將大量課程讀入（以商學院為例）取其 `['judge_final'][sdg]['final_score']` 做平均，快速找到該 院/系所 所對應的 SDG
  2. 取其 `['judge_final'][sdg]['reasoning']` 綜合 LLM 給的原因，給予後續人工審閱

  
  ## 延伸應用與改進方向
  
  #### 延伸應用
  *   **ESG 報告分析**：修改提示詞與解析邏輯，用於分析企業的 ESG 或永續報告書，評估其與 SDG 的對應程度。
  *   **學術論文分類**：將本系統應用於學術資料庫，自動為論文標註相關的 SDG 領域。
  *   **政策文件稽核**：分析政府或非營利組織的政策文件，檢視其內容是否符合永續發展精神。
  
  #### 技術改進方向
  *   **快取機制（Caching）**：對於已經分析過的課程，可將其結果存入快取資料庫（如 Redis），避免重複呼叫 API，節省時間與成本。
  *   **多模型比較與整合**：引入多個不同的 LLM（如 Gemini, GPT, 
  Claude），對同一課程進行分析，並比較或整合其結果，以提升分析的穩定性與準確度。
  *   **使用者介面（UI）**：開發一個簡單的 Web UI，讓使用者能更方便地輸入網址、調整參數，並視覺化地查看分析結果。
  
  ## 授權與貢獻
  
  *   **作者**: [請填寫您的姓名或團隊名稱]
  *   **開發環境**: Python 3.12, Google Gemini API, OpenAI API
  *   **授權**: 本專案採用 [MIT License](https://opensource.org/licenses/MIT) 授權。
  
  歡迎對本專案提出建議或貢獻！
