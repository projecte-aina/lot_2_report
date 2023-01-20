#! /usr/bin/python3
import sys
import json
import jsonschema
from jsonschema import validate
import jsonlines
# usage validate_json.py file

# Expected json
nerSchema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "text": {
      "type": "string"
    },
    "id": {
      "type": "string"
    },
    "annos": {
      "type": "array",
      "items": [
        {
          "type": "object",
          "properties": {
            "type": {
              "type": "string"
            },
            "offsets": {
              "type": "array",
              "items": [
                {
                  "type": "integer"
                },
                {
                  "type": "integer"
                }
              ],
              "additionalItems": True
            },
            "elink": {
              "type": "string"
            },
            "entity": {
              "type": "string"
            }
          },
          "additionalProperties": False
        }
      ],
      "additionalItems": True
    }
  },
  "additionalProperties": False
}






def validateJson(jsonData):
    try:
        validate(instance=jsonData, schema=nerSchema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True



 
# Opening JSON file
fs = open(sys.argv[1]).readlines()

# Convert json to python object
for f in fs: 
    jsonData = json.loads(f)
    # validate it
    isValid = validateJson(jsonData)

    if isValid:
    #print(jsonData)
        print("Given JSON data is Valid")
    else:
    #print(jsonData)
        print("Given JSON data is InValid")





