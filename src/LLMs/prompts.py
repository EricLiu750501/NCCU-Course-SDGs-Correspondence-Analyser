import json


class prompts():
    def __init__(self, domains):

        self.illustrate_title = \
        '''Based on the following paper title，
classify it into all major domains and assign a score from 0.001 to 10 for each domain，
reflecting the importance or relevance of the domain.
Provide a reason for the score.'''

        self.illustrate_title_author = \
        '''Based on the following paper title and auther information，
classify it into all major domains and assign a score from 0.001 to 10 for each domain，
reflecting the importance or relevance of the domain.
Provide a reason for the score.'''

        self.illustrate_college = \
        '''Based on the following college，
classify it into all major domains and assign a score from 0.001 to 10 for each domain，
reflecting the importance or relevance of the domain.
Provide a reason for the score.'''

        self.illustrate_a = \
        '''Based on the following college，
classify it into all major domains and assign a score from 0.001 to 10 for each domain，
reflecting the importance or relevance of the domain.
Provide a reason for the score.'''


        self.paper_title = \
        "Paper Title: "

        self.auther_info = \
        "Auther Information: "

        self.college = \
        "College: "

        self.paper_abstract = \
        "Abstract: "

        self.department = \
        "Department: "

        self.paper_keywords = \
        "Keywords: "

        self.domains = \
        f"Domains:{domains}"
        
        self.dashes = "\n\n---\n\n"

        self.response = \
        '''Respond in JSON format, structured as follows: {
    "Domain Name 1": {
        "reason": "reason"，
        "score": number
    }，
    ...
}
        '''

    def illustrater(self, s) -> str:
        return f'''Based on the following {s}，
classify it into all major domains and assign a score from 0.001 to 10 for each domain，
reflecting the importance or relevance of the domain.
Provide a reason for the score.'''

 
    def title_author(self, title:str, author:dict):
        author_str = json.dumps(author, indent=4, ensure_ascii=False)
        s = self.illustrater("paper title and auther information") + self.dashes+\
            self.paper_title + title + self.dashes+\
            self.auther_info + author_str +self.dashes+\
            self.domains +self.dashes+\
            self.response
        return s
    
    def title(self, title:str):
        s = self.illustrater("paper title") + self.dashes+\
            self.paper_title + title + self.dashes+\
            self.domains +self.dashes+\
            self.response
        return s

    def title_abstract(self, title:str, abstract:str):
        s = self.illustrater("paper title and abstract") + self.dashes+\
            self.paper_title + title + self.dashes+\
            self.paper_abstract + abstract +self.dashes+\
            self.domains +self.dashes+\
            self.response
        return s

    def title_keywords(self, title:str, keywords:str):
        s = self.illustrater("paper title and keywords") + self.dashes+\
            self.paper_title + title + self.dashes+\
            self.paper_keywords + keywords +self.dashes+\
            self.domains +self.dashes+\
            self.response
        return s


    def abstract(self, abstract:str):
        s = self.illustrater("abstract") + self.dashes+\
            self.paper_abstract + abstract +self.dashes+\
            self.domains +self.dashes+\
            self.response
        return s

    def abstract_keywords(self, abstract:str, keywords:str):
        s = self.illustrater("abstract and keywords") + self.dashes+\
            self.paper_abstract + abstract +self.dashes+\
            self.paper_keywords + keywords +self.dashes+\
            self.domains +self.dashes+\
            self.response
        return s

    def abstract_author(self, abstract:str, author:dict):
        author_str = json.dumps(author, indent=4, ensure_ascii=False)
        s = self.illustrater("abstract and author information") + self.dashes+\
            self.paper_abstract + abstract +self.dashes+\
            self.auther_info + author_str +self.dashes+\
            self.domains +self.dashes+\
            self.response
        return s


    def keywords(self, keywords:str):
        s = self.illustrater("keywords") + self.dashes+\
            self.paper_keywords + keywords +self.dashes+\
            self.domains +self.dashes+\
            self.response
        return s



    def author_keywords(self, author:dict, keywords:str):
        author_str = json.dumps(author, indent=4, ensure_ascii=False)
        s = self.illustrater("author information and keywords") + self.dashes+\
            self.auther_info + author_str +self.dashes+\
            self.paper_keywords + keywords +self.dashes+\
            self.domains +self.dashes+\
            self.response
        return s

    

if __name__ == "__main__":
    domains = "幹"
    p = prompts(domains)
    title = "A Study on the Effects of AI on Education"
    author = {
        "college": "College of Social Science",
        'department':"Department of Public Finance",
        "expertise": [
                "Industrial economy",
                "intellectual property rights and innovation",
                "enterprise competition",
                "fiscal policy"
                ],

    }
    abstract = "This paper explores the impact of AI on education, focusing on its benefits and challenges."
    # print(p.title_author(title, author))
    print(p.title_abstract(title, abstract))
    print(p.abstract(abstract))








