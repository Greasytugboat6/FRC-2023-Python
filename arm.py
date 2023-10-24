import rev

from robot_map import CAN

class Arm:
    def __init__(self, controller):
        # Intializes motors for the arm.
        self.shoulderMotor = rev.CANSparkMax(CAN.shoulderChannel, rev.CANSparkMax.MotorType.kBrushless)
        self.extenderMotor = rev.CANSparkMax(CAN.extenderChannel, rev.CANSparkMax.MotorType.kBrushless)
        self.intakeMotor = rev.CANSparkMax(CAN.intakeChannel, rev.CANSparkMax.MotorType.kBrushless)

        self.shoulderMotor.restoreFactoryDefaults()
        self.extenderMotor.restoreFactoryDefaults()
        self.intakeMotor.restoreFactoryDefaults()

        # Sets up shoulder PID controller.
        self.shoulderPIDController = self.shoulderMotor.getPIDController()
        self.shoulderPIDController.setP(0.5)
        self.shoulderPIDController.setI(0.0)
        self.shoulderPIDController.setD(7)
        self.shoulderPIDController.setFF(0.0)
        self.shoulderEncoder = self.shoulderMotor.getEncoder()

        # Sets up extender PID controller.
        self.extenderPIDController = self.extenderMotor.getPIDController()
        self.extenderPIDController.setP(0.5)
        self.extenderPIDController.setI(0.0)
        self.extenderPIDController.setD(7)
        self.extenderPIDController.setFF(0.0)
        self.extenderEncoder = self.extenderMotor.getEncoder()

        self.controller = controller

        self.shoulderPosition = self.shoulderEncoder.getPosition()
        self.extenderPosition = self.extenderEncoder.getPosition()

    def teleopInit(self):
        self.shoulderEncoder.setPosition(0)
        self.shoulderTarget = self.shoulderEncoder.getPosition()
        self.extenderEncoder.setPosition(0)
        self.extenderTarget = self.extenderEncoder.getPosition()

    def teleopPeriodic(self):
        # Handles control on the intake motor.
        if self.controller.getAButton():
            self.intakeMotor.set(1)
        elif self.controller.getBButton():
            self.intakeMotor.set(-1)
        else:
            self.intakeMotor.set(0)

        # Handles control on the shoulder motor.
        if self.controller.getYButton():
            self.shoulderMotor.set(0.5)    
            self.shoulderTarget = self.shoulderEncoder.getPosition()
        elif self.controller.getXButton():
            self.shoulderMotor.set(-0.01)
            self.shoulderTarget = self.shoulderEncoder.getPosition()
        else:
            self.shoulderPIDController.setReference(self.shoulderTarget, rev.CANSparkMax.ControlType.kPosition)

        # Handles control on the extender motor.
        if self.controller.getPOV() == 180:
            self.extenderMotor.set(0.25)
            self.extenderTarget = self.extenderEncoder.getPosition()
        elif self.controller.getPOV() == 0:
            self.extenderMotor.set(-0.25)
            self.extenderTarget = self.extenderEncoder.getPosition()
        else:
            self.extenderPIDController.setReference(self.extenderTarget, rev.CANSparkMax.ControlType.kPosition)

        print(f"Shoulder : {self.shoulderEncoder.getPosition()}")
        print(f"Extender : {self.extenderEncoder.getPosition()}")
