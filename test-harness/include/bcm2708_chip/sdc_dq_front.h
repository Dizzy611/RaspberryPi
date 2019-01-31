// This file was generated by the create_regs script
#define DPHY_CSR_BASE                                            0x7ee07000
#define DPHY_CSR_DQ_REV_ID                                       HW_REGISTER_RW( 0x7ee07000 ) 
#define DPHY_CSR_GLBL_DQ_DLL_RESET                               HW_REGISTER_RW( 0x7ee07004 ) 
#define DPHY_CSR_GLBL_DQ_DLL_RECALIBRATE                         HW_REGISTER_RW( 0x7ee07008 ) 
#define DPHY_CSR_GLBL_DQ_DLL_CNTRL                               HW_REGISTER_RW( 0x7ee0700c ) 
#define DPHY_CSR_GLBL_DQ_DLL_PHASE_LD_VL                         HW_REGISTER_RW( 0x7ee07010 ) 
#define DPHY_CSR_GLBL_DQ_MSTR_DLL_BYP_EN                         HW_REGISTER_RW( 0x7ee07014 ) 
#define DPHY_CSR_GLBL_MSTR_DLL_LOCK_STAT                         HW_REGISTER_RW( 0x7ee07018 ) 
#define DPHY_CSR_BYTE0_SLAVE_DLL_OFFSET                          HW_REGISTER_RW( 0x7ee0701c ) 
#define DPHY_CSR_BYTE1_SLAVE_DLL_OFFSET                          HW_REGISTER_RW( 0x7ee07020 ) 
#define DPHY_CSR_BYTE2_SLAVE_DLL_OFFSET                          HW_REGISTER_RW( 0x7ee07024 ) 
#define DPHY_CSR_BYTE3_SLAVE_DLL_OFFSET                          HW_REGISTER_RW( 0x7ee07028 ) 
#define DPHY_CSR_BYTE0_MASTER_DLL_OUTPUT                         HW_REGISTER_RW( 0x7ee0702c ) 
#define DPHY_CSR_BYTE1_MASTER_DLL_OUTPUT                         HW_REGISTER_RW( 0x7ee07030 ) 
#define DPHY_CSR_BYTE2_MASTER_DLL_OUTPUT                         HW_REGISTER_RW( 0x7ee07034 ) 
#define DPHY_CSR_BYTE3_MASTER_DLL_OUTPUT                         HW_REGISTER_RW( 0x7ee07038 ) 
#define DPHY_CSR_NORM_READ_DQS_GATE_CTRL                         HW_REGISTER_RW( 0x7ee0703c ) 
#define DPHY_CSR_BOOT_READ_DQS_GATE_CTRL                         HW_REGISTER_RW( 0x7ee07040 ) 
#define DPHY_CSR_PHY_FIFO_PNTRS                                  HW_REGISTER_RW( 0x7ee07044 ) 
#define DPHY_CSR_DQ_PHY_MISC_CTRL                                HW_REGISTER_RW( 0x7ee07048 ) 
#define DPHY_CSR_DQ_PAD_DRV_SLEW_CTRL                            HW_REGISTER_RW( 0x7ee0704c ) 
#define DPHY_CSR_DQ_PAD_MISC_CTRL                                HW_REGISTER_RW( 0x7ee07050 ) 
#define DPHY_CSR_DQ_PVT_COMP_CTRL                                HW_REGISTER_RW( 0x7ee07054 ) 
#define DPHY_CSR_DQ_PVT_COMP_OVERRD_CTRL                         HW_REGISTER_RW( 0x7ee07058 ) 
#define DPHY_CSR_DQ_PVT_COMP_STATUS                              HW_REGISTER_RW( 0x7ee0705c ) 
#define DPHY_CSR_DQ_PVT_COMP_DEBUG                               HW_REGISTER_RW( 0x7ee07060 ) 
#define DPHY_CSR_DQ_PHY_READ_CTRL                                HW_REGISTER_RW( 0x7ee07064 ) 
#define DPHY_CSR_DQ_PHY_READ_STATUS                              HW_REGISTER_RW( 0x7ee07068 ) 
#define DPHY_CSR_DQ_SPR_RW                                       HW_REGISTER_RW( 0x7ee0706c ) 
#define DPHY_CSR_DQ_SPR1_RO                                      HW_REGISTER_RW( 0x7ee07070 ) 
#define DPHY_CSR_DQ_SPR_RO                                       HW_REGISTER_RW( 0x7ee07074 ) 
#define DPHY_CSR_CRC_CTRL                                        HW_REGISTER_RW( 0x7ee07800 ) 
   #define DPHY_CSR_CRC_CTRL_MASK                                0x00000111
   #define DPHY_CSR_CRC_CTRL_WIDTH                               9
   #define DPHY_CSR_CRC_CTRL_RESET                               0000000000
#define DPHY_CSR_CRC_DATA                                        HW_REGISTER_RW( 0x7ee07804 ) 
   #define DPHY_CSR_CRC_DATA_MASK                                0x0fffffff
   #define DPHY_CSR_CRC_DATA_WIDTH                               28
   #define DPHY_CSR_CRC_DATA_RESET                               0000000000
