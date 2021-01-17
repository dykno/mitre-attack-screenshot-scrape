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
		if file.startswith('.'):
			continue
		with open(os.path.join('./eval-json/%s') % file) as inputJson:
			print("Opened %s" % file)
			# Set the company name for later use
			companyName = file.rstrip('.json').split('.')[0]
			# Load our JSON data
			data = json.load(inputJson)

			# Check for the company's output directory and create if it doesn't exist
			if not os.path.exists('./output/%s' % companyName):
				os.mkdir('./output/%s' % companyName)

			techniques = data['Techniques']
			# Loop through each entry in the file
			for technique in techniques:
				# Set our ATT&CK technique name for future reference (used in file naming)
				techniqueName = technique['TechniqueName'].replace('/', '')
				try:
					# Loop through each attack 'step' that was evaluated in relation to the technique
					for step in technique['Steps']:
						# Loop through each detection within the step
						for detection in step['Detections']:
							# Loop through each screenshot submitted for that detection.
							for screenshot in detection['Screenshots']:
								# Strip return characters because they existed in some places for an unknown reason
								screenshotObj = screenshot['ScreenshotName'].rstrip('\n')
								# The JSON can contain blank screenshot names for an unknown reason which just cause problems
								# Check if we already have the file to prevent overwriting
								# Check if the screenshot name is blank to prevent creating useless files
								if not screenshotObj == "" and not os.path.exists('./output/%s/%s-%s' % (companyName, techniqueName, screenshotObj)):
										# Make a request to download the raw screenshot
										pngResponse = downloadScreenshot(screenshotObj)

										# Write the screenshot
										with open('./output/%s/%s-%s' % (companyName, techniqueName, screenshotObj), "wb") as outputPng:
											outputPng.write(pngResponse.content)
				except KeyError as e:
					print('No screenshot detected for %s' % technique['TechniqueId'])
				
				except:
					print(technique.strip(u'\xa9'))
