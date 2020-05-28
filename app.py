from builder import MessengerBuilder

import click
import os
import re

@click.command()
@click.option(
	'--filepath',
	prompt='What\'s the path to the JSON file?', 
	help='JSON file path.')
@click.option(
	'--zipout',
	default='y',
	prompt='Would you like to zip the output? (y/N)',
	help='Whether or not to zip output.')
def start(filepath, zipout):
    """Entry point to builder, get JSON and start building!"""
    try:
    	if not os.path.exists(filepath):
    		raise FileNotFoundError('Invalid JSON file path, please try again.')
    	if not isinstance(zipout, str):
    		raise TypeError('Expecting "yes" or "no" input for "zipout" option.')
    	zipout = zipout.lower()
    	match = re.search('(y|n)[e,o]?', zipout)
    	if not match:
    		raise ValueError('Expecting "yes" or "no" input for "zipout" option.')
    	mb = MessengerBuilder(filepath, zipout)
    	mb.build()
    except Exception as e:
    	raise e

if __name__ == '__main__':
    start()