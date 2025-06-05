- json output ensurement:ok

- score distribution:
    - Auther + Keywords : weird  
    突出項：

    同時使用 Auther + Keywords
    ```json
    "General Computer Science": {
        "reason": "The author's department is Computer Science, and the expertise includes AI, Robotics, and Computational Linguistics, all of which fall under the umbrella of General Computer Science. Keywords like 'Institutional repository' and 'Archive policy' also relate to general CS principles of data management and organization.",
        "score": 7
        },
    ```
    
    但只依賴 author
    ```json
    "Artificial Intelligence": {
        "reason": "The author's expertise explicitly includes '人工智慧' (Artificial Intelligence), making this a highly relevant domain.",
        "score": 9
        },
    ```

- Spearman Rank Correlation:
    - Auther + Keywords :   
    - Title + Author : \[0:3] 有一點亂流跟大家不一樣
    - Abstract + Author : \[6] 特別低
        ```json
        "Computer Science Applications": {
            "reason": "Institutional repositories are a specific application of computer science principles, particularly in information management and access.",
            "score": 5
            },
        ```
