using System.Text.Json.Serialization;

namespace EnterpriseAgentOps.Infrastructure;

public sealed class AzureContext
{
    [JsonPropertyName("subscription")]
    public required SubscriptionContext Subscription { get; init; }

    [JsonPropertyName("workload")]
    public required WorkloadContext Workload { get; init; }

    [JsonPropertyName("environment")]
    public required string Environment { get; init; }

    [JsonPropertyName("location")]
    public required LocationContext Location { get; init; }

    [JsonPropertyName("sequence")]
    public required SequenceContext Sequence { get; init; }

    [JsonPropertyName("lifecycle")]
    public required LifecycleContext Lifecycle { get; init; }

    [JsonPropertyName("tags")]
    public required Dictionary<string, string> Tags { get; init; }

    [JsonPropertyName("recovery")]
    public required RecoveryContext Recovery { get; init; }

    [JsonPropertyName("bootstrapData")]
    public required BootstrapDataContext BootstrapData { get; init; }

    [JsonPropertyName("resources")]
    public required ResourceNamesContext Resources { get; init; }
}

public sealed class SubscriptionContext
{
    [JsonPropertyName("id")]
    public required string Id { get; init; }

    [JsonPropertyName("name")]
    public required string Name { get; init; }
}

public sealed class WorkloadContext
{
    [JsonPropertyName("root")]
    public required string Root { get; init; }

    [JsonPropertyName("description")]
    public required string Description { get; init; }
}

public sealed class LocationContext
{
    [JsonPropertyName("name")]
    public required string Name { get; init; }

    [JsonPropertyName("short")]
    public required string Short { get; init; }
}

public sealed class SequenceContext
{
    [JsonPropertyName("current")]
    public required string Current { get; init; }

    [JsonPropertyName("next")]
    public required string Next { get; init; }

    [JsonPropertyName("padTo")]
    public required int PadTo { get; init; }

    [JsonPropertyName("incrementOnDecommission")]
    public required bool IncrementOnDecommission { get; init; }
}

public sealed class LifecycleContext
{
    [JsonPropertyName("environmentMode")]
    public required string EnvironmentMode { get; init; }

    [JsonPropertyName("destroyWholeResourceGroup")]
    public required bool DestroyWholeResourceGroup { get; init; }

    [JsonPropertyName("restoreFromRecoveryOnProvision")]
    public required bool RestoreFromRecoveryOnProvision { get; init; }

    [JsonPropertyName("exportStateBeforeDestroy")]
    public required bool ExportStateBeforeDestroy { get; init; }
}

public sealed class RecoveryContext
{
    [JsonPropertyName("enabled")]
    public required bool Enabled { get; init; }

    [JsonPropertyName("subscription")]
    public required SubscriptionContext Subscription { get; init; }

    [JsonPropertyName("resourceGroup")]
    public required string ResourceGroup { get; init; }

    [JsonPropertyName("storageAccount")]
    public required string StorageAccount { get; init; }

    [JsonPropertyName("container")]
    public required string Container { get; init; }

    [JsonPropertyName("pathPrefix")]
    public required string PathPrefix { get; init; }
}

public sealed class BootstrapDataContext
{
    [JsonPropertyName("ingestOnProvision")]
    public required bool IngestOnProvision { get; init; }

    [JsonPropertyName("localSeedPaths")]
    public required List<string> LocalSeedPaths { get; init; }

    [JsonPropertyName("recoveryBlobFolders")]
    public required List<string> RecoveryBlobFolders { get; init; }
}

public sealed class ResourceNamesContext
{
    [JsonPropertyName("resourceGroup")]
    public required string ResourceGroup { get; init; }

    [JsonPropertyName("storageAccount")]
    public required string StorageAccount { get; init; }

    [JsonPropertyName("functionApp")]
    public required string FunctionApp { get; init; }

    [JsonPropertyName("appInsights")]
    public required string AppInsights { get; init; }

    [JsonPropertyName("logAnalyticsWorkspace")]
    public required string LogAnalyticsWorkspace { get; init; }

    [JsonPropertyName("keyVault")]
    public required string KeyVault { get; init; }

    [JsonPropertyName("serviceBusNamespace")]
    public required string ServiceBusNamespace { get; init; }

    [JsonPropertyName("aiSearch")]
    public required string AiSearch { get; init; }

    [JsonPropertyName("azureOpenAi")]
    public required string AzureOpenAi { get; init; }

    [JsonPropertyName("threadStateTable")]
    public string ThreadStateTable { get; init; } = "AgentThreadState";
}
