import yaml


class AnyType:
    pass


def dict_to_path(inp_dict: dict, cur_lvl: str, inp_lst: list) -> list:
    for key, val in inp_dict.items():
        if isinstance(inp_dict[key], dict):
            cur_lvl += str(key) + "."
            dict_to_path(inp_dict[key], cur_lvl, inp_lst)
            cur_lvl = ""
        else:
            inp_lst.append(f"{cur_lvl}{key}={val}")
    return inp_lst

def dict_to_yaml(inp_dict: str) -> str:
    return yaml.dump(inp_dict)

def yaml_to_dict(inp_yaml: str) -> str:
    return yaml.safe_load(inp_yaml)

def line_into_dict(inp_dict: dict, inp_lst: list, val: AnyType):
    if inp_lst:
        k, inp_lst = inp_lst[0], inp_lst[1:]
        if not inp_lst:
            try:
                inp_dict[k] = int(val)
            except ValueError:
                try:
                    inp_dict[k] = float(val)
                except ValueError:
                    if val.lower() == "true":
                        inp_dict[k] = True
                    elif val.lower() == "false":
                        inp_dict[k] = False
                    else:
                        inp_dict[k] = val
        else:
            if k not in inp_dict:
                inp_dict[k] = {}
        line_into_dict(inp_dict[k], inp_lst, val)
    else:
        inp_dict = val

def path_to_dict(inp_env: str) -> dict:
    out_dict = {}
    lst = inp_env.split()

    for line in lst:
        path, val = line.split("=")
        line_into_dict(out_dict, path.split("."), val)

    return out_dict

def yaml_to_env(config_file: str) -> str:
    y_dict = yaml_to_dict(config_file)
    y_lst = dict_to_path(y_dict, "", [])
    return "\n".join(y_lst)

def env_to_yaml(env_list: str) -> str:
    e_dict = path_to_dict(env_list)
    e_yaml = dict_to_yaml(e_dict)
    return e_yaml
