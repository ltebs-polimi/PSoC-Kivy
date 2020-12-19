/**
*   \file Serial_Interface_Defs.h
*   \brief Macros and commands for serial interface.
*/

#ifndef __SERIAL_INTERFACE_DEFS_H__
    
    #define __SERIAL_INTERFACE_DEFS_H__
    
    /**
    *   \brief Size of the packet to be transmitted.
    */
    #define SERIAL_PACKET_SIZE 4
    
    /**
    *   \brief Connection command.
    */
    #define SERIAL_CONN_CMD 'v'
    
    /**
    *   \brief Start streaming command.
    */
    #define SERIAL_START_STREAMING_CMD 'b'
    
    /**
    *   \brief Stop streaming command.
    */
    #define SERIAL_STOP_STREAMING_CMD 's'
    
    /**
    *   \brief Wave 1 select command.
    */
    #define SERIAL_WAVE_1_CMD 'e'
    
    /**
    *   \brief Wave 2 select command.
    */
    #define SERIAL_WAVE_2_CMD 'f'
    
    /**
    *   \brief Range small select command.
    */
    #define SERIAL_RANGE_SMALL_CMD 't'
    
    /**
    *   \brief Range large select command.
    */
    #define SERIAL_RANGE_LARGE_CMD 'y'
    
#endif
/* [] END OF FILE */
