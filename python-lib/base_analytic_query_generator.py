# -*- coding: utf-8 -*-
"""This file generates the SQL query string based on the parsed JSON inputs from OpenEndedQueryGenerator. Modified from teradataml's 
AnalyticQueryGenerator to now be completely independent code."""

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
from collections import OrderedDict
import logging


class BaseAnalyticQueryGenerator():
    '''
    This class creates a SQL-MR object, which can be used to generate
    SQL-MR/Analytical query in FFE syntax for Teradata.
    New arguments: (1) func_alias_name, (2) configure_column_casesensitive_handler, (3) exec_input_node 
    in order to make the base code generic and not rely on imports from teradataml.
    '''
    def __init__(self, func_alias_name, function_name, func_input_arg_sql_names, func_input_table_view_query, func_input_dataframe_type,
                 func_input_distribution, func_input_partition_by_cols, func_input_order_by_cols,
                 func_other_arg_sql_names, func_other_args_values, func_other_arg_json_datatypes,
                 func_output_args_sql_names, func_output_args_values, func_type="FFE",
                 engine="ENGINE_ML", configure_column_casesensitive_handler=True, exec_input_node=None, verbose=False):
        """
        AnalyticalQueryGenerator constructor, to create a map-reduce object, for
        SQL-MR/Analytical query generation.

        @param func_alias_name: Required Argument. Specifies the alias name of the function.

        @param function_name: Required Argument. Specifies the name of the function.

        @param func_input_arg_sql_names: Required Argument. Specifies the list of input SQL Argument names.

        @param func_input_table_view_query: Required Argument. Specifies the list of input argument values, with
            respect to 'func_input_arg_sql_names' which contains table_name or SQL (Select query).

        @param func_input_dataframe_type: Required Argument. Specifies the list of dataframe types for each input.
            Values can be "TABLE" or "QUERY".

        @param func_input_distribution: Required Argument. Specifies the list containing distributions for each
            input. Values can be "FACT", "DIMENSION", "NONE".

        @param func_input_partition_by_cols: Required Argument. Specifes the list containing partition columns for
            each input, if distribution is FACT.

        @param func_input_order_by_cols: Required Argument. Specifies the list of values, for each input, to be
            used order by clause.

        @param func_other_arg_sql_names: Required Argument. Specifies the list of other function arguments SQL name.

        @param func_other_args_values: Required Argument. Specifies the list of other function argument values,
            with respect to each member in 'func_other_arg_sql_names'.

        @param func_other_arg_json_datatypes: Required Argument. Specifies the list of JSON datatypes for each member in
            'func_other_arg_sql_names'.

        @param func_output_args_sql_names: Required Argument. Specifies the list of output SQL argument names.

        @param func_output_args_values: Required Argument. Specifies the list of output table names for each
            output table argument in 'func_output_args_sql_names'.

        @param func_type: Required Argument. Fixed value 'FFE'. Kept for future purpose, to generate different syntaxes.

        @param engine: Optional Argument. Specifies the type of engine. Default Value : ENGINE_ML 
            Permitted Values : ENGINE_ML, ENGINE_SQL

        @param configure_column_casesensitive_handler: Optional Argument. Specifies the configure column's case sensitive value. 
            Default Value : True - Kept to be used only by teradataml.

        @param exec_input_node: Optional Argument. Specifies a function that executes non “Lazy” input Data Frames
             Default Value: None - Kept to be used only by teradataml.

        @return: AnalyticalQueryGenerator object. (We can call this as map-reduce object)

        """

        self.__verbose = verbose

        if self.__verbose:
            print("teradata_analytic_lib--------------------------------")
            print("Input toAnalyticQueryGenerator")
            print("func_alias_name=", func_alias_name)
            print("configure_column_casesensitive_handler=", configure_column_casesensitive_handler)
            print("exec_input_node=", exec_input_node)
            print("SKS: function_name=", function_name)
            print("func_input_arg_sql_names=", func_input_arg_sql_names)
            print("func_input_table_view_query=", func_input_table_view_query)
            print("func_input_dataframe_type=", func_input_dataframe_type)
            print("func_input_distribution=", func_input_distribution)
            print("func_input_partition_by_cols=", func_input_partition_by_cols)
            print("func_input_order_by_cols=", func_input_order_by_cols)
            print("func_other_arg_sql_names=", func_other_arg_sql_names)
            print("func_other_args_values=", func_other_args_values)
            print("func_other_arg_json_datatypes=", func_other_arg_json_datatypes)
            print("func_output_args_sql_names=", func_output_args_sql_names)
            print("func_output_args_values=", func_output_args_values)
            print("func_type=", func_type)
            print("engine=", engine)
            print("teradata_analytic_lib--------------------------------")


        self.__engine = engine
        self.__configure_column_casesensitive_handler = configure_column_casesensitive_handler
        self.__exec_input_node = exec_input_node
        self.__function_name = func_alias_name
        self.__func_input_arg_sql_names = func_input_arg_sql_names
        self.__func_input_table_view_query = func_input_table_view_query
        self.__func_input_dataframe_type = func_input_dataframe_type
        self.__func_input_distribution = func_input_distribution
        self.__func_input_partition_by_cols = func_input_partition_by_cols
        self.__func_input_order_by_cols = func_input_order_by_cols
        self.__func_other_arg_sql_names = func_other_arg_sql_names
        self.__func_other_args_values = func_other_args_values
        self.__func_other_arg_json_datatypes = func_other_arg_json_datatypes
        self.__func_output_args_sql_names = func_output_args_sql_names
        self.__func_output_args_values = func_output_args_values
        self.__func_type = func_type
        self.__SELECT_STMT_FMT = "SELECT * FROM {} as sqlmr"
        self.__QUERY_SIZE = self.__get_string_size(self.__SELECT_STMT_FMT) + 20
        self.__input_arg_clause_lengths = []
        self._multi_query_input_nodes = []

    def __process_for_teradata_keyword(self, keyword):
        """
        Internal function to process Teradata Reserved keywords.
        If keyword is in list of Teradata Reserved keywords, then it'll be quoted in double quotes "keyword".

        @param keyword: A string to check whether it belongs to Teradata Reserved Keywords or not.

        @return: quoted string, if keyword is one of the Teradata Reserved Keyword, else str as is.

        @see:
        # Passing non-reserved returns "xyz" as is.

        keyword = self.__process_for_teradata_keyword("xyz")
        
        print(keyword)
        
        # Passing reserved str returns double-quoted str, i.e., "\"threshold\"".
        
        keyword = self.__process_for_teradata_keyword("threshold")
        
        print(keyword)

        """
        TERADATA_RESERVED_WORDS = ["INPUT", "THRESHOLD", "CHECK", "SUMMARY", "HASH", "METHOD"]
        if keyword.upper() in TERADATA_RESERVED_WORDS:
            if self.__verbose:
                print("teradata_analytic_lib: ", "keyword=", keyword, "_quote_arg", self._quote_arg(keyword, "\"", False))
            return self._quote_arg(keyword, "\"", False)
        else:
            return keyword

    def __generate_sqlmr_func_other_arg_sql(self):
        """
        Private function to generate a SQL clause for other function arguments.
        For Example, Step("False"), Family("BINOMIAL")

        @return: SQL string for other function arguments, as shown in example here.

        @see:
        __func_other_arg_sql_names = ["Step", "Family"]

        __func_other_args_values = ["False", "BINOMIAL"]

        other_arg_sql = self.__generate_sqlmr_func_other_arg_sql()

        # Output is as shown in example in description.

        """
        args_sql_str = ""
        for index in range(len(self.__func_other_arg_sql_names)):
            args_sql_str = "{0}\n\t{1}({2})".format(args_sql_str,
                                                    self.__process_for_teradata_keyword(
                                                        self.__func_other_arg_sql_names[index]),
                                                    self.__func_other_args_values[index])

        self.__QUERY_SIZE = self.__QUERY_SIZE + self.__get_string_size(args_sql_str)
        return args_sql_str

    def __generate_sqlmr_input_arg_sql(self, table_ref, table_ref_type, alias=None):
        """
        Private function to generate a ON clause for input function arguments.
        For Example, ON table_name AS InputTable
        For Exampple, ON (select * from table) AS InputTable

        @param table_ref: Table name or query, to be used as input.
        @param table_ref_type: Type of data frame.
        @param alias: Alias to be used for input.

        @return: ON clause SQL string for input function arguments, as shown in example here.

        @see:
        other_arg_sql = self.__generate_sqlmr_input_arg_sql("table_name", "TABLE", "InputTable")
        # Output is as shown in example in description.

        """
        returnSql = "\n\tON"
        if table_ref_type == "TABLE":
            returnSql = "{0} {1}".format(returnSql, table_ref)
        elif table_ref_type == "QUERY":
            returnSql = "{0} ({1})".format(returnSql, table_ref)
        else:
            #TODO raise # Error
            ""

        if alias is not None:
            returnSql = "{0} AS {1}".format(returnSql, self.__process_for_teradata_keyword(alias))

        return returnSql

    def __generate_sqlmr_output_arg_sql(self):
        """
        Private function to generate a SQL clause for output function arguments.
        For Example, OUT TABLE OutputTable("out_table_1")
        For Example, OUT TABLE CoefficientsTable("out_table_2")

        @return: SQL string for output function arguments, as shown in example here.

        @see:
        __func_output_args_sql_names = ["OutputTable", "CoefficientsTable"]

        __func_output_args_values = ["out_table_1", "out_table_2"]

        other_arg_sql = self.__generate_sqlmr_output_arg_sql()

        # Output is as shown in example in description.

        """
        args_sql_str = ""
        for index in range(len(self.__func_output_args_sql_names)):
            if self.__func_output_args_values[index] is not None:
                args_sql_str = "{0}\n\tOUT TABLE {1}({2})".format(args_sql_str,
                                                                  self.__process_for_teradata_keyword(
                                                                      self.__func_output_args_sql_names[index]),
                                                                  self.__func_output_args_values[index])

        self.__QUERY_SIZE = self.__QUERY_SIZE + self.__get_string_size(args_sql_str)
        return args_sql_str

    def _gen_sqlmr_select_stmt_sql(self):
        """
        Protected function to generate complete analytical query.
        For Example: SELECT * FROM GLM(input_arguments_clause output_arguments_clause USING other_arguments_clause ) as sqlmr

        @return: A SQL-MR/Analytical query, as shown in example here.

        @see:
        aqg_obj = AnalyticQueryGenerator(self.function_name, self.input_sql_args, self.input_table_qry,
        self.input_df_type,
        self.input_distribution, self.input_partition_columns,
        self.input_order_columns,
        self.other_sql_args, self.other_args_val, [], self.output_sql_args,
        self.output_args_val)

        anly_query = aqg_obj._gen_sqlmr_select_stmt_sql()

        # Output is as shown in example in description.

        """
        return self.__SELECT_STMT_FMT.format(self._gen_sqlmr_invocation_sql())

    def _gen_sqlmr_invocation_sql(self):
        """
        Protected function to generate a part of analytical query, to be used for map-reduce functions.
        For Example: GLM(input_arguments_clause output_arguments_clause USING other_arguments_clause)

        @return: A SQL-MR/Analytical query, as shown in example here.


        @see:
        aqg_obj = AnalyticQueryGenerator(self.function_name, self.input_sql_args, self.input_table_qry,
        self.input_df_type,
        self.input_distribution, self.input_partition_columns,
        self.input_order_columns,
        self.other_sql_args, self.other_args_val, [], self.output_sql_args,
        self.output_args_val)

        anly_query = aqg_obj._gen_sqlmr_invocation_sql()
        # Output is as shown in example in description.

        """
        self.__OUTPUT_ARG_CLAUSE = self.__generate_sqlmr_output_arg_sql()
        self.__OTHER_ARG_CLAUSE = self.__generate_sqlmr_func_other_arg_sql()
        self.__INPUT_ARG_CLAUSE = self.__single_complete_table_ref_clause()
        invocation_sql = "{0}({1}{2}".format(self.__function_name, self.__INPUT_ARG_CLAUSE, self.__OUTPUT_ARG_CLAUSE)

        if len(self.__func_other_arg_sql_names) != 0:
            invocation_sql = "{0}\n\tUSING{1}".format(invocation_sql, self.__OTHER_ARG_CLAUSE)

        invocation_sql = invocation_sql + "\n)"

        return invocation_sql

    def __single_complete_table_ref_clause(self):
        """
        Private function to generate complete ON clause for input function arguments, including
        partition by and order by clause, if any.
        For Example, ON table_name AS InputTable1 Partition By col1 Order By col2
        For Example, ON (select * from table) AS InputTable2 DIMENSION

        @return: Complete input argument clause, SQL string for input function arguments, as shown in example here.

        @see:
        __func_input_arg_sql_names = ["InputTable1", "InputTable2"]

        __func_input_table_view_query = ["table_name", "select * from table"]

        __func_input_dataframe_type = ["TABLE", "QUERY"]

        __func_input_distribution = ["FACT", "DIMENSION"]

        __func_input_partition_by_cols = ["col1", "NA_character_"]

        __func_input_order_by_cols = ["col2", "NA_character_"]

        other_arg_sql = self.__single_complete_table_ref_clause()

        # Output is as shown in example in description.

        """
        on_clause_dict = OrderedDict()
        args_sql_str = []
        # Let's iterate over the input arguments to the analytic functions.
        # Gather all the information provided by the wrapper.
        for index in range(len(self.__func_input_arg_sql_names)):
            # Get table reference. This contains following information:
            #   table name or view name OR
            #   A list of [view_name, query, node_query_type, node_id] gathered from
            #   'aed_exec_query_output' for the input node.
            table_ref = self.__func_input_table_view_query[index]
            # Get the table reference type, which is, either "TABLE" or "QUERY"
            table_ref_type = self.__func_input_dataframe_type[index]
            # Input argument alias
            alias = self.__func_input_arg_sql_names[index]
            # Partition information
            distribution = self.__func_input_distribution[index]
            partition_col = self.__func_input_partition_by_cols[index]
            # Order clause information
            order_col = self.__func_input_order_by_cols[index]

            # Get the Partition clause for the input argument.
            partition_clause = self.__gen_sqlmr_input_partition_clause(distribution, partition_col)
            # Get the Order clause for the input argument.
            order_clause = self.__gen_sqlmr_input_order_clause(order_col)

            if table_ref_type == "TABLE":
                # If table reference type is "TABLE", then let's use the table name in the query.
                on_clause = self.__generate_sqlmr_input_arg_sql(table_ref, table_ref_type, alias)
                on_clause_str = "{0}{1}{2}".format(on_clause, partition_clause, order_clause)
                args_sql_str.append(on_clause_str)
                # Update the length of the PARTITION clause.
                self.__QUERY_SIZE = self.__QUERY_SIZE + self.__get_string_size(on_clause_str)
            else:
                # Store the input argument information for the inputs, which will use query as input.
                on_clause_dict[index] = {}
                on_clause_dict[index]["PARTITION_CLAUSE"] = partition_clause
                on_clause_dict[index]["ORDER_CLAUSE"] = order_clause
                on_clause_dict[index]["ON_TABLE"] = self.__generate_sqlmr_input_arg_sql(table_ref[0], "TABLE", alias)
                on_clause_dict[index]["ON_QRY"] = self.__generate_sqlmr_input_arg_sql(table_ref[1], "QUERY", alias)
                on_clause_dict[index]["QRY_TYPE"] = table_ref[2]
                on_clause_dict[index]["NODEID"] = table_ref[3]
                on_clause_dict[index]["LAZY"] = table_ref[4]
                # If input node results in returning multiple queries save that input node
                # in '_multi_query_input_nodes' list.
                if table_ref[5]:
                    self._multi_query_input_nodes.append(table_ref[3])

        # Process OrderedDict to generate input argument clause.
        for key in on_clause_dict.keys():
            # 31000 is maximum query length supported in ON clause
            if self.__QUERY_SIZE + self.__get_string_size(on_clause_dict[key]["ON_QRY"]) <= 31000:
                on_clause_str = "{0}{1}{2}".format(on_clause_dict[key]["ON_QRY"],
                                                   on_clause_dict[key]["PARTITION_CLAUSE"],
                                                   on_clause_dict[key]["ORDER_CLAUSE"])
            else:
                # We are here means query maximum size will be exceeded here.
                # So let's add the input node to multi-query input node list, as
                # we would like execute this node as well as part of the execution.
                # Add it in the list, if we have not done it already.
                if on_clause_dict[key]["NODEID"] not in self._multi_query_input_nodes:
                    self._multi_query_input_nodes.append(on_clause_dict[key]["NODEID"])

                # Use the table name/view name in the on clause.
                on_clause_str = "{0}{1}{2}".format(on_clause_dict[key]["ON_TABLE"],
                                                   on_clause_dict[key]["PARTITION_CLAUSE"],
                                                   on_clause_dict[key]["ORDER_CLAUSE"])

                # Execute input node here, if function is not lazy.
                if not on_clause_dict[key]["LAZY"] and __exec_input_node != None:
                    __exec_input_node(on_clause_dict[key]["NODEID"])
                #    DataFrameUtils._execute_node_return_db_object_name(on_clause_dict[key]["NODEID"])

            args_sql_str.append(on_clause_str)

            # Add the length of the ON clause.
            self.__QUERY_SIZE = self.__QUERY_SIZE + self.__get_string_size(on_clause_str)

        return " ".join(args_sql_str)

    def __gen_sqlmr_input_order_clause(self, column_order):
        """
        Private function to generate complete order by clause for input function arguments.
        For Example, Order By col2

        @param column_order: Column to be used in ORDER BY clause. If this is "NA_character_" no ORDER BY clause is generated.

        @return: Order By clause, as shown in example here.

        @see:
        other_arg_sql = self.__gen_sqlmr_input_order_clause("col2")

        # Output is as shown in example in description.

        """
        if column_order == "NA_character_" or column_order is None:
          return ""
        args_sql_str = "\n\tORDER BY {}".format(column_order)

        # Get the length of the ORDER clause.
        self.__QUERY_SIZE = self.__QUERY_SIZE + self.__get_string_size(args_sql_str)
        return args_sql_str

    def __gen_sqlmr_input_partition_clause(self, distribution, column):
        """
        Private function to generate PARTITION BY or DIMENSION clause for input function arguments.
        For Example, Partition By col1
        For Example, DIMENSION

        @param distribution: Type of clause to be generated. Values accepted here are: FACT, DIMENSION, NONE
        @param column: Column to be used in PARTITION BY clause, when distribution is "FACT"

        @return: Partition clause, based on the type of distribution:
        When "FACT" - PARTITION BY clause is generated.
        When "DIMENSION" - DIMENSION cluase is generated.
        When "NONE" - No clause is generated, an empty string is returned.

        @see:
        other_arg_sql = self.__gen_sqlmr_input_partition_clause("FACT", "col1")

        # Output is as shown in example in description.

        """
        if distribution == "FACT" and column is not None:
            args_sql_str = "\n\tPARTITION BY {0}".format(column)
        elif distribution == "DIMENSION":
            args_sql_str = "\n\tDIMENSION"
        elif distribution == "NONE":
            return ""
        else:
            return ""
            # TODO raise error "invalid distribution type"

        # Get the length of the PARTITION clause.
        self.__QUERY_SIZE = self.__QUERY_SIZE + self.__get_string_size(args_sql_str)
        return args_sql_str




    def __get_string_size(self, string):
        return len(string.encode("utf8"))



    def _quote_arg(self, args, quote="'", call_from_wrapper=True):
        """
        Function to quote argument value.

        @param quote:  Argument to be quoted. (default "")
        @param call_from_wrapper:  Type of quote to be used for quoting. Default is single quote ('). (default True)
        
        @return: Argument with quotes as a string.

        @see:
        When a call is being made from wrapper: UtilFuncs._quote_arg(family, "'")

        When a call is being made from non-wrapper function. UtilFuncs._quote_arg(family, "'", False)
        """


        if call_from_wrapper and not __configure_column_casesensitive_handler:
            quote = ""
            return args

        # Returning same string if it already quoted. Applicable only for strings.
        if isinstance(args, str) and args.startswith(quote) and args.endswith(quote):
            return args
        if args is None:
            return None
        if isinstance(args, list):
            return ["{0}{1}{0}".format(quote, arg) for arg in args]

        return "{0}{1}{0}".format(quote, args)

