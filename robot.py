import wpilib
from portmap import USB
from components import DriveBase, Arm


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        controller = wpilib.XboxController(USB.controllerChannel)
        self.DriveBase = DriveBase(controller)
        self.Arm = Arm(controller)

    def autonomousInit(self):
        DriveBase.autonomousInit()
        Arm.autonomousInit()

    def autonomousPeriodic(self):
        DriveBase.autonomousInit
        Arm.autonomousInit

    def teleopInit(self):
        DriveBase.teleopInit()
        Arm.teleopInit()


    def teleopPeriodic(self):
        DriveBase.teleopPeriodic()
        Arm.teleopPeriodic()


if __name__ == "__main__":
    wpilib.run(MyRobot)
