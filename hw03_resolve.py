def resolve_decorator(transform = lambda x: x, defualt = ""):
    def resolve_internal(resolve_func):
        def resolve_pair(first_item, second_item):
            if first_item is None and second_item is None:
                return defualt
            if first_item is None:
                return transform(second_item)
            if second_item is None:
                return transform(first_item)
            return resolve_func(transform(first_item), transform(second_item))
        return resolve_pair
    return resolve_internal

@resolve_decorator()
def r_screen(str1, str2):
    chars1 = str1.replace('х', 'x').split('x')
    chars2 = str2.replace('х', 'x').split('x')
    chars = []
    for i in range(len(chars1)):
        chars.append(int((int(chars1[i]) + int(chars2[i])) / 2))
    return str(chars[0]) + 'x' + str(chars[1])

@resolve_decorator(transform=lambda x: int(x[:-2]))
def r_weight(weight1, weight2):
    return int((weight1 + weight2) / 2)

@resolve_decorator(transform=lambda x: int(x[:-4]))
def r_guarantee(guarantee1, guarantee2):
    return min(guarantee1, guarantee2)

@resolve_decorator(defualt="нет")
def r_g_nfc(g1, g2):
    yes_str = "есть"
    no_str = "нет"
    if g1 == no_str or g2 == no_str:
        return no_str
    if g1 == yes_str:
        return g2
    if g2 == yes_str:
        return g1
    return g1

@resolve_decorator(defualt="нет")
def r_bluetooth(bluetooth1, bluetooth2):
    return bluetooth1

@resolve_decorator(transform=lambda x: int(x.replace("SIM", '')), defualt=0)
def r_sim(sim1, sim2):
    return min(sim1, sim2)

@resolve_decorator(transform=lambda x: x.replace("ГБ","GB"))
def r_memory(memory1, memory2):
    mem1 = int(memory1.replace("GB", ''))
    mem2 = int(memory2.replace("GB", ''))
    return str(min(mem1, mem2)) + " GB"

@resolve_decorator()
def r_wifi(wifi1, wifi2):
    return wifi2

@resolve_decorator(transform=lambda x: int(x[:-1]))
def r_time(time1, time2):
    return int((time1 + time2) / 2)

@resolve_decorator(transform=lambda x: x.replace("  ", ' ').replace("ГБ","GB").upper())
def r_smartphone(smartphone1, smartphone2):
    return smartphone1

class Resolver:
    def __init__(self):
        self.resolve_dict = {
            "3G" : r_g_nfc,
            "4G" : r_g_nfc,
            "5G" : r_g_nfc,
            "NFC" : r_g_nfc,
            "Вес" : r_weight,
            "Стандарт Bluetooth": r_bluetooth,
            "Гарантия" : r_guarantee,
            "Разрешение экрана": r_screen,
            "Количество SIM-карт": r_sim,
            "Объем встроенной памяти": r_memory,
            "Wi-Fi": r_wifi,
            "Время работы при прослушивании музыки": r_time,
            "Время работы при воспроизведении видео": r_time,
            "Smartphone": r_smartphone
        }
    
    def resolve(self, characteristic, value_1, value_2):
        resolve = self.resolve_dict.get(characteristic)
        return resolve(value_1, value_2)
