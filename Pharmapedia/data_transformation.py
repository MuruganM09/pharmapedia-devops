from config import drug_file_path
import os

def transform_json(data):
    metadata = ["generic_name"]
    
    non_needed_metapage=["brand_name","substance_name","product_ndc","product_type","route","is_original_packager","pharm_class_epc","pharm_class_cs"
                         ,"manufacturer_name","rxcui","effective_time","version","set_id"]
    
    def extract_metadata(metadata,data,new_metadata=None):
            if new_metadata == None:
                 new_metadata={}
            if isinstance(data,dict):     
                for key,value in data.items():
                    if key in metadata:
                        new_metadata[key]=value
                    if isinstance(value,dict):
                        return extract_metadata(metadata,value,new_metadata)
            return new_metadata                         
                     
    def transform(basemeta,data):
        document=[]
        if isinstance(data,dict):
            for key,value in data.items():
                metadata=basemeta.copy()
            
                if key in non_needed_metapage:
                    continue

                if isinstance(value,str) and value:
                    content=value
                    section=key.replace('_',' ')
                    metadata['section']=section
                    drug=metadata.get('generic_name','NA')
                    if "set_id" in metadata:
                        idx=f"{metadata['set_id']}_{drug}_{key}_".strip().replace(' ','_')
                    else:
                        idx=f"set_id_{drug}_{key}_".strip().replace(' ','_')
                    document.append({
                        'page_content':content.strip(),
                        'metadata':metadata,
                        'id':idx
                    }) 
        return document            

    documents=[]
    for item in data:
        base_meta=extract_metadata(metadata,item)
        if 'generic_name' in base_meta:
            transformed_data=transform(base_meta,item)
            documents.extend(transformed_data)

    if os.path.exists(drug_file_path):
        with open(drug_file_path,mode='r') as file:
            drug_exists_list=file.read().splitlines()
    else:
        with open(drug_file_path,mode='w+') as file:
            file.write("")

    with open(drug_file_path,mode='+a') as file:
        drug_list=[]
        for drug_name in documents:
            drug_ele=drug_name['metadata']['generic_name']
            if drug_ele not in drug_list and drug_ele not in drug_exists_list:
                drug_list.append(drug_ele)
                file.write(drug_ele)
                file.write("\n")    
  
    return documents


