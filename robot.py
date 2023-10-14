import wpilib
from portmap import USB
from components import DriveBase, Arm


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        controller = wpilib.XboxController(USB.controllerChannel)
        self.DriveBase = DriveBase(controller)
        self.Arm = Arm(controller)

    def autonomousInit(self):
        self.DriveBase.autonomousInit()
        self.Arm.autonomousInit()

    def autonomousPeriodic(self):
        self.DriveBase.autonomousPeriodic()
        self.Arm.autonomousPeriodic()

    def teleopInit(self):
        self.DriveBase.teleopInit()
        self.Arm.teleopInit()


    def teleopPeriodic(self):
        self.DriveBase.teleopPeriodic()
        self.Arm.teleopPeriodic()


if __name__ == "__main__":
    wpilib.run(MyRobot)
