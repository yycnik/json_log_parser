# json_log_parser - Parsing JSON logs for Python

This project processes valid JSON data from a log file and prints out a list of unique extensions and the number of 
unique filenames for that extension.

JSON format
```
ts:  timestamp
pt:  processing time
si:  session ID
uu:  user UUID
bg:  business UUID
sha: sha256 of the file
nm:  file name
ph:  path
dp:  disposition (valid values: MALICIOUS (1), CLEAN (2), UNKNOWN (3))
```

## Example
### Input data
```buildoutcfg
{"ts":1551140352,"pt":55,"si":"3380fb19-0bdb-46ab-8781-e4c5cd448074","uu":"0dd24034-36d6-4b1e-a6c1-a52cc984f105","bg":"77e28e28-745a-474b-a496-3c0e086eaec0","sha":"abb3ec1b8174043d5cd21d21fbe3c3fb3e9a11c7ceff3314a3222404feedda52","nm":"phkkrw.ext","ph":"/efvrfutgp/expgh/phkkrw","dp":2}
{"ts":1551140352,"pt":55,"si":"3380fb19-0bdb-46ab-8781-e4c5cd448074","uu":"0dd24034-36d6-4b1e-a6c1-a52cc984f105","bg":"77e28e28-745a-474b-a496-3c0e086eaec0","sha":"abb3ec1b8174043d5cd21d21fbe3c3fb3e9a11c7ceff3314a3222404feedda52","nm":"asdf.pdf","ph":"/efvrfutgp/asdf.pdf","dp":2}
{"ts":1551140352,"pt":55,"si":"3380fb19-0bdb-46ab-8781-e4c5cd448074","uu":"0dd24034-36d6-4b1e-a6c1-a52cc984f105","bg":"77e28e28-745a-474b-a496-3c0e086eaec0","sha":"abb3ec1b8174043d5cd21d21fbe3c3fb3e9a11c7ceff3314a3222404feedda52","nm":"phkkrw.ext","ph":"/efvrfutgp/expgh/phkkrw","dp":2}
```
### Expected Output
```buildoutcfg
ext: 1
pdf: 1
```

