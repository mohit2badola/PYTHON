class Taskmanager:
    def __init__(self):
        self.task=[]
    def add_task(self,task,priority):
        self.task.append({"task":task , "Priority":priority})
        print(f"Task '{task}' added to the priority '{priority}'")

    def show_task(self):
        if not self.task:
            print("No task available")
            return

        sorted_tasks = sorted(self.task, key=lambda x: x["Priority"])
        print("Tasks")

        for t in sorted_tasks:
            print(f"Task: {t['task']} | Priority: {t['Priority']}")

t=Taskmanager()
t.add_task("Comple Assignment",5)
t.add_task("Sleep",7)
# t.add_task("Eat Biryani",25)

t.show_task()