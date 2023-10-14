from rev import CANSparkMax
from wpilib.drive import MecanumDrive

from portmap import CAN


class DriveBase:
    def __init__(self, controller):
        # Intializes motors for the drive base.
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

        self.controller = controller

        self.robotDrive = MecanumDrive(self.frontLeftMotor, self.rearLeftMotor, self.frontRightMotor,
                                       self.rearRightMotor)

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


class Arm:
    def __init__(self, controller):
        self.mode = "IDLE"

        # Intializes motors for the arm.
        self.shoulderMotor = CANSparkMax(CAN.shoulderChannel, CANSparkMax.MotorType.kBrushless)
        self.extenderMotor = CANSparkMax(CAN.extenderChannel, CANSparkMax.MotorType.kBrushless)
        self.intakeMotor = CANSparkMax(CAN.intakeChannel, CANSparkMax.MotorType.kBrushless)

        self.shoulderMotor.restoreFactoryDefaults()
        self.extenderMotor.restoreFactoryDefaults()
        self.intakeMotor.restoreFactoryDefaults()

        # Sets up shoulder PID controller.
        self.shoulderPIDController = self.shoulderMotor.getPIDController()
        self.shoulderPIDController.setP(0.1)
        self.shoulderPIDController.setI(0.01)
        self.shoulderPIDController.setD(0.001)
        self.shoulderEncoder = self.shoulderMotor.getEncoder()

        self.controller = controller

    def setMode(self, mode):
        self.mode = mode

    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        # Handles control on the intake motor.
        if self.controller.getAButton():
            self.intakeMotor.set(0.25)
        elif self.controller.getBButton():
            self.intakeMotor.set(-0.25)
        else:
            self.intakeMotor.set(0)

        # Handles control on the shoulder motor.
        if self.controller.getYButton():
            self.shoulderMotor.set(0.25)
        elif self.controller.getXButton():
            self.shoulderMotor.set(-0.25)
        else:
            targetPosition = self.shoulderEncoder.getPosition()
            self.shoulderPIDController.setReference(targetPosition, rev.CANSparkMax.ControlType.kPosition)

        # Handles control on the extender motor.
        if self.controller.getPOV() == 0:
            self.extenderMotor.set(0.25)
        elif self.controller.getPOV() == 90:
            self.extenderMotor.set(-0.25)
        else:
            self.extenderMotor.set(0)
