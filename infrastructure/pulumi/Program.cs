using Pulumi;
using Pulumi.AzureAD;
using Pulumi.AzureNative.Authorization;
using Pulumi.AzureNative.CognitiveServices;
using Pulumi.AzureNative.CognitiveServices.Inputs;
using Pulumi.AzureNative.Insights;
using Pulumi.AzureNative.KeyVault;
using Pulumi.AzureNative.KeyVault.Inputs;
using Pulumi.AzureNative.OperationalInsights;
using Pulumi.AzureNative.OperationalInsights.Inputs;
using Pulumi.AzureNative.Resources;
using Pulumi.AzureNative.Search;
using Pulumi.AzureNative.Search.Inputs;
using Pulumi.AzureNative.ServiceBus;
using Pulumi.AzureNative.ServiceBus.Inputs;
using Pulumi.AzureNative.Storage;
using Pulumi.AzureNative.Storage.Inputs;
using Pulumi.AzureNative.Web;
using Pulumi.AzureNative.Web.Inputs;
using EnterpriseAgentOps.Infrastructure;
using InsightsComponent = Pulumi.AzureNative.Insights.Component;
using InsightsComponentArgs = Pulumi.AzureNative.Insights.ComponentArgs;
using StorageAccountResource = Pulumi.AzureNative.Storage.StorageAccount;
using StorageAccountArgs = Pulumi.AzureNative.Storage.StorageAccountArgs;
using StorageKind = Pulumi.AzureNative.Storage.Kind;
using StorageSkuArgs = Pulumi.AzureNative.Storage.Inputs.SkuArgs;
using StorageSkuName = Pulumi.AzureNative.Storage.SkuName;
using SearchSkuArgs = Pulumi.AzureNative.Search.Inputs.SkuArgs;
using SearchSkuName = Pulumi.AzureNative.Search.SkuName;
using ServiceBusNamespace = Pulumi.AzureNative.ServiceBus.Namespace;
using ServiceBusNamespaceArgs = Pulumi.AzureNative.ServiceBus.NamespaceArgs;
using ServiceBusSkuArgs = Pulumi.AzureNative.ServiceBus.Inputs.SBSkuArgs;
using ServiceBusSkuName = Pulumi.AzureNative.ServiceBus.SkuName;
using ServiceBusSkuTier = Pulumi.AzureNative.ServiceBus.SkuTier;
using ServiceBusQueue = Pulumi.AzureNative.ServiceBus.Queue;
using ServiceBusQueueArgs = Pulumi.AzureNative.ServiceBus.QueueArgs;
using CognitiveAccount = Pulumi.AzureNative.CognitiveServices.Account;
using CognitiveAccountArgs = Pulumi.AzureNative.CognitiveServices.AccountArgs;
using CognitiveAccountPropertiesArgs = Pulumi.AzureNative.CognitiveServices.Inputs.AccountPropertiesArgs;
using CognitiveDeployment = Pulumi.AzureNative.CognitiveServices.Deployment;
using CognitiveDeploymentArgs = Pulumi.AzureNative.CognitiveServices.DeploymentArgs;
using CognitiveDeploymentModelArgs = Pulumi.AzureNative.CognitiveServices.Inputs.DeploymentModelArgs;
using CognitiveDeploymentPropertiesArgs = Pulumi.AzureNative.CognitiveServices.Inputs.DeploymentPropertiesArgs;
using CognitiveSkuArgs = Pulumi.AzureNative.CognitiveServices.Inputs.SkuArgs;
using KeyVaultSkuArgs = Pulumi.AzureNative.KeyVault.Inputs.SkuArgs;
using KeyVaultSkuName = Pulumi.AzureNative.KeyVault.SkuName;
using KeyVaultSecretArgs = Pulumi.AzureNative.KeyVault.SecretArgs;
using FlexWebApp = Pulumi.AzureNative.Web.V20240401.WebApp;
using FlexWebAppArgs = Pulumi.AzureNative.Web.V20240401.WebAppArgs;
using FlexFunctionAppConfigArgs = Pulumi.AzureNative.Web.V20240401.Inputs.FunctionAppConfigArgs;
using FlexFunctionsDeploymentArgs = Pulumi.AzureNative.Web.V20240401.Inputs.FunctionsDeploymentArgs;
using FlexFunctionsDeploymentAuthenticationArgs = Pulumi.AzureNative.Web.V20240401.Inputs.FunctionsDeploymentAuthenticationArgs;
using FlexFunctionsDeploymentStorageArgs = Pulumi.AzureNative.Web.V20240401.Inputs.FunctionsDeploymentStorageArgs;
using FlexFunctionsRuntimeArgs = Pulumi.AzureNative.Web.V20240401.Inputs.FunctionsRuntimeArgs;
using FlexFunctionsScaleAndConcurrencyArgs = Pulumi.AzureNative.Web.V20240401.Inputs.FunctionsScaleAndConcurrencyArgs;
using FlexManagedServiceIdentityArgs = Pulumi.AzureNative.Web.V20240401.Inputs.ManagedServiceIdentityArgs;
using FlexManagedServiceIdentityType = Pulumi.AzureNative.Web.V20240401.ManagedServiceIdentityType;
using FlexFunctionsDeploymentStorageType = Pulumi.AzureNative.Web.V20240401.FunctionsDeploymentStorageType;
using FlexSiteConfigArgs = Pulumi.AzureNative.Web.V20240401.Inputs.SiteConfigArgs;
using FlexNameValuePairArgs = Pulumi.AzureNative.Web.V20240401.Inputs.NameValuePairArgs;

