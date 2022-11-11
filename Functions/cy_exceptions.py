import logging


class Dict_Value_Error(Exception):
    """
    Custom Error to handle a Key-Value pair in a json having the wrong data type
    """""

    # todo arguments and proper docu
    def __init__(self, json_name, cur_type, intended_type):
        self.json_name = json_name
        self.cur_type = cur_type
        self.intended_type = intended_type
        pass

    def __str__(self):
        return f"{self.json_name} is a {self.cur_type}, should be a {self.intended_type}"


def Dict_Pair_Type_Check(json_name: str, var, intended_type):
    if type(var) != intended_type:
        raise Dict_Value_Error(json_name=json_name, cur_type=type(var), intended_type=intended_type)


class Dict_Missing_Keys(Exception):
    """
    Custom Error to handle a Key-Value Pair missing in a json.
    
    Generally the pythons built-in Keyerror would be raised on a missing Key.
    But in some functions multiple Keys handles with supress(Keyerror), so a catch is needed
    
    """""

    # todo tracing to where in the json file this is listed
    def __init__(self, possible_keys: list, message: str = ""):
        self.possible_keys = possible_keys
        self.message = message
        # super().__init__(self.message)

    def __str__(self):
        return f"This command block is missing a key, use one of the following:\n {self.possible_keys}\n {self.message}"

class Format_Exception(Exception):
    """
    This Exception is for when an incompatible Data Type is produced and the function cannot
    keep working
    """""
    def __init__(self, message: str = ""):
        self.message = message
        # super().__init__(self.message)

    def __str__(self):
        return f"Incompatible Type: {self.message}"

if __name__ == "__main__":
    print("Yeet")
    mystr = "test"
    assert mystr == str, printer()
