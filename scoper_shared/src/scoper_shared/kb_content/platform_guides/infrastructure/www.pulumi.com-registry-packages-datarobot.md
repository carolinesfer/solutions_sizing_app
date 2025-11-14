[All packages](/registry)

  * [Overview](/registry/packages/datarobot/)
  * [Install & config](/registry/packages/datarobot/installation-configuration/)
  * [API Docs](/registry/packages/datarobot/api-docs/)

  1. [Packages](/registry/)
  2. [DataRobot](/registry/packages/datarobot/)

![datarobot logo](https://raw.githubusercontent.com/datarobot-
community/pulumi-datarobot/main/assets/datarobot-logo.png) __

DataRobot v0.10.23, Nov 12 25

![datarobot logo](https://raw.githubusercontent.com/datarobot-
community/pulumi-datarobot/main/assets/datarobot-logo.png) __

DataRobot v0.10.23, Nov 12 25

DataRobot v0.10.23 published on Wednesday, Nov 12, 2025 by DataRobot, Inc.

__[ Schema (JSON)](/registry/packages/datarobot/schema.json)

__[ datarobot-community/pulumi-datarobot __](https://github.com/datarobot-
community/pulumi-datarobot)

# DataRobot

![datarobot logo](https://raw.githubusercontent.com/datarobot-
community/pulumi-datarobot/main/assets/datarobot-logo.png) __

DataRobot v0.10.23 published on Wednesday, Nov 12, 2025 by DataRobot, Inc.

__[ Schema (JSON)](/registry/packages/datarobot/schema.json)

__[ datarobot-community/pulumi-datarobot __](https://github.com/datarobot-
community/pulumi-datarobot)

## On this page

## On this page

  * [ __Edit this Page](https://github.com/datarobot-community/pulumi-datarobot/blob/v0.10.23/docs/_index.md)
  * [ __Request a Change](https://github.com/pulumi/registry/issues/new?body=File: \[themes%2fdefault%2fcontent/%2fregistry%2fpackages%2fdatarobot\]\(https%3a%2f%2fwww.pulumi.com%2fregistry%2fpackages%2fdatarobot%2f\))

The `DataRobot` provider for Pulumi can be used to provision any of the
resources available with [DataRobot](https://www.datarobot.com/).

## Example

    
    
    import pulumi_datarobot as datarobot
    import pulumi
    
    use_case = datarobot.UseCase("example fom python",
                                name="example use case",
                                description="pulumi"
    )
    
    playground = datarobot.Playground("playground",
                                    name="example playground",
                                    use_case_id=use_case.id,
    )
    
    
    
    name: yaml
    runtime: yaml
    description: Example using Pulumi YAML 
    config: {'pulumi:tags': {value: {'pulumi:template': yaml}}}
    resources:
      datarobotUseCase:
        type: datarobot:UseCase
        properties:
          name: Pulumi YAML Example
          description: Example using Pulumi YAML
    
    
    
    import * as datarobot from "@datarobot/pulumi-datarobot";
    
    const useCase = new datarobot.UseCase("example from Typescript", {
        name: "example from TypeScript",
        description: "An example use case from Typescript",
    });
    

![datarobot logo](https://raw.githubusercontent.com/datarobot-
community/pulumi-datarobot/main/assets/datarobot-logo.png) __

DataRobot v0.10.23 published on Wednesday, Nov 12, 2025 by DataRobot, Inc.

__[ Schema (JSON)](/registry/packages/datarobot/schema.json)

__[ datarobot-community/pulumi-datarobot __](https://github.com/datarobot-
community/pulumi-datarobot)

## On this page

## On this page

  * [ __Edit this Page](https://github.com/datarobot-community/pulumi-datarobot/blob/v0.10.23/docs/_index.md)
  * [ __Request a Change](https://github.com/pulumi/registry/issues/new?body=File: \[themes%2fdefault%2fcontent/%2fregistry%2fpackages%2fdatarobot\]\(https%3a%2f%2fwww.pulumi.com%2fregistry%2fpackages%2fdatarobot%2f\))

[![Meet Neo: Your AI Platform
Teammate](https://www.pulumi.com/images/docs/ad/neo-postlaunch-
ad.png)](/product/neo#video)

