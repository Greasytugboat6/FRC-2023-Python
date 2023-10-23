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

    def setPosition(self, shoulderPosition, extenderPosition):
        while ((self.shoulderEncoder.getPosition() > shoulderPosition + 0.1 or self.shoulderEncoder.getPosition() < shoulderPosition - 0.1) and 
               (self.extenderEncoder.getPosition() > extenderPosition + 0.1 or self.extenderEncoder.getPosition() < shoulderPosition - 0.1)):
            self.shoulderPIDController.setReference(shoulderPosition, rev.CANSparkMax.ControlType.kPosition)
            self.extenderPIDController.setReference(extenderPosition, rev.CANSparkMax.ControlType.kPosition)

        print("Done")

    def teleopInit(self):
        self.shoulderTarget = self.shoulderEncoder.getPosition()
        self.shoulderEncoder.setPosition(0)
        self.shoulderPIDController.setReference(self.shoulderTarget, rev.CANSparkMax.ControlType.kPosition)
        self.extenderTarget = self.extenderEncoder.getPosition()
        self.extenderEncoder.setPosition(0)
        self.extenderPIDController.setReference(self.extenderTarget, rev.CANSparkMax.ControlType.kPosition)

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
            # self.shoulderPIDController.setReference(0.25, rev.CANSparkMax.ControlType.kVelocity)
            self.shoulderMotor.set(0.5)    
            self.shoulderTarget = self.shoulderEncoder.getPosition()
        elif self.controller.getXButton():
            # self.shoulderPIDController.setReference(-0.1, rev.CANSparkMax.ControlType.kVelocity)
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

        print(f"Shoulder Target: {self.shoulderTarget}")
        print(f"Extender Target: {self.extenderTarget}")
