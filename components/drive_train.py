from rev import CANSparkMax
from wpilib.drive import MecanumDrive

from robot_map import CAN


class DriveTrain:
    def __init__(self, controller):
        self.BALANCE = False

        # Intializes motors for the drive basse.
        self.frontRightMotor = CANSparkMax(CAN.frontRightChannel, CANSparkMax.MotorType.kBrushless)
        self.rearRightMotor = CANSparkMax(CAN.rearRightChannel, CANSparkMax.MotorType.kBrushless)
        self.frontLeftMotor = CANSparkMax(CAN.frontLeftChannel, CANSparkMax.MotorType.kBrushless)
        self.rearLeftMotor = CANSparkMax(CAN.rearLeftChannel, CANSparkMax.MotorType.kBrushless)
        self.frontRightMotor.restoreFactoryDefaults()
        self.rearRightMotor.restoreFactoryDefaults()
        self.frontLeftMotor.restoreFactoryDefaults()
        self.rearLeftMotor.restoreFactoryDefaults()
        self.frontRightMotor.setInverted(True)
        self.rearRightMotor.setInverted(True)

        # Sets up the controller and drive train.
        self.controller = controller
        self.robotDrive = MecanumDrive(self.frontLeftMotor, self.rearLeftMotor, self.frontRightMotor,
                                       self.rearRightMotor)
        
    def autoBalance(self):
        roll = self.gyroscope.getRoll() - self.intialRoll
        if (abs(roll) > 1):
            self.robotDrive.driveCartesian(roll/100, 0, 0)
        else:
            self.robotDrive.driveCartesian(0, 0, 0)
        print(f"Roll: {roll}")

    def autonomousInit(self):
        self.intialRoll = self.DriveTrain.gyroscope.getRoll()
        self.DriveTrain.robotDrive.setSafetyEnabled(False)
    
    def autonomousPeriodic(self):
        if (self.BALANCE):
            self.autoBalance()

    def teleopInit(self):
        self.robotDrive.setSafetyEnabled(True)

    def teleopPeriodic(self):
        # Handles the movement of the drive base.
        self.robotDrive.driveCartesian(
            self.controller.getLeftY(),
            self.controller.getLeftX(),
            self.controller.getRightY()
        )