return await Pulumi.Deployment.RunAsync(() =>
{
    const string StorageBlobDataOwnerRoleDefinitionId = "b7e6dc6d-f1e8-4753-8033-0f276bb0955b";
    const string AzureOpenAiDeploymentName = "gpt-5-mini";
    const string AzureOpenAiModelName = "gpt-5-mini";
    const string AzureOpenAiModelVersion = "2025-08-07";

    var context = AzureContextLoader.Load();
    var tags = context.Tags.ToDictionary(pair => pair.Key, pair => pair.Value);
    var deploymentStorageContainerName = $"app-package-{context.Resources.FunctionApp[..Math.Min(context.Resources.FunctionApp.Length, 24)]}-{context.Sequence.Current.ToLowerInvariant()}";

    var workloadResourceGroup = new ResourceGroup("workload-resource-group", new ResourceGroupArgs
    {
        ResourceGroupName = context.Resources.ResourceGroup,
        Location = context.Location.Name,
        Tags = tags
    });

    var recoveryResourceGroup = new ResourceGroup("recovery-resource-group", new ResourceGroupArgs
    {
        ResourceGroupName = context.Recovery.ResourceGroup,
        Location = context.Location.Name,
        Tags = tags
    });

    var recoveryStorageAccount = new StorageAccountResource("recovery-storage-account", new StorageAccountArgs
    {
        ResourceGroupName = recoveryResourceGroup.Name,
        AccountName = context.Recovery.StorageAccount,
        Location = context.Location.Name,
        Kind = StorageKind.StorageV2,
        Sku = new StorageSkuArgs
        {
            Name = StorageSkuName.Standard_LRS
        },
        AllowBlobPublicAccess = false,
        MinimumTlsVersion = MinimumTlsVersion.TLS1_2,
        Tags = tags
    });

    var recoveryContainer = new BlobContainer("recovery-container", new BlobContainerArgs
    {
        ResourceGroupName = recoveryResourceGroup.Name,
        AccountName = recoveryStorageAccount.Name,
        ContainerName = context.Recovery.Container,
        PublicAccess = PublicAccess.None
    });

    var workloadStorageAccount = new StorageAccountResource("workload-storage-account", new StorageAccountArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        AccountName = context.Resources.StorageAccount,
        Location = context.Location.Name,
        Kind = StorageKind.StorageV2,
        Sku = new StorageSkuArgs
        {
            Name = StorageSkuName.Standard_LRS
        },
        AllowBlobPublicAccess = false,
        MinimumTlsVersion = MinimumTlsVersion.TLS1_2,
        AllowSharedKeyAccess = false,
        Tags = tags
    });

    var workloadDeploymentContainer = new BlobContainer("workload-deployment-container", new BlobContainerArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        AccountName = workloadStorageAccount.Name,
        ContainerName = deploymentStorageContainerName,
        PublicAccess = PublicAccess.None
    });

    var logAnalyticsWorkspace = new Workspace("log-analytics-workspace", new WorkspaceArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        WorkspaceName = context.Resources.LogAnalyticsWorkspace,
        Location = context.Location.Name,
        RetentionInDays = 30,
        Sku = new WorkspaceSkuArgs
        {
            Name = WorkspaceSkuNameEnum.PerGB2018
        },
        Tags = tags
    });

    var appInsights = new InsightsComponent("application-insights", new InsightsComponentArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        ResourceName = context.Resources.AppInsights,
        Location = context.Location.Name,
        ApplicationType = ApplicationType.Web,
        Kind = "web",
        WorkspaceResourceId = logAnalyticsWorkspace.Id,
        Tags = tags
    });

    var aiSearch = new Service("ai-search-service", new ServiceArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        SearchServiceName = context.Resources.AiSearch,
        Location = context.Location.Name,
        Sku = new SearchSkuArgs
        {
            Name = SearchSkuName.Free
        },
        ReplicaCount = 1,
        PartitionCount = 1,
        Tags = tags
    });

    var serviceBusNamespace = new ServiceBusNamespace("service-bus-namespace", new ServiceBusNamespaceArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        NamespaceName = context.Resources.ServiceBusNamespace,
        Location = context.Location.Name,
        Sku = new ServiceBusSkuArgs
        {
            Name = ServiceBusSkuName.Basic,
            Tier = ServiceBusSkuTier.Basic
        },
        MinimumTlsVersion = "1.2",
        PublicNetworkAccess = "Enabled",
        DisableLocalAuth = false,
        Tags = tags
    });

    var approvalRequestsQueue = new ServiceBusQueue("approval-requests-queue", new ServiceBusQueueArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        NamespaceName = serviceBusNamespace.Name,
        QueueName = "approval-requests",
        LockDuration = "PT1M",
        MaxDeliveryCount = 5,
        DeadLetteringOnMessageExpiration = true,
        DefaultMessageTimeToLive = "P14D",
        EnableBatchedOperations = true
    });

    var agentRunEventsQueue = new ServiceBusQueue("agent-run-events-queue", new ServiceBusQueueArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        NamespaceName = serviceBusNamespace.Name,
        QueueName = "agent-run-events",
        LockDuration = "PT1M",
        MaxDeliveryCount = 5,
        DeadLetteringOnMessageExpiration = true,
        DefaultMessageTimeToLive = "P14D",
        EnableBatchedOperations = true
    });

    var workflowDeadletterQueue = new ServiceBusQueue("workflow-deadletter-queue", new ServiceBusQueueArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        NamespaceName = serviceBusNamespace.Name,
        QueueName = "workflow-deadletter",
        LockDuration = "PT1M",
        MaxDeliveryCount = 10,
        DeadLetteringOnMessageExpiration = true,
        DefaultMessageTimeToLive = "P14D",
        EnableBatchedOperations = true
    });

    var serviceBusRuntimeRule = new NamespaceAuthorizationRule("service-bus-runtime-rule", new NamespaceAuthorizationRuleArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        NamespaceName = serviceBusNamespace.Name,
        AuthorizationRuleName = "agentops-runtime",
        Rights =
        {
            "Listen",
            "Send"
        }
    });

    var serviceBusRuntimeKeys = ListNamespaceKeys.Invoke(new ListNamespaceKeysInvokeArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        NamespaceName = serviceBusNamespace.Name,
        AuthorizationRuleName = serviceBusRuntimeRule.Name
    });

    var azureOpenAi = new CognitiveAccount("azure-openai-account", new CognitiveAccountArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        AccountName = context.Resources.AzureOpenAi,
        Location = context.Location.Name,
        Kind = "OpenAI",
        Sku = new CognitiveSkuArgs
        {
            Name = "S0"
        },
        Properties = new CognitiveAccountPropertiesArgs
        {
            CustomSubDomainName = context.Resources.AzureOpenAi,
            PublicNetworkAccess = "Enabled"
        },
        Tags = tags
    });

    var azureOpenAiDeployment = new CognitiveDeployment("azure-openai-chat-deployment", new CognitiveDeploymentArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        AccountName = azureOpenAi.Name,
        DeploymentName = AzureOpenAiDeploymentName,
        Properties = new CognitiveDeploymentPropertiesArgs
        {
            Model = new CognitiveDeploymentModelArgs
            {
                Format = "OpenAI",
                Name = AzureOpenAiModelName,
                Version = AzureOpenAiModelVersion
            }
        },
        Sku = new CognitiveSkuArgs
        {
            Name = "GlobalStandard",
            Capacity = 1
        }
    });

    var azureOpenAiKeys = ListAccountKeys.Invoke(new ListAccountKeysInvokeArgs
    {
        AccountName = azureOpenAi.Name,
        ResourceGroupName = workloadResourceGroup.Name
    });

    var azureOpenAiEndpoint = azureOpenAi.Name.Apply(name => $"https://{name}.openai.azure.com/");

    var clientConfig = Pulumi.AzureNative.Authorization.GetClientConfig.Invoke();

    var keyVault = new Vault("workload-key-vault", new VaultArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        VaultName = context.Resources.KeyVault,
        Location = context.Location.Name,
        Properties = new VaultPropertiesArgs
        {
            TenantId = clientConfig.Apply(config => config.TenantId),
            Sku = new KeyVaultSkuArgs
            {
                Family = SkuFamily.A,
                Name = KeyVaultSkuName.Standard
            },
            EnableRbacAuthorization = true,
            EnableSoftDelete = true,
            SoftDeleteRetentionInDays = 7,
            AccessPolicies = { }
        },
        Tags = tags
    });

    var dataverseApplication = new Application("dataverse-runtime-application", new ApplicationArgs
    {
        DisplayName = $"agentops-dataverse-{context.Environment}-{context.Sequence.Current}"
    });

    var dataverseServicePrincipal = new ServicePrincipal("dataverse-runtime-service-principal", new ServicePrincipalArgs
    {
        ClientId = dataverseApplication.ClientId
    });

    var dataverseClientSecret = new ApplicationPassword("dataverse-runtime-client-secret", new ApplicationPasswordArgs
    {
        ApplicationId = dataverseApplication.Id,
        DisplayName = "runtime"
    });

    var dataverseClientIdSecret = new Secret("dataverse-sp-client-id-secret", new KeyVaultSecretArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        VaultName = keyVault.Name,
        SecretName = "DATAVERSE-SP-CLIENT-ID",
        Properties = new SecretPropertiesArgs
        {
            Value = dataverseApplication.ClientId
        }
    });

    var dataverseClientSecretSecret = new Secret("dataverse-sp-client-secret-secret", new KeyVaultSecretArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        VaultName = keyVault.Name,
        SecretName = "DATAVERSE-SP-CLIENT-SECRET",
        Properties = new SecretPropertiesArgs
        {
            Value = Output.CreateSecret(dataverseClientSecret.Value)
        }
    });

    var dataverseTenantIdSecret = new Secret("dataverse-sp-tenant-id-secret", new KeyVaultSecretArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        VaultName = keyVault.Name,
        SecretName = "DATAVERSE-SP-TENANT-ID",
        Properties = new SecretPropertiesArgs
        {
            Value = clientConfig.Apply(config => config.TenantId)
        }
    });

    var serviceBusConnectionStringSecret = new Secret("service-bus-connection-string-secret", new KeyVaultSecretArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        VaultName = keyVault.Name,
        SecretName = "AZURE-SERVICE-BUS-CONNECTION-STRING",
        Properties = new SecretPropertiesArgs
        {
            Value = Output.CreateSecret(serviceBusRuntimeKeys.Apply(keys => keys.PrimaryConnectionString))
        }
    });

    var azureOpenAiEndpointSecret = new Secret("azure-openai-endpoint-secret", new KeyVaultSecretArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        VaultName = keyVault.Name,
        SecretName = "AZURE-OPENAI-ENDPOINT",
        Properties = new SecretPropertiesArgs
        {
            Value = azureOpenAiEndpoint
        }
    });

    var azureOpenAiApiKeySecret = new Secret("azure-openai-api-key-secret", new KeyVaultSecretArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        VaultName = keyVault.Name,
        SecretName = "AZURE-OPENAI-API-KEY",
        Properties = new SecretPropertiesArgs
        {
            Value = Output.CreateSecret(azureOpenAiKeys.Apply(keys =>
                keys.Key1 ?? throw new InvalidOperationException("Azure OpenAI account did not return key1.")))
        }
    });

    var azureOpenAiDeploymentNameSecret = new Secret("azure-openai-deployment-name-secret", new KeyVaultSecretArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        VaultName = keyVault.Name,
        SecretName = "AZURE-OPENAI-DEPLOYMENT-NAME",
        Properties = new SecretPropertiesArgs
        {
            Value = AzureOpenAiDeploymentName
        }
    });

    var functionPlan = new AppServicePlan("function-app-plan", new AppServicePlanArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        Name = $"plan-{context.Workload.Root}-{context.Environment}-{context.Sequence.Current}",
        Location = context.Location.Name,
        Kind = "functionapp",
        Reserved = true,
        Sku = new SkuDescriptionArgs
        {
            Name = "FC1",
            Tier = "FlexConsumption"
        },
        Tags = tags
    });

    var functionApp = new FlexWebApp("function-app", new FlexWebAppArgs
    {
        ResourceGroupName = workloadResourceGroup.Name,
        Name = context.Resources.FunctionApp,
        Location = context.Location.Name,
        Kind = "FunctionApp,linux",
        Identity = new FlexManagedServiceIdentityArgs
        {
            Type = FlexManagedServiceIdentityType.SystemAssigned
        },
        HttpsOnly = true,
        ServerFarmId = functionPlan.Id,
        FunctionAppConfig = new FlexFunctionAppConfigArgs
        {
            Deployment = new FlexFunctionsDeploymentArgs
            {
                Storage = new FlexFunctionsDeploymentStorageArgs
                {
                    Type = FlexFunctionsDeploymentStorageType.BlobContainer,
                    Value = Output.Format($"https://{workloadStorageAccount.Name}.blob.core.windows.net/{workloadDeploymentContainer.Name}"),
                    Authentication = new FlexFunctionsDeploymentAuthenticationArgs
                    {
                        Type = "SystemAssignedIdentity"
                    }
                }
            },
            Runtime = new FlexFunctionsRuntimeArgs
            {
                Name = "python",
                Version = "3.12"
            },
            ScaleAndConcurrency = new FlexFunctionsScaleAndConcurrencyArgs
            {
                MaximumInstanceCount = 100,
                InstanceMemoryMB = 2048
            }
        },
        SiteConfig = new FlexSiteConfigArgs
        {
            AppSettings =
            {
                new FlexNameValuePairArgs
                {
                    Name = "AzureWebJobsStorage__accountName",
                    Value = workloadStorageAccount.Name
                },
                new FlexNameValuePairArgs
                {
                    Name = "APPLICATIONINSIGHTS_CONNECTION_STRING",
                    Value = appInsights.ConnectionString
                },
                new FlexNameValuePairArgs
                {
                    Name = "MCP_DATA_MODE",
                    Value = "mock"
                }
            }
        },
        Tags = tags
    });

    var workloadStorageBlobOwnerAssignment = new RoleAssignment("function-app-storage-blob-owner", new RoleAssignmentArgs
    {
        PrincipalId = functionApp.Identity.Apply(identity => identity!.PrincipalId!),
        PrincipalType = PrincipalType.ServicePrincipal,
        RoleDefinitionId = Output.Format($"/subscriptions/{context.Subscription.Id}/providers/Microsoft.Authorization/roleDefinitions/{StorageBlobDataOwnerRoleDefinitionId}"),
        Scope = workloadStorageAccount.Id,
        RoleAssignmentName = workloadStorageAccount.Id.Apply(id => GuidUtility.Create(GuidUtility.UrlNamespace, $"{id}:{StorageBlobDataOwnerRoleDefinitionId}").ToString())
    });

    return new Dictionary<string, object?>
    {
        ["subscriptionId"] = context.Subscription.Id,
        ["environment"] = context.Environment,
        ["sequenceCurrent"] = context.Sequence.Current,
        ["workloadResourceGroupName"] = workloadResourceGroup.Name,
        ["workloadStorageAccountName"] = workloadStorageAccount.Name,
        ["logAnalyticsWorkspaceName"] = logAnalyticsWorkspace.Name,
        ["applicationInsightsName"] = appInsights.Name,
        ["aiSearchServiceName"] = aiSearch.Name,
        ["aiSearchEndpoint"] = aiSearch.Name.Apply(name => $"https://{name}.search.windows.net"),
        ["azureOpenAiAccountName"] = azureOpenAi.Name,
        ["azureOpenAiEndpoint"] = azureOpenAiEndpoint,
        ["azureOpenAiDeploymentName"] = azureOpenAiDeployment.Name,
        ["azureOpenAiEndpointSecretName"] = azureOpenAiEndpointSecret.Name,
        ["azureOpenAiApiKeySecretName"] = azureOpenAiApiKeySecret.Name,
        ["azureOpenAiDeploymentNameSecretName"] = azureOpenAiDeploymentNameSecret.Name,
        ["serviceBusNamespaceName"] = serviceBusNamespace.Name,
        ["serviceBusApprovalRequestsQueueName"] = approvalRequestsQueue.Name,
        ["serviceBusAgentRunEventsQueueName"] = agentRunEventsQueue.Name,
        ["serviceBusWorkflowDeadletterQueueName"] = workflowDeadletterQueue.Name,
        ["serviceBusConnectionStringSecretName"] = serviceBusConnectionStringSecret.Name,
        ["keyVaultName"] = keyVault.Name,
        ["dataverseApplicationDisplayName"] = dataverseApplication.DisplayName,
        ["dataverseServicePrincipalObjectId"] = dataverseServicePrincipal.ObjectId,
        ["dataverseSpClientIdSecretName"] = dataverseClientIdSecret.Name,
        ["dataverseSpClientSecretName"] = dataverseClientSecretSecret.Name,
        ["dataverseSpTenantIdSecretName"] = dataverseTenantIdSecret.Name,
        ["functionPlanName"] = functionPlan.Name,
        ["functionAppName"] = functionApp.Name,
        ["functionAppDefaultHostName"] = functionApp.DefaultHostName,
        ["workloadDeploymentContainerName"] = workloadDeploymentContainer.Name,
        ["functionAppStorageRoleAssignmentId"] = workloadStorageBlobOwnerAssignment.Id,
        ["recoveryResourceGroupName"] = recoveryResourceGroup.Name,
        ["recoveryStorageAccountName"] = recoveryStorageAccount.Name,
        ["recoveryContainerName"] = recoveryContainer.Name,
        ["recoveryPathPrefix"] = context.Recovery.PathPrefix
    };
});

