import pandas as pd


def read_class_info(path: str = "data\classes.csv"):
    return pd.read_csv(path)


def add_class_info(id: int, name: str, lecturer: str, path: str = "data\classes.csv"):
    classes = read_class_info(path)

    if id not in classes.id.values:
        classes = classes.append({"id": id, "name": name, "lecturer": lecturer}, ignore_index=True)
        return_message = f"Class {name} by {lecturer} has been added"
    else:
        classes.loc[classes.id == id, "name"] = name
        classes.loc[classes.id == id, "lecturer"] = lecturer
        return_message = f"Class {name} by {lecturer} has been updated"
    classes.to_csv(path, index=False)
    return return_message


def remove_class_info(id: int, path: str = "data\classes.csv"):
    classes = read_class_info(path)

    if id not in classes.id.values:
        return_message = f"Class {id} does not exist"
    else:
        classes = classes[classes.id != id]
        return_message = f"Class {id} has been removed"
    classes.to_csv(path, index=False)
    return return_message
