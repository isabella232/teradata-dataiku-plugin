# -*- coding: utf-8 -*-
"""This file takes in Teradata's Analytic Function JSON and outputs three things. It outputs a HTML, JavaScript, and JSON file
that are all automatically generated."""

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
import sys

_script_dir = os.path.dirname(__file__) 



def generate(full_function_name, function_json):
    """
    This function takes the inputted function name and analytic function JSON and outputs the HTML, JavaScript, 
    and JSON (JSON is used as input to OpenEndedQueryGenerator). These are all fully automated through this custom python script.

    @param full_function_name: A variable that represents the full function name; based off which function name is 
        requested, the appropriate HTML, JavaScript, and JSON are created.
    @type full_function_name: String.

    @param function_json: The inputted Teradata Analytic Function JSON that is used to parse the JSON and create the 
        appropriate HTML, JavaScript, and JSON.
    @type function_json: JSON.

    @return: This function returns the HTML, JavaScript, and JSON for the analytic function requested.
    """ 
    return _generate_html(full_function_name, function_json), _generate_js(full_function_name, function_json), _generate_json(full_function_name, function_json)


# generate html
def _generate_html(full_function_name, function_json):
    function_name = full_function_name.lower()

    # HTML, Javascript output
    with open(os.path.join(os.path.join(_script_dir, "templates"), "template.html"), "r") as f:
        html_template = f.read()
    
    # HTML Iterate input tables
    num_row_items = 0
    identifier_names = {}
    columns_list = {}
    index =0
    html_tables = ""
    req_or_optl = ""
    html_tables += ('<div class="row mt-3">\n') # first row
    for table in function_json['input_tables']:
        description = table['description'] if 'description' in table else ""
        description = description.replace('"', "'")
        table_name = table['name']
        identifier = function_name + "_" + table_name
        if 'isRequired' in table and table['isRequired'] == True:
            req_or_optl = 'required'
        elif 'isRequired' in table and table['isRequired'] == False:
            req_or_optl = 'optional'
        else:
            req_or_optl = 'required'
        # Ensure that we only allow unique identifiers
        if identifier in identifier_names:
            suffix_index = 2
            while True:
                identifier = function_name + "_" + table_name + "_" + str(suffix_index)
                if identifier not in identifier_names:
                    break
                suffix_index += 1
        identifier_names[identifier] = True
        html_tables += ('<div class="col '+req_or_optl+'">\n')
        html_tables += ('\t\t<label for="' + identifier + '" class="col-form-label" data-toggle="tooltip" data-container="body" data-placement="top" title="'+description+'" >'+table_name.title()+':</label>\n')
        html_tables += ('\t\t<input id="' + identifier + '" type="text" placeholder="Enter Input Table Name..." value="" class="form-control database-control" list="databases" >\n')
        html_tables += ('</div>\n')
        
        columns_list[table_name] = "dbcolumns_" + identifier

        if len(table['requiredInputKind']) > 0 and table['requiredInputKind'][0] == "PartitionByKey":
            html_tables += ('<div class="col '+req_or_optl+'">\n')
            html_tables += ('\t\t<label for="' + identifier + '_partitionby" class="col-form-label">Partition By:</label>\n')
            html_tables += ('\t\t<input id="' + identifier + '_partitionby" type="text" placeholder="Enter Column Name..." value="" class="form-control" list="' + columns_list[table_name] + '">\n')
            html_tables += ('</div>\n')

        html_tables += ('<div class="col '+req_or_optl+'">\n')
        html_tables += ('\t\t<label for="' + identifier + '_orderby" class="col-form-label">Order By:</label>\n')
        html_tables += ('\t\t<input id="' + identifier + '_orderby" type="text" placeholder="Enter Column Name..." value="" class="form-control" list="' + columns_list[table_name] + '">\n')
        html_tables += ('</div>\n')
       
        html_tables += ('<div class="col '+req_or_optl+'">\n')
        html_tables += ('\t\t<label for="' + identifier + '_orderdirection" class="col-form-label">Order Direction:</label>\n')
        html_tables += ('\t\t<select class="form-select form-control default_select" id="' + identifier +'_orderdirection" >\n')
        html_tables += ('\t\t\t<option selected value="" class="default_option">ASC</option>\n')
        html_tables += ('\t\t\t<option value="DESC">DESC</option>\n')
        html_tables += ('\t\t</select>\n')
        html_tables += ('</div>\n')


        html_tables += ('</div>\n') # end row
        html_tables += ('<div class="row mt-3">\n') # start new row

        index += 1 

    html_tables += ('</div>\n') # end row


    # HTML Iterate argument clauses
    num_row_items = 0
    html_args = ""
    req_or_optl = ""
    html_args += ('<div class="row mt-3">\n') # first row
    if 'argument_clauses' in function_json:
        for argument in function_json['argument_clauses']:
            identifier = function_name + "_" + argument['name']
            defaultValue = str(argument['defaultValue']) if 'defaultValue' in argument else ""
            description = argument['description'] if 'description' in argument else ""
            description = description.replace('"', "'")

            if 'isRequired' in argument and argument['isRequired'] == True:
                req_or_optl = 'required'
            elif 'isRequired' in argument and argument['isRequired'] == False:
                req_or_optl = 'optional'
            else:
                req_or_optl = 'required'

            if argument['datatype'] == 'BOOLEAN':
                html_args += ('<div class="col '+req_or_optl+'">\n')
                value = defaultValue
                html_args += ('\t<label for="' + identifier + '" class="col-form-label"  data-toggle="tooltip" data-container="body" data-placement="top" title="'+description+'" >'+argument['name']+':</label>\n')
                html_args += ('\t<select class="form-select form-control default_select" id="' + identifier + '"  >\n')
                if value==True:
                    html_args += ('\t\t<option value="False">False</option>\n')
                    html_args += ('\t\t<option selected class="default_option" value="True">True</option>\n')
                else:
                    html_args += ('\t\t<option selected class="default_option" value="False">False</option>\n')
                    html_args += ('\t\t<option value="True">True</option>\n')
                html_args += ('\t</select>\n')
                html_args += ('</div>\n')            
                num_row_items += 1

            elif argument['datatype'] =='DOUBLE PRECISION' or argument['datatype'] =='INTEGER':
                html_args += ('<div class="col '+req_or_optl+'">\n')
                min_value = str(argument['lowerBound'] if 'lowerBound' in argument else "")
                max_value = str(argument['upperBound'] if 'upperBound' in argument else "")
                if 'upperBound' in argument and 'lowerBound' in argument and argument['upperBound'] < 10:
                    step_value = str((argument['upperBound']-argument['lowerBound'])/100.0)
                else:
                    step_value = '1'
                html_args += ('\t<label for="' + identifier + '" class="col-form-label"  data-container="body"  data-toggle="tooltip" data-placement="top" title="'+description+'">'+argument['name']+':</label>\n')
                html_args += ('\t<input type="number"  placeholder="' +defaultValue+ '" min="'+min_value+'" max="'+max_value+'" step="'+step_value+'" id="'+identifier+'" name="'+argument['name']+'" value="'+defaultValue+'" \n\t data-bind="value:replyNumber" class="form-control numeric" >\n')
                html_args += ('</div>\n')
                num_row_items += 1

            elif (argument['datatype'] == 'STRING') and ('permittedValues' in argument) and (argument['permittedValues'] != []):
                html_args += ('<div class="col '+req_or_optl+'">\n')
                html_args += ('\t<label for="' + identifier + '" class="col-form-label"  data-container="body"  data-toggle="tooltip" data-placement="top" title="'+description+'">'+argument['name']+':</label>\n')
                html_args += ('\t<select class="form-select form-control default_select" id="' + identifier + '" >\n')
                if defaultValue == "":
                    defaultValue = argument['permittedValues'][0] # use the first option if there is no default
                for option in argument['permittedValues']:
                    if defaultValue == option:
                        html_args += ('\t\t<option selected value="' + option + '" class="default_option" >' + option + '</option>\n')
                    else:
                        html_args += ('\t\t<option value="' + option + '">' + option + '</option>\n')
                html_args += ('\t</select>\n')
                html_args += ('</div>\n')
                num_row_items += 1

            elif (argument['datatype'] == 'STRING'):
                html_args += ('<div class="col '+req_or_optl+'">\n')
                html_args += ('\t<label for="' + identifier + '" class="col-form-label"  data-container="body"  data-toggle="tooltip" data-placement="top" title="'+description+'">'+argument['name']+':</label>\n')
                html_args += ('\t<input id="' + identifier + '" type="text" placeholder="' +defaultValue+ '" class="form-control" >\n')
                html_args += ('</div>\n')
                num_row_items += 1

            elif (argument['datatype'] == 'COLUMNS'):
                html_args += ('<div class="col '+req_or_optl+'">\n')
                list_name = ""
                if 'targetTable' in argument and len(argument['targetTable']) > 0 and argument['targetTable'][0] in columns_list:
                    list_name = columns_list[argument['targetTable'][0]]
                html_args += ('\t<label for="' + identifier + '" class="col-form-label" data-container="body"  data-toggle="tooltip" data-placement="top" title="'+description+'">'+argument['name']+':</label>\n')
                html_args += ('\t<input id="' + identifier + '" type="text" placeholder="Enter Column Name..." value="' +defaultValue+ '" class="form-control" list="'+list_name+'">\n')
                html_args += ('</div>\n')
                num_row_items += 1


            if num_row_items >= 5:
                num_row_items = 0
                html_args += ('</div>\n') # end row
                html_args += ('<div class="row mt-3">\n') # start new row


    # Fill the last row so that it has 5 items in it
    for _ in range(5-num_row_items):
        html_args += ('<div class="col">\n') 
        html_args += ('</div>\n') 

    html_args += ('</div>\n') # end row

    # SQL Clauses
    html_sqlclauses = ""
    html_sqlclauses += ('<div class="row mt-3">\n')

    html_sqlclauses += ('<div class="col required">\n')
    html_sqlclauses += ('\t<label for="' + function_name + '_isCustomSelectClause" class="col-form-label">Customize Select Columns:</label>\n')
    html_sqlclauses += ('\t<select class="form-select form-control default_select" id="' + function_name + '_isCustomSelectClause">\n'  )              
    html_sqlclauses += ('\t\t<option selected value="False" class="default_option">False</option>\n')
    html_sqlclauses += ('\t\t<option value="True">True</option>\n')
    html_sqlclauses += ('\t</select>')
    html_sqlclauses += ('</div>\n')

    html_sqlclauses += ('<div class="col required">\n')
    html_sqlclauses += ('\t<label for="' + function_name + '_customSelectClause" class="col-form-label">Modify Select Columns of Output Query:</label>\n')
    html_sqlclauses += ('\t<input id="' + function_name + '_customSelectClause" type="text" value="*" class="form-control">\n')
    html_sqlclauses += ('</div>\n')

    html_sqlclauses += ('<div class="col required">\n')
    html_sqlclauses += ('\t<label for="' + function_name + '_additionalSQLClause" class="col-form-label" >Additional Clauses:</label>\n')
    html_sqlclauses += ('\t<input id="' + function_name + '_additionalSQLClause" placeholder="Enter Additional Clauses..." type="text" value="" class="form-control">\n')
    html_sqlclauses += ('</div>\n')


    html_sqlclauses += ('</div>\n')

    # Add Datalist
    for key in columns_list:
        value = columns_list[key]
        html_args += '<datalist id="'+value+'"></datalist>'
        

    # Tab all lines
    html_tables = html_tables.replace("\n", "\n\t\t\t\t")
    html_args = html_args.replace("\n", "\n\t\t\t\t")
    html_sqlclauses = html_sqlclauses.replace("\n", "\n\t\t\t\t")
    
    # Replace the template with contents
    html_output = html_template.replace("__HTML_TABLES__", html_tables)
    html_output = html_output.replace("__HTML_ARGS__", html_args)
    html_output = html_output.replace("__HTML_SQLCLAUSES__", html_sqlclauses)
    
    return html_output


