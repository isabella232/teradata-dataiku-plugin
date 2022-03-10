
import dataiku
# Import the helpers for custom recipes
from dataiku.customrecipe import *
from teradatabyomtest import handle_models
import json

model= handle_models.get_input_output(has_model_as_second_input=True)

print('=========================== MODEL')
print(model)
# get whatever information you need from your model here

model_def = model.get_definition()
print('================================ DEFINITION')
print(model_def)
# view model definition 

version_id = model_def.get('activeVersion')
print('======================================== Version ID')
print(version_id)

project_key = model_def.get('projectKey')
print('======================================== Project Key')
print(project_key)

saved_model_id = model_def.get('id')
print('======================================== Saved Model ID')
print(saved_model_id)

import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
# Own_env_model
#model_1 = dataiku.Model("9K5HCVpz")
#pred_1 = model_1.get_predictor()
valid_connection = 1

client = dataiku.api_client()
pmml_model = client.get_project(project_key).get_saved_model(saved_model_id).get_version_details(version_id).get_scoring_pmml_stream().content

connection_name = str(get_recipe_config()["connection_name"][0])
dss_connection_prams = client.get_connection(name=connection_name).get_info().get_params()
    
user_param = str(dss_connection_prams['user'])
print(user_param)
    
host_param = str(dss_connection_prams['host'])
print(host_param)
    
password_param = str(dss_connection_prams['password'])
 
database_param_by_user = str(get_recipe_config()["database_existing"])
if database_param_by_user == "":
   database_param = str(dss_connection_prams['defaultDatabase'])
else:
   database_param = database_param_by_user
    
properties_string = json.dumps(dss_connection_prams['properties'])

if 'logmech' and 'ldap' in properties_string.lower():
   logmech_param = 'LDAP'
elif 'logmech' and 'jwt' in properties_string.lower():
     logmech_param = 'JWT'
elif 'logmech' and 'krb5' in properties_string.lower():
     logmech_param = 'KRB5'
elif 'logmech' and 'tdnego' in properties_string.lower():
     logmech_param = 'TDNEGO'
else:
     logmech_param = 'TD2'
print('======================================== EXISTING LDAP')
print(logmech_param)

#encryption_param = "false"
#if bool(get_recipe_config()["encryption"]):
#    encryption_param = "true"

create_new_table_param = bool(get_recipe_config()["create"])
table_name_param = str(get_recipe_config()["tablename"])
modelname_param = str(get_recipe_config()["modelname"])

# For optional parameters, you should provide a default value in case the parameter is not present:
#my_variable = get_recipe_config().get('parameter_name', None)

# Note about typing:
# The configuration of the recipe is passed through a JSON object
# As such, INT parameters of the recipe are received in the get_recipe_config() dict as a Python float.
# If you absolutely require a Python int, use int(get_recipe_config()["my_int_param"])


#############################
# Your original recipe
#############################

# -*- coding: utf-8 -*-


import sqlalchemy
#creating connection
connection_text = 'teradatasql://whomooz/?user={}&password={}&host={}&database={}&logmech={}'
connection_text = connection_text.format(user_param,password_param,host_param,database_param,logmech_param)
#connection_text = connection_text.format(user_param,password_param,host_param,database_param,logmech_param, encryption_param)
eng = sqlalchemy.create_engine(connection_text)

if valid_connection == 1:
    if (create_new_table_param == True):
        #delete_table_if_exists = f"DROP TABLE \"{table_name_param}\";"
        #eng.execute(delete_table_if_exists)
        create_table = f"CREATE SET TABLE \"{database_param}\".\"{table_name_param}\" (model_id VARCHAR (30), model BLOB ) PRIMARY INDEX (model_id);"
        delete_table_if_exists = f"DROP TABLE \"{database_param}\".\"{table_name_param}\";"
        try:
            eng.execute(create_table);
        except:
            eng.execute(delete_table_if_exists);
            eng.execute(create_table);

        delete_record_if_exists = f"delete from \"{database_param}\".\"{table_name_param}\" where model_id = '{modelname_param}';"
        #Push the pmml
        insert_model = f"insert into \"{database_param}\".\"{table_name_param}\" (model_id, model) values(?,?);"
        eng.execute(insert_model, modelname_param, pmml_model)
    else:
        delete_record_if_exists = f"delete from \"{database_param}\".\"{table_name_param}\" where model_id = '{modelname_param[0:30]}';"
        insert_model = f"insert into \"{database_param}\".\"{table_name_param}\" (model_id, model) values(?,?);"
        eng.execute(delete_record_if_exists)
        eng.execute(insert_model, modelname_param, pmml_model)

output_dataset_name = get_output_names_for_role('output_dataset')[0]
output_dataset = dataiku.Dataset(output_dataset_name) 
if valid_connection == 1:
    lst = [f"Successfully inserted model_id:\"{modelname_param[0:30]}\" into Vantage Table \"{database_param}\".\"{table_name_param}\""]
else:
    lst = ["Recipe failed. Specify valid Vantage connection."]
df = pd.DataFrame(lst)
output_dataset.write_with_schema(df)
