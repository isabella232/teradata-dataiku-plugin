# -*- coding: utf-8 -*-
"""Abstract code for the engine in order to keep the main code independent. This wrapper has all the methods that are specific to the application it is used for."""

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

class QueryEngineWrapper:

    def execute(self, query_string):
        """
        A method that must be used in all wrappers, it has the specific implementation for execute.
        This function takes in a query string and outputs the query results.   

        @param query_string: A variable that represents the query string used to access the necessary
            from the Vantage Capability Table.
        @type query_string: String.

        @return: This function returns the results of executing a query string.
        """ 
        raise Exception("NotImplementedException")

    def iteratable(self, result):
        """
        A method that must be used in all wrappers, it has the specific implementation for iteration.
        This function takes in a string (the query result) and outputs it as an iterable object.   

        @param result: A variable that represents the iterable object for each row of the query results
            from the Vantage Capability Table.
        @type result: Object.

        @return: This function returns an iterable object where each row represents a query result.
        """         
        raise Exception("NotImplementedException")

    def row_value(self, row, column_name):
        """
        A method that must be used in all wrappers, it has the specific implementation for accessing the row's value.
        This function takes in the row (the query result) and a column name and outputs the column name value for that given row.   

        @param row: A variable that represents the each row of the query results
            from the Vantage Capability Table.
        @type row: Object.

        @param column_name: A variable that represents the column name
            from the Vantage Capability Table (where you want results from).
        @type column_name: String.

        @return: This function returns the column name value for the row of the query result.
        """ 
        raise Exception("NotImplementedException")




