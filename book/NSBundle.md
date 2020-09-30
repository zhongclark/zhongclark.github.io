iOS开发-动态库的加载方式（二）以资源文件（NSBundle）的形式添加


写在前面：对于开发企业级应用的开发者而已，以资源文件的形式来加载动态库就显得尤为重要，因为，给不同的客户打不同的IPA包，里面的有些功能是不一样，比如说有一个动态库是专门为一个客户制定的，那么在给其他客户打包时就不应该把这个动态库打进去。所以，为了解决这个问题，我们可以使用下面的这种加载方式。

1.添加动态库到资源

277EFE9E-0FBC-4288-991E-5BD5914D15FA.png
237D411C-396B-4B9D-9355-829A45AF9053.png
然后，选择你刚才放在主工程目录下的动态库。这时项目目录下多了一个动态库。倘若你之前直接拖进来时目录下就已经存在，请先右键删除引用。

2.动态加载动态库
直接上我项目中实际使用的代码：
这个动态库主要实现的是一个视频会议的功能
这个TBConfMeetingApi类是我处理这个创建会议和加入会议的一个工具类
.h文件

//
//  TBConfMeetingApi.h
//  Ecm
//
//  Created by zengchunjun on 16/9/13.
//
//

#import <Foundation/Foundation.h>
#import "TBConfMeetingManager.h"

@interface TBConfMeetingApi : NSObject

+ (void)joinConfWithSiteName:(NSString*)siteName DisplayName:(NSString*)displayName andUserName:(NSString*)userName MeetingID:(NSString*)meetingID MeetingPwd:(NSString*)meetingPwd WithPortrait:(NSString*) portrait VC:(UIViewController*)vc shareCallBack:(TBConferenceShareCallback)shareCallBack;

+ (void)createConfWithSiteName:(NSString*)siteName DisplayName:(NSString *)displayName andUserName:(NSString*)userName HostPwd:(NSString*)hostPwd MeetingTopic:(NSString*)meetingTopic MeetingPwd:(NSString *)meetingPwd WithAutoAdjustVideoBitrate:(BOOL)autoAdjustVideoBitrate VC:(UIViewController *)vc createCallBack:(TBConferenceEnterCallback)createCallBack shareCallBack:(TBConferenceShareCallback)shareCallBack;

@end
.m文件

//
//  TBConfMeetingApi.m
//  Ecm
//
//  Created by zengchunjun on 16/9/13.
//
//

#import "TBConfMeetingApi.h"

@implementation TBConfMeetingApi
// 初始化动态库，也就是加载动态库
+ (BOOL)initFramework
{
    if ([[UIDevice currentDevice].systemVersion floatValue] < 8.0)
    {
        NSLog(@"%s",__func__);
        return NO;
    }
    // 使用GCD一次性代码来只加载一次动态库
    static dispatch_once_t priOnceToken;
    dispatch_once(&priOnceToken, ^
                  {
                      NSString *path = [[[NSBundle mainBundle] bundlePath] stringByAppendingPathComponent:@"TBConfMeeting.framework"];
                      
                      NSError *err = nil;
                      NSBundle *bundle = [NSBundle bundleWithPath:path];
                      if ([bundle loadAndReturnError:&err])
                      {
                          NSLog(@"bundle load framework success.");
                          
                      }
                      else
                      {
                          NSLog(@"bundle load framework err:%@", err);
                          
                      }
                  });
    return YES;
}

