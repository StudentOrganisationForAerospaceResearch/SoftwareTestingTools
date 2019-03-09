/**
  ******************************************************************************
  * File Name          : KalmanFilterTesting.c
  * Description        : This file contains an implementation of a Kalman filter
  *                      designed to obtain accurate altitude readings from both
  *                      the accelerometer and barometer on board the rocket.
  *                      I have totally chainsawed the file to work with the
  *                      provided testing data.
  ******************************************************************************
*/

/* Includes ------------------------------------------------------------------*/

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Constants -----------------------------------------------------------------*/

static const int SEA_LEVEL_PRESSURE = 101421.93903699999;
// TODO: THIS NEEDS TO BE UPDATED AND RECORDED ON LAUNCH DAY

static const double KALMAN_GAIN[][2] =
{
    {0.105553059 * 2, 0.109271566},
    {0.0361533034, 0.0661198847},
    {0.000273178915, 0.618030079}
};

/* Structs -------------------------------------------------------------------*/

struct KalmanStateVector
{
    double altitude;
    double velocity;
    double acceleration;
};

/* Functions -----------------------------------------------------------------*/

/**
 * Gets the ith field in a line seperated by commas.
 *
 * Params:
 *   line - (char*) Pointer to a string seperated by commas
 *   num  - (int) The number of the field to get. 1 indexed. I'm sorry.
 */
char* getfield(char* line, int num)
{
    char* tok;

    for (tok = strtok(line, ",");
            tok && *tok;
            tok = strtok(NULL, ",\n"))
    {
        if (!--num)
        {
            return tok;
        }
    }

    return NULL;
}


/**
 * Takes an old state vector and current state measurements and
 * converts them into a prediction of the rocket's current state.
 *
 * This is the exact code from AvionicsSoftware.
 * It has not been changed.
 *
 * Params:
 *   oldState        - (KalmanStateVector) Past altitude, velocity and acceleration
 *   currentAccel    - (double) Measured acceleration
 *   currentAltitude - (double) Measured altitude
 *   dt              - (double) Time since last step. In ms.
 *
 * Returns:
 *   newState        - (KalmanStateVector) Current altitude, velocity and acceleration
 */
struct KalmanStateVector filterSensors(
    struct KalmanStateVector oldState,
    double currentAccel,
    double currentPressure,
    double dt
)
{
    struct KalmanStateVector newState;

    double accelIn = (double) currentAccel; // Milli-g -> g -> m/s

    // Convert from 100*millibars to m. This may or may not be right, depending on where you look. Needs testing
    double altIn = (double) 44307.69396 * (1 - pow(currentPressure / SEA_LEVEL_PRESSURE, 0.190284));


    // Propagate old state using simple kinematics equations
    newState.altitude = oldState.altitude + oldState.velocity * dt + 0.5 * dt * dt * oldState.acceleration;
    newState.velocity = oldState.velocity + oldState.acceleration * dt;
    newState.acceleration = oldState.acceleration;

    // Calculate the difference between the new state and the measurements
    double baroDifference = altIn - newState.altitude;
    double accelDifference = accelIn - newState.acceleration;

    // Minimize the chi2 error by means of the Kalman gain matrix
    newState.altitude = newState.altitude + KALMAN_GAIN[0][0] * baroDifference + KALMAN_GAIN[0][1] * accelDifference;
    newState.velocity = newState.velocity + KALMAN_GAIN[1][0] * baroDifference + KALMAN_GAIN[1][1] * accelDifference;
    newState.acceleration = newState.velocity + KALMAN_GAIN[2][0] * baroDifference + KALMAN_GAIN[2][1] * accelDifference;

    return newState;
}

/**
 * Runs through the input file, reading acceleration, pressure, time, and read altitude.
 * Uses just the acceleration, pressure, and time to calculate altitude using the Kalman filter.
 * Logs all of the data to the output file.
 *
 * Must configure data in the "Touchy" section.
 * Leave the "No Touchy" section alone unless you know what you're doing.
 */
int main()
{
    /* Touchy --------------------------------------------------------------- */

    // File names
    char* inputFileName  = "KalmanTestInput.csv";
    char* outputFileName = "KalmanTestOutput.csv";

    // Line max settings
    int lineMaxEnable = 0;
    int lineMax       = 3;

    // Initial readings before launch
    double lastTime = 1174.0074;
    double lastAlt  = 1289;

    // Field indexes. 1 indexed. I'm sorry.
    int timeIndex         = 1;
    int accelIndex        = 15;
    int pressureIndex     = 10;
    int readAltitudeIndex = 11;

    // Detectionp parameters
    int detectStart = 200; // Line to start checking for descent on
    int desTrigger  = 3; // Number of descents in a row to confirm the rocket is descending

    /* No Touchy ------------------------------------------------------------ */

    // IO
    FILE* inputStream  = fopen(inputFileName, "r");
    FILE* outputStream = fopen(outputFileName, "w");
    fprintf(outputStream, "dt, Acceleration, Pressure, Their Altitude, Our Altitude, DES\n");
    char line[1024];

    // Parameters
    int i        = 0; // Number of lines processed
    int descount = 0; // Number of descents counted in a row
    double DES   = 0; // "Digital" parameter, stores altitude of descent detection

    // Kalman Vector
    struct KalmanStateVector ksv;
    ksv.altitude = lastAlt;

    // For each line in the input file
    while (fgets(line, 1024, inputStream) && ((lineMaxEnable && i <= lineMax) || ~lineMaxEnable))
    {
        // The empty pointers are things to help strtok. They're stupid, but they work.

        // Get the time
        char*  timeStr         = getfield(strdup(line), 1);
        char*  ptr1;
        double time            = strtod(timeStr, &ptr1) / 10000;
        double dt              = time - lastTime;

        // Get the acceleration
        char*  accelerationStr = getfield(strdup(line), 15);
        char*  ptr2;
        double acceleration    = strtod(accelerationStr, &ptr2);

        // Get the pressure
        char*  pressureStr     = getfield(strdup(line), 10);
        char*  ptr3;
        double pressure        = strtod(pressureStr, &ptr3);

        // Get the read altitude
        char*  altitudeStr     = getfield(strdup(line), 11);
        char*  ptr4;
        double theirAltitude   = strtod(altitudeStr, &ptr4);

        // Calculate our altitude
        ksv = filterSensors(ksv, acceleration, pressure, dt);

        // Check for descent
        if (i >= detectStart)
        {
            if (ksv.altitude < lastAlt)
            {
                descount++;
            }
            else
            {
                descount = 0;
            }

            if (descount > desTrigger && DES == 0)
            {
                DES = ksv.altitude; // Activate descent stuff!
            }
        }

        // Log data
        fprintf(outputStream, "%f,%f,%f,%f,%f,%f\n", dt, acceleration, pressure, theirAltitude, ksv.altitude, DES);

        // Update parameters
        lastAlt = ksv.altitude;
        lastTime = time;
        i++;
    }

    printf("Done.\n");
}
