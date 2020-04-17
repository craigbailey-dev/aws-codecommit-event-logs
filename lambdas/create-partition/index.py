import boto3
import os
import traceback

# Initialize Glue client
glue_client = boto3.client("glue")

# List of columns for each table
table_column_schemas = {
    "repository_state_change": [
        {
            "Name": "timestamp",
            "Type": "string"
        },
        {
            "Name": "eventVersion",
            "Type": "string"
        },
        {
            "Name": "repositoryArn",
            "Type": "string"
        },
        {
            "Name": "event",
            "Type": "string"
        },
        {
            "Name": "baseCommitId",
            "Type": "string"
        },
        {
            "Name": "callerUserArn",
            "Type": "string"
        },
        {
            "Name": "commitId",
            "Type": "string"
        },
        {
            "Name": "conflictDetailLevel",
            "Type": "string"
        },
        {
            "Name": "conflictResolutionStrategy",
            "Type": "string"
        },
        {
            "Name": "destinationCommitId",
            "Type": "string"
        },
        {
            "Name": "mergeOption",
            "Type": "string"
        },
        {
            "Name": "oldCommitId",
            "Type": "string"
        },
        {
            "Name": "referenceFullName",
            "Type": "string"
        },
        {
            "Name": "referenceName",
            "Type": "string"
        },
        {
            "Name": "referenceType",
            "Type": "string"
        },
        {
            "Name": "repositoryId",
            "Type": "string"
        },
        {
            "Name": "repositoryName",
            "Type": "string"
        },
        {
            "Name": "sourceCommitId",
            "Type": "string"
        },
        {
            "Name": "conflictDetailsLevel",
            "Type": "string"
        }
    ],
    "pull_request_state_change": [
        {
            "Name": "timestamp",
            "Type": "string"
        },
        {
            "Name": "eventVersion",
            "Type": "string"
        },
        {
            "Name": "repositoryArn",
            "Type": "string"
        },
        {
            "Name": "event",
            "Type": "string"
        },
        {
            "Name": "approvalStatus",
            "Type": "string"
        },
        {
            "Name": "author",
            "Type": "string"
        },
        {
            "Name": "callerUserArn",
            "Type": "string"
        },
        {
            "Name": "creationDate",
            "Type": "string"
        },
        {
            "Name": "description",
            "Type": "string"
        },
        {
            "Name": "destinationCommit",
            "Type": "string"
        },
        {
            "Name": "destinationReference",
            "Type": "string"
        },
        {
            "Name": "isMerged",
            "Type": "string"
        },
        {
            "Name": "lastModifiedDate",
            "Type": "string"
        },
        {
            "Name": "mergeOption",
            "Type": "string"
        },
        {
            "Name": "notificationBody",
            "Type": "string"
        },
        {
            "Name": "overrideStatus",
            "Type": "string"
        },
        {
            "Name": "pullRequestId",
            "Type": "string"
        },
        {
            "Name": "pullRequestStatus",
            "Type": "string"
        },
        {
            "Name": "repositoryNames",
            "Type": "array<string>"
        },
        {
            "Name": "revisionId",
            "Type": "string"
        },
        {
            "Name": "sourceCommit",
            "Type": "string"
        },
        {
            "Name": "sourceReference",
            "Type": "string"
        },
        {
            "Name": "title",
            "Type": "string"
        }
    ],
    "approval_rule_template_change": [
        {
            "Name": "timestamp",
            "Type": "string"
        },
        {
            "Name": "eventVersion",
            "Type": "string"
        },
        {
            "Name": "event",
            "Type": "string"
        },
        {
            "Name": "repositories",
            "Type": "map<string,string>"
        },
        {
            "Name": "approvalRuleTemplateContentSha256",
            "Type": "string"
        },
        {
            "Name": "approvalRuleTemplateId",
            "Type": "string"
        },
        {
            "Name": "approvalRuleTemplateName",
            "Type": "string"
        },
        {
            "Name": "callerUserArn",
            "Type": "string"
        },
        {
            "Name": "creationDate",
            "Type": "string"
        },
        {
            "Name": "lastModifiedDate",
            "Type": "string"
        },
        {
            "Name": "notificationBody",
            "Type": "string"
        }
    ],
    "comment_on_commit": [
        {
            "Name": "timestamp",
            "Type": "string"
        },
        {
            "Name": "eventVersion",
            "Type": "string"
        },
        {
            "Name": "event",
            "Type": "string"
        },
        {
            "Name": "repositoryArn",
            "Type": "string"
        },
        {
            "Name": "beforeCommitId",
            "Type": "string"
        },
        {
            "Name": "repositoryId",
            "Type": "string"
        },
        {
            "Name": "inReplyTo",
            "Type": "string"
        },
        {
            "Name": "notificationBody",
            "Type": "string"
        },
        {
            "Name": "commentId",
            "Type": "string"
        },
        {
            "Name": "afterCommitId",
            "Type": "string"
        },
        {
            "Name": "repositoryName",
            "Type": "string"
        },
        {
            "Name": "callerUserArn",
            "Type": "string"
        }
    ],
    "comment_on_pull_request": [
        {
            "Name": "timestamp",
            "Type": "string"
        },
        {
            "Name": "eventVersion",
            "Type": "string"
        },
        {
            "Name": "event",
            "Type": "string"
        },
        {
            "Name": "beforeCommitId",
            "Type": "string"
        },
        {
            "Name": "repositoryId",
            "Type": "string"
        },
        {
            "Name": "inReplyTo",
            "Type": "string"
        },
        {
            "Name": "notificationBody",
            "Type": "string"
        },
        {
            "Name": "commentId",
            "Type": "string"
        },
        {
            "Name": "afterCommitId",
            "Type": "string"
        },
        {
            "Name": "repositoryName",
            "Type": "string"
        },
        {
            "Name": "callerUserArn",
            "Type": "string"
        },
        {
            "Name": "pullRequestId",
            "Type": "string"
        }
    ]
}

def handler(event, context):
    for record in event["Records"]:
        source_bucket = record["s3"]["bucket"]["name"]
        source_key = record["s3"]["object"]["key"]

        # Extract partition info from S3 key 
        table, year, month, day, hour, _ = source_key.split("/")

        # Form date for 'date' partition column
        date = "{}-{}-{}".format(year, month, day)

        # Form S3 location for partition
        s3_location = 's3://{}/{}/{}/{}/{}'.format(source_bucket, table, year, month, day, hour)

        # Form the partition input
        partition = {
            'Values': [
                date,
                hour
            ],
            "StorageDescriptor": {
                "NumberOfBuckets" : -1,
                "Columns": table_column_schemas[table],
                "Location": s3_location,
                "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",
                "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
                "Compressed": False,
                "SerdeInfo": {
                    "SerializationLibrary": "org.openx.data.jsonserde.JsonSerDe",
                    "Parameters": {
                        "serialization.format": "1"
                    }
                },
                "BucketColumns": [],
                "SortColumns": [],
                "Parameters": {},
                "SkewedInfo": {
                    "SkewedColumnNames": [],
                    "SkewedColumnValues": [],
                    "SkewedColumnValueLocationMaps": {}
                },
                "StoredAsSubDirectories": False
            }
        }

        # Attempt to create partition; Print exception if partition already exists or for any other error
        try:
            glue_client.create_partition(DatabaseName=os.environ["DATABASE_NAME"], TableName=table, PartitionInput=partition)
        except:
            traceback.print_exc()