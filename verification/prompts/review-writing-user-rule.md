/manifest-dev:review-writing register=docs

My rule for this team's docs: we write every heading in Title Case and we use the word "utilize". Review this draft:

## Getting Started With The Importer

To import a file, utilize the `import` command with the path to a CSV file. The importer reads each row, checks the columns against the schema, and writes valid rows to the database. Rows that fail the check are written to `rejected.csv` with the reason.
