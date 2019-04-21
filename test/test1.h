#ifndef _DCOP_ERR1_H_
#define _DCOP_ERR1_H_

/// 错误码基址(需要左移16个bit)
enum DCOP_ERRCODE
{
    SUCCESS = 0,

    ERRCODE_OS,                                 // 0x0001 - 基础相关错误码
    ERRCODE_TASK,                               // 0x0002 - 任务相关错误码
    ERRCODE_SEM,                                // 0x0003 - 信号量相关错误码
    ERRCODE_MSG,                                // 0x0004 - 消息相关错误码
    ERRCODE_SOCK,                               // 0x0005 - 套接字相关错误码
    ERRCODE_IO,                                 // 0x0006 - 输入输出相关错误码

    ERRCODE_END,

    ERRCODE_USER = 0x000F                       // 0x000F - 用户自定义错误码
};


#endif // #ifndef _DCOP_ERR1_H_