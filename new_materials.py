#!/usr/bin/env python3
import os
from os import listdir
from os.path import isfile, join
import errno
import shutil
import re
import pickle
import time
from datetime import date, datetime, timedelta
import logging
import json
import requests
from pprint import pprint
import time
from ApiHandler import ApiHandler
import yaml

#Check if the given path is an absolute path
def createAbsolutePath(path):
	if not os.path.isabs(path):
		currentDir = os.path.dirname(os.path.realpath(__file__))
		path = os.path.join(currentDir, path)
		
	return path

def main():
	configFile = "config.yml"
	logFile = "insert_new_material.log"
	#Set logging file
	logging.basicConfig(filename=createAbsolutePath(logFile),level=logging.ERROR,format='%(asctime)s %(levelname)-8s %(message)s')
	#Load config
	with open(createAbsolutePath(configFile), 'r') as stream:
		try:
			config = yaml.load(stream)
			#Info from yaml configuration file
			username = config['Settings']['username']
			tokenPath = createAbsolutePath(config['Settings']['tokenPath'])
			url = config['Settings']['urlHandler']
			logLevel = config['Settings']['logLevel']
			upload_file = config['Settings']['upload_per_request']
			materials = config['Settings']['material_list']
			logging.getLogger().setLevel(logLevel)
			logging.info('Loaded settings started')
		except yaml.YAMLError as exc:
			print("Cannot load file: ["+configFile+"] - Error: "+exc)
			logging.error("Cannot load file: ["+configFile+"] - Error: "+exc)
			exit()

	#Creates handler to send request to the backend site
	handler = ApiHandler(username, url, tokenPath, logging)
	
	#Append films
	for material in materials:
		logging.info("Start appending "+material)
		try:
			while True:
				response = handler.insertNewMaterial(material, upload_file)
				try:
					inserted = int(response)
				except ValueError:
					print("The response ["+str(response)+"] cannot be converted to integer")
					logging.error("The response ["+str(response)+"] cannot be converted to integer")
					break
				print("Added "+str(inserted)+" new releases!");
				logging.info("Added "+str(inserted)+" new releases!")
				#Check if everything is inserted
				if inserted < upload_file:
					logging.info("Stop insertion of "+str(material))
					break
		except UnknownTypeFile:
			logging.error("Cannot insert this material: "+str(material))
			continue
		except Exception as exc:
			#Something very unexpected happened
			logging.error("Unexpected exception: "+str(exc) + "during insertion of a "+str(material))
			break
	
	logging.info("END: Appended "+str(len(materials))+ " new materials: " +str(materials) )


main()
