from wpilib.drive import MecanumDrive
from portmap import CAN
import rev
import math

class DriveBase:
    def __init__(self, controller):
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

        self.robotDrive = MecanumDrive(self.DriveBase.frontLeftMotor, self.DriveBase.rearLeftMotor, self.DriveBase.frontRightMotor, self.DriveBase.rearRightMotor)


    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        self.robotDrive.setSafetyEnabled(True)

    def teleopPeriodic(self):
        self.robotDrive.driveCartesian(
            self.controller.getLeftY(),
            self.controller.getLeftX(),
            self.controller.getRightY()
        )

    def driveForward(self, speed, meters):
        """Moves the robot forward specified distance"""
        distance = 0
        self.frontRightMotor.getEncoder().setPosition(0)
        while distance < meters:
            self.robotDrive.driveCartesian(xSpeed = speed)
            distance = self.frontRightMotor.getEncoder().getPosition() * 0.61
        self.robotDrive.stopMotor()
    
    def translateDistance(self, xMeters, yMeters, rotation, speed):
        """Translates robot at specified speed"""
        totalDisplacement = math.sqrt(xMeters ** 2 + yMeters ** 2) + math.abs(rotation) * 2.5
        currentDisplacement = 0
        if xMeters > yMeters and xMeters > rotation:
            speedCoefficient = speed / xMeters
        elif yMeters > rotation:
            speedCoefficient = speed / yMeters
        else:
            speedCoefficient = speed / rotation
        
        encoders = (self.frontLeftMotor.getEncoder(), self.frontRightMotor.getEncoder(), self.rearLeftMotor.getEncoder(), self.rearRightMotor.getEncoder())
        for encoder in encoders:
            encoder.setPosition(0)
        
        while currentDisplacement < currentDisplacement:
            self.robotDrive.driveCartesian(xSpeed = xMeters * speedCoefficient, ySpeed = yMeters * speedCoefficient, zRotation = rotation * speedCoefficient)
            currentDisplacement = 0
            for encoder in encoders:
                currentDisplacement += math.abs(encoder.getPosition())
            currentDisplacement /= 4
        self.robotDrive.stopMotor()




class Arm:
    def __init__(self, controller):
        self.shoulderMotor = rev.CANSparkMax(CAN.shoulderChannel, rev.CANSparkMax.MotorType.kBrushless)
        self.extenderMotor = rev.CANSparkMax(CAN.extenderChannel, rev.CANSparkMax.MotorType.kBrushless)
        self.intakeMotor = rev.CANSparkMax(CAN.intakeChannel, rev.CANSparkMax.MotorType.kBrushless)

        self.shoulderMotor.restoreFactoryDefaults()
        self.extenderMotor.restoreFactoryDefaults()
        self.intakeMotor.restoreFactoryDefaults()

        self.controller = controller

    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        if self.controller.getAButton():
            self.intakeMotor.set(0.25)
        elif self.controller.getBButton():
            self.intakeMotor.set(-0.25)
        else:
            self.intakeMotor.set(0)
