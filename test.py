import os
import re

x = """
      case "foo":
        response = "foo waaahaawaaaahaaa"
        break;

      case "bar":
        response = "bar waaahaawaaaahaaa"
        break;

      case "baz":
        response = "baz waaahaawaaaahaaa"
        break;

      case "bash":
        response = "bash waaahaawaaaahaaa"
        break;
"""

delim = '%$$%'

with open('sample.js', 'r') as file:
    data = file.read().replace(delim, x)
    f = open('run.js', 'w')
    f.write(data)
    f.close()