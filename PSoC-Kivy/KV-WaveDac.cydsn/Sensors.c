/**
*   Source file for Sensors module.
*/

#include "ADC_DelSig.h"
#include "CR_WDac.h"
#include "isr_timer.h"
#include "Sensors.h"
#include "Serial_Interface.h"
#include "Timer_Send.h"

static uint8_t is_streaming = 0;
static uint8_t send_data = 0;

CY_ISR_PROTO(isr_send_data);

/**
*   \brief Start the sensors module.
*/
void Sensors_Start(void)
{
    WaveDAC8_Start();
    ADC_DelSig_Start();
    Sensors_Reset();
}

/**
*   \brief Stop the sensors module.
*/
void Sensors_Stop(void)
{
    WaveDAC8_Stop();
    ADC_DelSig_Stop();
}

void Sensors_Reset(void)
{
    Sensors_StopStreaming();
    Sensors_SetInputRange(SENSORS_RANGE_LARGE);
    Sensors_SetInputWave(SENSORS_WAVE_1);
}

/**
*   \brief Start streaming of sensors data.
*/
void Sensors_StartStreaming(void)
{
    is_streaming = 1;
    // Start isr
    isr_timer_StartEx(isr_send_data);
    // Start timer 
    Timer_Send_Start();
}

// Stop streaming of sensors data.

void Sensors_StopStreaming(void)
{
    is_streaming = 0;
    Timer_Send_Stop();
    isr_timer_Stop();
}

// Check if it is streaming
uint8_t Sensors_IsStreaming(void)
{
    return is_streaming;
}

// Set input range for the wave.
void Sensors_SetInputRange(uint8_t range)
{
    if ( (range != SENSORS_RANGE_LARGE) && (range != SENSORS_RANGE_SMALL) )
    {
        return;
    }
    
    WaveDAC8_SetRange(range);
}

// Set input wave
void Sensors_SetInputWave(uint8_t wave)
{
    if ( (wave != SENSORS_WAVE_1) && (wave != SENSORS_WAVE_2))
    {
        return;
    }
    CR_WDac_Write(wave);
}

// Send data
void Sensors_SendData(void)
{
    if (is_streaming && send_data)
    {
        uint16_t wave = ((uint16_t)ADC_DelSig_Read32());
        Serial_SendDataPacket(wave);
        send_data = 0;
    }
}

CY_ISR(isr_send_data)
{
    send_data = 1;
    Timer_Send_ReadStatusRegister();
}

/* [] END OF FILE */
