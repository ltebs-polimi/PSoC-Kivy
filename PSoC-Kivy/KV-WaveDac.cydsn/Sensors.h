/**
*   \file Sensors.h
*   \brief Header file for sensors module.
*/

#ifndef __SENSORS_H__
    #define __SENSORS_H__
    
    #include "cytypes.h"
    #include "Sensors_Defs.h"
    
    /**
    *   \brief Start the sensors module.
    */
    void Sensors_Start(void);
    
    /**
    *   \brief Stop the sensors module.
    */
    void Sensors_Stop(void);
    
    /**
    *   \brief Start the sensors module.
    */
    void Sensors_Reset(void);
    
    /**
    *   \brief Start streaming of sensors data.
    */
    void Sensors_StartStreaming(void);
    
    /**
    *   \brief Check if module is streaming data
    */
    uint8_t Sensors_IsStreaming(void);
    
    /**
    *   \brief Stop streaming of sensors data.
    */
    void Sensors_StopStreaming(void);
    
    /**
    *   \brief Set input range for the wave.
    */
    void Sensors_SetInputRange(uint8_t range);
    
    /**
    *   \brief Set input wave.
    */
    void Sensors_SetInputWave(uint8_t wave);
    
    /**
    *   \brief Send sampled data.
    */
    void Sensors_SendData(void);
    
#endif

/* [] END OF FILE */
