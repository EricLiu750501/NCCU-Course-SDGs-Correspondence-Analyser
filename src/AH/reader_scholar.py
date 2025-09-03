import json

class reader:
    def __init__(self, path:str="./scholars_info_all.json"):
        with open(path, 'r', encoding='utf-8') as file:
            self.scholars_info = json.load(file)
            # print("Reading")

    def scholars_infos(self):
        

        result = []
        
        
        # print("Scholar Information:" + str(scholars_info))
        
        for college, value in self.scholars_info.items():
            # print(college)
            # print("--------")
            for depart, value2 in value.items():
                # print(depart + ": ")
                for scholar in value2:
                    # print("    " + str(scholar['expertise']))
                    for paper in scholar['publications']:
                        # print(college + " |" + depart + ": " + str(scholar['expertise']) + str(paper['title']))
                        # print("        " + str(paper))
                        result.append({
                            'college': college,
                            'department': depart,
                            'expertise': scholar['expertise'],
                            'title': paper
                        })

        return result
    
    def colleges(self):
        result = []
        for college, value in self.scholars_info.items():
            result.append(college)
        return result

    def scholars_with_college(self, college:str): #College of Informatics
        result = []
        
        # print("Scholar Information:" + str(scholars_info))
        # Check if the college exists in scholars_info
        if college not in self.scholars_info:
            return result  # Return empty list if college not found

        for depart, value2 in self.scholars_info[college].items():
            # print(depart + ": ")
            for scholar in value2:
                # print("    " + str(scholar['expertise']))
                for paper in scholar['publications']:
                    # print(college + " |" + depart + ": " + str(scholar['expertise']) + str(paper['title']))
                    # print("        " + str(paper))
                    result.append({
                        'url': scholar['url'],
                        'college': college,
                        'department': depart,
                        'expertise': scholar['expertise'],
                        'title': paper
                    })

        return result
        
    
                
if __name__ == "__main__":
    r = reader()
    # for ele in r.scholars_infos():
    #     print(ele)
    # print(r.colleges())
    cs = r.scholars_with_college("College of Informatics")
    with open("temp.json", "w", encoding='utf-8') as f:
        
        f.write(json.dumps(cs, indent=4, ensure_ascii=False))
