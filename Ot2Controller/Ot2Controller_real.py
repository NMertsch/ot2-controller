"""
________________________________________________________________________

:PROJECT: SiLA2_python

*OT-2 Controller*

:details: Ot2Controller:
    A SiLA 2 complaint controller for an OT-2 Liquid Handler robot.

:file:    Ot2Controller_real.py
:authors: Florian Bauer <florian.bauer.dev@gmail.com>

:date: (creation)          2020-08-16T15:26:46.856669
:date: (last modification) 2020-08-16T15:26:46.856669

.. note:: Code generated by sila2codegenerator 0.2.0

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

__version__ = "0.0.1"

# import general packages
import logging
import time  # used for observables
import uuid  # used for observables
import grpc  # used for type hinting only
import paramiko  # used for SSH
# import SiLA2 library
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2

# import gRPC modules for this feature
from .gRPC import Ot2Controller_pb2 as Ot2Controller_pb2
# from .gRPC import Ot2Controller_pb2_grpc as Ot2Controller_pb2_grpc

# import default arguments
from .Ot2Controller_default_arguments import default_dict


# noinspection PyPep8Naming,PyUnusedLocal
class Ot2ControllerReal:
    """
    Implementation of the *OT-2 Controller* in *Real* mode
        A SiLA 2 service enabling the execution of python protocols on a Opentrons 2 liquid handler robot.
    """

    def __init__(self):
        """Class initialiser"""

        logging.debug('Started server in mode: {mode}'.format(mode='Real'))

    def _get_command_state(self, command_uuid: str) -> silaFW_pb2.ExecutionInfo:
        """
        Method to fill an ExecutionInfo message from the SiLA server for observable commands

        :param command_uuid: The uuid of the command for which to return the current state

        :return: An execution info object with the current command state
        """

        #: Enumeration of silaFW_pb2.ExecutionInfo.CommandStatus
        command_status = silaFW_pb2.ExecutionInfo.CommandStatus.waiting
        #: Real silaFW_pb2.Real(0...1)
        command_progress = None
        #: Duration silaFW_pb2.Duration(seconds=<seconds>, nanos=<nanos>)
        command_estimated_remaining = None
        #: Duration silaFW_pb2.Duration(seconds=<seconds>, nanos=<nanos>)
        command_lifetime_of_execution = None

        # TODO: check the state of the command with the given uuid and return the correct information

        # just return a default in this example
        return silaFW_pb2.ExecutionInfo(
            commandStatus=command_status,
            progressInfo=(
                command_progress if command_progress is not None else None
            ),
            estimatedRemainingTime=(
                command_estimated_remaining if command_estimated_remaining is not None else None
            ),
            updatedLifetimeOfExecution=(
                command_lifetime_of_execution if command_lifetime_of_execution is not None else None
            )
        )

    def UploadProtocol(self, request, context: grpc.ServicerContext) \
            -> Ot2Controller_pb2.UploadProtocol_Responses:
        """
        Executes the unobservable command "Upload Protocol"
            Uploads the given Protocol to the OT-2.
    
        :param request: gRPC request containing the parameters passed:
            request.ProtocolSourcePath (Protocol Source Path): The path to the Protocol to upload.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: The return object defined for the command with the following fields:
            request.EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """

        # initialise the return value
        return_value = None

        # TODO:
        #   Add implementation of Real for command UploadProtocol here and write the resulting response
        #   in return_value

        # fallback to default
        if return_value is None:
            return_value = Ot2Controller_pb2.UploadProtocol_Responses(
                **default_dict['UploadProtocol_Responses']
            )

        return return_value

    def RemoveProtocol(self, request, context: grpc.ServicerContext) \
            -> Ot2Controller_pb2.RemoveProtocol_Responses:
        """
        Executes the unobservable command "Remove Protocol"
            Removes the given Protocol to the OT-2.
    
        :param request: gRPC request containing the parameters passed:
            request.ProtocolFile (Protocol File): The file name of the Protocol to remove.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: The return object defined for the command with the following fields:
            request.EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """

        # initialise the return value
        return_value = None

        # TODO:
        #   Add implementation of Real for command RemoveProtocol here and write the resulting response
        #   in return_value

        # fallback to default
        if return_value is None:
            return_value = Ot2Controller_pb2.RemoveProtocol_Responses(
                **default_dict['RemoveProtocol_Responses']
            )

        return return_value

    def RunProtocol(self, request, context: grpc.ServicerContext) \
            -> Ot2Controller_pb2.RunProtocol_Responses:
        """
        Executes the unobservable command "Run Protocol"
            Runs the given Protocol on the OT-2.
    
        :param request: gRPC request containing the parameters passed:
            request.ProtocolFile (Protocol File): The file name of the Protocol to run.
            request.IsSimulating (Is Simulating): Defines whether the protocol gets just simulated or actually executed.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: The return object defined for the command with the following fields:
            request.ReturnValue (Return Value): The returned value.
        """

        # initialise the return value
        return_value = None

        # TODO:
        #   Add implementation of Real for command RunProtocol here and write the resulting response
        #   in return_value

        # fallback to default
        if return_value is None:
            return_value = Ot2Controller_pb2.RunProtocol_Responses(
                **default_dict['RunProtocol_Responses']
            )

        return return_value

    def Get_Connection(self, request, context: grpc.ServicerContext) \
            -> Ot2Controller_pb2.Get_Connection_Responses:
        """
        Requests the unobservable property Connection
            Connection details to the remote OT-2.
    
        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: A response object with the following fields:
            request.Connection (Connection): Connection details to the remote OT-2.
        """

        # initialise the return value
        return_value: Ot2Controller_pb2.Get_Connection_Responses = None

        # TODO:
        #   Add implementation of Real for property Connection here and write the resulting response
        #   in return_value

        # fallback to default
        if return_value is None:
            return_value = Ot2Controller_pb2.Get_Connection_Responses(
                **default_dict['Get_Connection_Responses']
            )

        return return_value

    def Get_InstalledProtocols(self, request, context: grpc.ServicerContext) \
            -> Ot2Controller_pb2.Get_InstalledProtocols_Responses:
        """
        Requests the unobservable property Installed Protocols
            List of the available Protocols already installed on the OT-2.
    
        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: A response object with the following fields:
            request.InstalledProtocols (Installed Protocols): List of the available Protocols already installed on the OT-2.
        """

        # initialize the return value
        return_value: Ot2Controller_pb2.Get_InstalledProtocols_Responses = None

        ot2_device_ip = "127.0.0.1"
        router_username = ""
        router_password = ""
        local_test_path = "~/dummy"
        user_storage_dir = local_test_path + "/data/user_storage"
        jupyter_notebooks_dir = local_test_path + "/var/lib/jupyter/notebooks"

        ssh = paramiko.SSHClient()
        # Load SSH host keys.
        ssh.load_system_host_keys()
        # Add SSH host key automatically if needed.
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Connect to router using username/password authentication.
        ssh.connect(ot2_device_ip,
                    username=router_username,
                    password=router_password,
                    look_for_keys=False)

        # Run command.
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("ls " + user_storage_dir)
        output = ssh_stdout.readlines()

        # Close connection.
        ssh.close()

        protocol_list = []
        for line in output:
            protocol_list.append(silaFW_pb2.String(value=line))

        return_value = Ot2Controller_pb2.Get_InstalledProtocols_Responses(InstalledProtocols=protocol_list)

        # fallback to default
        if return_value is None:
            return_value = Ot2Controller_pb2.Get_InstalledProtocols_Responses(
                **default_dict['Get_InstalledProtocols_Responses']
            )

        return return_value
