import wpilib
import wpilib.drive


class MyRobot(wpilib.TimedRobot):
    # Channels on the roboRIO that the motor controllers are plugged in to
    frontRightChannel = 2
    rearRightChannel = 1
    frontLeftChannel = 3
    rearLeftChannel = 4
    shoulderChannel = 5
    extenderChannel = 6
    intakeChannel = 7

    # The channel on the driver station that the joystick is connected to
    joystickChannel = 0

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any intialization code.
        """
        self.frontRightMotor = wpilib.PWMSparkMax(self.frontRightChannel)
        self.rearRightMotor = wpilib.PWMSparkMax(self.rearRightChannel)
        self.frontLeftMotor = wpilib.PWMSparkMax(self.frontLeftChannel)
        self.rearLeftMotor = wpilib.PWMSparkMax(self.rearLeftChannel)
        self.shoulderMotor = wpilib.PWMSparkMax(self.shoulderChannel)
        self.extenderMotor = wpilib.PWMSparkMax(self.extenderChannel)
        self.intakeMotor = wpilib.PWMSparkMax(self.intakeChannel)

        self.robotDrive = wpilib.drive.MecanumDrive(self.frontLeftMotor,
                                                    self.rearLeftMotor,
                                                    self.frontRightMotor,
                                                    self.rearRightMotor)

        self.stick = wpilib.XboxController(self.joystickChannel)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        pass

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous"""
        pass

    def teleopInit(self):
        """This function is run once each time the robot enters operator control."""
        self.robotDrive.setSafetyEnabled(True)

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.robotDrive.driveCartesian(
            self.stick.getLeftX(),
            self.stick.getLeftY(),
            self.stick.getRightY(),
        )


if __name__ == "__main__":
    wpilib.run(MyRobot)
