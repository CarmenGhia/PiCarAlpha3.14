char filename[20];
sprintf(filename, "/dev/i2c-%d, 1); 
file = open(filename, O_RDWR);
if (file<0) (
	printf("Unable to open I2C bus!");
	exit(1);
)

if (ioctl(file, I2c_SLAVE, <em>device_address</em>)
	printf("Error: could not select magnetometer");
)

void selectDevice(int file, int addr(
{
	char device[3];

	if (ioctl, I2C_SLAVE, addr) < 0) {
	printf("Failed to select I2C device.");
	}
}

selectDevice(file,ACC ADDRESS);

## Enable accelerometer
	writeAccReg(CTRL_REG1_XM, 0b01100111); ## z,
	writeAccReg(CTRL_REG2 XM, 0b00100000); ## +/-

