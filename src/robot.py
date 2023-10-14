import wpilib
from portmap import USB
from components import DriveBase, Arm


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """ This function is called upon program startup."""
        controller = wpilib.XboxController(USB.controllerChannel)
        self.DriveBase = DriveBase(controller)
        self.Arm = Arm(controller)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.DriveBase.autonomousInit()
        self.Arm.autonomousInit()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        pass

    def teleopInit(self):
        """This function is run once each time the robot enters teleoperated mode."""
        self.DriveBase.teleopInit()
        self.Arm.teleopInit()

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.DriveBase.teleopPeriodic()
        self.Arm.teleopPeriodic()


if __name__ == "__main__":
    wpilib.run(MyRobot)
