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
    # print("Performed sender")

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
            max_qubits=10,
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
        from angle_value import gamma, beta
        q_a1 = Qubit(connection)
        q_a2 = Qubit(connection)
        q_a1.H()
        q_a2.H()
        # q_a1.rot_X(angle = 2*beta)
        # q_a2.rot_X(angle = 2*beta)
        yield from connection.flush()

        # RZZ(0,1)
        q_a1.cnot(q_a2)
        q_a2.rot_Z(angle = 2*gamma)
        q_a1.cnot(q_a2)
        yield from connection.flush()

        # RZZ(0,3)
        yield from cnot_sender(connection, q_a1, epr_qubit, csocket)
        yield from connection.flush()
        epr_qubit = epr_socket.create_keep()[0]
        yield from cnot_sender(connection, q_a1, epr_qubit, csocket)
        yield from connection.flush()

        # RZZ(1,2)
        epr_qubit = epr_socket.create_keep()[0]
        yield from cnot_sender(connection, q_a2, epr_qubit, csocket)
        yield from connection.flush()
        epr_qubit = epr_socket.create_keep()[0]
        yield from cnot_sender(connection, q_a2, epr_qubit, csocket)
        yield from connection.flush()

        q_a1.rot_X(angle = 2*beta)
        q_a2.rot_X(angle = 2*beta)
        result0 = q_a1.measure()
        result1 = q_a2.measure()
        yield from connection.flush()
        # print(f"Alice: {result}")
        return {"measurement": (int(result0),int(result1) )}


class BobProgram(Program):
    PEER_NAME = "Alice"

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name="tutorial_program",
            csockets=[self.PEER_NAME],
            epr_sockets=[self.PEER_NAME],
            max_qubits=10,
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

        q_b1 = Qubit(connection)
        q_b2 = Qubit(connection)
        from angle_value import gamma, beta

        q_b1.H()
        q_b2.H()
        # q_b1.rot_X(angle = 2*beta)
        # q_b2.rot_X(angle = 2*beta)
        yield from connection.flush()

        # RZZ(0,3)
        yield from cnot_reciever(connection, q_b2, epr_qubit, csocket)
        # ROTATION
        q_b2.rot_Z(angle = 2*gamma)
        yield from connection.flush()
        epr_qubit = epr_socket.recv_keep()[0]
        yield from connection.flush()
        yield from cnot_reciever(connection, q_b2, epr_qubit, csocket)
        yield from connection.flush()

        # RZZ(1,2)
        epr_qubit = epr_socket.recv_keep()[0]
        yield from connection.flush()
        yield from cnot_reciever(connection, q_b1, epr_qubit, csocket)
        # ROTATION
        q_b1.rot_Z(angle =2*gamma)
        yield from connection.flush()
        epr_qubit = epr_socket.recv_keep()[0]
        yield from connection.flush()
        yield from cnot_reciever(connection, q_b1, epr_qubit, csocket)
        yield from connection.flush()

        # RZZ(2,3)
        q_b1.cnot(q_b2)
        q_b2.rot_Z(angle = 2*gamma)
        q_b1.cnot(q_b2)
        yield from connection.flush()


        q_b1.rot_X(angle = 2*beta)
        q_b2.rot_X(angle = 2*beta)
        result0 = q_b1.measure()
        result1 = q_b2.measure()
        yield from connection.flush()
        # print(f"Alice: {result}")
        return {"measurement": (int(result0),int(result1))}
