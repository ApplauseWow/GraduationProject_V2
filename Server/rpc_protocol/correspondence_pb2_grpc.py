# -*-coding:utf-8-*-
# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import correspondence_pb2 as correspondence__pb2


class BackendStub(object):
    """Missing associated documentation comment in .proto file"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SayHello = channel.unary_unary(
                '/Backend/SayHello',
                request_serializer=correspondence__pb2.HelloRequest.SerializeToString,
                response_deserializer=correspondence__pb2.HelloResponse.FromString,
                )
        self.SayHelloAgain = channel.unary_unary(
                '/Backend/SayHelloAgain',
                request_serializer=correspondence__pb2.HelloRequest.SerializeToString,
                response_deserializer=correspondence__pb2.HelloResponse.FromString,
                )
        self.GetRecordsCount = channel.unary_unary(
                '/Backend/GetRecordsCount',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.GetAllNotes = channel.unary_unary(
                '/Backend/GetAllNotes',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.InsertANote = channel.unary_unary(
                '/Backend/InsertANote',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.ModifyTheNote = channel.unary_unary(
                '/Backend/ModifyTheNote',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.VoidTheNote = channel.unary_unary(
                '/Backend/VoidTheNote',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.GetAllUsers = channel.unary_unary(
                '/Backend/GetAllUsers',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.DeleteTheUser = channel.unary_unary(
                '/Backend/DeleteTheUser',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.InsertAUser = channel.unary_unary(
                '/Backend/InsertAUser',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.ModifyTheUser = channel.unary_unary(
                '/Backend/ModifyTheUser',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.GetTheUser = channel.unary_unary(
                '/Backend/GetTheUser',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.GetWorkHourEverYDay = channel.unary_unary(
                '/Backend/GetWorkHourEverYDay',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.GetClockInOrOutTimeStamp = channel.unary_unary(
                '/Backend/GetClockInOrOutTimeStamp',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.GetClockInOrOutCountEachHour = channel.unary_unary(
                '/Backend/GetClockInOrOutCountEachHour',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.GetClockInRateToday = channel.unary_unary(
                '/Backend/GetClockInRateToday',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.CheckIdentityByFace = channel.unary_unary(
                '/Backend/CheckIdentityByFace',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.Register = channel.unary_unary(
                '/Backend/Register',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.ClockInOrOut = channel.unary_unary(
                '/Backend/ClockInOrOut',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.DeploySeats = channel.unary_unary(
                '/Backend/DeploySeats',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.GetSeatsDeployment = channel.unary_unary(
                '/Backend/GetSeatsDeployment',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.GetSeatsArrangement = channel.unary_unary(
                '/Backend/GetSeatsArrangement',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.GetTheSeatArrangement = channel.unary_unary(
                '/Backend/GetTheSeatArrangement',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.DeleteTheArrangement = channel.unary_unary(
                '/Backend/DeleteTheArrangement',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.GetAllStudents = channel.unary_unary(
                '/Backend/GetAllStudents',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )
        self.ArrangeTheStudentHere = channel.unary_unary(
                '/Backend/ArrangeTheStudentHere',
                request_serializer=correspondence__pb2.RequestStruct.SerializeToString,
                response_deserializer=correspondence__pb2.ResponseStruct.FromString,
                )


class BackendServicer(object):
    """Missing associated documentation comment in .proto file"""

    def SayHello(self, request, context):
        """测试接口
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SayHelloAgain(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetRecordsCount(self, request, context):
        """正式接口
        ->数据交互相关接口
        ->->共用接口
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllNotes(self, request, context):
        """->->公告相关接口
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def InsertANote(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ModifyTheNote(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VoidTheNote(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllUsers(self, request, context):
        """->->用户相关接口
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteTheUser(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def InsertAUser(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ModifyTheUser(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTheUser(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetWorkHourEverYDay(self, request, context):
        """->->考勤统计相关接口
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetClockInOrOutTimeStamp(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetClockInOrOutCountEachHour(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetClockInRateToday(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CheckIdentityByFace(self, request, context):
        """->人脸相关接口
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Register(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClockInOrOut(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeploySeats(self, request, context):
        """工位相关
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSeatsDeployment(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSeatsArrangement(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTheSeatArrangement(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteTheArrangement(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllStudents(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ArrangeTheStudentHere(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BackendServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SayHello': grpc.unary_unary_rpc_method_handler(
                    servicer.SayHello,
                    request_deserializer=correspondence__pb2.HelloRequest.FromString,
                    response_serializer=correspondence__pb2.HelloResponse.SerializeToString,
            ),
            'SayHelloAgain': grpc.unary_unary_rpc_method_handler(
                    servicer.SayHelloAgain,
                    request_deserializer=correspondence__pb2.HelloRequest.FromString,
                    response_serializer=correspondence__pb2.HelloResponse.SerializeToString,
            ),
            'GetRecordsCount': grpc.unary_unary_rpc_method_handler(
                    servicer.GetRecordsCount,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'GetAllNotes': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllNotes,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'InsertANote': grpc.unary_unary_rpc_method_handler(
                    servicer.InsertANote,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'ModifyTheNote': grpc.unary_unary_rpc_method_handler(
                    servicer.ModifyTheNote,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'VoidTheNote': grpc.unary_unary_rpc_method_handler(
                    servicer.VoidTheNote,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'GetAllUsers': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllUsers,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'DeleteTheUser': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteTheUser,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'InsertAUser': grpc.unary_unary_rpc_method_handler(
                    servicer.InsertAUser,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'ModifyTheUser': grpc.unary_unary_rpc_method_handler(
                    servicer.ModifyTheUser,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'GetTheUser': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTheUser,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'GetWorkHourEverYDay': grpc.unary_unary_rpc_method_handler(
                    servicer.GetWorkHourEverYDay,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'GetClockInOrOutTimeStamp': grpc.unary_unary_rpc_method_handler(
                    servicer.GetClockInOrOutTimeStamp,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'GetClockInOrOutCountEachHour': grpc.unary_unary_rpc_method_handler(
                    servicer.GetClockInOrOutCountEachHour,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'GetClockInRateToday': grpc.unary_unary_rpc_method_handler(
                    servicer.GetClockInRateToday,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'CheckIdentityByFace': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckIdentityByFace,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'Register': grpc.unary_unary_rpc_method_handler(
                    servicer.Register,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'ClockInOrOut': grpc.unary_unary_rpc_method_handler(
                    servicer.ClockInOrOut,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'DeploySeats': grpc.unary_unary_rpc_method_handler(
                    servicer.DeploySeats,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'GetSeatsDeployment': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSeatsDeployment,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'GetSeatsArrangement': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSeatsArrangement,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'GetTheSeatArrangement': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTheSeatArrangement,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'DeleteTheArrangement': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteTheArrangement,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'GetAllStudents': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllStudents,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
            'ArrangeTheStudentHere': grpc.unary_unary_rpc_method_handler(
                    servicer.ArrangeTheStudentHere,
                    request_deserializer=correspondence__pb2.RequestStruct.FromString,
                    response_serializer=correspondence__pb2.ResponseStruct.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Backend', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Backend(object):
    """Missing associated documentation comment in .proto file"""

    @staticmethod
    def SayHello(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/SayHello',
            correspondence__pb2.HelloRequest.SerializeToString,
            correspondence__pb2.HelloResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SayHelloAgain(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/SayHelloAgain',
            correspondence__pb2.HelloRequest.SerializeToString,
            correspondence__pb2.HelloResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetRecordsCount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/GetRecordsCount',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAllNotes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/GetAllNotes',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def InsertANote(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/InsertANote',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ModifyTheNote(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/ModifyTheNote',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def VoidTheNote(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/VoidTheNote',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAllUsers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/GetAllUsers',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteTheUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/DeleteTheUser',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def InsertAUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/InsertAUser',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ModifyTheUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/ModifyTheUser',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTheUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/GetTheUser',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetWorkHourEverYDay(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/GetWorkHourEverYDay',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetClockInOrOutTimeStamp(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/GetClockInOrOutTimeStamp',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetClockInOrOutCountEachHour(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/GetClockInOrOutCountEachHour',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetClockInRateToday(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/GetClockInRateToday',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CheckIdentityByFace(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/CheckIdentityByFace',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Register(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/Register',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ClockInOrOut(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/ClockInOrOut',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeploySeats(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/DeploySeats',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSeatsDeployment(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/GetSeatsDeployment',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSeatsArrangement(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/GetSeatsArrangement',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTheSeatArrangement(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/GetTheSeatArrangement',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteTheArrangement(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/DeleteTheArrangement',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAllStudents(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/GetAllStudents',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ArrangeTheStudentHere(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/ArrangeTheStudentHere',
            correspondence__pb2.RequestStruct.SerializeToString,
            correspondence__pb2.ResponseStruct.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
