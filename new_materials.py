#!/usr/bin/env python3
import os
from IUBBaseTools import ApiHandler, IUBConfiguration
import logging


#Check if the given path is an absolute path
def createAbsolutePath(path):
	if not os.path.isabs(path):
		currentDir = os.path.dirname(os.path.realpath(__file__))
		path = os.path.join(currentDir, path)
		
	return path


def main():
	configFile = "config.yml"
	logFile = "insert_new_material.log"
	# Set logging file
	logging.basicConfig(filename=createAbsolutePath(logFile), level=logging.ERROR, format='%(asctime)s %(levelname)-8s %(message)s')
	# Load config
	config_class = IUBConfiguration(createAbsolutePath(configFile), logging)
	logging.getLogger().setLevel(config_class.get_config('GlobalSettings', 'logLevel'))
	logging.info('Loaded settings started')

	#Creates handler to send request to the backend site
	handler = ApiHandler(
		config_class.get_config('GlobalSettings', 'username'),
		config_class.get_config('GlobalSettings', 'urlHandler'),
		config_class.get_config('GlobalSettings', 'tokenPath'),
		logging)
	
	#Append films
	upload_file = config_class.get_config('GlobalSettings', 'upload_per_request')
	materials = config_class.get_config('GlobalSettings', 'material_list')
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
				print("Added "+str(inserted)+" new releases!")
				logging.info("Added "+str(inserted)+" new releases!")
				#Check if everything is inserted
				if inserted < upload_file:
					logging.info("Stop insertion of "+str(material))
					break
		except Exception as exc:
			#Something very unexpected happened
			logging.error("Unexpected exception: "+str(exc) + "during insertion of a "+str(material))
			break
	
	logging.info("END: Appended " + str(len(materials)) + " new materials: " + str(materials))


main()
