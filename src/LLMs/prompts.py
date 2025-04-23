import json


class prompts():
    def __init__(self, domains):
        self.illustrate_title = \
        '''Based on the following paper title，
classify it into all major domains and assign a score from 0.5 to 10 for each domain，
reflecting the importance or relevance of the domain.
Provide a reason for the score.'''

        self.illustrate_title_author = \
        '''Based on the following paper title and auther information，
classify it into all major domains and assign a score from 0.5 to 10 for each domain，
reflecting the importance or relevance of the domain.
Provide a reason for the score.'''

        self.paper_title = \
        "Paper Title: "

        self.auther_info = \
        "Auther Information: "

        self.domains = \
        f"Domains:{domains}"
        
        self.dashes = "\n\n---\n\n"

        self.response = \
        '''Respond in JSON format， structured as follows: {
    "Domain Name 1": {
        "reason": "reason"，
        "score": number
    }，
    ...
}
        '''

    def title_author(self, title:str, author:dict):
        author_str = json.dumps(author, indent=4, ensure_ascii=False)
        s = self.illustrate_title_author + self.dashes+\
            self.paper_title + title + self.dashes+\
            self.auther_info + author_str +self.dashes+\
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
    print(p.title_author(title, author))








