# -*- coding: utf-8 -*-
import os
import sys
import json
import dataiku
from dataiku.customrecipe import get_input_names_for_role, get_output_names_for_role, get_recipe_config

def get_input_output(has_model_as_second_input=False):

    if has_model_as_second_input:
        if len(get_input_names_for_role('model')) == 0:
            raise ValueError('No input model.')
        model_name = get_input_names_for_role('model')[0]
        model = dataiku.Model(model_name)
        return (model)
    else:
        if len(get_input_names_for_role('original')) == 0:
            raise ValueError('No original dataset.')

        original_dataset_name = get_input_names_for_role('original')[0]
        original_dataset = dataiku.Dataset(original_dataset_name)
        return (original_dataset)
