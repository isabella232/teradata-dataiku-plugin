import dataiku
import dataiku
from dataiku.customrecipe import *
from dataiku import SQLExecutor2

def do(payload, config, plugin_config, inputs):
    if payload.get('parameterName') == 'connection_name':
        client = dataiku.api_client()
        connections = client.list_connections()
        choices = []
        for key in connections:
            dict = { "value" : key, "label" : key}
            choices.append(dict)
        return {"choices": choices}   
    
    
    input_table_name = inputs[0]['fullName'].split('.')[1]
    input_dataset =  dataiku.Dataset(input_table_name)
    # Create the Dataiku SQL Executor
    conn = dataiku.core.sql.SQLExecutor2(dataset=input_dataset)
    
    if payload.get('parameterName') == 'model_database_name':
        query = """SELECT  distinct DatabaseName FROM DBC.TablesV
                   WHERE TableKind = 'T' 
                   AND   DatabaseName NOT IN ('All', 'Crashdumps', 'DBC', 'dbcmngr',
                                              'Default', 'External_AP', 'EXTUSER', 'LockLogShredder', 'PUBLIC', 'SQLJ',
                                              'Sys_Calendar', 'SysAdmin', 'SYSBAR', 'SYSJDBC', 'SYSLIB', 'SYSSPATIAL',
                                              'SystemFe', 'SYSUDTLIB', 'SYSUIF', 'TD_SERVER_DB', 'TD_SYSFNLIB',
                                              'TD_SYSGPL', 'TD_SYSXML', 'TDMaps', 'TDPUSER', 'TDQCD', 'TDStats', 'tdwm')
                   ORDER BY DatabaseName, TableName;"""
        dblistDF = conn.query_to_df(query)
        dict_names = dblistDF.to_dict()["DataBaseName"]
        choices = []
        for key in dict_names:
            dict = { "value" : dict_names[key].strip(), "label" : dict_names[key].strip()}
            choices.append(dict)
        return {"choices": choices}

    if payload.get('parameterName') == 'table_name':
        mdbs_name = config.get("model_database_name")
        if not mdbs_name :
            mdbs_name = config.get("user_Typed_DBName")
            
        print(f"mdbs_name value = {mdbs_name}")
        query = f"select TableName from DBC.TablesV WHERE TableKind = 'T' and LOWER(Databasename) = \'{mdbs_name}\' order by TableName"
        tablesListDF = conn.query_to_df(query)
        dict_names = tablesListDF.to_dict()["TableName"]
        choices = []
        for key in dict_names:
            dict = { "value" : dict_names[key].strip(), "label" : dict_names[key].strip()}
            choices.append(dict)
        return {"choices": choices}
    
    
    if payload.get('parameterName') == 'model_name':
        mdbs_name = config.get("model_database_name")
        if not mdbs_name :
            mdbs_name = config.get("user_Typed_DBName")

        tbl_name = config.get("table_name")
        if not tbl_name:
            tbl_name = config.get("user_Typed_TBLName")
        
        print(f"tbl_name =====> \"{mdbs_name}\".\"{tbl_name}\"")    
        # Create the Dataiku SQL Executor
        query = f"select model_id from \"{mdbs_name}\".\"{tbl_name}\""
        tablesListDF = conn.query_to_df(query)
        dict_names = tablesListDF.to_dict()["model_id"]
        choices = []
        for key in dict_names:
            dict = { "value" : dict_names[key].strip(), "label" : dict_names[key].strip()}
            choices.append(dict)
        return {"choices": choices}