# generate javascript
def _generate_js(full_function_name, function_json):
    function_name = full_function_name.lower()
    # Javascript, load template
    javascript_output = "";
    with open(os.path.join(os.path.join(_script_dir, "templates"), "template.js"), "r") as f:
        javascript_output = f.read()
    javascript_output = javascript_output.replace("__FUNCTION_NAME__", function_name)
    json2html = "\n"
    html2json = "\n"
    dbUpdateColumns = "\n"

    # Tables
    index =0
    identifier_names = {}
    for table in function_json['input_tables']:
        identifier = function_name + "_" + table['name']

        # Ensure that we only allow unique identifiers
        if identifier in identifier_names:
            suffix_index = 2
            while True:
                identifier = function_name + "_" + table['name'] + "_" + str(suffix_index)
                if identifier not in identifier_names:
                    break
                suffix_index += 1
        identifier_names[identifier] = True

        
        # Table
        json2html += '$( "#'+identifier+'" ).val(json["function"]["required_input"]['+str(index)+']["value"]);\n'
        json2html += '$( "#'+identifier+'_partitionby" ).val(json["function"]["required_input"]['+str(index)+']["partitionAttributes"][0]);\n'
        json2html += '$( "#'+identifier+'_orderby" ).val(json["function"]["required_input"]['+str(index)+']["orderByColumn"][0]);\n'
        json2html += '$( "#'+identifier+'_orderdirection" ).val(json["function"]["required_input"]['+str(index)+']["orderByColumnDirection"][0]);\n'
        
        # updateDatabaseColumns call 
        column_list_name = "dbcolumns_" + identifier
        json2html += 'updateDatabaseColumns("'+identifier+'", "'+column_list_name+'");\n'
        

        html2json += 'json["function"]["required_input"]['+str(index)+']["value"] = $( "#'+identifier+'" ).val();\n'
        html2json += 'json["function"]["required_input"]['+str(index)+']["partitionAttributes"][0] = $( "#'+identifier+'_partitionby" ).val();\n'
        html2json += 'json["function"]["required_input"]['+str(index)+']["orderByColumn"][0] = $( "#'+identifier+'_orderby" ).val();\n'
        html2json += 'json["function"]["required_input"]['+str(index)+']["orderByColumnDirection"][0] = $( "#'+identifier+'_orderdirection" ).val();\n'
        

        index += 1


    # Argument Clauses
    index = 0
    if 'argument_clauses' in function_json:
        for argument in function_json['argument_clauses']:
            identifier = function_name + "_" + argument['name']
            
            if argument['datatype'] == 'BOOLEAN':
                json2html += '$( "#'+identifier+'" ).val(json["function"]["arguments"]['+str(index)+']["value"]);\n'
                html2json += 'json["function"]["arguments"]['+str(index)+']["value"] = $( "#'+identifier+'" ).val();\n'

            elif argument['datatype'] =='DOUBLE PRECISION':
                json2html += '$( "#'+identifier+'" ).val(json["function"]["arguments"]['+str(index)+']["value"]);\n'
                html2json += 'json["function"]["arguments"]['+str(index)+']["value"] = parseFloat($( "#'+identifier+'" ).val());\n'

            elif argument['datatype'] =='INTEGER':
                json2html += '$( "#'+identifier+'" ).val(json["function"]["arguments"]['+str(index)+']["value"]);\n'
                html2json += 'json["function"]["arguments"]['+str(index)+']["value"] = parseInt($( "#'+identifier+'" ).val());\n'

            elif argument['datatype'] == 'STRING':
                json2html += '$( "#'+identifier+'" ).val(json["function"]["arguments"]['+str(index)+']["value"]);\n'
                html2json += 'json["function"]["arguments"]['+str(index)+']["value"] = $( "#'+identifier+'" ).val();\n'
            
            elif argument['datatype'] == 'COLUMNS':
                json2html += '$( "#'+identifier+'" ).val(json["function"]["arguments"]['+str(index)+']["value"][0]);\n'
                html2json += 'json["function"]["arguments"]['+str(index)+']["value"][0] = $( "#'+identifier+'" ).val();\n'

            index += 1

    # SQL Clauses
    json2html += '$( "#'+function_name+'_isCustomSelectClause" ).val(json["function"]["customSelectClause"] == true ? "True" : "False");\n'
    json2html += '$( "#'+function_name+'_customSelectClause" ).val(json["function"]["select_clause"]);\n'
    json2html += '$( "#'+function_name+'_additionalSQLClause" ).val(json["function"]["additionalSQLClause"][0]);\n'

    html2json += 'json["function"]["customSelectClause"] = ($( "#'+function_name+'_isCustomSelectClause" ).val()).toLowerCase()  == "true";\n'
    html2json += 'json["function"]["select_clause"] = $( "#'+function_name+'_customSelectClause" ).val();\n'
    html2json += 'json["function"]["additionalSQLClause"][0] = $( "#'+function_name+'_additionalSQLClause" ).val();\n'


    # Update the javascript
    javascript_output = javascript_output.replace("__JSON_2_HTML__", json2html.replace("\n", "\n\t\t\t"))
    javascript_output = javascript_output.replace("__HTML_2_JSON__", html2json.replace("\n", "\n\t\t"))
    javascript_output = javascript_output.replace("__DB_UPDATE_COLUMNS__", dbUpdateColumns.replace("\n", "\n\t\t\t\t"))

    return javascript_output


