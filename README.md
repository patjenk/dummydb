An inefficient and error prone database for prototyping python projects.

# Installation
`pip install git+https://github.com/patjenk/dummydb.git`

# Internals

## File Storage
The data on disk is in JSON. It's meant to be a basic readable format.

The top level keys are table names. The "definition" key under each table name is the structure of the table." The "data" key under each table name is the data. Everything is stored AS dicts because I don't care about efficiency.
