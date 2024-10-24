# function-debug

This function is useful if you're getting started using crossplane functions and/or writing compositions and are
wondering what data is available to you. This function simply prints out the RunFunctionRequest object that gets passed
to it.

Embed this function once or multiple times in your function pipeline and tail the logs.

## Install manifest

    apiVersion: pkg.crossplane.io/v1beta1
    kind: Function
    metadata:
      name: function-debug
    spec:
      package: xpkg.upbound.io/modulo2/function-debug:v0.1.0

## Example pipeline with input

    apiVersion: apiextensions.crossplane.io/v1
    kind: Composition
    metadata:
      name: s3buckets
      labels:
        provider: aws
    spec:
      compositeTypeRef:
        apiVersion: s3.modulo2.nl/v1alpha1
        kind: S3Bucket
      mode: Pipeline
      pipeline:
        - step: environmentConfigs
          functionRef:
            name: function-environment-configs
          input:
            apiVersion: environmentconfigs.fn.crossplane.io/v1beta1
            kind: Input
            spec:
              environmentConfigs:
                - ref:
                    name: aws
        - step: create-bucket
          functionRef:
            name: function-go-templating
          input:
            ...
        - step: debug
          functionRef:
            name: function-debug
          input:
            apiVersion: function-debug.fn.crossplane.io/v1beta1
            kind: Input
            spec:
              depth: 3

## Example output

    {"tag": "", "level": "info", "lineno": 21, "filename": "fn.py", "ts": 1729766405.5250773, "msg": "Called with RunFunctionRequest:"}
    {
        'observed': {
            'composite': {'resource': {...}},
            'resources': {
                'policy': {...},
                'bucket-lifecycle': {...},
                'bucket': {...},
                'serversideencryption': {...},
                'versioning': {...}
            }
        },
        'desired': {
            'composite': {'resource': {...}},
            'resources': {'bucket': {...}}
        },
        'input': {
            'kind': 'Input',
            'apiVersion': 'debug.fn.crossplane.io/v1alpha1',
            'spec': {'depth': float(...)}
        },
        'context': {
            'apiextensions.crossplane.io/environment': {
                'kind': str(...),
                'aws.account-id': str(...),
            }
        }
    }