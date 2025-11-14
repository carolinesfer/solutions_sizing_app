## Modern Infrastructure as Code for Microsoft Azure

Pulumi brings Infrastructure as Code to Azure using familiar programming
languages. Manage 100% of your Azure resources, including compute, containers,
and serverless with C#, Python, Go, TypeScript, and more. Replace or
interoperate with Azure Resource Manager (ARM) templates using Pulumi’s modern
SDKs.

[Get Started](/docs/iac/get-started/azure/) [Try Pulumi Cloud for
FREE](https://app.pulumi.com/signup)

  * C#

  * TypeScript

  * Python

  * Go

  * YAML

  * Java

  * 

    
    
    using Pulumi;
    using Pulumi.AzureNative.Resources;
    using Pulumi.AzureNative.Storage;
    using Pulumi.AzureNative.Storage.Inputs;
    
    class MyStack : Stack
    {
        public MyStack()
        {
            var resourceGroup = new ResourceGroup("resourceGroup");
    
            var storageAccount = new StorageAccount("sa", new StorageAccountArgs
            {
                ResourceGroupName = resourceGroup.Name,
                Sku = new SkuArgs { Name = "Standard_LRS" },
                Kind = "StorageV2"
            });
        }
    }
    
    
    
    import * as resources from "@pulumi/azure-native/resources";
    import * as storage from "@pulumi/azure-native/storage";
    
    const resourceGroup = new resources.ResourceGroup("resourceGroup");
    
    const storageAccount = new storage.StorageAccount("sa", {
        resourceGroupName: resourceGroup.name,
        sku: {
            name: "Standard_LRS",
        },
        kind: "StorageV2",
    });
    
    
    
    from pulumi_azure_native import storage
    from pulumi_azure_native import resources
    
    resource_group = resources.ResourceGroup('resource_group')
    
    account = storage.StorageAccount('sa',
        resource_group_name=resource_group.name,
        sku=storage.SkuArgs(name='Standard_LRS'),
        kind='StorageV2')
    
    
    
    package main
    
    import (
        "github.com/pulumi/pulumi-azure-native/sdk/go/azure/resources"
        "github.com/pulumi/pulumi-azure-native/sdk/go/azure/storage"
        "github.com/pulumi/pulumi/sdk/v2/go/pulumi"
    )
    
    func main() {
        pulumi.Run(func(ctx *pulumi.Context) error {
            resourceGroup, err := resources.NewResourceGroup(ctx, "resourceGroup", nil)
            if err != nil {
                return err
            }
    
            account, err := storage.NewStorageAccount(ctx, "sa", &storage.StorageAccountArgs{
                ResourceGroupName: resourceGroup.Name,
                Sku: &storage.SkuArgs{
                    Name: pulumi.String("Standard_LRS"),
                },
                Kind: pulumi.String("StorageV2"),
            })
    
            return err
        })
    }
    
    
    
    name: azure-storage-account
    runtime: yaml
    description: A simple Pulumi program.
    resources:
      resourcegroup:
        type: azure-native:resources:ResourceGroup
      sa:
        type: azure-native:storage:StorageAccount
        properties:
          resourceGroupName: ${resourcegroup.name}
          kind: 'StorageV2'
          sku: { name: 'Standard_LRS' }
    
    
    
    package com.pulumi.example.infra;
    
    import com.pulumi.Context;
    import com.pulumi.Exports;
    import com.pulumi.Pulumi;
    import com.pulumi.azurenative.resources.ResourceGroup;
    import com.pulumi.azurenative.storage.StorageAccount;
    import com.pulumi.azurenative.storage.StorageAccountArgs;
    import com.pulumi.azurenative.storage.enums.Kind;
    import com.pulumi.azurenative.storage.enums.SkuName;
    import com.pulumi.azurenative.storage.inputs.SkuArgs;
    
    public class Main {
    
        public static void main(String[] args) {
            Pulumi.run(Main::stack);
        }
    
        private static Exports stack(Context ctx) {
            var resourceGroup = new ResourceGroup("linux-fn-rg");
    
            var storageAccount = new StorageAccount("linux-fn-sa", StorageAccountArgs.builder()
                    .resourceGroupName(resourceGroup.name())
                    .kind(Kind.StorageV2)
                    .sku(SkuArgs.builder()
                            .name(SkuName.Standard_LRS)
                            .build())
                    .build());
    
            return ctx.exports();
        }
    }
    

![](/logos/tech/java.svg)

![](/images/partners/azure-insights.png)

### Azure Infrastructure in any Programming Language

  * Define infrastructure in JavaScript, TypeScript, Python, Go, Java, YAML, or any .NET language, including C#, F#, and VB.
  * Increase your productivity using the full ecosystem of dev tools such as IDE auto-completion, type & error checking, linting, refactoring, and test frameworks to validate all of your Azure resources.
  * Keep your cloud secure and in compliance by enforcing policies on every deployment.
  * Codify best practices and policies, then share them with your team or community as self-service architectures.

[Try Pulumi Cloud for FREE](https://app.pulumi.com/signup)

### ARM → Pulumi

Whether you’re new to Microsoft Azure or already using it to manage your
infrastructure, Pulumi makes getting started easy. If you’re just starting
out, you can write your infrastructure code using the Pulumi Azure SDK. Or if
you’re already managing resources with Azure, you can deploy an existing ARM
template using Pulumi or you can rewrite the ARM template JSON in a
programming language, either entirely, or one resource at a time.

If you can deploy a resource with ARM templates, you can deploy it with the
Pulumi Azure provider!

[Learn More](/docs/iac/adopting-pulumi/migrating-to-pulumi/from-arm/)

![](/images/partners/arm2pulumi.png)

### 100% API Coverage

The Pulumi Azure provider covers 100% of the resources available in Azure
Resource Manager giving you the full power of Azure at your fingertips. Every
property of each resource is always represented in the SDKs.

##### Everything In One Place

The SDKs include full coverage for Azure services, including Azure Static Web
Apps, Azure Synapse Analytics, Azure Logic Apps, Azure Service Fabric, Azure
Blockchain Service, Azure API Management, and dozens of other services.

##### Efficient Adoption

There’s no need to rewrite your existing Azure configurations to get started
with Pulumi. You can efficiently adopt existing Azure resources to deploy your
application to yourself save time and effort.

##### Secrets Management

Use Pulumi to ensure secret data is encrypted in transit, at rest, and
physically anywhere it gets stored. Bring your own preferred cloud encryption
provider or use Pulumi’s native secrets provider.

##### Multi Cloud

Pulumi allows you to use top programming languages across all public clouds
with support for over +170 popular cloud and service integrations, including
private and hybrid clouds helping ensure any multi-cloud strategy is
successful.

##### Convenience Functions

The provider also contains functions to retrieve keys, secrets, and connection
strings from all resources that expose them.

##### Automate Delivery

You can integrate Pulumi directly with your favorite CI/CD and SCM systems to
continuously deliver Azure infrastructure and applications. Improve the
velocity and visibility into your deployments from simple to complex global
environments.

[Try Pulumi Cloud for FREE](https://app.pulumi.com/signup)

### Always Up to Date

Pulumi’s Microsoft Azure Native provider is designed to stay up-to-date with
additions and changes to Azure APIs. The `azure-native` SDK is generated
automatically from the Azure API specifications published by Microsoft, which
means you’ll always have access to the latest Azure features and improvements.

##### Auto Generated

An automated pipeline releases updated resources within hours after any
current API specifications are merged. Auto-generated means less manual
implementation and fewer chances for bugs, meaning a high fidelity, high
quality experience.

##### Familiar Concepts

Azure Resource Manager API is structured around Resource Providers — high-
level groups like `storage`, `compute`, or `web`. We map Resource Providers to
top-level modules or namespaces in Pulumi SDKs.

##### API Versions

Each resource provider defines one or more API versions, for example,
`2015-05-01`, `2020-09-01`, or `2020-08-01-preview`. Every version of every
ARM API is available in Pulumi SDKs, and each version has its own module or
namespace.

##### All Languages

The Pulumi Azure Native provider is available in all Pulumi languages,
including JavaScript, TypeScript, Python, Go, .NET, Java, and YAML. All SDKs
are open source on GitHub and available as npm, NuGet, PyPI, and Go modules.

##### Built-in Guardrails

When you enable Pulumi’s Policy as Code feature, you instantly gain the power
to prevent mistakes from being deployed. Enforce security, compliance, cost
controls, and best practices using policies defined in modern languages.

##### Reduce Deployment Complexity

Pulumi lets you take advantage of common tools, frameworks, and techniques to
unit, integration, and property test your Azure infrastructure. Ensure your
infrastructure is correct before and after deployment.

[Try Pulumi Cloud for FREE](https://app.pulumi.com/signup)

## Need Help?

##### Need technical help?

Use our Support Portal to get in touch.

[Submit support ticket](https://support.pulumi.com/)

##### Need help getting started?

Send us a note, and someone will reach out to help you.

[Get help](/contact/?form=onboarding)

##### Want a demo?

Talk with an expert to see how Pulumi fits your use case.

[Request a demo](/request-a-demo/)

##### Something else on your mind?

Send us a note.

[Ask a question](/contact/?form=general)

