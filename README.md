# aws-codecommit-event-logs
AWS CodeCommit event logs stored in S3 and query-able by Athena 

## Architecture

![enter image description here](https://d50daux61fgb.cloudfront.net/aws-codecommit-event-logs/solution-architecture.png)

Five EventBridge event rules for the default event bus track each type of CodeCommit event. Each event rule targets a specific Kinesis Firehose delivery stream that will put log files into a certain S3 folder corresponding to a Glue table. A Lambda function is used by each delivery stream to transform the CloudWatch event payload into the log file format. After a log file is placed in the bucket, a Lambda function is run that creates a partition for the corresponding Glue table, is one does not exist.

## Event Types

### Repository State Change

An action has been made on a repository

#### Log Format

 - **timestamp** *(string)* - The ISO 8601 format of the timestamp of the event
 - **eventVersion** *(string)* - The version of the event format
 - **event** *(string)* - The name of the specific event type
 - **repositoryArn** *(string)* - The ARN of the repository
 - **baseCommitId** *(string)* - The commit ID of the merge base
 - **callerUserArn** *(string)* - The ARN of the user that initiated the action
 - **commitId** *(string)* - The ID of the commit
 - **conflictDetailLevel** *(string)* - The level of conflict detail (FILE_LEVEL | LINE_LEVEL)
 - **conflictResolutionStrategy** *(string)* - Specifies which branch to use when resolving conflicts, or whether to attempt automatically merging two versions of a file (NONE | ACCEPT_SOURCE | ACCEPT_DESTINATION | AUTOMERGE)
 - **destinationCommitId** *(string)* - The commit ID of the destination commit specifier that was used in the merge evaluation
 - **mergeOption** *(string)* - The merge option or strategy you want to use to merge the code (FAST_FORWARD_MERGE|SQUASH_MERGE|THREE_WAY_MERGE)
 - **oldCommitId** *(string)* - The ID of the old commit after a reference update
 - **referenceFullName** *(string)* - The full name of the reference (e.g 'refs/heads/myBranch')
 - **referenceName** *(string)* - The name of the reference (e.g. 'myBranch')
 - **referenceType** *(string)* - The type of the reference
 - **repositoryId** *(string)* - The ID of the repository
 - **repositoryName** *(string)* - The name of the repository
 - **sourceCommitId** *(string)* - The commit ID of the source commit specifier that was used in the merge evaluation
 - **conflictDetailsLevel** *(string)* - The level of conflict detail (FILE_LEVEL | LINE_LEVEL)

### Pull Request State Change

An action has been made on a pull request

#### Log Format

 - **timestamp** *(string)* - The ISO 8601 format of the timestamp of the event
 - **eventVersion** *(string)* - The version of the event format
 - **event** *(string)* - The name of the specific event type
 - **repositoryArn** *(string)* - The ARN of the repository 
 - **approvalStatus** *(string)* - The status of approval for the pull request (APPROVE|REVOKE)
 - **author** *(string)* - The author of the pull request
 - **callerUserArn** *(string)* - The ARN of the user that initiated the action
 - **creationDate** *(string)* - Creation date of the pull request
 - **description** *(string)* - The description of the pull request
 - **destinationCommit** *(string)* - The commit ID of the destination commit specifier that was used in the merge evaluation
 - **destinationReference** *(string)* - The full name of the destination reference
 - **isMerged** *(string)* - 'True' if the pull request was merged, 'False' otherwise
 - **lastModifiedDate** *(string)* - The last modified date of the pull request
 - **mergeOption** *(string)* - The merge option or strategy you want to use to merge the code (FAST_FORWARD_MERGE|SQUASH_MERGE|THREE_WAY_MERGE)
 - **notificationBody** *(string)* - The content of the notification for the CodeCommit event
 - **overrideStatus** *(string)* - The status of approval rule requirements (OVERRIDE|REVOKE)
 - **pullRequestId** *(string)* - ID of the pull request
 - **pullRequestStatus** *(string)* - The status of the pull request
 - **repositoryNames** *(Array<string>)* - List of repoistory names 
 - **revisionId** *(string)* - The ID of the revision
 - **sourceCommit** *(string)* - The commit ID of the source commit specifier that was used in the merge evaluation
 - **sourceReference** *(string)* - The full name of the source reference
 - **title** *(string)* - The title of the pull request


###  Approval Rule Template Change

An action has been made on an approval rule template

#### Log Format

 - **timestamp** *(string)* - The ISO 8601 format of the timestamp of the event
 - **eventVersion** *(string)* - The version of the event format
 - **event** *(string)* - The name of the specific event type
 - **repositories** *(Map<string,string>)* - Map of repository names to repository IDs
 - **approvalRuleTemplateContentSha256** *(string)* - Hash of the approval rule template content
 - **approvalRuleTemplateId** *(string)* - The ID of the approval rule template
 - **approvalRuleTemplateName** *(string)* - Name of the approval rule template
 - **callerUserArn** *(string)* - The ARN of the user that initiated the action
 - **creationDate** *(string)* - Creation date of the approval rule template
 - **lastModifiedDate** *(string)* - Last modification date of the approval rule template
 - **notificationBody** *(string)* - The content of the notification for the CodeCommit event

###  Comment on Commit

An action has been made on a comment for a commit

#### Log Format

 - **timestamp** *(string)* - The ISO 8601 format of the timestamp of the event
 - **eventVersion** *(string)* - The version of the event format
 - **event** *(string)* - The name of the specific event type
 - **repositoryArn** *(string)* - The ARN of the repository
 - **beforeCommitId** *(string)* - The full commit ID of the before commit
 - **repositoryId** *(string)* - The ID of the repository
 - **inReplyTo** *(string)* - The ID of the comment to which this comment is replying to
 - **notificationBody** *(string)* - The content of the notification for the CodeCommit event
 - **commentId** *(string)* - The ID of the comment
 - **afterCommitId** *(string)* - The full commit ID of the commit that was the tip of the source branch at the time the comment was made 
 - **repositoryName** *(string)* - The name of the repository
 - **callerUserArn** *(string)* - The ARN of the user that initiated the action


###  Comment on Pull Request

An action has been made on a comment for a pull request

#### Log Format

 - **timestamp** *(string)* - The ISO 8601 format of the timestamp of the event
 - **eventVersion** *(string)* - The version of the event format
 - **event** *(string)* - The name of the specific event type
  - **repositoryArn** *(string)* - The ARN of the repository
 - **beforeCommitId** *(string)* - The full commit ID of the commit that was the tip of the destination branch when the pull request was created. This commit is superceded by the after commit in the source branch when and if you merge the source branch into the destination branch
 - **repositoryId** *(string)* - The ID of the repository
 - **inReplyTo** *(string)* - The ID of the comment to which this comment is replying to
 - **notificationBody** *(string)* - The content of the notification for the CodeCommit event
 - **commentId** *(string)* - The ID of the comment
 - **afterCommitId** *(string)* - The full commit ID of the commit that was the tip of the source branch at the time the comment was made
 - **repositoryName** *(string)* - The name of the repository
 - **callerUserArn** *(string)* - The ARN of the user that initiated the action
 - **pullRequestId** *(string)* - The ID of the pull request


## Log Partitions

All Glue tables are partitioned by the date and hour that the log arrives in S3. It is highly recommended that Athena queries on Glue database filter based on these paritions, as it will greatly reduce quety execution time and the amount of data processed by the query.


## Build and Deploy

To deploy the application, use the `cloudformation package` command from the AWS CLI. 
 
#### Example:

`aws cloudformation package --template templates/root.yaml --s3-bucket $S3_BUCKET --s3-prefix $S3_PREFIX --output-template template-export.yaml`