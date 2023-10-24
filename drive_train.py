import rev
from wpilib import SPI
from wpilib.drive import MecanumDrive
from navx import AHRS

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

        self.frontRightEncoder = self.frontRightMotor.getEncoder()
        self.rearRightEncoder = self.rearRightMotor.getEncoder()
        self.frontLeftEncoder = self.frontLeftMotor.getEncoder()
        self.rearLeftEncoder = self.rearLeftMotor.getEncoder()

        self.controller = controller

        self.gyroscope = AHRS(SPI.Port.kMXP)
        self.gyroscope.reset()

        self.robotDrive = MecanumDrive(self.frontRightMotor, self.rearRightMotor, self.frontLeftMotor,
                                       self.rearLeftMotor)
        
        self.AUTO = False

    def autoBalance(self):
        roll = self.gyroscope.getRoll() - self.intialRoll
        if (abs(roll) > 1):
            self.robotDrive.driveCartesian(roll/100, 0, 0)
        else:
            self.robotDrive.driveCartesian(0, 0, 0)
        print(f"Roll {roll}")
            
    def teleopInit(self):
        self.intialRoll = self.gyroscope.getRoll()
        self.robotDrive.setSafetyEnabled(False)

    def teleopPeriodic(self):
        # Handles the movement of the drive base.
        self.robotDrive.driveCartesian(
            self.controller.getLeftY(),
            -self.controller.getLeftX(),
            self.controller.getRightX()
        )
        if self.controller.getLeftBumper():
            self.autoBalance()