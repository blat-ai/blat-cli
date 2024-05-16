<div align="center">
  <a href="https://blat.ai">
    <img src="https://framerusercontent.com/assets/ZD9Sg28IboDmP0DfMFxuv0EOQBk.png" alt="Blat">
  </a>
</div>
</br>

# Blat CLI
Are you frustrated of creating and maintaining web scraping scripts?

Fear not! Blat CLI is a Command Line Interface to **manage Blat AI agents that generate web scraping algorithms automatically.**

## Getting Started
### Requirements
Blat CLI is available on Linux, macOS and Windows platforms because it runs on Python. The package currently supports the following versions:
* 3.9
* 3.10
* 3.11
* 3.12

### Installation
The blat-cli package is available in the PyPI repository, so just run:
```bash
pip install blat-cli
```
Now the ```blat``` command should be available on your terminal.

### Initial Setup
The blat-cli package needs to install some dependencies for it to work properly. They can be installed running the following commands:
```bash
BLAT_API_KEY="Get it from https://blat.ai"

sudo blat init-system
blat init --api-key $BLAT_API_KEY
```
Once these steps are executed, the command will be ready! ✅

### Generating your first Harvester
The main feature of Blat AI is to automatically generate data extraction code for a specific website and a given schema. So, you just need to execute the following steps:

```bash
# First find a website from which you'd like to extract data
export TARGET_URL=https://webscraper.io/test-sites/e-commerce/allinone
# Then define a JSON schema that would be your desired output for the data extraction algorithm
export BLAT_SCHEMA='{"properties":{"name":{"title":"Name","type":"string"},"price":{"title":"Price","type":"number"},"currency":{"title":"Currency","type":"string"}},"required":["name"],"title":"Product that can be purchased","type":"object"}'

# Then just call Blat and follow the instructions
blat harvester generate --schema $BLAT_SCHEMA --url $TARGET_URL
```
This will return you a zip file in your current folder if the generation was succesful. Decompress the file and you should have a web scraping algorithm ready to be used, just follow the README! 🚀

## Features
* XPath generation for data in HTML, lists included
* Generation of post processing functions
* Code generation in Python

## Limitations
* Parsing JSON responses might not fully work
* The generated code doesn't navigate/paginate
* Files and multimedia extraction is not implemented (workaround is to extract the URL)

## Getting Help
GitHub is currently the only way to interact with our team. You can [open an issue](https://github.com/blat-ai/blat-cli/issues/new/choose) and choose one of the templates to ask for guidance, to report a bug, or to request a new feature.

Before opening a new issue, please check if there's similar [issues](https://github.com/blat-ai/blat-cli/issues) already created.