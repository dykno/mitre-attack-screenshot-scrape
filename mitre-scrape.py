import json
import os
import requests
import sys

# Method to download the raw screenshot results
def downloadScreenshot(screenshot):
	baseURL = 'https://d1zq5d3dtjfcoj.cloudfront.net/'
	fullURL = '%s%s' % (baseURL, screenshot)
	print(fullURL)
	response = requests.request("GET", fullURL)
	return response

# Check for and create our output directory if it doesn't exist
if not os.path.exists('./output/'):
	os.mkdir('./output/')

# Get all of the JSON files that we need to parse
for root, dirs, files in os.walk('./eval-json/'):
	for file in files:
		# Open each company's JSON result file
		with open(os.path.join('./eval-json/%s') % file) as inputJson:
			print("Opened %s" % file)
			# Set the company name for later use
			companyName = file.rstrip('.json').split('.')[0]
			# Load our JSON data
			data = json.load(inputJson)

			# Check for the company's output directory and create if it doesn't exist
			if not os.path.exists('./output/%s' % companyName):
				os.mkdir('./output/%s' % companyName)

			# Loop through each entry in the file
			for technique in data:
				# Set our ATT&CK technique name for future reference (used in file naming)
				techniqueName = data[technique]

				try:

					# Loop through each attack 'step' that was evaluated in relation to the technique
					for step in data[technique]['Steps']:
						# Gather each screenshot that was submitted for that step (steps can have multiple screenshots)
						for screenshot in data[technique]['Steps'][step]['Screenshots']:
							# Strip return characters because they existed in some places for an unknown reason
							screenshot = screenshot.rstrip('\n')
							# The JSON can contain blank screenshot names for an unknown reason which just cause problems
							# Check if we already have the file to prevent overwriting
							# Check if the screenshot name is blank to prevent creating useless files
							if not screenshot == "" and not os.path.exists('./output/%s/%s-%s' % (companyName, technique, screenshot)):
									# Make a request to download the raw screenshot
									pngResponse = downloadScreenshot(screenshot)

									# Write the screenshot
									with open('./output/%s/%s-%s' % (companyName, technique, screenshot), "wb") as outputPng:
										outputPng.write(pngResponse.content)
				except:
					print(data[technique].strip(u'\xa9'))