# generate json
def _generate_json(full_function_name, function_json):
    function_name = full_function_name.lower()
    # Output JSON
    json_output = {}
    json_output["function"] = {}
    json_output["function"]["function_alias_name"] = full_function_name
    json_output["function"]["name"] = full_function_name
    json_output["function"]["required_input"] = function_json["input_tables"]
    if 'argument_clauses' in function_json:
        json_output["function"]["arguments"] = function_json["argument_clauses"]
    else:
        json_output["function"]["arguments"] = {}
    for required_input in json_output["function"]["required_input"]:
        required_input["value"] = ""
        required_input["inputKindChoices"] = [ "PartitionByKey" ]
        # TODO: What to do when required_input["requiredInputKind"] has no entries?
        required_input["kind"] = required_input["requiredInputKind"][0] if len(required_input["requiredInputKind"])>0 else ""
        required_input["orderByColumn"] = [ "" ]
        required_input["partitionAttributes"] = [ "" ]
        required_input["orderByColumnDirection"] = [ "" ]
    for argument in json_output["function"]["arguments"]:
        if argument["datatype"] == "COLUMNS":
            argument["value"] = [""]
        elif argument["datatype"] == "BOOLEAN" and "defaultValue" in argument:
            if type(argument["defaultValue"] ) == str:
                argument["value"] = argument["defaultValue"] 
            else:
                argument["value"] = "True" if argument["defaultValue"] else "False"
        elif (argument['datatype'] == 'STRING') and ('permittedValues' in argument) and (argument['permittedValues'] != [])  and "defaultValue" in argument:
            argument["value"] = argument["defaultValue"] 
        else:
            argument["value"] = ""

    json_output["function"]["short_description"] = function_json["short_description"]
    json_output["function"]["long_description"] = function_json["long_description"]

    json_output["function"]["select_clause"] = "*"
    json_output["function"]["customSelectClause"] = False
    json_output["function"]["additionalSQLClause"] = [""]

    return json_output



def _save_files(output_dir, html_output, javascript_output, json_output):
    # Save HTML
    html_output_file = open(os.path.join(output_dir, function_name.lower()) + ".html", "w")
    html_output_file.write(html_output)
    html_output_file.close()

    # Save Javascript
    javascript_output_file = open(os.path.join(output_dir, function_name.lower() + ".js"), "w")
    javascript_output_file.write(javascript_output)
    javascript_output_file.close()

    # Save json output
    jsonString = json.dumps(json_output, indent=4)
    jsonFile = open(os.path.join(output_dir, function_name.lower() + ".json"), "w")
    jsonFile.write(jsonString)
    jsonFile.close()



if __name__ == "__main__":

    _output_dir = "../build"
    _file_name = "../versions/vantage2.0/MovingAverage.json" if len(sys.argv)==1 else str(sys.argv[1])
    with open(file_name) as f:
      _function_json = json.load(f)
    _function_name = os.path.basename(_file_name).replace(".json", "")
    _html_output, _javascript_output, _json_output = generate(_function_name, _function_json)
    _save_files(output_dir, _html_output, _javascript_output, _json_output)


