from bs4 import BeautifulSoup

def clean_json(data):
    def remove_table(obj):
        soup=BeautifulSoup(obj,'html.parser')
        for table in soup.find_all('table'):
            table.decompose()
        return str(soup).strip().lower()

    def process_json(obj):
        if isinstance(obj,dict):
            new_dict={}
            for key,value in obj.items():
                val=process_json(value)
                if val==[]:
                    pass
                elif key!='results' and isinstance(val,list):
                    new_dict[key]=' '.join(map(str,val))
                else:
                    new_dict[key]=val
            return new_dict        
                    
        elif isinstance(obj,list):
            new_list=[]
            for item in obj:
                ele=process_json(item)
                if ele:
                    new_list.append(ele)
            return new_list        

        elif isinstance(obj,str):
            if '<table' in obj:
                return remove_table(obj)
            else:
                return obj.lower()
        else:
            return obj     

    cleaned_json=process_json(data)
    for k,v in cleaned_json.items():
        if k=='results':
            return cleaned_json['results']
    else:
        raise Exception('Absence of results key in your json')    
