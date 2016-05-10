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

## Enable Gyro
       writeGyrReg(CTRL_REG1_G, 0b00001111); // Normal power mode, all axes enabled
       writeGyrReg(CTRL_REG4_G, 0b00110000); // Continuos update, 2000 dps full scale

void readACC(int  *a)

## Read the Accelerometer
{
        uint8_t block[6];
        selectDevice(file,ACC_ADDRESS);
        readBlock(0x80 | OUT_X_L_A, sizeof(block), block);
 
        *a = (int16_t)(block[0] | block[1] << 8);
        *(a+1) = (int16_t)(block[2] | block[3] << 8);
        *(a+2) = (int16_t)(block[4] | block[5] << 8);
}

## Read the Gyroscope

void readGYR(int *g)
{
    uint8_t block[6];
 
        selectDevice(file,GYR_ADDRESS);
 
    readBlock(0x80 | OUT_X_L_G, sizeof(block), block);
 
        *g = (int16_t)(block[0] | block[1] << 8);
        *(g+1) = (int16_t)(block[2] | block[3] << 8);
        *(g+2) = (int16_t)(block[4] | block[5] << 8)
}

## Convert Gyro raw to degrees per second
rate_gyr_x = (float) gyrRaw[0] * G_GAIN;
rate_gyr_y = (float) gyrRaw[1]  * G_GAIN;
rate_gyr_z = (float) gyrRaw[2]  * G_GAIN;

## Calculate the angles from the gyro
gyroXangle+=rate_gyr_x*DT;
gyroYangle+=rate_gyr_y*DT;
gyroZangle+=rate_gyr_z*DT;

## Convert Accelerometer values to degrees
 
AccXangle = (float) (atan2(accRaw[1],accRaw[2])+M_PI)*RAD_TO_DEG;
AccYangle = (float) (atan2(accRaw[2],accRaw[0])+M_PI)*RAD_TO_DEG;

CFangleX=AA*(CFangleX+rate_gyr_x*DT) +(1 - AA) * AccXangle;
CFangleY=AA*(CFangleY+rate_gyr_y*DT) +(1 - AA) * AccYangle;

while(mymillis() - startInt < 20)
{
        usleep(100);
}

AccXangle -= (float)180.0;
if (AccYangle > 90)
      AccYangle -= (float)270;
else
       AccYangle += (float)90;
       
printf ("GyroX  %7.3f \t AccXangle \e[m %7.3f \t \033[22;31mCFangleX %7.3f\033[0m\t GyroY  %7.3f \t AccYangle %7.3f \t \033[22;36mCFangleY %7.3f\t\033[0m\n",gyroXangle,AccXangle,CFangleX,gyroYangle,AccYangle,CFangleY);