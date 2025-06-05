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

    def subDomainQuery(self, domain:str, l:list) -> list[str]:
        """
        Query subdomain names based on a domain and a list of ASJC codes.
        
        Args:
            domain: The name of the domain to query.
            l: A list of ASJC codes to filter by.
            
        Returns:
            A list of subdomain names that match the given ASJC codes in the specified domain.
        """
        result = []
        subdomains = self.subDomains(domain)
        if subdomains:
            result = [f"({q}):{subdomains[q]}" for q in l]
        return result

# Create __init__.py to make the directory a proper package
def create_init_file():
    import os
    init_path = os.path.join(os.path.dirname(__file__), "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, "w") as f:
            f.write("# ASJC Code package\n")
            f.write("from .getASJC import ASJC\n")
        print(f"Created {init_path}")

# When this module is imported, ensure the package is properly set up
create_init_file()
    



if __name__ == "__main__":
    asjc = ASJC('./detailed.json')
    # print(asjc.full_code())
    # print(asjc.subDomains('Medicine'))
    print(asjc.domains())
    # print("\n".join(asjc.subDomainQuery("Computer Science", [i for i in range(13)])))
