import numpy as np
from cv_bridge import CvBridge, CvBridgeError

from .observation_manager import RobotObservation

class LeRobotBridge:
    def __init__(self, joint_order):
        """
        initialize ros to python conversion.

        args:
            joint_order: canonical ordering of robot joints
        """

        self.bridge = CvBridge()

        self.joint_order = list(joint_order)
        if not self.joint_order:
            raise ValueError('Joint order cannot be empty.')

    def observation_to_python(self, observation: RobotObservation):
        """
        convert observation into a model independent python structure.

        returns:
            dict:
                image: rgb numpy array (uint8)
                state: joint positions in canonical order (float32)
                task: natural language task instruction (str)

        does not perform model specific preprocessing, normalization,
        feature mapping, or tensor construction.
        """

        # TODO: Reject missing or invalid observations.

        # TODO: Convert ros image message to rgb numpy array
        #       using cvbridge and desired_encoding='rgb8'

        # TODO: extract joint positions from JointState
        #       reorder them according to self.joint_order

        # TODO: Check for missing joints and invalid position values

        # TODO: Extract the task instruction

        # TODO: Return a dictionary containing image, state, and task

        pass

    def action_to_array(self, model_output):
        """
        convert model output into a numpy array

        expected eventual shape: (chunk_length, action_dimension)

        does not interpret or validate robot actions
        """

        # TODO: Handle numpy arrays and pytorch tensors
        # TODO: Convert to float32 numpy array
        # TODO: Check dimensionality and finite values
        # TODO: check that resulting array is non empty

        pass