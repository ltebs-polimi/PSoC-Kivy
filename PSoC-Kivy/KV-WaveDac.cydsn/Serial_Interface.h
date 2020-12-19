/**
*   \file Serial_Interface.h
*   \brief Header file for Serial module.
*
*   The serial module takes care of handling all
*   the received commands and of streaming data.
*/

#ifndef __SERIAL_INTERFACE_H__
    #define __SERIAL_INTERFACE_H__
    
    #include "cytypes.h"
    #include "Serial_Interface_Defs.h"
    
    /**
    *   \brief Start the serial module.
    */
    void Serial_Start(void);
    
    /**
    *   \brief Stop the serial module.
    */
    void Serial_Stop(void);
    
    /**
    *   \brief Check if there are data in the rx buffer.
    */
    uint8_t Serial_Available(void);
    
    /**
    *   \brief Handle a command received from UART.
    */
    void Serial_HandleReceivedCommand();
    
    /**
    *   \brief Send a packet with signal data.
    */
    void Serial_SendDataPacket(uint16_t wave);
    
    /**
    *   \brief Send a packet with a predefined string.
    */
    void Serial_SendConnectionPacket(void);
    
    /**
    *   \brief Send error message when unknown cmd is received.
    */
    void Serial_SendErrorMessage(char c);
    
#endif

/* [] END OF FILE */
