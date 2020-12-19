/**
*   \file Sensors_Defs.h
*   \brief Macros for sensor module.
*/

#ifndef __SENSORS_DEFS_H__
    #define __SENSORS_DEFS_H__
    
    #include "WaveDAC8.h"
    
    /**
    *   \brief Range small (1V).
    */
    #define SENSORS_RANGE_SMALL WaveDAC8_VDAC8_RANGE_1V 
    
    /**
    *   \brief Range large (4V).
    */
    #define SENSORS_RANGE_LARGE WaveDAC8_VDAC8_RANGE_4V
    
    /**
    *   \brief Input wave 1
    */
    #define SENSORS_WAVE_1 0
    
    /**
    *   \brief Input wave 2
    */
    #define SENSORS_WAVE_2 1
    
#endif

/* [] END OF FILE */
