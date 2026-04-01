# Production-Level Scoring System v2.0
# Tier 5 (8-10): Critical Infrastructure
# Tier 4 (5-7): High Impact
# Tier 3 (3-4): Medium Impact
# Tier 2 (1-2): Low Impact
# Tier 1 (0): Read-only

SCORING_RULES = {
    # COMPUTE - EC2
    'EC2': {
        'RunInstances': 5,
        'TerminateInstances': 3,
        'StopInstances': 1,
        'StartInstances': 1,
        'RebootInstances': 1,
        'ModifyInstanceAttribute': 3,
        'CreateImage': 4,
        'CreateSnapshot': 3,
        'DeleteSnapshot': 2,
        'AttachVolume': 2,
        'DetachVolume': 2,
        'CreateVolume': 3,
        'DeleteVolume': 2,
        # VPC Actions
        'CreateVpc': 8,
        'DeleteVpc': 6,
        'CreateSubnet': 6,
        'DeleteSubnet': 4,
        'CreateSecurityGroup': 5,
        'DeleteSecurityGroup': 4,
        'AuthorizeSecurityGroupIngress': 4,
        'RevokeSecurityGroupIngress': 3,
        'AuthorizeSecurityGroupEgress': 4,
        'CreateInternetGateway': 7,
        'AttachInternetGateway': 6,
        'CreateNatGateway': 7,
        'CreateRouteTable': 5,
        'CreateRoute': 4,
        'AssociateRouteTable': 4,
    },
    
    # STORAGE - S3
    'S3': {
        'CreateBucket': 4,
        'DeleteBucket': 3,
        'PutBucketPolicy': 5,
        'DeleteBucketPolicy': 4,
        'PutBucketVersioning': 3,
        'PutBucketEncryption': 4,
        'PutBucketLogging': 2,
        'PutBucketCors': 2,
        'PutBucketLifecycle': 3,
        'PutObject': 1,
        'DeleteObject': 1,
        'PutBucketReplication': 5,
    },
    
    # SECURITY - IAM
    'IAM': {
        'CreateRole': 6,
        'DeleteRole': 5,
        'CreateUser': 5,
        'DeleteUser': 4,
        'AttachRolePolicy': 6,
        'DetachRolePolicy': 5,
        'CreatePolicy': 7,
        'DeletePolicy': 5,
        'PutRolePolicy': 6,
        'CreateAccessKey': 4,
        'DeleteAccessKey': 3,
        'AttachUserPolicy': 5,
        'CreateGroup': 4,
        'AddUserToGroup': 3,
    },
    
    # NETWORKING - VPC
    'VPC': {
        'CreateVpc': 8,
        'DeleteVpc': 6,
        'CreateSubnet': 6,
        'DeleteSubnet': 4,
        'CreateSecurityGroup': 5,
        'DeleteSecurityGroup': 4,
        'AuthorizeSecurityGroupIngress': 4,
        'RevokeSecurityGroupIngress': 3,
        'AuthorizeSecurityGroupEgress': 4,
        'CreateInternetGateway': 7,
        'AttachInternetGateway': 6,
        'CreateNatGateway': 7,
        'CreateRouteTable': 5,
        'CreateRoute': 4,
        'AssociateRouteTable': 4,
    },
    
    # SERVERLESS - Lambda
    'LAMBDA': {
        'CreateFunction': 6,
        'DeleteFunction': 4,
        'UpdateFunctionCode': 4,
        'UpdateFunctionConfiguration': 3,
        'PublishVersion': 3,
        'CreateAlias': 2,
        'UpdateAlias': 2,
        'AddPermission': 4,
        'RemovePermission': 3,
        'PutFunctionConcurrency': 3,
        'CreateEventSourceMapping': 5,
    },
    
    # DATABASE - RDS
    'RDS': {
        'CreateDBInstance': 9,
        'DeleteDBInstance': 7,
        'ModifyDBInstance': 5,
        'RebootDBInstance': 3,
        'StartDBInstance': 2,
        'StopDBInstance': 2,
        'CreateDBSnapshot': 4,
        'DeleteDBSnapshot': 3,
        'RestoreDBInstanceFromSnapshot': 7,
        'CreateDBCluster': 10,
        'ModifyDBCluster': 6,
        'CreateDBParameterGroup': 3,
        'ModifyDBParameterGroup': 3,
    },
    
    # INFRASTRUCTURE AS CODE - CloudFormation
    'CLOUDFORMATION': {
        'CreateStack': 10,
        'UpdateStack': 8,
        'DeleteStack': 6,
        'CreateChangeSet': 5,
        'ExecuteChangeSet': 7,
        'CancelUpdateStack': 4,
        'ContinueUpdateRollback': 5,
    },
    
    # CONTAINERS - EKS
    'EKS': {
        'CreateCluster': 10,
        'DeleteCluster': 8,
        'UpdateClusterVersion': 7,
        'UpdateClusterConfig': 6,
        'CreateNodegroup': 8,
        'DeleteNodegroup': 6,
        'UpdateNodegroupConfig': 5,
        'CreateAddon': 4,
        'UpdateAddon': 3,
    },

    # CONTAINERS - ECS
    'ECS': {
        'CreateCluster': 8,
        'DeleteCluster': 6,
        'RegisterTaskDefinition': 6,
        'DeregisterTaskDefinition': 4,
        'CreateService': 7,
        'UpdateService': 5,
        'DeleteService': 5,
        'RunTask': 4,
        'StopTask': 2,
        'CreateTaskSet': 5,
        'UpdateTaskSet': 4,
    },

    # CONTAINER REGISTRY - ECR
    'ECR': {
        'CreateRepository': 5,
        'DeleteRepository': 4,
        'PutImage': 3,
        'SetRepositoryPolicy': 4,
        'DeleteRepositoryPolicy': 3,
        'PutLifecyclePolicy': 3,
        'CreatePullThroughCacheRule': 4,
    },

    # NOSQL DATABASE - DynamoDB
    'DYNAMODB': {
        'CreateTable': 7,
        'DeleteTable': 5,
        'UpdateTable': 5,
        'PutItem': 1,
        'DeleteItem': 1,
        'UpdateItem': 1,
        'CreateBackup': 4,
        'RestoreTableFromBackup': 6,
        'CreateGlobalTable': 8,
        'UpdateGlobalTable': 6,
        'EnableKinesisStreamingDestination': 4,
    },

    # MESSAGING - SNS
    'SNS': {
        'CreateTopic': 4,
        'DeleteTopic': 3,
        'Subscribe': 3,
        'Unsubscribe': 2,
        'Publish': 1,
        'SetTopicAttributes': 3,
        'CreatePlatformApplication': 4,
    },

    # MESSAGING - SQS
    'SQS': {
        'CreateQueue': 4,
        'DeleteQueue': 3,
        'SendMessage': 1,
        'SetQueueAttributes': 3,
        'AddPermission': 3,
        'RemovePermission': 2,
    },

    # API GATEWAY
    'APIGATEWAY': {
        'CreateRestApi': 6,
        'DeleteRestApi': 5,
        'CreateDeployment': 6,
        'CreateStage': 5,
        'DeleteStage': 4,
        'CreateResource': 4,
        'DeleteResource': 3,
        'PutMethod': 4,
        'PutIntegration': 4,
        'CreateApiKey': 3,
        'CreateUsagePlan': 4,
    },

    # DNS - Route53
    'ROUTE53': {
        'CreateHostedZone': 6,
        'DeleteHostedZone': 5,
        'ChangeResourceRecordSets': 4,
        'CreateHealthCheck': 4,
        'DeleteHealthCheck': 3,
        'CreateTrafficPolicy': 5,
        'AssociateVPCWithHostedZone': 5,
    },

    # MONITORING - CloudWatch
    'CLOUDWATCH': {
        'PutMetricAlarm': 4,
        'DeleteAlarms': 3,
        'CreateDashboard': 4,
        'DeleteDashboards': 3,
        'PutDashboard': 3,
        'EnableAlarmActions': 2,
        'PutMetricData': 1,
        'PutAnomalyDetector': 4,
    },

    # MONITORING - CloudWatch Logs
    'LOGS': {
        'CreateLogGroup': 3,
        'DeleteLogGroup': 2,
        'CreateLogStream': 2,
        'PutLogEvents': 1,
        'PutSubscriptionFilter': 4,
        'DeleteSubscriptionFilter': 3,
        'PutRetentionPolicy': 3,
        'CreateExportTask': 3,
    },

    # CACHING - ElastiCache
    'ELASTICACHE': {
        'CreateCacheCluster': 8,
        'DeleteCacheCluster': 6,
        'ModifyCacheCluster': 5,
        'CreateReplicationGroup': 9,
        'DeleteReplicationGroup': 7,
        'ModifyReplicationGroup': 6,
        'CreateCacheSubnetGroup': 4,
        'CreateSnapshot': 4,
        'RestoreFromSnapshot': 6,
    },

    # SECRETS - Secrets Manager
    'SECRETSMANAGER': {
        'CreateSecret': 5,
        'DeleteSecret': 4,
        'UpdateSecret': 4,
        'RotateSecret': 5,
        'PutSecretValue': 3,
        'TagResource': 2,
    },

    # PARAMETER STORE - SSM
    'SSM': {
        'PutParameter': 3,
        'DeleteParameter': 2,
        'AddTagsToResource': 2,
        'CreateDocument': 5,
        'DeleteDocument': 4,
        'CreateAssociation': 4,
        'StartAutomationExecution': 5,
        'SendCommand': 3,
    },

    # CI/CD - CodePipeline
    'CODEPIPELINE': {
        'CreatePipeline': 7,
        'DeletePipeline': 5,
        'UpdatePipeline': 5,
        'StartPipelineExecution': 4,
        'StopPipelineExecution': 3,
        'PutApprovalResult': 3,
        'CreateCustomActionType': 5,
    },

    # CI/CD - CodeBuild
    'CODEBUILD': {
        'CreateProject': 6,
        'DeleteProject': 5,
        'UpdateProject': 4,
        'StartBuild': 3,
        'StopBuild': 2,
        'CreateReportGroup': 4,
        'BatchDeleteBuilds': 3,
    },

    # CI/CD - CodeDeploy
    'CODEDEPLOY': {
        'CreateApplication': 5,
        'DeleteApplication': 4,
        'CreateDeploymentGroup': 6,
        'DeleteDeploymentGroup': 5,
        'CreateDeployment': 5,
        'StopDeployment': 3,
        'CreateDeploymentConfig': 4,
    },

    # CI/CD - CodeCommit
    'CODECOMMIT': {
        'CreateRepository': 5,
        'DeleteRepository': 4,
        'CreateBranch': 3,
        'DeleteBranch': 2,
        'MergeBranchesByFastForward': 3,
        'CreatePullRequest': 3,
        'MergePullRequestBySquash': 3,
    },

    # DATA - Glue
    'GLUE': {
        'CreateDatabase': 5,
        'DeleteDatabase': 4,
        'CreateTable': 4,
        'DeleteTable': 3,
        'CreateJob': 6,
        'DeleteJob': 4,
        'StartJobRun': 4,
        'CreateCrawler': 5,
        'StartCrawler': 3,
        'CreateTrigger': 4,
        'CreateWorkflow': 5,
    },

    # DATA - Athena
    'ATHENA': {
        'CreateWorkGroup': 5,
        'DeleteWorkGroup': 4,
        'StartQueryExecution': 2,
        'CreateDataCatalog': 5,
        'CreateNamedQuery': 3,
        'CreatePreparedStatement': 3,
    },

    # DATA - Kinesis
    'KINESIS': {
        'CreateStream': 6,
        'DeleteStream': 5,
        'MergeShards': 4,
        'SplitShard': 4,
        'AddTagsToStream': 2,
        'EnableEnhancedMonitoring': 3,
        'StartStreamEncryption': 4,
    },

    # DATA - Kinesis Firehose
    'FIREHOSE': {
        'CreateDeliveryStream': 6,
        'DeleteDeliveryStream': 5,
        'UpdateDestination': 4,
        'TagDeliveryStream': 2,
    },

    # ML - SageMaker
    'SAGEMAKER': {
        'CreateNotebookInstance': 7,
        'DeleteNotebookInstance': 5,
        'CreateTrainingJob': 8,
        'CreateModel': 6,
        'CreateEndpoint': 8,
        'DeleteEndpoint': 6,
        'CreateEndpointConfig': 5,
        'CreatePipeline': 7,
        'CreateDomain': 8,
        'CreateFeatureGroup': 6,
    },

    # WORKFLOW - Step Functions
    'STATES': {
        'CreateStateMachine': 7,
        'DeleteStateMachine': 5,
        'UpdateStateMachine': 5,
        'StartExecution': 3,
        'StopExecution': 2,
        'CreateActivity': 4,
    },

    # CDN - CloudFront
    'CLOUDFRONT': {
        'CreateDistribution': 7,
        'DeleteDistribution': 6,
        'UpdateDistribution': 5,
        'CreateInvalidation': 3,
        'CreateCachePolicy': 4,
        'CreateOriginAccessControl': 4,
        'AssociateAlias': 4,
    },

    # PLATFORM - Elastic Beanstalk
    'ELASTICBEANSTALK': {
        'CreateApplication': 6,
        'DeleteApplication': 5,
        'CreateEnvironment': 7,
        'TerminateEnvironment': 5,
        'UpdateEnvironment': 5,
        'CreateApplicationVersion': 4,
        'DeleteApplicationVersion': 3,
        'SwapEnvironmentCNAMEs': 4,
    },

    # LOAD BALANCING - ELB
    'ELASTICLOADBALANCING': {
        'CreateLoadBalancer': 7,
        'DeleteLoadBalancer': 6,
        'CreateTargetGroup': 5,
        'DeleteTargetGroup': 4,
        'CreateListener': 5,
        'DeleteListener': 4,
        'RegisterTargets': 3,
        'DeregisterTargets': 2,
        'ModifyLoadBalancerAttributes': 4,
        'CreateRule': 4,
    },

    # AUTO SCALING
    'AUTOSCALING': {
        'CreateAutoScalingGroup': 7,
        'DeleteAutoScalingGroup': 5,
        'UpdateAutoScalingGroup': 5,
        'CreateLaunchConfiguration': 5,
        'DeleteLaunchConfiguration': 4,
        'PutScalingPolicy': 5,
        'DeletePolicy': 4,
        'AttachLoadBalancerTargetGroups': 4,
        'SetDesiredCapacity': 3,
    },

    # SECURITY - KMS
    'KMS': {
        'CreateKey': 6,
        'ScheduleKeyDeletion': 5,
        'EnableKey': 3,
        'DisableKey': 3,
        'CreateAlias': 3,
        'DeleteAlias': 2,
        'PutKeyPolicy': 5,
        'EnableKeyRotation': 4,
        'CreateGrant': 4,
    },

    # SECURITY - WAF
    'WAFV2': {
        'CreateWebACL': 7,
        'DeleteWebACL': 6,
        'UpdateWebACL': 5,
        'CreateRuleGroup': 6,
        'DeleteRuleGroup': 5,
        'CreateIPSet': 4,
        'AssociateWebACL': 5,
    },

    # SECURITY - GuardDuty
    'GUARDDUTY': {
        'CreateDetector': 6,
        'DeleteDetector': 5,
        'CreateFilter': 4,
        'CreateIPSet': 4,
        'CreateThreatIntelSet': 4,
        'ArchiveFindings': 3,
        'CreatePublishingDestination': 4,
    },

    # SECURITY - Config
    'CONFIG': {
        'PutConfigRule': 5,
        'DeleteConfigRule': 4,
        'PutConfigurationRecorder': 5,
        'StartConfigurationRecorder': 4,
        'StopConfigurationRecorder': 3,
        'PutDeliveryChannel': 4,
        'PutRemediationConfigurations': 5,
    },

    # NETWORKING - Direct Connect
    'DIRECTCONNECT': {
        'CreateConnection': 8,
        'DeleteConnection': 7,
        'CreateVirtualInterface': 7,
        'DeleteVirtualInterface': 6,
        'CreateDirectConnectGateway': 8,
        'AssociateVirtualInterface': 6,
    },

    # NETWORKING - VPN
    'EC2_VPN': {
        'CreateVpnConnection': 7,
        'DeleteVpnConnection': 6,
        'CreateVpnGateway': 7,
        'AttachVpnGateway': 6,
        'CreateCustomerGateway': 6,
    },

    # STORAGE - EFS
    'ELASTICFILESYSTEM': {
        'CreateFileSystem': 6,
        'DeleteFileSystem': 5,
        'CreateMountTarget': 5,
        'DeleteMountTarget': 4,
        'PutFileSystemPolicy': 4,
        'CreateAccessPoint': 4,
        'PutBackupPolicy': 3,
    },

    # STORAGE - Backup
    'BACKUP': {
        'CreateBackupPlan': 5,
        'DeleteBackupPlan': 4,
        'CreateBackupSelection': 4,
        'StartBackupJob': 4,
        'StartRestoreJob': 6,
        'CreateBackupVault': 5,
        'DeleteBackupVault': 4,
    },

    # ANALYTICS - EMR
    'EMR': {
        'RunJobFlow': 9,
        'TerminateJobFlows': 7,
        'AddJobFlowSteps': 5,
        'CreateSecurityConfiguration': 5,
        'AddInstanceGroups': 6,
        'ModifyInstanceGroups': 5,
    },

    # ANALYTICS - Redshift
    'REDSHIFT': {
        'CreateCluster': 10,
        'DeleteCluster': 8,
        'ModifyCluster': 6,
        'CreateClusterSnapshot': 5,
        'RestoreFromClusterSnapshot': 8,
        'CreateClusterSubnetGroup': 5,
        'CreateEventSubscription': 4,
        'EnableLogging': 3,
    },

    # SEARCH - OpenSearch / Elasticsearch
    'ES': {
        'CreateDomain': 8,
        'DeleteDomain': 7,
        'UpdateDomainConfig': 5,
        'CreateOutboundConnection': 5,
        'AddTags': 2,
    },

    # IOT
    'IOT': {
        'CreateThing': 4,
        'DeleteThing': 3,
        'CreatePolicy': 5,
        'CreateTopicRule': 5,
        'DeleteTopicRule': 4,
        'CreateCertificateFromCsr': 4,
        'CreateProvisioningTemplate': 5,
    },

    # AMPLIFY
    'AMPLIFY': {
        'CreateApp': 5,
        'DeleteApp': 4,
        'CreateBranch': 4,
        'DeleteBranch': 3,
        'CreateDeployment': 5,
        'StartDeployment': 4,
        'CreateDomainAssociation': 5,
    },

    # LIGHTSAIL
    'LIGHTSAIL': {
        'CreateInstances': 5,
        'DeleteInstance': 4,
        'CreateRelationalDatabase': 8,
        'DeleteRelationalDatabase': 6,
        'CreateLoadBalancer': 6,
        'CreateDisk': 4,
        'CreateDomainEntry': 4,
    },

    # TRANSFER FAMILY
    'TRANSFER': {
        'CreateServer': 6,
        'DeleteServer': 5,
        'CreateUser': 4,
        'DeleteUser': 3,
        'ImportSshPublicKey': 3,
    },

    # APPRUNNER
    'APPRUNNER': {
        'CreateService': 6,
        'DeleteService': 5,
        'UpdateService': 4,
        'PauseService': 2,
        'ResumeService': 2,
        'CreateConnection': 4,
        'CreateAutoScalingConfiguration': 4,
    },
}

IGNORED_ACTIONS = [
    'ConsoleLogin', 'Describe', 'Get', 'List', 'Head', 'AssumeRole'
]

DAILY_SCORE_CAP = 100
SERVICE_DAILY_CAP = 30
ACTION_DAILY_CAP = 15

def should_ignore_action(action):
    for ignored in IGNORED_ACTIONS:
        if action.startswith(ignored):
            return True
    return False

def calculate_score(service, action):
    if should_ignore_action(action):
        return 0
    return SCORING_RULES.get(service, {}).get(action, 0)
