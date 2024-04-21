################################################
########### Vito Giacalone (546646) ############
####### Digital content retrival project #######
################################################



################################################
############ Database Bulk script ##############
################################################



################################################
################# Libraries ####################
################################################
import os
import csv
import datetime
import re
import mysql.connector



############ Database connection ###############

def connect_db(host, user, pwd, db, auth):
    db_conn = mysql.connector.connect(
        host=host, 
        user=user, 
        password=pwd, 
        database=db, 
        auth_plugin=auth
    )
    return db_conn



############################## Definition and creation of the tables ################################
# Drop of the constraint on foreign key, drop of the tables if they exist yet
# Setting of the charset for each table
# Commit
#####################################################################################################

def create_tables(db_connection, maxsize):
    db_reference = db_connection.cursor()
    db_reference.execute("SET FOREIGN_KEY_CHECKS = 0")
    db_reference.execute("DROP TABLE IF EXISTS file_info")
    db_reference.execute("""
        CREATE TABLE file_info (
            ID INT NOT NULL AUTO_INCREMENT, 
            Name VARCHAR(255) NOT NULL, 
            Path VARCHAR(""" + str(maxsize) + """), 
            SizeInBytes BIGINT, 
            Type VARCHAR(""" + str(maxsize) + """),
            CreationTime DATETIME, 
            LastModifiedTime DATETIME, 
            Txt MEDIUMTEXT,
            PRIMARY KEY(id)
        )
    """)
    db_reference.execute("SET NAMES 'UTF8MB4'")
    db_reference.execute("SET CHARACTER SET UTF8MB4")
    db_connection.commit() #specify the type of transaction, in this wa i'm using autocommit mode of mysql.



########################## Insertion of tuples into the table file_info ##############################
# This table contains informations about the considered file
# A list of tuples is given as input (info)
# Each tuple contains the necessary to fill the table
# Commit
######################################################################################################

def insert_info_tuple(db_reference, info):
    info_insert_query = """
        INSERT INTO `file_info` (Name, Path, SizeInBytes, Type, CreationTime, LastModifiedTime, Txt) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
    db_reference.executemany(info_insert_query, info)
    db_connection.commit()


###################### Creation of index on column of file_content ##################################
# The index is created on Txt field of file_content table
# Commit
#####################################################################################################

def create_index(db_connection):
    db_reference = db_connection.cursor()
    db_reference.execute("CREATE FULLTEXT INDEX idx_page ON file_info (Txt);")
    db_connection.commit()



############################ Remove char from string ###############################################
# This function filters "special" characters from a string 
# The string is typically the name of the file
####################################################################################################

def remove_char_from_string(string):
    for c in "#?$&/%!\"£*,:;_-#":
        string = string.replace(c, " ")
    return string



##################### Extraction of information about a file from path #############################
# The function returns:
# file_size
# file_name
# extension (mp3, html,...)
# creation_time
# last_modified_time
####################################################################################################

def _stats_(path):
    file_size = os.stat(path).st_size
    file_name = remove_char_from_string(path.split("/")[-1])
    extension = path.split(".")[-1]
    creation_time = datetime.datetime.fromtimestamp(os.path.getctime(path)).strftime('%Y-%m-%d %H:%M:%S')
    last_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')
    return file_size, file_name, extension, creation_time, last_modified_time



########################## Function to check if the batch is full ##################################
# The function returns:
# an empty list if the batch is full
# the batch if is not already full
# the function also insert the tuples in the DB if the batch is full
# This type of implementation has been designed to avoid that the complete filling of the RAM memory
# The batch implementation provides that a constant number of tuples are in RAM
####################################################################################################

def check_and_submit(batch, MAX_BATCH_SIZE, db_reference):
    if len(batch) == MAX_BATCH_SIZE:
        insert_info_tuple(db_reference, batch)
        return []
    else:
        return batch



################################### Bulk of the database ###########################################
# This function populate the database
# The function focus on the filetype "html"
# Each file is analyzed, but only html files are inserted into the DB
# The insertion of the data is done tuple by tuple: this type of insertion has been used
# because it requires a minimum quantity of memory.
# An eventual population of the DB starting from the root may saturate the RAM because
# the data structures become too big (In the case without batch)
# Thanks to the batch insertion a constant quantitative of ram is allocated
# This parameter is fixed inside the code
# A future update may provide to read the size of the batch from command line
####################################################################################################

def populate_db(startpath, db_connection, MAX_BATCH_SIZE):
    batch = []
    db_reference = db_connection.cursor()
    for root, dirs, files in os.walk(startpath):
        for file in files:
            if len(batch) < MAX_BATCH_SIZE:
                try:
                    file_path = os.path.join(root, file)
                    file_size, file_name, extension, creation_time, last_modified_time = _stats_(file_path)
                    print(file_size, file_name, extension, creation_time, last_modified_time)
                    txt = ""
                    if extension == "html":
                        with open(file_path, 'r', encoding='utf-8') as file:
                            txt = str(file.read())
                            batch.append((file_name, file_path, file_size, extension, creation_time, last_modified_time, txt))
                    else:
                        batch.append((file_name, file_path, file_size, extension, creation_time, last_modified_time, None))
                    batch = check_and_submit(batch, MAX_BATCH_SIZE, db_reference)
                except Exception as e:
                    continue
        
        for dir in dirs:
            if len(batch) < MAX_BATCH_SIZE:
                try:
                    dir_path = os.path.join(root, dir)
                    dir_size, dir_name, _, creation_time, last_modified_time = _stats_(dir_path)
                    batch.append((dir_name, dir_path, dir_size, "Directory", creation_time, last_modified_time, None))
                    batch = check_and_submit(batch, MAX_BATCH_SIZE, db_reference)
                except Exception as e:
                    continue

    insert_info_tuple(db_reference, batch)
    db_reference.close()



#####################################################################################################
#################################### Main ###########################################################
# Please, use the character "/" if you are using this program on Linux or MacOS system.
# Use "\" otherwise
#####################################################################################################

db_connection = connect_db("localhost", "root", "your_db_password", "DCR", "mysql_native_password")
create_tables(db_connection, os.pathconf('/', os.pathconf_names['PC_PATH_MAX']))
MAX_BATCH_SIZE = 10
populate_db('/Users/svitol/', db_connection, MAX_BATCH_SIZE)
create_index(db_connection)
db_connection.close()

#implementare batch per transaction
