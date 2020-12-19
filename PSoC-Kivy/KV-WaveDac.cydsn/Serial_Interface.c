/* ========================================
 *
 * Copyright YOUR COMPANY, THE YEAR
 * All Rights Reserved
 * UNPUBLISHED, LICENSED SOFTWARE.
 *
 * CONFIDENTIAL AND PROPRIETARY INFORMATION
 * WHICH IS THE PROPERTY OF your company.
 *
 * ========================================
*/
#include "Serial_Interface.h"
#include "Sensors.h"
#include "stdio.h"
#include "UART.h"

static const char conn_msg[] = "Wave Kivy $$$";
static const char error_msg[] = "Unknown command ";
static uint8_t data_packet[SERIAL_PACKET_SIZE];

// Start serial module
void Serial_Start(void)
{
    UART_Start();
}

// Stop serial module
void Serial_Stop(void)
{
    UART_Stop();
}

// Check if we have data in rx buffer
uint8_t Serial_Available(void)
{
    return UART_GetRxBufferSize();
}

// Handle a command received
void Serial_HandleReceivedCommand()
{
    char rec = UART_GetChar();
    switch (rec)
    {
        case SERIAL_CONN_CMD:
            // Send string for connection
            Serial_SendConnectionPacket();
            Sensors_Reset();
            break;
        case SERIAL_START_STREAMING_CMD:
            // Start streaming
            Sensors_StartStreaming();
            break;
        case SERIAL_STOP_STREAMING_CMD:
            // Stop streaming
            Sensors_StopStreaming();
            break;
        case SERIAL_WAVE_1_CMD:
            // Set wave 1 
            Sensors_SetInputWave(SENSORS_WAVE_1);
            break;
        case SERIAL_WAVE_2_CMD:
            // Set wave 2
            Sensors_SetInputWave(SENSORS_WAVE_2);
            break;
        case SERIAL_RANGE_SMALL_CMD:
            // Set range to be small
            Sensors_SetInputRange(SENSORS_RANGE_SMALL);
            break;
        case SERIAL_RANGE_LARGE_CMD:
            // Set range to be large
            Sensors_SetInputRange(SENSORS_RANGE_LARGE);
            break;
        default:
            Serial_SendErrorMessage(rec);
    }
}

// Send a packet with signals data.
void Serial_SendDataPacket(uint16_t wave_1)
{
    // Send a packet with data
    data_packet[0] = 0xA0;
    data_packet[1] = wave_1 >> 8;
    data_packet[2] = wave_1 & 0xFF;
    data_packet[3] = 0xC0;
    UART_PutArray(data_packet, SERIAL_PACKET_SIZE);
}

// Send connection packet
void Serial_SendConnectionPacket(void)
{
    UART_PutString(conn_msg);
}

// Send error message
void Serial_SendErrorMessage(char c)
{
    UART_PutString(error_msg);
    char msg[3];
    sprintf(msg, "%c\r\n", c);
    UART_PutString(msg);
}
/* [] END OF FILE */
