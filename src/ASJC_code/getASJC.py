import json

class ASJC:
    def __init__(self, path:str):
        with open(path, 'r') as f:
            self.code = json.load(f)

    def full_code(self):
        return self.code

    def subDomains(self, domain:str):
        for ele in self.code:
            if ele['Domain'] == domain:
                return ele['Subdomains']
    
    def domains(self):
        result = []
        for ele in self.code:
            result.append(ele['Domain'])
        return result


if __name__ == "__main__":
    asjc = ASJC('./detailed.json')
    print(asjc.full_code())
    print(asjc.subDomains('Medicine'))
    print(asjc.domains())
