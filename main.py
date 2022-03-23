# -*- coding: utf-8 -*-
"""
Created on Mar 2022
@authors: Katerina Drakoulaki and Polykarpos Polykarpidis
github repo: https://github.com/PolykarposPolykarpidis/CompBMus_FAIR
"""

# import libraries 
import frictionless
from pprint import pprint


import os
my_list = os.listdir('dataset/')


# create a descriptor object for all .csv files, provide a title and more detailed description. 
package = frictionless.describe('dataset/*.csv')
package.title = 'MBn FAIR dataset'
package.description = 'This is the Making Byzantine Computational Musicology FAIR dataset. It contains the resources (datasets), package schema, and other metadata.'

#schema of the metadata 
schema = frictionless.describe_schema("dataset/"+my_list[0])

'''
editing the schema with information relevant to our dataset
we provide more detailed descriptions for variables, and set constraints on 
some of them, e.g. the variable 'pitches' cannot have null values. 

'''
schema.get_field("id").title = "Identifier"
schema.get_field("m/p").title = "martyria line or phrase line"
schema.get_field("m/p").description = "this variable is binary: either a characteristic of 'martyria' or 'phrase_line' can be attributed. See below on constraints."
schema.get_field("pitches").title = "comma separated string of pitches"
schema.get_field("pitches").description = "this field contains a list of pitches, not always one pitch for each cell"
schema.get_field("pitches").constraints["required"] = True
schema.get_field("m/p").constraints["required"] = True
schema.get_field("m/p").constraints["pattern"] = r'martyria|phrase_line'
schema.get_field("voiced_unit").title = "voiced unit identifier"
schema.get_field("intervals").title = "comma separated string of intervals"
schema.get_field("intervals").description = "this field contains a list of intervals, not always one interval for each cell"
schema.get_field("syl").title = "a syllable"
schema.get_field("syl_is_accented").title = "the syllable is accented"
schema.get_field("syl_is_continue").title = "the syllable continues to the next phrase line"
schema.get_field("syl_is_continue").description = "this field is used to provide information whether a syllable contains more than one Voiced unit"
schema.get_field("is_last_syl_word").title = "this syllable ends the word"
schema.get_field("Voiceless").title = "comma separated string of Voiceless identifiers"
schema.get_field("Voiceless").description = "this field includes Voiceless identifiers which refer to a Voiced unit of this phrase line. It contains a list of identifiers, not always one identifier for each cell."
schema.get_field("Voiceless_continue").title = "comma separated string of Voiceless identifiers that continues to the next phrase line"
schema.get_field("Voiceless_continue").description = "this field includes Voiceless identifiers which refer to a Voiced unit which continues the grouping for the next phrase line. It contains a list of identifiers, not always one identifier for each cell."
schema.get_field("is_last_syllable_phrase").title = "this syllable ends the phrase"
schema.get_field("is_last_syllable_phrase").constraints["required"] = True
# export schema to a yaml file 

file_name_of_yaml_schema = "MBn_dataset.schema.yaml"
schema.to_yaml(file_name_of_yaml_schema)


#establish the same schema to each resource of the package ????? 
for each_resource in package.resources:
	each_resource.schema = file_name_of_yaml_schema

# export metadata for datapackage 

package.to_yaml("MBn_dataset.package.yaml")

'''
Validation checks
Validate: the dataset, the schema, and the package metadata 

'''

with open("MBn_dataset.package.yaml", 'a', encoding='utf-8') as f:
	f.write("""licenses:
- name: CC-BY-4.0
  path: https://creativecommons.org/licenses/by/4.0/
  title: Creative Commons Attribution 4.0
contributors:
- title: Katerina Drakoulaki
  email: Katerina.Drakoulaki@gmail.com
  role: author
- title: Polykarpos Polykarpidis
  email: polykarpospolykarpidis@gmail.com
  role: author
homepage: https://github.com/PolykarposPolykarpidis/CompBMus_FAIR""")

validation_report_schema = frictionless.validate('MBn_dataset.schema.yaml')
validation_report_package = frictionless.validate('MBn_dataset.package.yaml')
validation_report_dataset = frictionless.validate("dataset/*.csv")

	
pprint(validation_report_package.flatten(["rowPosition", "fieldPosition", "code", "message"]))











