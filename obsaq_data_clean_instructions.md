
# **Instructions for the added mode - data cleaning and merging**
This update resolves several issues present in the original package. The previous version produced non-standard CSV files after downloading, which contained numerous invisible or corrupted characters. As a result, users frequently encountered severe errors during file reading, cleaning, and merging. Common problems included unreadable files, non-unique column names, metadata interfering with header recognition, and non-standard site name columns.
To address these issues, this update introduces a dedicated data cleaning and merging module (obsaq_data_clean). Its purpose is to re-encode and restructure the raw CSV files downloaded from the AURN website across different monitoring sites. The module performs site information extraction, empty row/column removal, table structure resetting, row/column reorganization, and consolidated output generation.
Additionally, a comprehensive set of error-handling checkpoints has been implemented to help users identify the exact cause of failures, enabling targeted troubleshooting.

## Explanation of several normal errors or warnings:
• Skip site name extraction
The site name could not be detected. This may occur if the downloaded raw data does not contain station information. Please check whether the source CSV file includes a valid site name field.
• Missing valid data
No valid pollutant values were found. This may happen when the selected site has no pollutant data for the specified year, or if the data download was unsuccessful.
• Error: An error occurred while processing…
An error occurred during data cleaning. The package outputs the name of the problematic file along with the specific error message each time an error is encountered, enabling targeted troubleshooting.
• No CSV files were successfully processed
No output file could be generated. This may indicate that none of the CSV files were recognized as valid, or that all files failed to be cleaned and merged successfully.
<img width="451" height="621" alt="image" src="https://github.com/user-attachments/assets/1f3d67a0-cf22-40ae-befe-47120a00dc1c" />
