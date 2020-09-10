"""
________________________________________________________________________

:PROJECT: *OT-2 Controller*

:details: Ot2Controller:
    A SiLA 2 complaint controller for an OT-2 Liquid Handler robot.

:file:    Ot2Controller_real.py
:authors: Florian Bauer <florian.bauer.dev@gmail.com>

.. note:: Code generated by sila2codegenerator 0.2.0

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

__version__ = "0.0.1"

import logging
import grpc  # used for type hinting only
import paramiko  # used for SSH connections
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2

from pathlib import Path
from scp import SCPClient, SCPException
from .gRPC import Ot2Controller_pb2 as Ot2Controller_pb2

USER_STORAGE_DIR: str = "~/dummy" + "/data/user_storage/"
JUPYTER_NOTEBOOK_DIR: str = "~/dummy" + "/var/lib/jupyter/notebooks/"


# noinspection PyPep8Naming,PyUnusedLocal
class Ot2ControllerReal:
    """
    Implementation of the *OT-2 Controller* in *Real* mode
        A SiLA 2 service enabling the execution of python protocols on a Opentrons 2 liquid handler robot.
    """
    _device_ip: str = "127.0.0.1"
    # The the location of the generated private key.
    # (see https://support.opentrons.com/en/articles/3203681-setting-up-ssh-access-to-your-ot-2)
    _pkey: str = "~/.ssh/ot2_ssh_key"

    def __init__(self):
        """Class initializer"""
        self.ssh = paramiko.SSHClient()
        # Load SSH host keys.
        self.ssh.load_system_host_keys()
        # Add SSH host key automatically if needed.
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Connect to device using key file authentication.
        self.ssh.connect(hostname=Ot2ControllerReal._device_ip,
                         pkey=Ot2ControllerReal._pkey,
                         look_for_keys=False)
        logging.debug('Started server in mode: {mode}'.format(mode='Real'))

    def __del__(self):
        """Class finalizer"""
        # Close connection.
        self.ssh.close()

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
            progressInfo=(command_progress if command_progress is not None else None),
            estimatedRemainingTime=(command_estimated_remaining if command_estimated_remaining is not None else None),
            updatedLifetimeOfExecution=(
                command_lifetime_of_execution if command_lifetime_of_execution is not None else None)
        )

    def UploadProtocol(self, request, context: grpc.ServicerContext) \
            -> Ot2Controller_pb2.UploadProtocol_Responses:
        """
        Executes the unobservable command "Upload Protocol"
            Uploads the given Protocol to the "/data/user_storage" dir on the OT-2.
    
        :param request: gRPC request containing the parameters passed:
            request.ProtocolSourcePath (Protocol Source Path): The path to the Protocol to upload.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: The return object defined for the command with the following fields:
            request.EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """
        scp = SCPClient(self.ssh.get_transport())
        file: str = str(Path(request.ProtocolSourcePath.value).expanduser().resolve())

        try:
            scp.put(file, recursive=True, remote_path=USER_STORAGE_DIR)
        except SCPException as error:
            logging.error(error)
            raise
        finally:
            scp.close()

        logging.debug(f"Uploaded {file} to {USER_STORAGE_DIR}")
        return Ot2Controller_pb2.UploadProtocol_Responses()

    def RemoveProtocol(self, request, context: grpc.ServicerContext) \
            -> Ot2Controller_pb2.RemoveProtocol_Responses:
        """
        Executes the unobservable command "Remove Protocol"
            Removes the given Protocol from the "/data/user_storage" dir on the OT-2.
    
        :param request: gRPC request containing the parameters passed:
            request.ProtocolFile (Protocol File): The file name of the Protocol to remove.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: The return object defined for the command with the following fields:
            request.EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """
        file: str = str(Path(USER_STORAGE_DIR + request.ProtocolFile.value).expanduser().resolve())
        logging.debug(f"remove: {file}")
        ftp_client = self.ssh.open_sftp()

        try:
            ftp_client.remove(file)
        except FileNotFoundError as error:
            logging.error(error)
            raise
        finally:
            ftp_client.close()

        return Ot2Controller_pb2.RemoveProtocol_Responses()

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
        is_simulating: bool = request.IsSimulating.value
        if is_simulating:
            cmd: str = "python3 -m opentrons.simulate " + USER_STORAGE_DIR + request.ProtocolFile.value
        else:
            cmd: str = "python3 -m opentrons.execute " + USER_STORAGE_DIR + request.ProtocolFile.value

        logging.debug(f"run '{cmd}'")
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(cmd)
        run_ret: int = ssh_stdout.channel.recv_exit_status()
        logging.debug("run returned '" + str(run_ret) + "'")

        if is_simulating and run_ret != 0:
            raise ValueError("The simulation of the protocol was not successful.")

        return Ot2Controller_pb2.RunProtocol_Responses(ReturnValue=silaFW_pb2.Integer(value=run_ret))

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
        connection_info = silaFW_pb2.String(value="Device IP: " + Ot2ControllerReal._device_ip
                                                  + ", User: " + Ot2ControllerReal._device_username)

        return Ot2Controller_pb2.Get_Connection_Responses(Connection=connection_info)

    def Get_AvailableProtocols(self, request, context: grpc.ServicerContext) \
            -> Ot2Controller_pb2.Get_AvailableProtocols_Responses:
        """
        Requests the unobservable property Available Protocols
            List of the stored files available on the OT-2.

        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            request.AvailableProtocols (Available Protocols): List of the stored files available on the OT-2.
        """
        # Run 'ls' command to collect the files.
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command("ls " + USER_STORAGE_DIR)
        output = ssh_stdout.readlines()

        protocol_list = []
        for line in output:
            protocol_list.append(silaFW_pb2.String(value=line))

        return Ot2Controller_pb2.Get_AvailableProtocols_Responses(AvailableProtocols=protocol_list)

    def Get_AvailableJupyterNotebooks(self, request, context: grpc.ServicerContext) \
            -> Ot2Controller_pb2.Get_AvailableJupyterNotebooks_Responses:
        """
        Requests the unobservable property Available Jupyter Notebooks
            List of the stored Jupyter Notebooks available on the OT-2.

        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            request.AvailableJupyterNotebooks (Available Jupyter Notebooks): List of the stored Jupyter Notebooks
            available on the OT-2.
        """
        # Run 'ls' command to collect the files.
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command("ls " + JUPYTER_NOTEBOOK_DIR)
        output = ssh_stdout.readlines()

        notebook_list = []
        for line in output:
            notebook_list.append(silaFW_pb2.String(value=line))

        return Ot2Controller_pb2.Get_AvailableJupyterNotebooks_Responses(AvailableJupyterNotebooks=notebook_list)

    def Get_CameraPicture(self, request, context: grpc.ServicerContext) \
            -> Ot2Controller_pb2.Get_CameraPicture_Responses:
        """
        Requests the unobservable property Camera Picture
            A current picture from the inside of the OT-2 made with the built-in camera.

        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            request.CameraPicture (Camera Picture): A current picture from the inside of the OT-2 made with the built-in
            camera.
        """
        payload: str = "BlaBlaBla"
        byte_stream = bytes(payload, "utf-8")

        cam_pic_struct = Ot2Controller_pb2.Get_CameraPicture_Responses.CameraPicture_Struct(
            ImageData=silaFW_pb2.Binary(value=byte_stream),
            ImageTimestamp=silaFW_pb2.Timestamp())

        return Ot2Controller_pb2.Get_CameraPicture_Responses(CameraPicture=cam_pic_struct)
