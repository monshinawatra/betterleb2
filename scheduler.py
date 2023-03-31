import commands.command_handler as command_handler
import pandas as pd
import datetime
def update_status():
    assign_df = pd.read_csv("data/assignments.csv")
    assign_df = command_handler.update_due_date(assign_df)
    assign_df.to_csv("data/assignments.csv", index=False)

    texts = ""
    for idx, row in assign_df.iterrows():
        
        if row["status"] == "late":
            continue
        due = command_handler.str_to_date(row["due"])
        remaining_days = (due - datetime.datetime.now()).days
        remaining_minutes = (due - datetime.datetime.now()).seconds // 60
        if remaining_minutes <= 10:
            texts += f"Assignment `{row['name']}` for class `{row['class_id']}` is due in {remaining_minutes} minutes\n"
            continue
        if remaining_days <= 2:
            texts += f"Assignment `{row['name']}` for class `{row['class_id']}` is due in {remaining_days} days\n"

    return texts