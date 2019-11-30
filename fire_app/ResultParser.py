import json
#keys may be ['rois','scores','class_ids','masks','time']       
def jsonParse (result,keys):
    response={}
    print(keys)
    for key in keys:
        response[key]= result[key].tolist()
    return json.dump(response)
