"""A Crossplane composition function."""

import grpc
from prettyprinter import pformat

from crossplane.function import logging, resource, response
from crossplane.function.proto.v1 import run_function_pb2 as fnv1
from crossplane.function.proto.v1 import run_function_pb2_grpc as grpcv1
from google.protobuf.json_format import MessageToDict


class FunctionRunner(grpcv1.FunctionRunnerService):

    def __init__(self):
        self.log = logging.get_logger()

    async def RunFunction(
        self, req: fnv1.RunFunctionRequest, _: grpc.aio.ServicerContext
    ) -> fnv1.RunFunctionResponse:
        log = self.log.bind(tag=req.meta.tag)
        log.info("Called with RunFunctionRequest:")

        if req.input and "spec" in req.input:
            print(pformat(MessageToDict(req, preserving_proto_field_name=True), depth=req.input["spec"]["depth"]))
        else:
            print(pformat(MessageToDict(req, preserving_proto_field_name=True)))

        rsp = response.to(req)
        return rsp
