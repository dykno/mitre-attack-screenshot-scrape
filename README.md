MITRE ATT&CK Evaluation Screenshot Scraper
==========================================

A quick script to scrape MITRE ATT&CK Evaluation screenshots.

Usage
-----
1. Gather desired companys' Result JSON files from MITRE's website. For example: `https://attackevals.mitre.org/COMPANY_NAME.1.APT3.1_Results.json`.
2. Put the resulting JSON files into `./eval-json/`.
3. Make sure the JSON files have an identifiable name as the name of the JSON file dictates the name of the output directory.
4. Run the script.
5. Wait.
6. View the results in `./output/COMPANY_NAME/`. Results are named as follows: `$TECHNIQUE_ID-$COMPANY_PREFIX-$EVAL_STEP_ID.png`