import pymysql
import time
import datetime
import pickle

def MySqlConnect(_host, _user, _passwd, _db):
    conn = pymysql.connect(host=_host, user=_user, passwd=_passwd, db=_db)
    return conn

def MySQLInsertModel(_conn, _model, _CV_Accuracy, _dataSource, _numRecords):
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    
    cur = _conn.cursor(pymysql.cursors.DictCursor)
    sql = "INSERT INTO models(Model, Timestamp, CV_Accuracy, Data_Source, Num_Records) \
            VALUES (%s, %s, %s, %s, %s)"
    print("Attempting to insert")
    cur.execute(sql, (repr(_model), timestamp, float(_CV_Accuracy), _dataSource, _numRecords))
    _conn.commit()
    cur.close()
    print("Model updated")
    _conn.close()
    return "OK"

def MySQLGetPatientsNotInTrainingData(_conn):
    cur = _conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT Patient_ID \
            FROM patient_history \
            WHERE Patient_ID NOT IN  (SELECT id FROM uw_data) \
            AND Predicted_diagnosis IS NOT NULL;"
    cur.execute(sql)
    _conn.commit()
    print("All patients IDs that are not in the training data")
    cur.close()
    _conn.close()
    return cur

#def MySQLAddPatientDataToTrainingData(_conn):
#    cur = _conn.cursor(pymysql.cursors.DictCursor)
#    sql = ""
