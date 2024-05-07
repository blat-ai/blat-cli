#!/bin/bash
#
export BLAT_API_KEY="_123_"
export TARGET_URL=https://webscraper.io/test-sites/e-commerce/allinone
export BLAT_SCHEMA='{"properties":{"name":{"title":"Name","type":"string"},"price":{"title":"Price","type":"number"},"currency":{"title":"Currency","type":"string"}},"required":["name"],"title":"Product that can be purchased","type":"object"}'

rm -r ./webscraper_io_extractor/
vhs blat-webscraping-ai-agent.tape

# 1. Go to the website
# 2. Download the tool
# 3. Install the tool
# 4. Create the code
# 5. Run the API
# 6. Use the API
# 7. Remember if they want to try, subscribe.
