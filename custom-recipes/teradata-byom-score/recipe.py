import dataiku
# Import the helpers for custom recipes
from dataiku.customrecipe import *
import pandas as pd

# Inputs and outputs are defined by roles. In the recipe's I/O tab, the user can associate one
# or more dataset to each input and output role.
# Roles need to be defined in recipe.json, in the inputRoles and outputRoles fields.

# To  retrieve the datasets of an input role named 'input_A' as an array of dataset names:
input_dataset_name = get_input_names_for_role('input_dataset')[0]
input_dataset = dataiku.Dataset(input_dataset_name)
testing_dataset = input_dataset_name.split('.')[1]
output_dataset_name = get_output_names_for_role('output_dataset')[0]
output_dataset = dataiku.Dataset(output_dataset_name) 

from dataiku import SQLExecutor2

scoring_type = str(get_recipe_config()["scoring_type"])
userDBInputChoice = str(get_recipe_config()["user_DBInput_Choice"])

if userDBInputChoice == 'db_drop_down':
    database_name = str(get_recipe_config()["model_database_name"])
elif userDBInputChoice == 'user_db_choice':
    database_name = str(get_recipe_config()["user_Typed_DBName"])

userTBLInputChoice = str(get_recipe_config()["user_TBLInput_Choice"])
if userTBLInputChoice == 'tbl_drop_down':
    table_name = str(get_recipe_config()["table_name"])
elif userTBLInputChoice == 'user_tbl_choice':
    table_name = str(get_recipe_config()["user_Typed_TBLName"])
    
model_name = str(get_recipe_config()["model_name"])
    
accumulate_all = bool(get_recipe_config()["accumulate_all"])
modeloutputfields_user = bool(get_recipe_config()["modeloutputfields_user"])
predict_func_dbname = str(get_recipe_config()["PMMLPredict_database_name"])

if predict_func_dbname == 'user_choice':
    PMMLPredict_db = str(get_recipe_config()["BYOM_Predict_User_DB"])
else:
    PMMLPredict_db = "mldb"

if modeloutputfields_user == True:
    modeloutputfields_values = str(get_recipe_config()["modeloutputfields_values"])

    modeloutputfield_list = modeloutputfields_values.split(',')
    stripped_list = []
    for i in range(len(modeloutputfield_list)):
        stripped_list.append(modeloutputfield_list[i].strip())
    def listToString(s): 
        str1 =""
        for ele in range(len(s)):  
            str1 += s[ele] + " "
        return str1 
    modeloutputfields_values = listToString(stripped_list).strip().replace(" ","\',\'")

if accumulate_all == True:
    accumulate = '*'
if accumulate_all == False:
    accumulate = str(get_recipe_config()["accumulate_column_names"])
    accumulate = accumulate[2:]
    accumulate = accumulate[:-2]



overwrite_cache = ""

if bool(get_recipe_config()["overwrite_cache"]):
    overwrite_cache = f"OverwriteCachedModel('{model_name}')"

conn =  SQLExecutor2(dataset = input_dataset)

    

if scoring_type == 'dataiku':
    if modeloutputfields_user == False:
        query = f"SELECT * FROM {PMMLPredict_db}.PMMLPredict ( ON (select * from \"{database_name}\".\"{testing_dataset}\") AS InputTable ON (SELECT * FROM \"{database_name}\".\"{table_name}\" WHERE model_id = '{model_name}') AS ModelTable DIMENSION USING Accumulate ('{accumulate}') {overwrite_cache})AS td;"
    else:
        query = f"SELECT * FROM {PMMLPredict_db}.PMMLPredict ( ON (select * from \"{database_name}\".\"{testing_dataset}\") AS InputTable ON (SELECT * FROM \"{database_name}\".\"{table_name}\" WHERE model_id = '{model_name}') AS ModelTable DIMENSION USING Accumulate ('{accumulate}') ModelOutputFields('{modeloutputfields_values}') {overwrite_cache})AS td;"
    predicted = conn.query_to_df(query)
    
if scoring_type == 'h2o':
    h2o_model_type = str(get_recipe_config()["H2O_Model_Type"])
        
    if h2o_model_type == 'h2o_dai':
        if modeloutputfields_user == False:
            query = f"SELECT * FROM {PMMLPredict_db}.H2OPredict ( ON (select * from \"{database_name}\".\"{testing_dataset}\") AS InputTable ON (SELECT model_id, model, \"{database_name}\".h2o_lic.license FROM \"{database_name}\".\"{table_name}\" WHERE model_id = '{model_name}') AS ModelTable DIMENSION USING Accumulate ('{accumulate}') ModelType ('DAI') {overwrite_cache})AS td;"
        else:
            query = f"SELECT * FROM {PMMLPredict_db}.H2OPredict ( ON (select * from \"{database_name}\".\"{testing_dataset}\") AS InputTable ON (SELECT model_id, model, \"{database_name}\".h2o_lic.license FROM \"{database_name}\".\"{table_name}\" WHERE model_id = '{model_name}') AS ModelTable DIMENSION USING Accumulate ('{accumulate}') ModelType ('DAI') ModelOutputFields('{modeloutputfields_values}') {overwrite_cache})AS td;"
    else:
        if modeloutputfields_user == False:
            query = f"SELECT * FROM {PMMLPredict_db}.H2OPredict ( ON (select * from \"{database_name}\".\"{testing_dataset}\") AS InputTable ON (SELECT model_id, model FROM \"{database_name}\".\"{table_name}\" WHERE model_id = '{model_name}') AS ModelTable DIMENSION USING Accumulate ('{accumulate}') {overwrite_cache})AS td;"
        else:
            query = f"SELECT * FROM {PMMLPredict_db}.H2OPredict ( ON (select * from \"{database_name}\".\"{testing_dataset}\") AS InputTable ON (SELECT model_id, model FROM \"{database_name}\".\"{table_name}\" WHERE model_id = '{model_name}') AS ModelTable DIMENSION USING Accumulate ('{accumulate}') ModelOutputFields('{modeloutputfields_values}') {overwrite_cache})AS td;"
    predicted = conn.query_to_df(query)
    
print(f"Prediction Query ==> {query}")
output_dataset.write_with_schema(pd.DataFrame(predicted))
