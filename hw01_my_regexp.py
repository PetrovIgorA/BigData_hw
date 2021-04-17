import hw_base

def myregexp(text : str, reg : str, value : str):
    if '*' in reg:
        return find_any(text, reg[1:], value)
    elif '[' in reg:
        return find_cond(text, reg, value)
    else:
        return find_simple(text, reg, value)

def find_simple(text : str, reg : str, value : str):
    if text == reg:
        return value
    return hw_base.UNUSED_CHARACTERISTICS_NAME

def find_any(text: str, reg : str, value : str):
    if '[' in reg:
        return find_any_cond(text, reg, value)
    elif text.find(reg) != -1:
        return value
    else:
        return hw_base.UNUSED_CHARACTERISTICS_NAME

def find_any_cond(text: str, reg : str, value : str):
    index_s = reg.find('[')
    index_e = reg.find(']')
    variants = reg[index_s + 1: index_e].split('|')
    for variant in variants:
        if text.find(variant) != -1:
            return value
    return hw_base.UNUSED_CHARACTERISTICS_NAME

def find_cond(text : str, reg : str, value : str):
    index_s = reg.find('[')
    index_e = reg.find(']')
    variants = reg[index_s + 1: index_e].split('|')
    if index_s == 0:
        other_reg = reg[index_e + 1:]
        for variant in variants:
            if text.find(variant) == 0 and text[len(variant):] == other_reg:
                return value
        return hw_base.UNUSED_CHARACTERISTICS_NAME
    else:
        other_reg = reg[:index_s]
        #hw_base.debug(reg, other_reg)
        for variant in variants:
            if text.find(variant) == len(other_reg) and text[:len(other_reg)] == other_reg and len(other_reg) + len(variant) == len(text):
                return value
    return hw_base.UNUSED_CHARACTERISTICS_NAME
