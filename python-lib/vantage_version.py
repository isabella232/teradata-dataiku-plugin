# -*- coding: utf-8 -*-
"""This file is for accessing the Vantage Version i.e. the Vantage Capability Table does not exist, 
so we use the fallback of loading the JSONs. However, we want to have all the different versions accounted for so that 
the correct JSON is used."""

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

from query_engine_wrapper import QueryEngineWrapper
import logging

def get_vantage_version(query_engine_wrapper):
    """
    This function is used to get the correct Vantage version. 

    @param query_engine_wrapper: See query_engine_wrapper.py file. The query_engine_wrapper must have an execute function which will
        be used to execute a query_string (SQL query to get the necessary version information from the pm table). 
        It must also have iteratable and row_value functions which will be used to iterate over each row of the query results.
    @type query_engine_wrapper: QueryEngineWrapper class.

    @return: This function returns the cleaned Vantage Version.
    """ 

    assert isinstance(query_engine_wrapper, QueryEngineWrapper)==True, "Error argument to query_engine_wrapper must be an instance of QueryEngineWrapper"

    vantage_version = None

    # SKS create query where you get back vantage version
    query_string = "SELECT InfoData FROM pm.versionInfo WHERE InfoKey = 'RELEASE' (NOT CASESPECIFIC)"
    # SKS print query
    logging.info("teradata_analytic_lib: SQL Version Query", query_string)

    # SKS execute query and recieve panda result
    query_results = None
    try:
        query_results = query_engine_wrapper.execute(query_string)
   
        # SKS loop once: for each JSON column of row, 
        # In theory only one row exists which is the InfoData we care about
        for row in query_engine_wrapper.iteratable(query_results):
            vantage_version = query_engine_wrapper.row_value(row, "InfoData")
            logging.info("teradata_analytic_lib: the pm.versionInfo table returns", vantage_version)
            break
    except:
        logging.info("teradata_analytic_lib: get_vantage_version exception")


    if vantage_version is None:
        vantage_version = "vantage1.3" # TODO: Should this be 1.0 or 1.3
    elif "vantage 1.1" in vantage_version.lower().replace(" ", ""):
        vantage_version = "vantage1.1"
    elif "mlengine9.0" in vantage_version.lower().replace(" ", ""):
        vantage_version = "vantage1.3"
    elif "mlengine08.10" in vantage_version.lower().replace(" ", ""):
        vantage_version = "vantage2.0"
    else:
        vantage_version = "vantage1.3"  # TODO: Should this be 1.0 or 1.3

    logging.info("teradata_analytic_lib: Vantage version number", vantage_version)

    return vantage_version
    

