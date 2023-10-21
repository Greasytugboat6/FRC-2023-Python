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

    def moveDistance(self, distance):
        """Move the drive train a specified distance in inches."""
        print(f"Moving {distance}")
        self.frontRightEncoder.setPosition(0.0)
        self.rearRightEncoder.setPosition(0.0)
        self.frontLeftEncoder.setPosition(0.0)
        self.rearLeftEncoder.setPosition(0.0)

        distance /= 1.93

        avgDistance = (abs(self.frontRightEncoder.getPosition()) + abs(self.rearRightEncoder.getPosition()) 
                       + abs(self.frontLeftEncoder.getPosition()) + abs(self.rearLeftEncoder.getPosition())) / 4
        
        while avgDistance < distance:
            avgDistance = (abs(self.frontRightEncoder.getPosition()) + abs(self.rearRightEncoder.getPosition()) 
                           + abs(self.frontLeftEncoder.getPosition()) + abs(self.rearLeftEncoder.getPosition())) / 4
            print(avgDistance)
            self.robotDrive.driveCartesian(-.2, 0, 0)

    def autoBalance(self):
        roll = self.gyroscope.getRoll() - self.intialRoll
        if (roll> 1):
            self.robotDrive.driveCartesian(roll/100, 0, 0)
        elif (roll < -1):
            self.robotDrive.driveCartesian(roll/100, 0, 0)
        else:
            self.robotDrive.driveCartesian(0, 0, 0)
            

    def autonomousInit(self):
        self.intialRoll = self.gyroscope.getRoll()
        self.robotDrive.setSafetyEnabled(False)

    def autonomousPeriodic(self):
        self.autoBalance()

    def teleopInit(self):
        self.intialRoll = self.gyroscope.getRoll()
        self.robotDrive.setSafetyEnabled(False)

    def teleopPeriodic(self):
        # Handles the movement of the drive base.
        if abs(self.controller.getLeftX()) > 0.1 or abs(self.controller.getLeftY()) > 0.1 or abs(self.controller.getRightY()) > 0.1:
            self.robotDrive.driveCartesian(
                self.controller.getLeftY(),
                -self.controller.getLeftX(),
                self.controller.getRightY()
            )
        if self.controller.getLeftBumper():
            print("bumper")
            self.autoBalance()