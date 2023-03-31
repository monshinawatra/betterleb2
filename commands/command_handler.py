import pandas as pd
import datetime
from typing import List

def str_to_date(date: str) -> datetime.datetime:
    return datetime.datetime(*list(map(int, date.split(":"))))

def update_due_date(assign_df):
    for idx, row in assign_df.iterrows():
        date_assignment = str_to_date(row["due"])
        if date_assignment < datetime.datetime.now():
            assign_df.loc[idx, "status"] = "late"
        else:
            assign_df.loc[idx, "status"] = "now"
    
    assign_df.to_csv("data/assignments.csv", index=False)
    return assign_df

def run_command(command: List[str]):
    df = pd.read_csv("data/classes.csv")
    assign_df = pd.read_csv("data/assignments.csv")
    if command[0] == "class":
        if len(command) == 1:
            texts = ""
            for idx, row in df.iterrows():
                texts += f"{idx+1} `{row['id']}` by {row['lecturer']}\n"
            return "Available classes: \n" + texts

        # The command query should be in the format: 
        # /leb2 class <add|del> <class_id> <class_name> <lecturer>
        if command[1] == "add":
            if command[2] in df["id"].values:
                return f"Class {command[2]} already exists"
            
            df = df.append({"id": command[2], "name": command[3], "lecturer": command[4], "assignment_id": len(df)}, ignore_index=True)
            df.to_csv("data/classes.csv", index=False)
            return f"Added class {command[2]}"
        elif command[1] == "del":
            df = df[df["id"] != command[2]]
            df.to_csv("data/classes.csv", index=False)
            return f"Deleted class {command[2]}"
        elif command[1] == "assignments":
            assignment_id = df[df["id"] == command[2]]["assignment_id"].values[0]
            assign_df = assign_df[assign_df["id"] == assignment_id]
            assign_df = update_due_date(assign_df)
            texts = ""
            for idx, row in assign_df.iterrows():
                texts += f"{idx+1} `{row['class_id']}` `{row['name']}` due on {str(str_to_date(row['due']))} ({row['status']})\n"
            return f"Assignments `{command[2]}`: \n" + texts
    elif command[0] == "assignments":
        # /leb2 class assignment add <class_id> <assignment_name> <due_date>
        # /leb2 class assignment del <class_id> <assignment_name>
        # Due date should be in the format: YYYY:MM:DD:HH:MM
        
        
        if command[1] in ["now", "late"]:
            # Update the status of the assignments
            assign_df = update_due_date(assign_df)

            number_of_assignments = len(assign_df[assign_df["status"] == command[1]])
            if number_of_assignments == 0:
                return f"No assignments {command[1]}"
            
            texts = ""
            for idx, row in assign_df[assign_df["status"] == command[1]].iterrows():
                texts += f"{idx+1} `{row['class_id']}` `{row['name']}` due on {str(str_to_date(row['due']))}\n"
            return f"Assignments {command[1]}: \n" + texts
        
        class_id = command[2]
        if class_id not in df.id.unique():
            return f"Class {class_id} does not exist please add it first"
        if command[1] == "add":
            # id,name,class_id,due,status
            assignment_id = df.loc[df["id"] == class_id]["assignment_id"].values[0]
            data_dict = {"id": assignment_id, "class_id": class_id, "name": command[3], "due": command[4]}
            if str_to_date(command[4]) < datetime.datetime.now():
                data_dict["status"] = "late"
            else:
                data_dict["status"] = "now"
            assign_df = assign_df.append(data_dict, ignore_index=True)
            assign_df.to_csv("data/assignments.csv", index=False)
            
            return f"Added assignment {command[3]} for class {class_id}"

        if command[1] == "del":
            pass