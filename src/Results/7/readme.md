- json output ensurement:ok

- 大家蠻亂的
    - 意見分歧點
        (1):Computer Science (miscellaneous)
        (2):Artificial Intelligence
        (5):Computer Networks and Communications
        (7):Computer Vision and Pattern Recognition
        (8):Hardware and Architecture
        (9):Human-Computer Interaction
- score distribution:
    - Abstract + Keywords: 有些大家分高他最低 \[3, 10] 
    ```json
    "Computational Theory and Mathematics": {
      "reason": "The abstract mentions 'proving the reliability property', which implies some level of formal verification or mathematical modeling.",
      "score": 4
    },
    "Information Systems": {
      "reason": "The abstract discusses service management and information flow within a system, which are relevant to information systems.",
      "score": 5
    },

    ```

    - keywords:
    總體評分較低 \[3, 6, 8] 會以關鍵字無提到理由作為說明
    ```json
    "Computational Theory and Mathematics": {
      "reason": "While underlying mathematical principles might be used in the design of service models, the keywords don't directly relate to computational theory or advanced mathematics.",
      "score": 0.01
    },

    "Computer Science Applications": {
      "reason": "Service models and architectures are used in a wide variety of computer science applications, making this domain relevant.",
      "score": 5
    },

    "Hardware and Architecture": {
      "reason": "While services run on hardware, the keywords focus on the software architecture and models, not the underlying hardware.",
      "score": 0.5
    },
    ```

- Heatmap
    - Abstract
        - + keyword : 幾乎一樣
        - + Author : 幾乎一樣 

    - Title
        - + keyword , Author, Abstract (相似性由高至低)
    
    - Keyword
        - + Abstract : 差異相對高

    - Author
        - 不管配誰(Title, Abstract, keyword)都沒什麼差


 - overall
    - Author 沒什麼用
    - Title / Title + keyword : 可能可以比一下 誰好
