import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, JointState
from std_msgs.msg import String

from dataclasses import dataclass
from typing import Optional
import time

@dataclass
class RobotObservation:
	image: Image
	joint_state: JointState
	instruction: str

	image_timestamp: float
	joint_timestamp: float
	instruction_timestamp: float

class ObservationManager(Node):
	def __init__(self):
		super().__init__('observation_manager')

		self.latest_image: Optional[Image] = None
		self.latest_joint_state: Optional[JointState] = None
		self.latest_instruction: Optional[str] = None

		self.image_received_at: Optional[float] = None
		self.joint_received_at: Optional[float] = None
		self.instruction_received_at: Optional[float] = None

		self.max_observation_age = 1.0

		self.image_sub = self.create_subscription(Image, '/camera/top/image_raw', self.image_callback, 10)
		self.joint_sub = self.create_subscription(JointState, '/joint_states', self.joint_callback, 10)
		self.instruction_sub = self.create_subscription(String, '/arm/task_instruction', self.instruction_callback, 10)

		self.get_logger().info("Observation Manager initialized!")

	def image_callback(self, msg: Image):
		self.latest_image = msg
		self.image_received_at = time.monotonic()

	def joint_callback(self, msg: JointState):
		if msg.name or len(msg.name) != len(msg.position):
			self.get_logger().warning('Received invalid joint state')
			return
		
		self.latest_joint_state = msg
		self.joint_received_at = time.monotonic()

	def instruction_callback(self, msg: String):
		instruction = msg.data.strip()
		if not instruction:
			self.get_logger().warning('Received empty task instruction')
			return
		
		self.latest_instruction = instruction
		self.instruction_received_at = time.monotonic()

	def observation_ready(self) -> bool:
		if (self.latest_image is None or self.latest_joint_state is None or self.latest_instruction is None):
			return False
		
		now = time.monotonic()

		timestamps = [self.image_received_at, self.joint_received_at, self.instruction_received_at]

		if any(t is None for t in timestamps):
			return False

		return True

	def get_observation(self) -> Optional[RobotObservation]:
		if not self.observation_ready():
			return None

		return RobotObservation(
			image=self.latest_image, joint_state=self.latest_joint_state, instruction=self.latest_instruction, 
			image_timestamp=self.image_received_at, joint_timestamp=self.joint_received_at, instruction_timestamp=self.instruction_received_at
		)

def main(args=None):
	rclpy.init(args=args)
	node = ObservationManager()

	try:
		rclpy.spin(node)
	except KeyboardInterrupt:
		pass
	finally:
		rclpy.destroy_node()
		rclpy.shutdown()

if __name__ == "__main__":
	main()