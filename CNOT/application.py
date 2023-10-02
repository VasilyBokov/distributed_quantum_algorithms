from netqasm.sdk.classical_communication.socket import Socket
from netqasm.sdk.connection import BaseNetQASMConnection
from netqasm.sdk.epr_socket import EPRSocket
from netqasm.sdk.qubit import Qubit

from squidasm.sim.stack.program import Program, ProgramContext, ProgramMeta

def cnot_sender(connection, q, epr_qubit, csocket):

    q.cnot(epr_qubit)
    m = epr_qubit.measure()
    yield from connection.flush()
    csocket.send(str(m)) 
    m1 = yield from csocket.recv()

    if int(m1) == 1:
        q.Z()
    yield from connection.flush()

def cnot_reciever(connection, q, epr_qubit, csocket):
    # Bob listens for messages on his classical socket
    m = yield from csocket.recv()

    # Receive the outcome from alice
    if int(m) == 1:
        epr_qubit.X()
    epr_qubit.cnot(q)
    epr_qubit.H()

    # Measure the entangled qubit
    m_epr = epr_qubit.measure()

    yield from connection.flush()
    csocket.send(str(m_epr)) 

class AliceProgram(Program):
    PEER_NAME = "Bob"

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name="tutorial_program",
            csockets=[self.PEER_NAME],
            epr_sockets=[self.PEER_NAME],
            max_qubits=2,
        )
    

    def run(self, context: ProgramContext):
        # get classical socket to peer
        csocket = context.csockets[self.PEER_NAME]
        # get EPR socket to peer
        epr_socket = context.epr_sockets[self.PEER_NAME]
        # get connection to quantum network processing unit
        connection = context.connection

        # Register a request to create an EPR pair, then apply a Hadamard gate on the epr qubit and measure
        epr_qubit = epr_socket.create_keep()[0]
        # Qubits on a local node can be obtained, but require the connection to be initialized
        q_a = Qubit(connection)
        q_a.X()

        # FIRST CNOT
        yield from cnot_sender(connection, q_a, epr_qubit, csocket)
        

        result = q_a.measure()
        yield from connection.flush()
        print(f"Alice: {result}")

        return {}


class BobProgram(Program):
    PEER_NAME = "Alice"

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name="tutorial_program",
            csockets=[self.PEER_NAME],
            epr_sockets=[self.PEER_NAME],
            max_qubits=2,
        )

    def run(self, context: ProgramContext):
        # get classical socket to peer
        csocket: Socket = context.csockets[self.PEER_NAME]
        # get EPR socket to peer
        epr_socket: EPRSocket = context.epr_sockets[self.PEER_NAME]
        # get connection to quantum network processing unit
        connection: BaseNetQASMConnection = context.connection

        # EPR pair should be created simultaneously with the Alice's epr pair's
        epr_qubit = epr_socket.recv_keep()[0]
        q_b = Qubit(connection)
        # m = epr_qubit.measure()
        yield from connection.flush()

        # FIRST CNOT
        yield from cnot_reciever(connection, q_b, epr_qubit, csocket)

        result = q_b.measure()
        yield from connection.flush()

        print(f"Bob : {result}")
        return {}
