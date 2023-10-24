import wpilib
import wpilib.drive
import rev
from drive_train import DriveTrain
from arm import Arm
from robot_map import USB
from robotpy_ext.autonomous import AutonomousModeSelector


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """This function is called upon program startup."""
        self.controller = wpilib.XboxController(USB.controllerChannel)
        self.DriveTrain = DriveTrain(self.controller)
        self.Arm = Arm(self.controller)

        self.components = {"DriveTrain": self.DriveTrain,
                           "Arm": self.Arm}

        self.automodes = AutonomousModeSelector("autonomous", self.components)

        self.automodes.active_mode = self.automodes.modes["Auto Mode"]


    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.DriveTrain.intialRoll = self.DriveTrain.gyroscope.getRoll()
        self.Arm.shoulderEncoder.setPosition(0)
        self.Arm.shoulderTarget = self.Arm.shoulderEncoder.getPosition()
        self.Arm.extenderEncoder.setPosition(0)
        self.Arm.extenderTarget = self.Arm.extenderEncoder.getPosition()
        self.Arm.shoulderPIDController.setP(0.5)
        self.Arm.shoulderPIDController.setI(0.0)
        self.Arm.shoulderPIDController.setD(.1)
        self.Arm.shoulderPIDController.setFF(0.0)
        self.Arm.extenderPIDController.setP(0.5)
        self.Arm.extenderPIDController.setI(0.0)
        self.Arm.extenderPIDController.setD(.1)
        self.Arm.extenderPIDController.setFF(0.0)
        print(f"Auto Shoulder : {self.Arm.shoulderEncoder.getPosition()}")
        print(f"Auto Extender : {self.Arm.extenderEncoder.getPosition()}")
        self.DriveTrain.robotDrive.setSafetyEnabled(False)
        print(self.automodes.modes)
        self.automodes.start()


    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        self.automodes.periodic()
        self.Arm.shoulderPIDController.setReference(self.Arm.shoulderPosition, rev.CANSparkMax.ControlType.kPosition)
        self.Arm.extenderPIDController.setReference(self.Arm.extenderPosition, rev.CANSparkMax.ControlType.kPosition)

        if (self.DriveTrain.AUTO):
            self.DriveTrain.autoBalance()
    
    def disabledInit(self):
        self.automodes.disable()


    def teleopInit(self):
        """This function is run once each time the robot enters teleoperated mode."""
        self.DriveTrain.teleopInit()
        self.Arm.teleopInit()
        self.Arm.shoulderPIDController.setP(0.5)
        self.Arm.shoulderPIDController.setI(0.0)
        self.Arm.shoulderPIDController.setD(7)
        self.Arm.shoulderPIDController.setFF(0.0)
        self.Arm.extenderPIDController.setP(0.5)
        self.Arm.extenderPIDController.setI(0.0)
        self.Arm.extenderPIDController.setD(7)
        self.Arm.extenderPIDController.setFF(0.0)

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.DriveTrain.teleopPeriodic()
        self.Arm.teleopPeriodic()

        if self.controller.getStartButton():
            self.Arm.shoulderEncoder.setPosition(0)
            self.Arm.extenderEncoder.setPosition(0)

        if self.controller.getBackButton():
            # resets the yaw
            self.DriveTrain.gyroscope.reset()


if __name__ == "__main__":
    wpilib.run(MyRobot)
