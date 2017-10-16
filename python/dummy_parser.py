

def parse_key_val(line):
    line = line.strip()
    key, val = line.split('=')
    val = val.strip().rstrip(';')

    retkey = key.strip()

    if val.startswith('"'):
        # String
        retval = val[1:-1]

    else:
        # Value
        retval = int(val)

    return retkey, retval

def parse_classfile(data):
    retval = {}
    for line in data.splitlines():
        line = line.strip()
        if line.startswith('//') or line.startswith('#'):
            continue

        if line.startswith('class ') or line.startswith('}'):
            continue

        try:
            key, val = parse_key_val(line)
        except:
            raise
            continue

        retval[key] = val

        print(key, val)

    return retval
