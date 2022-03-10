# -*- coding: utf-8 -*-
'''
Copyright © 2019 by Teradata.
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import dataiku
from dataiku import Dataset
from dataiku.customrecipe import *
from dataiku.core.sql import SQLExecutor2


def set_schema_from_vantage(outputTableName, output_dataset, executor, post_query, autocommit, pre_query):
    # Write the schema to the output table
    # Types Documentation: 
    # https://docs.teradata.com/r/rgAb27O_xRmMVc_aQq2VGw/6CYL2QcAvXykzEc8mG__Xg
    # https://www.tutorialspoint.com/teradata/teradata_data_types.htm
    help_query = 'help table ' + outputTableName + ';'

    if not autocommit:
        executor.query_to_df(pre_query)
    help_results = executor.query_to_df(help_query, post_queries=post_query)
    column_names =  help_results["Column SQL Name"].tolist()
    column_types =  help_results["Type"].tolist()
    column_type_list = []
    mapping = {'I' : 'int', 'I8' : 'bigint', 'I1': 'tinyint', 'I2' : 'smallint', \
    'F' : 'float', 'D' : 'float', 'DA' : 'date', 'CV' : 'string', 'TS' : 'date', \
    'AN' : 'array', 'D' : 'float', 'F' : 'float'}
    for index in range(len(column_names)):
        # Why do we need to strip??
        column_name = column_names[index].strip('"')
        column_type = column_types[index].strip().upper()
        if column_type in mapping:
             column_type_list.append({'name' : column_name, 'type' : mapping[column_type] })
             print("Column name=", column_name, "type=", column_type, 'dataiku_type=', mapping[column_type])
        else:
            column_type_list.append({'name' : column_name, 'type' : 'string' })
            print("Column name=", column_name, "type=", column_type, 'dataiku_type=', 'string')
    print("column_type_list=", column_type_list)
    output_dataset.write_schema(column_type_list)