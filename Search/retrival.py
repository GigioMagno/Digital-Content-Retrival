#!/usr/bin/python3

################################################
############## Retrieval script ################
################################################



################################################
################# Libraries ####################
################################################
import mysql.connector
from tabulate import tabulate



################################################
########### Vito Giacalone (546646) ############
####### Digital content retrival project #######
################################################

def connect_db(host, user, pwd, db, auth):
    db_connection = mysql.connector.connect(
        host=host, 
        user=user, 
        password=pwd, 
        database=db, 
        auth_plugin=auth
    )
    return db_connection


######### Search into the content of the file and into the nam field of the file ############
# The parameter "keyword" is the word to retrieve inside the Txt field (html) 
# and inside the name field
# Execute the query
#############################################################################################

def search_query(db_reference, keyword):
    query = """
            SELECT file_info.Path, file_info.Type, SUM(count)
            FROM (SELECT DISTINCT ID, count
                  FROM (SELECT ID, count
                        FROM (SELECT ID, Name, ROUND ((LENGTH(Txt) - LENGTH( REPLACE ( Txt, \""""+str(keyword)+"""\", ""))) / LENGTH(\""""+str(keyword)+"""\")) AS count 
                              FROM file_info) AS A
                        WHERE count > 0
            
              UNION 
    
                  SELECT ID, 0 AS count
                  FROM file_info
                  WHERE Name LIKE \"%"""+str(keyword)+"""%\") AS B) AS C 
            NATURAL JOIN file_info
            GROUP BY file_info.ID, file_info.NAME
            """
    db_reference.execute(query)
    return db_reference


###################### Process the results of the DB and print them #########################
# The parameter "keyword" is the word to retrieve inside the Txt field (html) 
# and inside the name field
# The tuples are retrieved in batches from the cursor
# Print the results
# Close the reference to DB
#############################################################################################

def search_name_and_occurrences(db_connection, keyword, batch_size):
    db_reference = db_connection.cursor()
    search_query(db_reference, keyword)
    print("Path", "Type", "Occurrences Inside text")
    while True:
        out = db_reference.fetchmany(batch_size)
        if not out:
            break
        for _list_ in out:
            print(f'%s\t%s\t%d' % (_list_[0], _list_[1], _list_[2]))

    db_reference.close()
    #query che ritorna il le tuple che hanno occorrenza nel nome



########################################## Main #############################################
#############################################################################################

db_connection = connect_db("localhost", "root", "GCLVTI99P27F061Y", "dcr", "mysql_native_password")
keyword = input("Insert the name or partial name to retrive: ")
MAX_BATCH_SIZE = 10
search_name_and_occurrences(db_connection, keyword, MAX_BATCH_SIZE)
db_connection.close()