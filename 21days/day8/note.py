import csv
FILE="Notes.csv"

def add_notes():
    title=input("Title : ")
    content= input("Content : ")

    with open(FILE , "a", newline="") as f:
        writer=csv.writer(f)
        writer.writerow([title,content])

    print("Notes Added")

def view_note():
    try:
        with open(FILE,"r") as f:
            f.seek(0)
            reader=csv.reader(f)
            for i,row in enumerate(reader,start=1):
                print(i, row[0], "-", row[1])

    except:
        print("No notes Found")


def delete_note():
    notes=[]
    try:
        with open(FILE, "r") as f:
            reader=csv.reader(f)
            notes=list(reader)

    except:
        print("No Notes to delete")
        return

    view_note()
    n=int(input("ENter the note number to delete "))

    if 0<=n <len(notes):
        notes.pop(n)

        with open(FILE, "w", newline="") as f:
            writer=csv.writer(f)
            writer.writerows(notes)

        print("Note deleted")

    else:
        print("Invalid Number")

while True:
    print("\n1. ADD 2.view 3.Delete 4.exit")
    choice=input("ENter your choice")

    if choice =="1":
        add_notes()
    elif choice =="2":
        view_note()
    elif choice =="3":
        delete_note()
    elif choice =="4":
        break
    else:
        print("Wrong Choice")