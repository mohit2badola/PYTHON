import csv 
import os

def main():
    filename="student.csv"
    try:
        f=open(filename, "w", newline="")
        writer=csv.writer(f)
        writer.writerows(
            [
                [1,"Mohit",85],
                [2,"Amit",90],
                [3,"Riya",78]
            ]
        )
        f.close()
        print("Data written Successfully")

        with open(filename,"a",newline="") as f:
            writer=csv.writer(f)
            writer.writerow([4,"Sneha",88])

        print("Data appended successfully")

        f=open(filename,"r")
        reader=csv.reader(f)
        for i in reader:
            print(i)

        f.close()

        print("\n File Methods demo")
        print(f"File Name : {f.name} ")
        print(f"File Closed : {f.closed} ")
        print(f"File Mode: {f.mode} ")


        print("Current working directory", os.getcwd())
        print("Files in Directory", os.listdir())


        try:
            f=open("nofile.csv","r")
        except FileNotFoundError as e:
            print("Exception Caught", e)

        try:
            num=int("abc")
            result=10/0
        except ValueError as e:
            print("Value error caught : ",e)
        except ZeroDivisionError as e:
            print("Zero Division error caught : ",e)
        except Exception as e:
            print("General Exception Caught : ",e)
        else:
            print("No exception Occured")
        finally:
            print("finally bolck always executed")


        marks = 40
        if marks<50:
            raise Exception ("Marks too low")

        assert marks >=0, "Marks Cannot be negative"
    except Exception as e:
        print("Outer exception", e)

if __name__=="__main__":
    main()
