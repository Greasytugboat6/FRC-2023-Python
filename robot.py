import wpilib
import rev
from drive_train import DriveTrain
from arm import Arm
from robot_map import USB


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """This function is called upon program startup."""
        controller = wpilib.XboxController(USB.controllerChannel)
        self.DriveTrain = DriveTrain(controller)
        self.Arm = Arm(controller)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.IDLE = False
        self.BALANCE = False
        self.Arm.shoulderEncoder.setPosition(0)
        self.Arm.extenderEncoder.setPosition(0)
        self.DriveTrain.intialRoll = self.gyroscope.getRoll()
        self.DriveTrain.robotDrive.setSafetyEnabled(False)
        self.Arm.setPosition(16, 13)
        self.IDLE = True
        self.DriveTrain.moveDistance(18)


    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        if (self.IDLE):
            print("Idling")
            self.Arm.shoulderPIDController.setReference(self.shoulderPosition, rev.CANSparkMax.ControlType.kPosition)
            self.Arm.extenderPIDController.setReference(self.extenderPosition, rev.CANSparkMax.ControlType.kPosition)
        if (self.BALANCE):
            self.DriveTrain.autoBalance()
        self.shoulderPosition = self.Arm.shoulderEncoder.getPosition()
        self.extenderPosition = self.Arm.extenderEncoder.getPosition()

    def teleopInit(self):
        """This function is run once each time the robot enters teleoperated mode."""
        self.DriveTrain.teleopInit()
        self.Arm.teleopInit()

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.DriveTrain.teleopPeriodic()
        self.Arm.teleopPeriodic()


if __name__ == "__main__":
    wpilib.run(MyRobot)
