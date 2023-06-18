import json
from sklearn.tree import DecisionTreeClassifier



def build_branch_leaf(left, right, threshold, features, value, node):
    """For building branches and leaves"""
    s_dict = {}
    if threshold[node] != -2:
        s_dict["feature_index"] = int(features[node])
        s_dict["threshold"] = round(float(threshold[node]), 4)
        if left[node] != -1:
            s_dict["left"] = build_branch_leaf(left, right,
                                               threshold, features,
                                               value, left[node])
        if right[node] != -1:
            s_dict["right"] = build_branch_leaf(left, right,
                                                threshold, features,
                                                value, right[node])
    else:
        s_dict["class"] = int(value[node].argmax())

    return s_dict

def convert_tree_to_json(tree: DecisionTreeClassifier) -> str:

    dict_res = build_branch_leaf(tree.tree_.children_left,
                                 tree.tree_.children_right,
                                 tree.tree_.threshold,
                                 tree.tree_.feature,
                                 tree.tree_.value,
                                 0)

    tree_as_json = json.dumps(dict_res)

    return tree_as_json

def write_sql_query(inp_dict: dict, features: list) -> str:

    string = ""

    if "threshold" in inp_dict:
        string += "CASE\n"
        ftr = features[inp_dict["feature_index"]]
        string += f"WHEN {ftr} > {inp_dict['threshold']} THEN "
        if "right" in inp_dict:
            string += write_sql_query(inp_dict["right"], features)
        string += "ELSE "
        if "left" in inp_dict:
            string += write_sql_query(inp_dict["left"], features)
            string += "END\n"
    else:
        string += f"{inp_dict['class']} "

    return string

def generate_sql_query(tree_as_json: str, features: list) -> str:
    
    tree_as_json = json.loads(tree_as_json)

    sql_query = "SELECT "
    sql_query += write_sql_query(tree_as_json, features)
    sql_query = sql_query[:-1] + " AS class_label"

    return sql_query
