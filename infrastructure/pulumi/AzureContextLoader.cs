using System.Text.Json;

namespace EnterpriseAgentOps.Infrastructure;

public static class AzureContextLoader
{
    public static AzureContext Load()
    {
        var contextPath = ResolveContextPath();
        if (!File.Exists(contextPath))
        {
            throw new FileNotFoundException(
                $"Azure context file not found. Run infrastructure/scripts/Initialize-AzureContext.ps1 first. Expected path: {contextPath}");
        }

        var json = File.ReadAllText(contextPath);
        var context = JsonSerializer.Deserialize<AzureContext>(
            json,
            new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = false
            });

        if (context is null)
        {
            throw new InvalidOperationException($"Failed to deserialize Azure context JSON from '{contextPath}'.");
        }

        Validate(context, contextPath);
        return context;
    }

    private static string ResolveContextPath()
    {
        var projectDirectory = AppContext.BaseDirectory;
        var root = Path.GetFullPath(Path.Combine(projectDirectory, "..", "..", "..", ".."));
        return Path.Combine(root, "config", "azure-context.json");
    }

    private static void Validate(AzureContext context, string contextPath)
    {
        if (string.IsNullOrWhiteSpace(context.Resources.ResourceGroup))
        {
            throw new InvalidOperationException($"The Azure context file '{contextPath}' is missing resources.resourceGroup.");
        }

        if (string.IsNullOrWhiteSpace(context.Recovery.ResourceGroup) ||
            string.IsNullOrWhiteSpace(context.Recovery.StorageAccount) ||
            string.IsNullOrWhiteSpace(context.Recovery.Container))
        {
            throw new InvalidOperationException(
                $"The Azure context file '{contextPath}' is missing required recovery settings.");
        }
    }
}
