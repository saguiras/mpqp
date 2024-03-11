"""File regrouping all features for translating QASM code to Amazon Braket objects."""

import io

# import warnings
from logging import StreamHandler, getLogger

from braket.circuits import Circuit
from braket.ir.openqasm import Program
from typeguard import typechecked

from mpqp.qasm.open_qasm_2_and_3 import open_qasm_hard_includes

# from mpqp.tools.errors import UnsupportedBraketFeaturesWarning


@typechecked
def qasm3_to_braket_Program(qasm3_str: str) -> Program:
    """Converting a OpenQASM 3.0 code into a Braket Program.

    Args:
        qasm3_str: A string representing the OpenQASM 3.0 code.

    Returns:
        A Program equivalent to the QASM code in parameter.
    """

    # PROBLEM: import and standard gates are not supported by Braket
    # NOTE: however custom OpenQASM 3 gates declaration is supported by Braket,
    # the idea is then to hard import the standard lib and other files into the qasm string's header before
    # giving it to the Program.
    after_stdgates_included = open_qasm_hard_includes(qasm3_str, set())

    program = Program(source=after_stdgates_included, inputs=None)
    return program


@typechecked
def qasm3_to_braket_Circuit(qasm3_str: str) -> Circuit:
    """
    Converting a OpenQASM 3.0 code into a Braket Circuit

    Args:
        qasm3_str: A string representing the OpenQASM 3.0 code.

    Returns:
        A Circuit equivalent to the QASM code in parameter.
    """

    # PROBLEM: import and standard gates are not supported by Braket
    # NOTE: however custom OpenQASM 3 gates declaration is supported by Braket,
    # SOLUTION: the idea is then to hard import the standard lib and other files into the qasm string's header before
    # giving it to the Circuit.
    # PROBLEM2: Braket doesn't support NATIVE freaking gates U and gphase, so the trick may not work for the moment
    # for circuit, only for program
    # SOLUTION: import a specific qasm file with U and gphase redefined with the supported Braket SDK gates, and by
    # removing from this import file the already handled gates

    # we remove any include of stdgates.inc and replace it with custom include
    qasm3_str = qasm3_str.replace("stdgates.inc", "braket_custom_include.inc")

    after_stdgates_included = open_qasm_hard_includes(qasm3_str, set())
    # try:
    # except Exception as e:
    #     warning_message = (
    #         f"An error occurred while processing the OpenQASM code with Braket: {e}"
    #     )
    #     warnings.warn(warning_message, UnsupportedBraketFeaturesWarning)
    #     return None

    # # NOTE: gphase is already used in Braket and thus cannot be redefined as a native gate in OpenQASM.
    # # We used ggphase instead
    # if "U(" in after_stdgates_included or "gphase(" in after_stdgates_included:
    #     # Issue a warning only if not already issued
    #     warning_message = "This program uses OpenQASM language features that may not be supported on QPUs or on-demand simulators."
    #     warnings.warn(warning_message, UnsupportedBraketFeaturesWarning)

    # capture the Braket logger
    braket_logger = getLogger()

    # TODO: catch the logged warning
    logger_output_stream = io.StringIO()
    stream_handler = StreamHandler(logger_output_stream)
    braket_logger.addHandler(stream_handler)
    # if message == warning_message:
    #     warnings.warn(warning_message, UnsupportedBraketFeaturesWarning)
    stream_handler.addFilter(...)

    circuit = Circuit.from_ir(after_stdgates_included)

    # remove the logger handler
    braket_logger.removeHandler(stream_handler)

    return circuit
