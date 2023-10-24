from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state

class Autonomous(StatefulAutonomous):
    MODE_NAME = "Auto Mode"

    def initialize(self):
        self.initial_called = None

    @timed_state(duration=1, next_state="drive_0", first=True)
    def arm_0(self):
        self.Arm.shoulderPosition = 16
        self.Arm.extenderPosition = 13
            
    @timed_state(duration=0.5, next_state="arm_1")
    def drive_0(self):
        self.DriveTrain.robotDrive.driveCartesian(-.2,0,0)
    
    @timed_state(duration=1, next_state="arm_2")
    def arm_1(self):
        self.DriveTrain.robotDrive.driveCartesian(0,0,0)
        self.Arm.extenderPosition = -20
    
    @timed_state(duration=1, next_state="extender")
    def arm_2(self):
        self.Arm.intakeMotor.set(-1)

    @timed_state(duration=1, next_state="arm_3")
    def extender(self):
        self.Arm.intakeMotor.set(-1)
        self.Arm.extenderPosition = 20
    
    @timed_state(duration=1, next_state="drive_1")
    def arm_3(self):
        self.Arm.intakeMotor.set(0)
        self.Arm.shoulderPosition = 5
    
    @timed_state(duration=2, next_state="auto_balance")
    def drive_1(self):
        self.DriveTrain.robotDrive.driveCartesian(0.2,0,0)
    
    @timed_state(duration=7)
    def auto_balance(self):
        self.DriveTrain.robotDrive.driveCartesian(0,0,0)
        self.DriveTrain.AUTO = True
    