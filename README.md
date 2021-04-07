# MSDS_SERA_capstone

## Prerequisites

To fully run all of the code in the repository below, install the following packages:

- [Node.js](https://nodejs.org/en/download/)
- [AWS cli](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)

## File Structure:

- stata_replication
  - Work related to reproducing Stata code in python
- Stata
  - Raw Stata files
- RDS
  - Work related to creating and querying the database
- aws
  - Work related to AWS
- API Gateway
  - Work related to querying via the API
- nlp
  - Work related to NLP Captstone deployment in the cloud
- build.zip
  - Zip file that can can deploy and take down the entire infrastructure

## Documenatation

### Build.zip

### API

### NLP

#### Container

Container code found in `sera-nlp-container`. See [Docker Documentation](https://docs.docker.com/get-started/) for how to deploy a container.

#### Helper Files

##### uploadData.sh

Prompts for folder in local directory to upload to NLP raw data S3 bucket.

##### results.sh

Prompts for folder in local directory to download NLP parsed data S3 bucket.
