# import the libraries 

# import datetime as dt 
from datetime import timedelta 

# The DAG object; we'll need this to instantiate a DAG 
from airflow import DAG 

# Operators; we need this to write tasks! 
from airflow.operators.bash_operator import BashOperator 

# This makes scheduling easy 
from airflow.utils.dates import days_ago 
 

# Task 1.1 - Define DAG arguments 

default_args = { 
'owner': 'Mohammad Shaik', 
# 'start_date': dt.datetime(2023,3,21), 
'start_date': days_ago(0), 
'email': ['mohammadshaik351@gmail.com'], 
'email_on_failure': True, 
'email_on_retry': True, 
'retries': 1, 
'retry_delay': timedelta(minutes=5) 
} 


# Task 1.2 - Define the DAG 

dag = DAG( 
'ETL_toll_data', 
schedule_interval=timedelta(days=1), 
default_args=default_args, 
description='Apache Airflow Final Assignment' 
) 


# Task 1.3 - Create a task to unzip data  

unzip_data = BashOperator( 
task_id='unzip_data', 
bash_command='tar -zxvf /home/project/tolldata.tgz > /home/project/airflow/dags/finalassignment', 
# bash_command='unzip tolldata.tgz -d home/project/airflow/dags/finalassignment', 
# bash_command='tar -xzf /home/project/airflow/dags/finalassignment/tolldata.tgz', 
dag=dag 
) 


# Read through the file fileformats.txt to understand the column details. 
# Task 1.4 - Create a task to extract data from csv file 

extract_data_from_csv = BashOperator( 
task_id='extract_data_from_csv', 
bash_command='cut -f1-4 -d"," home/project/airflow/dags/finalassignment/vehicle-data.csv > \
    home/project/airflow/dags/finalassignment/csv_data.csv',  
dag=dag 
) 


# Task 1.5 - Create a task to extract data from tsv file 

extract_data_from_tsv = BashOperator( 
task_id='extract_data_from_tsv', 
bash_command='cut -f5-7 -d"\t" tollplaza-data.tsv > tsv_data.csv', 
dag=dag 
) 


# Task 1.6 - Create a task to extract data from fixed width file 

extract_data_from_fixed_width = BashOperator( 
task_id='extract_data_from_fixed_width', 
bash_command='awk "{print $6, $7}" payment-data.txt > fixed_width_data.csv',  
# bash_command = 'awk "NF{print $(NF-1),$NF}" OFS="\t" payment-data.txt > fixed_width_data.csv', 
dag=dag 
) 

# Task 1.7 - Create a task to consolidate data extracted from previous tasks 

consolidate_data = BashOperator( 
task_id='consolidate_data', 
bash_command='cd /home/project/airflow/dags/finalassignment |\
    paste csv_data.csv tsv_data.csv fixed_width_data.csv > extracted_data.csv',  
# task_id='paste csv_data.csv tsv_data.csv fixed_width_data.csv > extracted_data.csv', 
dag=dag 
) 


# Task 1.8 - Transform and load the data 

transform_data = BashOperator( 
task_id='transform_data', 
bash_command='cd /home/project/airflow/dags/finalassignment |\
    cut -f4 -d"," extracted_data.csv | tr "[a-z]" "[A-Z]" > transformed_data.csv', 
# bash_command = 'awk "$5 = toupper($5)" < extracted_data.csv > transformed_data.csv', 
dag=dag 
) 

 
# Task 1.9 - Define the task pipeline 
 
unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data 

 

 