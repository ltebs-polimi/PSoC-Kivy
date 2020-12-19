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
#include "project.h"
#include "Serial_Interface.h"
#include "Sensors.h"

int main(void)
{
    CyGlobalIntEnable; /* Enable global interrupts. */

    /* Place your initialization/startup code here (e.g. MyInst_Start()) */
    Serial_Start();
    Sensors_Start();
    
    for(;;)
    {
        if (Serial_Available())
        {
            Serial_HandleReceivedCommand();
        }
        if (Sensors_IsStreaming())
        {
            Sensors_SendData();
        }
    }
}

/* [] END OF FILE */
