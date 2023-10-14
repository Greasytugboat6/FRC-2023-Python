import wpilib
from wpilib.drive import MecanumDrive
from portmap import CAN, USB
import rev


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.frontRightMotor = rev.CANSparkMax(CAN.frontRightChannel, rev.CANSparkMax.MotorType.kBrushless)
        self.rearRightMotor = rev.CANSparkMax(CAN.rearRightChannel, rev.CANSparkMax.MotorType.kBrushless)
        self.frontLeftMotor = rev.CANSparkMax(CAN.frontLeftChannel, rev.CANSparkMax.MotorType.kBrushless)
        self.rearLeftMotor = rev.CANSparkMax(CAN.rearLeftChannel, rev.CANSparkMax.MotorType.kBrushless)
        self.shoulderMotor = rev.CANSparkMax(CAN.shoulderChannel, rev.CANSparkMax.MotorType.kBrushless)
        self.extenderMotor = rev.CANSparkMax(CAN.extenderChannel, rev.CANSparkMax.MotorType.kBrushless)
        self.intakeMotor = rev.CANSparkMax(CAN.intakeChannel, rev.CANSparkMax.MotorType.kBrushless)

        self.frontRightMotor.restoreFactoryDefaults()
        self.rearRightMotor.restoreFactoryDefaults()
        self.frontLeftMotor.restoreFactoryDefaults()
        self.rearLeftMotor.restoreFactoryDefaults()
        self.shoulderMotor.restoreFactoryDefaults()
        self.extenderMotor.restoreFactoryDefaults()
        self.intakeMotor.restoreFactoryDefaults()

        self.frontRightMotor.setInverted(True)
        self.rearRightMotor.setInverted(True)

        self.robotDrive = MecanumDrive(CAN.frontLeftMotor,
                                       CAN.rearLeftMotor,
                                       CAN.frontRightMotor,
                                       CAN.rearRightMotor)

        self.stick = wpilib.XboxController(USB.joystickChannel)

    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        self.robotDrive.setSafetyEnabled(True)

    def teleopPeriodic(self):
        self.robotDrive.driveCartesian(
            self.stick.getLeftX(),
            self.stick.getLeftY(),
            self.stick.getRightY(),
        )


if __name__ == "__main__":
    wpilib.run(MyRobot)
