import rev
# from rev import CANSparkMax has issues with the library for some reason

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

        # Sets up the controller.
        self.controller = controller

    def teleopInit(self):
        # Intializes position to 0
        self.shoulderEncoder.setPosition(0)
        self.shoulderPosition = 0
        self.extenderEncoder.setPosition(0)
        self.extenderPosition = 0

        # Sets PID values for teleoperated.
        self.shoulderPIDController.setP(0.5)
        self.shoulderPIDController.setI(0.0)
        self.shoulderPIDController.setD(7)
        self.shoulderPIDController.setFF(0.0)
        self.extenderPIDController.setP(0.5)
        self.extenderPIDController.setI(0.0)
        self.extenderPIDController.setD(7)
        self.extenderPIDController.setFF(0.0)

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
            self.shoulderPosition = self.shoulderEncoder.getPosition()
        elif self.controller.getXButton():
            self.shoulderMotor.set(-0.01)
            self.shoulderPosition = self.shoulderEncoder.getPosition()
        else:
            self.shoulderPIDController.setReference(self.shoulderPosition, rev.CANSparkMax.ControlType.kPosition)

        # Handles control on the extender motor.
        if self.controller.getPOV() == 0:
            self.extenderMotor.set(0.25)
            self.extenderPosition = self.extenderEncoder.getPosition()
        elif self.controller.getPOV() == 180:
            self.extenderMotor.set(-0.25)
            self.extenderPosition = self.extenderEncoder.getPosition()
        else:
            self.extenderPIDController.setReference(self.extenderPosition, rev.CANSparkMax.ControlType.kPosition)

        # print(f"Shoulder : {self.shoulderEncoder.getPosition()}")
        # print(f"Extender : {self.extenderEncoder.getPosition()}")


    def autonomousInit(self):
        # Intializes position to 0
        self.shoulderEncoder.setPosition(0)
        self.shoulderPosition = 0
        self.extenderEncoder.setPosition(0)
        self.extenderPosition = 0

        # Sets PID values for AUTO
        self.shoulderPIDController.setP(0.5)
        self.shoulderPIDController.setI(0.0)
        self.shoulderPIDController.setD(1)
        self.shoulderPIDController.setFF(0.0)
        self.extenderPIDController.setP(0.5)
        self.extenderPIDController.setI(0.0)
        self.extenderPIDController.setD(.1)
        self.extenderPIDController.setFF(0.0)

        # print(f"Auto Shoulder : {self.shoulderEncoder.getPosition()}")
        # print(f"Auto Extender : {self.extenderEncoder.getPosition()}")
    
    def autonomousPeriodic(self):
        # Move to position
        self.shoulderPIDController.setReference(self.shoulderPosition, rev.CANSparkMax.ControlType.kPosition)
        self.extenderPIDController.setReference(self.extenderPosition, rev.CANSparkMax.ControlType.kPosition)
