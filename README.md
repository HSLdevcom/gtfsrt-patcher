# gtfsrt-patcher
Contains Azure functions related to patching GTFS RT (download from a feed, do edits and upload in blob storage).

To run locally, local.settings.json should be edited to contain the real secrets in the following format:
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

## lmj and tre no_info-to-skipped-patchers

These functions download a Trip Update file from the original feed and replaces NO_DATA stop time updates with SKIPPED because they are used in the original feed to indicate that a stop is closed but OpenTripPlanner does not handle them as such. The end result is uploaded to blob storage under tampere or lmj container. These functions run every thirty seconds.
