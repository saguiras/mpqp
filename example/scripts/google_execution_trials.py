from mpqp.gates import H, Rx, Ry, Rz
from mpqp import QCircuit
from mpqp.measures import BasisMeasure
from mpqp.execution.devices import GOOGLEDevice, IBMDevice
from mpqp.execution import run

circuit = QCircuit(3)
circuit.add(H(0))
circuit.add(H(1))
circuit.add(H(2))
circuit.add(Rx(1.76, 1))
circuit.add(Ry(1.76, 1))
circuit.add(Rz(1.987, 0))
circuit.add(BasisMeasure([0, 1, 2], shots=1000))

print(circuit)

results = run(circuit, [GOOGLEDevice.CIRQ, GOOGLEDevice.PROCESSOR_RAINBOW, GOOGLEDevice.PROCESSOR_WEBER])
print(results)

#FIXME demonstation off circuit_to_grid() for processor