################################################
############ Database Bulk script ##############
################################################



################################################
########### Vito Giacalone (546646) ############
####### Digital content retrival project #######
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
    db_reference.execute("ALTER TABLE file_content DROP CONSTRAINT file_content_ibfk_1")
    #db_reference.execute("SET FOREIGN_KEY_CHECKS = 0")
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
            PRIMARY KEY(id)
        )
    """)
    db_reference.execute("SET NAMES 'UTF8MB4'")
    db_reference.execute("SET CHARACTER SET UTF8MB4")


    db_reference.execute("DROP TABLE IF EXISTS file_content")
    #db_reference.execute("SET FOREIGN_KEY_CHECKS = 1;")
    db_reference.execute("""
        CREATE TABLE file_content (
            ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(255) NOT NULL, 
            Txt MEDIUMTEXT#,  
            #FOREIGN KEY(id) REFERENCES file_info(ID)
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

def insert_info_tuple(db_connection, info):
    db_reference = db_connection.cursor()
    info_insert_query = """
        INSERT INTO `file_info` (Name, Path, SizeInBytes, Type, CreationTime, LastModifiedTime) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
    db_reference.executemany(info_insert_query, info)
    db_connection.commit()
    db_reference.close()



############################ Insertion of tuples into the tables #####################################
# This table contains the data about the considered file
# A list of tuples is given as input (content)
# Each tuple contains the necessary to fill the table
# Commit
######################################################################################################

def insert_content_tuple(db_connection, content):
    db_reference = db_connection.cursor()
    content_insert_query = """
        INSERT INTO `file_content` (Name, Txt) 
        VALUES (%s, %s)
        """
    db_reference.executemany(content_insert_query, content)
    db_connection.commit()
    db_reference.close()



###################### Creation of index on column of file_content ##################################
# The index is created on Txt field of file_content table
# Commit
#####################################################################################################

def create_index(db_connection):
    db_reference = db_connection.cursor()
    db_reference.execute("CREATE FULLTEXT INDEX idx_page ON file_content (Txt);")
    db_reference.execute("CREATE INDEX idx_name ON file_info (Name);")
    db_connection.commit()
    db_reference.close()



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



################################### Bulk of the database ###########################################
# This function populate the database
# The function focus on the filetype "html"
# Each file is analyzed, but only html files are inserted into the DB
# The insertion of the data is done tuple by tuple: this type of insertion has been used
# because it requires a minimum quantity of memory.
# An eventual population of the DB starting from the root may saturate the RAM because
# the data structures become too big
# For a future Update of this program may insert tuples in batches, but this impose a 
# minimum requirement on the quantity of RAM memory available on the device
####################################################################################################

def populate_db(startpath, db_connection):
    db_reference = db_connection.cursor()
    for root, dirs, files in os.walk(startpath):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                file_size, file_name, extension, creation_time, last_modified_time = _stats_(file_path)
                print(file_size, file_name, extension, creation_time, last_modified_time)
                txt = ""
                if extension == "html":
                    with open(file_path, 'r', encoding='utf-8') as file:
                        txt = str(file.read())
                        insert_info_tuple(db_connection, [(file_name, file_path, file_size, extension, creation_time, last_modified_time)])
                        insert_content_tuple(db_connection, [(file_name, txt)])
                else:
                    insert_info_tuple(db_connection, [(file_name, file_path, file_size, extension, creation_time, last_modified_time)])
                    insert_content_tuple(db_connection, [(file_name, None)])
            except Exception as e:
                continue
        
        for dir in dirs:
            try:
                dir_path = os.path.join(root, dir)
                dir_size, dir_name, _, creation_time, last_modified_time = _stats_(dir_path)
                insert_info_tuple(db_connection, [(dir_name, dir_path, dir_size, "Directory", creation_time, last_modified_time)])
                insert_content_tuple(db_connection, [(dir_name, None)])
            except Exception as e:
                continue
    db_reference.close()



#####################################################################################################
#################################### Main ###########################################################
# Please, use the character "/" if you are using this program on Linux or MacOS system.
# Use "/" otherwise
#####################################################################################################

db_connection = connect_db("localhost", "root", "your_db_password", "DCR", "mysql_native_password")
create_tables(db_connection, os.pathconf('/', os.pathconf_names['PC_PATH_MAX']))
create_index(db_connection)
populate_db('/Users/svitol/Desktop', db_connection) 
db_connection.close()

#implementare batch per transaction
