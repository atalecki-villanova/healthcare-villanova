import connect
app_active = True

#conn = connect.MySqlConnect('localhost', 'root', 'root', 'sampledb')

def action(f):
    conn = connect.MySqlConnect('localhost', 'root', 'root', 'sampledb')
    if f == '1':
        c = connect.MySQLGetPatientsNotInTrainingData(conn)
        for r in c:
            print(r)
    elif f == '2':
        print("2")
    else:
        return "select a valid option"


print("What would you like to do today?")

while app_active:
    options = '0'
    options = input("\n(1) See all patients not in the training database? ")
    action(options)
