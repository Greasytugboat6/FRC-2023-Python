import rev
from wpilib.drive import MecanumDrive

from robot_map import CAN


class DriveTrain:
    def __init__(self, controller):
        # Intializes motors for the drive base.
        self.frontRightMotor = rev.CANSparkMax(CAN.frontRightChannel, rev.CANSparkMax.MotorType.kBrushless)
        self.rearRightMotor = rev.CANSparkMax(CAN.rearRightChannel, rev.CANSparkMax.MotorType.kBrushless)
        self.frontLeftMotor = rev.CANSparkMax(CAN.frontLeftChannel, rev.CANSparkMax.MotorType.kBrushless)
        self.rearLeftMotor = rev.CANSparkMax(CAN.rearLeftChannel, rev.CANSparkMax.MotorType.kBrushless)

        self.frontRightMotor.restoreFactoryDefaults()
        self.rearRightMotor.restoreFactoryDefaults()
        self.frontLeftMotor.restoreFactoryDefaults()
        self.rearLeftMotor.restoreFactoryDefaults()

        self.frontRightMotor.setInverted(True)
        self.rearRightMotor.setInverted(True)

        self.controller = controller

        self.robotDrive = MecanumDrive(self.frontLeftMotor, self.rearLeftMotor, self.frontRightMotor,
                                       self.rearRightMotor)

    def moveDistance(self, distance):
        """Move the drive train a specified distance."""
        # To calculate the distanceSoFar, use the following formula:
        # distanceSoFar = (avgDistance / encoder_resolution) * distance_per_revolution

        # Where:
        # - encoder_resolution: Number of encoder counts per revolution.
        # - avgDistance: The average encoder count from all wheels (initialize each count to 0).
        # - distance_per_revolution: The distance covered by one revolution.

        # Ensure that this function maintains forward motion as long as the distance is less than distanceSoFar.
        pass

    def autonomousInit(self):
        # In Python, I *think* calling functions one by one should execute them in order. 
        # If we need parallelism for speed, we may need to explore some libraries such as asyncio .
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        self.robotDrive.setSafetyEnabled(True)

    def teleopPeriodic(self):
        # Handles the movement of the drive base.
        self.robotDrive.driveCartesian(
            self.controller.getLeftY(),
            self.controller.getLeftX(),
            self.controller.getRightY()
        )