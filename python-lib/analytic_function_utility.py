# -*- coding: utf-8 -*-
"""This file has all the functions that check whether it can use the Vantage Capability Table if it exists, 
otherwise it gets the information from the fallback directory of JSONs."""

'''
Copyright © 2019 by Teradata.
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notsdkice shall be included in all copies or
substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import os
import json
import logging

table_name = "VantageAnalyticsJSON" 

def get_all_functions(query_engine_wrapper, fallback_directory, category_name = None, plugin_name = None, check_analytic_table = False):
    """
    This function gets all the analytic functions (for the purpose of retrieving all possible analytic function choices). 
    If the Vantage Capability Table exists it uses that to get the functions, otherwise it uses the fallback directory of JSONs.

    @param query_engine_wrapper: See query_engine_wrapper.py file. The query_engine_wrapper must have an execute method which will
        be used to execute a query_string (SQL query to get each function). It must also have iteratable and row_value methods 
        which will be used to iterate over each row of the query results.

        >>> query_results = query_engine_wrapper.execute(query_string+ ";")
        Example of using execute method 

        >>> for row in query_engine_wrapper.iteratable(query_results):
        >>>    lst.append(query_engine_wrapper.row_value(row, "FunctionName"))
        Example of iterating over using iteratable and row_value methods

    @type query_engine_wrapper: QueryEngineWrapper class.

    @param fallback_directory: A variable represents the file path for the analytic function JSONs.
        It is used when the Vantage Capability Table does not exist.
    @type fallback_directory: String.

    @param category_name: A variable that
        that represents the specific category name (default is None, 
        if it is None then category_name is not included in the query).
    @type category_name: String.

    @param plugin_name: A variable that
        that represents the specific plugin name i.e. MLE or SQLE 
        (default is None, if it is None then plugin_name is not included in the query).
    @type plugin_name: String.

    @param check_analytic_table: A variable that
        that represents whether the analytic table should be checked. The variable will be set to 
        False until the table is created to save UI loading time when the database is down.
    @type check_analytic_table: Boolean.

    @return: This function returns a list which holds 
        every analytic function that was iterated over
        and added via the Vantage Capability table
        if that exists, otherwise from the fallback directory of JSONs.
    """ 

    lst = []
    if check_analytic_table == True:
        try:
            # execute the query to get the function names from the VCT
            query_string = "SELECT FunctionName FROM " + table_name
            if category_name != None and plugin_name != None:
                query_string += " WHERE Category LIKE '"+ category_name +"' AND Plugin LIKE '" + plugin_name + "'"
            elif category_name != None:
                query_string += " WHERE Category LIKE '"+ category_name +"'"
            elif plugin_name != None:
                query_string += " WHERE Plugin LIKE '"+ plugin_name +"'"
            query_results = query_engine_wrapper.execute(query_string+ ";")
            # loop through each function and append to the list
            for row in query_engine_wrapper.iteratable(query_results):
                lst.append(query_engine_wrapper.row_value(row, "FunctionName"))
        except BaseException as e:
            logging.info("teradata_analytic_lib: " +table_name+ " does not exist!", e)
            lst = []
    # If the VCT does not have many functions then it is not correct, mark is as false
    min_num_functions = 20
    if len(lst) < min_num_functions:
        logging.info("teradata_analytic_lib: " +table_name+ " does not have enough functions!, only", len(lst))
        lst = []
    if not lst:
        # In this case VCT doesnt exist, so use JSONs on filesystem with the appropriate version
        lst = os.listdir(fallback_directory)
        lst = [x.replace(".json", "") for x in lst if x.index(".json") != -1]
    return lst
    


def get_function_json(query_engine_wrapper, function_name, fallback_directory, category_name = None, plugin_name = None, check_analytic_table = False):
    """
    This function gets the specific a analytic function JSON based on the function name. 
    If the Vantage Capability Table exists it uses that to get the functions, otherwise it uses the fallback directory of JSONs.

    @param query_engine_wrapper: See query_engine_wrapper.py file. The query_engine_wrapper must have an execute method which will
        be used to execute a query_string (SQL query to get each function). It must also have iteratable and row_value methods 
        which will be used to iterate over each row of the query results.

        >>> query_results = query_engine_wrapper.execute(query_string+ ";")
        Example of using execute method 

        >>> for row in query_engine_wrapper.iteratable(query_results):
        >>>    lst.append(query_engine_wrapper.row_value(row, "FunctionName"))
        Example of iterating over using iteratable and row_value methods

    @type query_engine_wrapper: QueryEngineWrapper class.

    @param function_name: A variable for the 
        analytic function name.
    @type function_name: String.

    @param fallback_directory: A variable represents the file path for the analytic function JSONs.
        It is used when the Vantage Capability Table does not exist.
    @type fallback_directory: String.

    @param category_name: A variable that
        that represents the specific category name (default is None, 
        if it is None then category_name is not included in the query).
    @type category_name: String.

    @param plugin_name: A variable that
        that represents the specific plugin name i.e. MLE or SQLE 
        (default is None, if it is None then plugin_name is not included in the query).
    @type plugin_name: String.

    @param check_analytic_table: A variable that
        that represents whether the analytic table should be checked. The variable will be set to 
        False until the table is created to save UI loading time when the database is down.
    @type check_analytic_table: Boolean.

    @return: This function returns a dictionary which has each analytic
        function as the key and its appropriate JSON as its value that was iterated over
        and added via the Vantage Capability table
        if that exists, otherwise from the fallback directory of JSONs.
    """ 
    function_json = {} 
    if check_analytic_table == True:           
        try:
            # execute the query to get the JSON from the VCT that matches the function requested
            query_string = "SELECT JSON FROM  '"+ table_name + "' WHERE FunctionName LIKE '" + function_name + "'"

            if category_name != None and plugin_name != None:
                query_string += " AND Category LIKE '" + category_name + "' AND Plugin LIKE '" + plugin_name + "'"
            elif category_name != None:
                query_string += " AND Category LIKE '" + category_name + "'"
            elif plugin_name != None:
                query_string += " AND Plugin LIKE '" + plugin_name + "'"

            query_results = query_engine_wrapper.execute(query_string + ";")

            # loop through each function and append to the list 
            for row in query_engine_wrapper.iteratable(query_results):
                function_json = json.loads(query_engine_wrapper.row_value(row, 'JSON').decode("utf-8"))
                break

            if not function_json:
                logging.info("teradata_analytic_lib: " +table_name+ " exists but the function is missing", function_name)
        
        except BaseException as e:
            logging.info("teradata_analytic_lib: " +table_name+ " does not exist! Falling back to JSON on filesystem", e)
            function_json = {}

    if not function_json:
        # In this case VCT doesnt exist, so use JSONs on filesystem with the appropriate version and function name
        file_name = os.path.join(fallback_directory, function_name+".json")
        if not os.path.isfile(file_name):
            raise IOError
        with open(file_name) as f:
          function_json = json.load(f)

    return function_json


def get_all_function_jsons(query_engine_wrapper, fallback_directory, category_name = None, plugin_name = None, check_analytic_table = False):
    """
    This function gets all the analytic functions and its appropriate JSON. 
    If the Vantage Capability Table exists it uses that to get the functions, otherwise it uses the fallback directory of JSONs.

    @param query_engine_wrapper: See query_engine_wrapper.py file. The query_engine_wrapper must have an execute method which will
        be used to execute a query_string (SQL query to get each function). It must also have iteratable and row_value methods 
        which will be used to iterate over each row of the query results.

        >>> query_results = query_engine_wrapper.execute(query_string+ ";")
        Example of using execute method 

        >>> for row in query_engine_wrapper.iteratable(query_results):
        >>>    lst.append(query_engine_wrapper.row_value(row, "FunctionName"))
        Example of iterating over using iteratable and row_value methods

    @type query_engine_wrapper: QueryEngineWrapper class.

    @param fallback_directory: A variable represents the file path for the analytic function JSONs.
        It is used when the Vantage Capability Table does not exist.
    @type fallback_directory: String.

    @param category_name: A variable that
        that represents the specific category name (default is None, 
        if it is None then category_name is not included in the query).
    @type category_name: String.

    @param plugin_name: A variable that
        that represents the specific plugin name i.e. MLE or SQLE 
        (default is None, if it is None then plugin_name is not included in the query).
    @type plugin_name: String.

    @param check_analytic_table: A variable that
        that represents whether the analytic table should be checked. The variable will be set to 
        False until the table is created to save UI loading time when the database is down.
    @type check_analytic_table: Boolean.

    @return: This function returns a list which holds 
        every analytic function that was iterated over
        and added via the Vantage Capability table
        if that exists, otherwise from the fallback directory of JSONs.
    """ 
    
    result = []           
    sql_query_worked = False
    if check_analytic_table == True: 
        try:
            # execute the query to get the JSON from the VCT that matches the function requested
            query_string = "SELECT CAST(FROM_BYTES(VCT.JSON, 'base16') AS VARCHAR(30000)) AS JSON FROM '"+ table_name + "' AS VCT"
            if category_name != None and plugin_name != None:
                query_string += " WHERE Category LIKE '" + category_name + "' AND Plugin LIKE '" + plugin_name + "'"
            elif category_name != None:
                query_string += " WHERE Category LIKE '" + category_name + "'"
            elif plugin_name != None:
                query_string += " WHERE Plugin LIKE '" + plugin_name + "'"
            
            query_results = query_engine_wrapper.execute(query_string + ";")

      
            # loop through each function and append to the list 
            for row in query_engine_wrapper.iteratable(query_results):
                logging.info("teradata_analytic_lib: Loaded JSON from " +table_name+ "!")
                json_string = bytearray.fromhex(query_engine_wrapper.row_value(row, 'JSON')).decode()
                function_json = json.loads(json_string)
                result.append(function_json)
                sql_query_worked = True
                
            if len(result)==0:
                logging.info("teradata_analytic_lib: " +table_name+ " exists but no matching functions")
        
        except BaseException as e:
            logging.info("teradata_analytic_lib: " +table_name+ " does not exist! Falling back to JSON on filesystem", e)
            result = []
      

    if len(result)==0:
        # In this case VCT doesnt exist, so use JSONs on filesystem with the appropriate version and function name
        logging.info("teradata_analytic_lib: fallback_directory=", fallback_directory)
        for filename in os.listdir(fallback_directory):
            if not filename.endswith(".json"):
                continue 
            file_name = os.path.join(fallback_directory, filename)
            if not os.path.isfile(file_name):
                raise IOError
            with open(file_name) as f:
              result.append(json.load(f))

    return result, sql_query_worked
