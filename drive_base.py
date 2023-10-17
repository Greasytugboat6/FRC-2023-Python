import rev
from wpilib.drive import MecanumDrive

from robot_map import CAN


class DriveBase:
    def __init__(self, controller):
        self.mode = "IDLE"

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

    def setMode(self, mode):
        self.mode = mode

    def autonomousInit(self):
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