# gtfsrt-patcher

Contains Azure functions related to patching GTFS RT (download from a feed, do edits and upload in blob storage).

## local development setup

For OS X and pyenv:


```
brew tap azure/functions
brew install azure-functions-core-tools@4
pyenv install 3.12.11
pyenv virtualenv 3.12.11 gtfsrt-patcher-3.12.11
echo "gtfsrt-patcher-3.12.11" > .python-version
func start
```

azure-functions-core-tools install can complain about xcode versions, but
that does not matter because we are using pure python.

func start is slow to start, because it bootstraps the entire azure functions environment. Be patient.

local.settings.json must be edited to contain the real secrets in the following format:
```
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": "<connection string to storage that function is stored in>",
    "StorageConnectionString": "<connection string to storage that realtime data should get uploaded to>",
    "TRE_USER": "<username for tampere realtime>",
    "TRE_PASSWORD": "<password for tampere realtime>",
    "LMJ_USER": "<username for lmj realtime>>",
    "LMJ_PASSWORD": "<password for lmj realtime>"
  }
}
```


## library version note

protobuf and gtfs-realtime-bindings versions are interdependent in ways
not described properly in the packages, because gtfs-realtime-bindings
contains _pb2.py files which must be compatible with the installed
protobuf version.


## lmj and tre no_info-to-skipped-patchers

These functions download a Trip Update file from the original feed and replaces NO_DATA stop time updates with SKIPPED because they are used in the original feed to indicate that a stop is closed but OpenTripPlanner does not handle them as such. The end result is uploaded to blob storage under tampere or lmj container. These functions run every thirty seconds.

