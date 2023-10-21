import rev

from robot_map import CAN

class Arm:
    def __init__(self, controller):
        self.mode = "IDLE"

        # Intializes motors for the arm.
        self.shoulderMotor = rev.CANSparkMax(CAN.shoulderChannel, rev.CANSparkMax.MotorType.kBrushless)
        self.extenderMotor = rev.CANSparkMax(CAN.extenderChannel, rev.CANSparkMax.MotorType.kBrushless)
        self.intakeMotor = rev.CANSparkMax(CAN.intakeChannel, rev.CANSparkMax.MotorType.kBrushless)

        self.shoulderMotor.restoreFactoryDefaults()
        self.extenderMotor.restoreFactoryDefaults()
        self.intakeMotor.restoreFactoryDefaults()

        # Sets up shoulder PID controller.
        self.shoulderPIDController = self.shoulderMotor.getPIDController()
        self.shoulderPIDController.setP(0.1)
        self.shoulderPIDController.setI(0.01)
        self.shoulderPIDController.setD(0.001)
        self.shoulderEncoder = self.shoulderMotor.getEncoder()
        self.targetPosition = self.shoulderEncoder.getPosition()

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
            self.shoulderPIDController.setReference(0.1, rev.CANSparkMax.ControlType.kVelocity)
            self.targetPosition = self.shoulderEncoder.getPosition()
        elif self.controller.getXButton():
            self.shoulderPIDController.setReference(-0.1, rev.CANSparkMax.ControlType.kVelocity)
            self.targetPosition = self.shoulderEncoder.getPosition()
        else:
            self.shoulderPIDController.setReference(self.targetPosition, rev.CANSparkMax.ControlType.kPosition)
            self.shoulderPIDController.setReference(0, rev.CANSparkMax.ControlType.kVelocity)

        # Handles control on the extender motor.
        if self.controller.getPOV() == 180:
            self.extenderMotor.set(0.25)
        elif self.controller.getPOV() == 0:
            self.extenderMotor.set(-0.25)
        else:
            self.extenderMotor.set(0)
