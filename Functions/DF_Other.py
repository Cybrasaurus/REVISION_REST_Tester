import logging


def _loop_keyword_replacer(json_contents, pri_key, replacement):
    import json
    #todo docu
    working_string = ""
    working_string = str(json_contents)

    working_string = working_string.replace(str(pri_key), str(replacement))

    # Old methon via json.loads
    #working_string = working_string.replace("'", '"')
    #return_json = json.loads(working_string)

    import ast
    return_json = ast.literal_eval(working_string)

    return return_json

def loop_keyword_replacer(config_commands, cur_replacement):

    primary_key = config_commands["Primary_Key"]
    json_contents = config_commands["Loop_Commands"]

    return _loop_keyword_replacer(json_contents=json_contents, pri_key=primary_key, replacement=cur_replacement)
