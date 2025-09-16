def calc_time_to_level(pc:float, change_per_10):
    if change_per_10 == 0:
        change_per_10 = 1

    remain = (( 100-pc / change_per_10 ) * 10) / 60 # 100/10 = 10 * 10 = 100mins / 60 = 1.666 -> 1hr and .66hrs (.66*60)
    hrs = int(remain)
    mins = int((remain-hrs) * 60)
    return f"{hrs}h {mins}m"

def extract_exp(val:str):
    return val[val.rindex("P")+1:val.index("%")+2]

def validate_exp_string(value:str):
    if "[" not in value: return False
    if "." not in value: return False
    if "%" not in value: return False

    return True