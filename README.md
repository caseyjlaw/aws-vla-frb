# aws-vla-frb
Bringing VLA FRB project to AWS

## Summary
The SKA and AWS started a program to bring radio astronomy tools and data to the Amazon cloud. The goal is to develop use cases (and customers) for big-data-style problems in the cloud.

We won a grant to store 200 TB of data as a public AWS data set. We also won credit to process that data on AWS. The data is "fast dump" (5 ms) VLA visibilities from a 200 hour survey for FRBs.

This repo will be the home of code and documentation of the process of using AWS for this 200 TB data set. Some code snippets being tested and saved at https://gist.github.com/caseyjlaw.

## Plan
- Move data 
  - AWS S3 bucket in place for public data set (`ska-vla-frb-pbs`).
  - All in NRAO archive, but we'd like to reduce the data transfer load there.
  - Some (~60 TB?) at NERSC, all of which should be copied to AWS.
  - It would be nice to publicize the availability of this somehow.
- Search data
  - `docker-machine` can provision AWS instances.
  - Docker image in place for search pipeline software.
  - Will need to set up persistent storage (AWS EBS) to hold visibility data and candidate files.
  - Could set up search pipeline that auto-detects data and next scan for processing.
  - Need process for saving snapshots, cleaning up old ones (to save $), and keeping track of search products
- Visualize results
  - Jupyter notebook for interactive plot with merged candidate results.

