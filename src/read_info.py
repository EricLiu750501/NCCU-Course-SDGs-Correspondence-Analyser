from LLMs import prompts, ask
from AH.reader_scholar import reader
import os
from ASJC_code.getASJC import ASJC

def code_college_mapping(college:str):
    dict = {
        'College of Social Science': "Social Sciences",
        'College of Liberal Arts':"Arts and Humanities",
        'Affiliated Centers': "Multidisciplinary",
        'College of Commerce':"Business, Management, and Accounting",
        'College of Education':"Social Sciences"

    }
    if dict.get(college) is None:
        # print("Error: " + college + " not in dict")
        return None
    return dict[college]


if __name__ == "__main__":
    # print(os.getcwd())
    r = reader("./AH/scholars_info.json")
    asjc = ASJC('./ASJC_code/detailed.json')
    gpt = ask.GPT()
    gemini = ask.Gemini()

    for ele in r.scholars_infos()[:1]:
        title = ele['title']
        author = {
            "college": ele['college'],
            'department': ele['department'],
            "expertise": ele['expertise']
        }
        domain = code_college_mapping(author['college'])
        if domain:
            subdomain = asjc.subDomains(domain)
            p = prompts.prompts(subdomain)
            generate_prompt = p.title_author(title, author)
            print("Prompt: " + generate_prompt)
            print("Result: " + gpt.ask(generate_prompt))
            
            print("-" * 40)
        else:
            print("Error: " + author['college'] + " not in dict")