+ (void)createConfWithSiteName:(NSString*)siteName DisplayName:(NSString *)displayName andUserName:(NSString*)userName HostPwd:(NSString*)hostPwd MeetingTopic:(NSString*)meetingTopic MeetingPwd:(NSString *)meetingPwd WithAutoAdjustVideoBitrate:(BOOL)autoAdjustVideoBitrate VC:(UIViewController *)vc createCallBack:(TBConferenceEnterCallback)createCallBack shareCallBack:(TBConferenceShareCallback)shareCallBack
{
//#if !TARGET_IPHONE_SIMULATOR
//    [[ConfWithVc shareInstance] createConfWithSiteName:siteName DisplayName:displayName andUserName:userName HostPwd:hostPwd MeetingTopic:meetingTopic MeetingPwd:meetingPwd WithAutoAdjustVideoBitrate:autoAdjustVideoBitrate VC:vc createCallBack:callBack];
//#endif
    
    if (![self initFramework]) {
        return ;
    }
    NSString *className = @"TBConfMeetingManager";
    NSString *methodName = @"createConfWithSiteName:DisplayName:andUserName:HostPwd:MeetingTopic:MeetingPwd:WithAutoAdjustVideoBitrate:VC:createCallBack:shareCallBack:";
    Class class = NSClassFromString(className);
    NSMethodSignature *sig = [[class class] methodSignatureForSelector:NSSelectorFromString(methodName)];
    if (sig)
    {
        NSInvocation *invocation = [NSInvocation invocationWithMethodSignature:sig];
        if (invocation)
        {
            [invocation setTarget:class];
            [invocation setSelector:NSSelectorFromString(methodName)];
            [invocation setArgument:&siteName atIndex:2];
            [invocation setArgument:&displayName atIndex:3];
            [invocation setArgument:&userName atIndex:4];
            [invocation setArgument:&hostPwd atIndex:5];
            [invocation setArgument:&meetingTopic atIndex:6];
            [invocation setArgument:&meetingPwd atIndex:7];
            [invocation setArgument:&autoAdjustVideoBitrate atIndex:8];
            [invocation setArgument:&vc atIndex:9];
            [invocation setArgument:&createCallBack atIndex:10];
            [invocation setArgument:&shareCallBack atIndex:11];
            [invocation invoke];
            const char *returnType = sig.methodReturnType;
            int *result;
            if(!strcmp(returnType, @encode(int)))
            {
                [invocation getReturnValue:&result];
            }
//            return result;
        }
    }
    
    
}

+ (void)joinConfWithSiteName:(NSString*)siteName DisplayName:(NSString*)displayName andUserName:(NSString*)userName MeetingID:(NSString*)meetingID MeetingPwd:(NSString*)meetingPwd WithPortrait:(NSString*) portrait VC:(UIViewController*)vc shareCallBack:(TBConferenceShareCallback)shareCallBack
{
//#if !TARGET_IPHONE_SIMULATOR
//    [[ConfWithVc shareInstance] joinConfWithSiteName:siteName DisplayName:displayName andUserName:userName MeetingID:meetingID MeetingPwd:meetingPwd WithPortrait:nil VC:vc];
//#endif
    
    if (![self initFramework]) {
        return;
    }
    NSString *className = @"TBConfMeetingManager";
    NSString *methodName = @"joinConfWithSiteName:DisplayName:andUserName:MeetingID:MeetingPwd:WithPortrait:VC:shareCallBack:";
    Class class = NSClassFromString(className);
    NSMethodSignature *sig = [[class class] methodSignatureForSelector:NSSelectorFromString(methodName)];
    if (sig)
    {
        NSInvocation *invocation = [NSInvocation invocationWithMethodSignature:sig];
        if (invocation)
        {
            [invocation setTarget:class];
            [invocation setSelector:NSSelectorFromString(methodName)];
            [invocation setArgument:&siteName atIndex:2];
            [invocation setArgument:&displayName atIndex:3];
            [invocation setArgument:&userName atIndex:4];
            [invocation setArgument:&meetingID atIndex:5];
            [invocation setArgument:&meetingPwd atIndex:6];
            [invocation setArgument:&portrait atIndex:7];
            [invocation setArgument:&vc atIndex:8];
            [invocation setArgument:&shareCallBack atIndex:9];
            
            [invocation invoke];
                    }
    }
}

@end
