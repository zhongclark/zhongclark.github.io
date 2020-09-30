子工程：
1、pod   第三方管理工程

2、core  核心层，数据的加密处理，接口的访问验证SSk加密方式，支付验证方式等，独立存在，不依赖任何模块
3、base  基本应用，基本类封装，分类，类扩展等，基本的数据处理，项目的底层安全过滤，依赖core核心层；
4、service  服务层，网络构架的封装，SQL数据的封装，各种使用技术的封装处理，项目的工具类的处理封装，依赖core核心层和base基本层；


5、QM           主项目，业务层，我们的表层代码，依赖basse和service


注意⚠️：core base service 创建动态库项目，原来MACO-Type 要改为静态，不然不允许上架;最新.framework选动态库还是静态库,都行,动态库现在也可以审核通过,其实这里选动态库没什么意义
base 里有分类，记得使用符号（一个空函数），使得category会被链接；或者在other linker flag内添加-ObjC。
service 内使用了一部分第三方库，Cartfile方式引入；
        brew install Carthage
        touch Cartfile
        Carthage update --platform iOS
        open Carthage


⚠️注意业务分的子模块，Build Active Architecture Only 的Debug 不要去设置为NO;

Demo1和Demo2文件的相互引用  https://www.jianshu.com/p/1fbf6f5ecf92
如果要在项目Demo1中引用Demo2中的文件，则必须要修改路径。在Demo1的Build Settings 里找到Header Search Paths，添加一项     (SRCROOT)是当前的工程路径，.. 是返回上一层，然后到TestApp_2文件夹。使用了相对路径，为了是项目移动不会影响这个配置，只要主工程和其他工程的相对位置不变，这里的相对位置是固定在同一个文件夹。
引入工程中的文件时，必须同时引入 .h 和 .m 文件。测试结果：
当Demo1里其他地方也同时调用了Demo2里的方法，则只需要引入.h文件，否则编译失败。

当我们开发framework时，在同时将多个自定义framework引入项目，framework如果想要达到之间相互访问(比如frameworkA想要访问frameworkB中的HelloWorld.h)，需要进行设置，否则会出现无法找到对应头文件的问题，常用于framework的模块化开发，当我们自己负责的模块需要引用公有模块时，可如此进行paths的设置

Swift中的访问修饰符对于扩展（extension）的影响 在Swift中，有一种结构extension，类似于OC中的Category分类，非常适合于对代码进行管理
同时，常用的访问修饰符有public、internal、private，而对于这三个访问修饰符，对extension的影响是各不一样的
在本文中，我将对同一文件下和不同文件下的extension、在本类和其他类调用，共四种情况进行分别介绍。
请说明并比较以下关键词：Open, Public, Internal, File-private, Private
Swift 有五个级别的访问控制权限，从高到低依次为 Open，Public，Internal，File-private，Private。

他们遵循的基本原则是：高级别的变量不允许被定义为低级别变量的成员变量。比如一个private的class中不能含有public的String。反之，低级别的变量却可以定义在高级别的变量中。比如public的class中可以含有private的Int。

Open 具备最高的访问权限。其修饰的类和方法可以在任意 Module 中被访问和重写；它是 Swift 3 中新添加的访问权限。
Public 的权限仅次于 Open。与 Open 唯一的区别在于它修饰的对象可以在任意 Module 中被访问，但不能重写。
Internal 是默认的权限。它表示只能在当前定义的 Module 中访问和重写，它可以被一个 Module 中的多个文件访问，但不可以被其他的 Module 中被访问。
File-private 也是 Swift 3 新添加的权限。其被修饰的对象只能在当前文件中被使用。例如它可以被一个文件中的class，extension，struct共同使用。
Private 是最低的访问权限。它的对象只能在定义的作用域内使用。离开了这个作用域，即使是同一个文件中的其他作用域，也无法访问。



在ios 7下，使用@import代替#import

#import "" 表示引用本地文件// 自己创建
#import <> 表示引用库文件 // 系统文件

在xcode 5 下，为了更易于开发，增加了modules和 auto-linking 这两个新特性。用 @import 来增加框架 到项目中比用 #import会更有效. 我们来看看为什么：

"Modules for system frameworks speed build time and provide an alternate means to import APIs from the SDK instead of using the C preprocessor. Modules provide many of the build-time improvements of precompiled headers with less maintenance or need for optimization. They are designed for easy adoption with little or no source changes. Beyond build-time improvements, modules provide a cleaner API model that enables many great features in the tools, such as Auto Linking."

Modules and auto-linking 默认情况下是enabled的。 如果是旧的项目，你可以通过设置"Language - Modules." 来设置Enable Modules 和Link Frameworks Automatically 为Yes。 另外一个使用moudules的好处是你再也不用去链接你的framework到你的项目了。例如，在以前，如果你要使用MapKit这个框架，你要这样做1) 使用语句 #import导入框架，2) 去到项目的build phases 设置项，找到MapKit.framework.并加入到Link Binary With Libraries里面。如果使用modules的话，只需要加入语句 "@import MapKit;" 你就可以开始使用了,根本不需要链接到你的项目。

解决 “building for iOS simulator, but linking in object file built for OSX, for architecture x86_64”
2016年3月14日发表评论阅读评论
在升级XCode到版本7以后，使用某些静态库(.a文件)，并为IOS模拟器编译时，可能会出现如标题所示错误，提示这个库是为OSX系统的X86_64平台编译的。这可能是XCode版本的一个BUG,在链接静态库时，优先链接了OSX平台下的obj,并抛编译错误。

xcode error

为解决此问题，我们在编译静态库时，不要将添加OSX系统下的平台，或者使用lipo将静态库中关于OSX系统平台的内容移除。

首先使用 “-info”选项查看静态库里包含了哪些平台内容：
╭─clark@lkbdeiMac.local /Users/WWW/FC/ZIKRouter/Products
╰─➤  lipo -info /Users/clark/Library/Developer/Xcode/DerivedData/Runner-dunriuopvgvvcycxlfjvkamsybfc/Build/Products/Debug-iphonesimulator/ZIKRouter.framework/ZIKRouter
Non-fat file: /Users/clark/Library/Developer/Xcode/DerivedData/Runner-dunriuopvgvvcycxlfjvkamsybfc/Build/Products/Debug-iphonesimulator/ZIKRouter.framework/ZIKRouter is architecture: x86_64
╭─clark@lkbdeiMac.local /Users/WWW/FC/ZIKRouter/Products
╰─➤  lipo -info /Users/clark/Library/Developer/Xcode/DerivedData/Runner-dunriuopvgvvcycxlfjvkamsybfc/Build/Products/Debug-iphoneos/ZIKRouter.framework/ZIKRouter
Non-fat file: /Users/clark/Library/Developer/Xcode/DerivedData/Runner-dunriuopvgvvcycxlfjvkamsybfc/Build/Products/Debug-iphoneos/ZIKRouter.framework/ZIKRouter is architecture: arm64

$ lipo -info libuuid.a 
Architectures in the fat file: libuuid3.a are: armv6 armv7 armv7s i386 arm64 x86_64
$ lipo -info libuuid.a 
Architectures in the fat file: libuuid3.a are: armv6 armv7 armv7s i386 arm64 x86_64
可以看到此静态库中包含了 i386和x86_64两个平台内容。然后使用 “-remove” 将其移除：

$ lipo libuuid.a -remove i386 -output libuuid.a
$ lipo libuuid.a -remove x86_64 -output libuuid.a
$ lipo -info libuuid.a
Architectures in the fat file: libuuid.a are: armv6 armv7 armv7s arm64
1
2
3
4
$ lipo libuuid.a -remove i386 -output libuuid.a
$ lipo libuuid.a -remove x86_64 -output libuuid.a
$ lipo -info libuuid.a
Architectures in the fat file: libuuid.a are: armv6 armv7 armv7s arm64
使用移除OSX平台内容后的静态库再次编译，问题解决。

但是会出现warning:

“ld: warning: ignoring file ……/libuuid.a, missing required architecture x86_64 in file ……/libuuid.a (4 slices)”

可以不用理会。但是在发布或部署到真机的时候，还是需要使用带有x86_64平台的静态库。


 1.采用手动方式导入的第三方库,在打包framework时候,添加到工程时候不要够算添加到当前打包的工程的framework
使用方法
1. 添加framework search路径
在settings中添加framework Search Paths参数$(PROJECT_DIR)/$(PROJECT_NAME)

cartfile要加：
$(SRCROOT)/../../Carthage/Build/iOS
并且脚本，framework也要引入

参数名	说明
$(PROJECT_DIR)	项目文件夹的相对路径
$(PROJECT_NAME)	项目名
image.png
注：$(PROJECT_DIR)/$(PROJECT_NAME)的路径设置生效前提是我们将多个framework引入项目。这样我们设置了路径的framework就能够访问项目路径下的其他framework。


3.在build Settings中 搜索 header search,会看到如下图：

 在 Header search Paths 中，加上你要引用的工程的路径，我采用的是相对路径；然后再搜 other link,会搜到如下图：

 
 在 Other LInker Flags 中加上 -Objc  和 -all_load

 

4.然后找到build Phases选项，如图

 加上B 工程的framework

并且确认，在Link Binary with libraries 中已经加入了 B工程中需要的framework, 和B工程生成的framework

image.png
2. 使用__has_include进行动态判断
由于不确定要引用的framework是否存在，使用__has_include进行动态判断避免编译失败

#if __has_include("FrameworkOne/FrameworkOne.h")
    #import "FrameworkOne/FrameworkOne.h"
#else
#endif
注：相关的方法调用也应进行__has_include判断


Xcode编译时出现ld: framework not found XXX的另一奇葩原因

之前自己抓包了一个直播平台的数据，自己写了一个简单的应用玩（并未上架，只是上传到github），用到了B站的IJKMediaFramework，之前都能好好安装，后来发现加载不出平台数据，然后更新了token，接口测试没问题，然后再重新往手机上安装，却总是报ld: framework not found IJKMediaFramework ld: framework not found IJKMediaFramework这样的错误。然后按照之前的方法：

添加Framework Search Path，没用；
删掉重新导入，没用；
重新添加IJKMediaFramework的依赖库，没用；
各种Clean，重启，没用；
回退到之前的版本，再运行，没用。
真是让人头大.gif
然后开始了各种奇思妙想，终于被我试出来了

解决办法
在主工程目录下，新建了一个文件夹，把IJKMediaFramework.framework拖进去，再Clean，编译，success！
WTF？ 为何这么坑爹！

关于ld: framework not found -xxxx 解决问题

每次遇到这种问题时解决起来都会很繁琐，因为这次用了这种方法解决了下次不一定管用，所以索性把问题和解决方法记录下来
ld: framework not found XXX

syqaxldy 2020-06-02 13:57:43  170  收藏
分类专栏： Xcode不能运行问题 报错信息
版权
ld: framework not found XXX
clang: error: linker command failed with exit code 1 (use -v to see invocation)

如遇到上面的问题
先确认Mac系统是否最近更新过, 如果更新过 就在终端 执行 sudo gem install cocoapods 命令
出现error 替换为 sudo gem install -n /usr/local/bin cocoapods

然后执行pod Install

最后cmd+ Shift +k - >清洁项目, 在编译即可!


iOS Framework lipo报错 lipo: can't map input file
fatal error: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/lipo: can't map input file: xxxFramework.framework/ (Invalid argument)

 

原因在于：

lipo -info xxxFramework.framework
 

而命令需要是

lipo -info xxxFramework.framework/xxxFramework
 

或者

cd xxxFramework.framework
lipo -info xxxFramework







//----------------------------------------------------------------------

# 运行此脚本前
# 先编译一遍工程  确保正常运行 没有报错
# 方式一：作为sh文件运行  修改 MY_LIB_NAME   MY_BUILD_TARGET_NAME 变量为目标targetName
# 工程目录下创建test.sh文件 全选粘贴此文本 命令行cd到工程目录下 运行命令sh test.sh
# 工程目录下/Products 生成合并后的framework文件


# 方式二：作为Xcode Aggregate运行
# file-->new target-->cross-platform-->Aggregate
# 修改 MY_LIB_NAME   MY_BUILD_TARGET_NAME 变量为目标targetName
# 注释代码 TARGET_DIR=${CUR_DIR}  打开代码 TARGET_DIR=${SRCROOT}
# bulild phases-->点击+号-->new run script phases-->拷贝本文件全部内容到脚本中
# 选择运行Aggregate -->工程目录下/Products 生成合并后的framework文件

# 关键字
# ${BUILD_ROOT}工程编译目录下 /Users/xxx/Library/Developer/Xcode/DerivedData/XXX-bpsdeolxlfmipxgqgqhtwtqqhzcy/Build/Products
# ${CONFIGURATION} 编译环境  Release   Debug
# ${SRCROOT}  作为sh文件单独运行 代表硬盘的根目录  作为Xcode Aggregate运行 代表工程目录

echo '****************Build Start*************'
#脚本运行当前目录
CUR_DIR=$(cd "$(dirname "$0")"; pwd)
echo '*****当前目录----'$CUR_DIR'*****'

#定义库的名字  ${PROJECT_NAME} "TestFramework"
MY_LIB_NAME= ${PROJECT_NAME}
#编译对象 target的名字  一般与工程名字一致
MY_BUILD_TARGET_NAME=${PROJECT_NAME}

#目标目录
#TARGET_DIR=${SRCROOT}  #作为Xcode-Aggregate运行打开
TARGET_DIR=${CUR_DIR}  #作为sh文件运行打开

#定义编译目录  当前工程的目录下
WRK_DIR=build

#编译模式  ${CONFIGURATION}   Release   Debug
MY_BUILD_MODE="Release"

#源文件
DEVICE_DIR=${WRK_DIR}/${MY_BUILD_MODE}-iphoneos/${MY_LIB_NAME}.framework
SIMULATOR_DIR=${WRK_DIR}/${MY_BUILD_MODE}-iphonesimulator/${MY_LIB_NAME}.framework

#swift库特有文件 AEXML.framework/Modules/AEXML.swiftmodule
MODULES_DEVICE_DIR=${DEVICE_DIR}/Modules/${MY_LIB_NAME}.swiftmodule
MODULES_SIMULATOR_DIR=${SIMULATOR_DIR}/Modules/${MY_LIB_NAME}.swiftmodule

# 目标文件
INSTALL_DIR=${TARGET_DIR}/Products/${MY_LIB_NAME}.framework
MODULES_INSTALL_DIR=${TARGET_DIR}/Products/${MY_LIB_NAME}.framework/Modules/${MY_LIB_NAME}.swiftmodule

# -configuration ${CONFIGURATION}
# Clean and Building both architectures.
xcodebuild -configuration "${MY_BUILD_MODE}" -target "${MY_BUILD_TARGET_NAME}" -sdk iphoneos -arch armv7 -arch armv7s -arch arm64 clean build
xcodebuild -configuration "${MY_BUILD_MODE}" -target "${MY_BUILD_TARGET_NAME}" -sdk iphonesimulator  -arch i386 -arch x86_64 clean build


echo '****************Build End*************'
echo '****************Compound Start*************'

#删除已经存在的文件
if [ -d "${INSTALL_DIR}" ]
then
rm -rf "${INSTALL_DIR}"
fi

#递归重建文件
mkdir -p "${INSTALL_DIR}"
#拷贝文件  ${DEVICE_DIR}/目录下的文件  拷贝到${INSTALL_DIR}/目录下
cp -R "${DEVICE_DIR}/" "${INSTALL_DIR}/"
#ditto "${DEVICE_DIR}/Headers" "${INSTALL_DIR}/Headers"

#合并库架构 同时支持模拟器和真机
lipo -create "${DEVICE_DIR}/${MY_LIB_NAME}" "${SIMULATOR_DIR}/${MY_LIB_NAME}" -output "${INSTALL_DIR}/${MY_LIB_NAME}"


#合并swift库特有文件 AEXML.framework/Modules/AEXML.swiftmodule
if [ -d "${MODULES_SIMULATOR_DIR}" ]
then

if [ -d "${MODULES_SIMULATOR_DIR}" ]
then
cp -R "${MODULES_SIMULATOR_DIR}/" "${MODULES_INSTALL_DIR}/"
fi

fi


rm -r "${WRK_DIR}"


# 打开文件夹
open "${TARGET_DIR}/Products"

echo '****************Compound End*************'



//----------------------------------------------------------------------


















1. ld: framework not found AFNetworking
一般出现这个问题是在swift项目上，因为swift需要用到use_framework!的原因。

网上搜索了一下，在stackoverflow找到了答案 >> 前往查看

终端输入对应的MyProject.xcworkspace,根据终端结果修改直到结果为：** BUILD SUCCEEDED **

xcodebuild -workspace MyProject.xcworkspace -configuration Debug -scheme MyProject build

2. ld: library not found for -xxxx clang: error: linker command failed with exit code 1 (use -v to see invocation)
这个一般出现在Object-C项目的pods上了，

尝试了添加$(inherited)无效之后,又尝试了Editor中的build添加+上pods上的库，依然解决不了，又疯狂寻找解决方法，可是网上答案众多可是基本解决不了，郁闷。

最后

把 pods 上的Build Active Architecture Only 改成NO就可以了

业务需求模拟
公司需要开发一款学习类的app，针对不同的用户层级开放两个用户端：学生端、老师端。

项目分析
方法一（普通版）：
新建俩个项目，一个是学生app，老师app
在开发的过程中，你会发现这俩个app有很多公共的模块，比如登录模块，用户中心模块.........
当你在学生端写完登录模块的时候，然后手动拷贝登录模块的代码到老师端，接着进行开发

-----来自菜鸟的阐述

方法二（改进版）
新建俩个项目，一个是学生app，老师app
把公共的模块组件化，在学生app，老师app分别我pod引用，省略了手动拷贝的操作。当公共组件更新的时候，分别在两个app项目端进行更新。

-----来自不那么菜的菜鸟的阐述

方法三（进阶版）
新建一个工作组workspace，在这个工作组上面新增学生project和老师project，两个工程公用一个工作组。同时工作组pod公共组件，俩project公用一套公共模块，这样可以及时更新。

-----来自具有逼格的老鸟的阐述




# 写在最上面，表示公用
platform :ios, '9.0'

#  用cocoapods导入OC框架到Swift项目 (混编项目)必须写该项
use_frameworks!

## workspace文件名
workspace 'Runner.xcworkspace'

##  主工程路径
project 'QM/QM.xcodeproj'

## 工程路径
target 'QM' do
project 'QM/QM.xcodeproj'
# pod 'SVProgressHUD'
end

##  工程路径
target 'QMService' do
project 'QMService/QMService.xcodeproj'
# pod 'MJRefresh'
end


## core
### 1、数据加密
数据加密方式（3类）
链路加密方式：加密是逐跳进行的，此方式为在离开一个节点进入信道时加密，在离开信道通过节点时解密，因此数据在信道中呈现密文形式，在节点中呈现明文形式

节点到节点加密方式：不允许信息在节点中以明文形式存在，为了解决在节点中是明文的情况，在中间节点里装有加密解密的保护装置，在节点中完成一个密钥向另一个密钥转换的过程，即将数据进行解密和加密，在节点中有一个安全模块，在模块中采用另一个密钥进行数据的加密，加密过程是不可见的，解决了在节点中是明文的情况（节点加密要求报头和路由信息都是明文，以便中间节点能够得到如何处理信息的信息）

端到端加密方式：在源端进行加密，在传输过程中不解密，一直到达目的端才进行解密。因此对于中继节点来说，用户数据是不可知的密文。
一、MD5
SHA1
二、 RSA 非对称加密算法 (公钥私钥生成步骤点击 https://blog.csdn.net/u013983033/article/details/84565003)
AES256
三、对称加密算法  DES
Base64编码解码： https://www.cnblogs.com/Blueleaf-tech/p/9807826.html


四、应用加密
字符串加密：对字符串进行加密保护，防止通过IDA等工具获取关键词定位核心业务代码
代码逻辑混淆：在编译环节将iOS代码逻辑变形膨胀复杂化，降低反编译及逆向破解风险
符号混淆 ：将代码中类名、方法名、属性名替换为无意义符号，增加代码逆向难度
反调试 ：高级的反调试技术，防止攻击者、恶意分析者动态调试分析程序

五、数据库加密 https://www.jianshu.com/p/c5e2ca4f5057 
https://en.softonic.com/download/mesasqlite/mac/post-download  mesasqlite下载
https://blog.csdn.net/shihuboke/article/details/76695323 MesaSQLite数据库简单使用
### 2、API加密
https://blog.csdn.net/GeeLoong/article/details/101364760?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param



### 3、接口的访问验证
https://blog.csdn.net/weixin_33856370/article/details/88017870 iOS实现简书的登录验证方式(极验验证==>验证码中带广告)
token验证机制 
HTTPS 证书链的验证 

### 4、 SSK 加密方式（SSK Key的秘钥对）

### 5、支付验证方式
https://www.cnblogs.com/zhaoqingqing/p/4597794.html 
https://www.cnblogs.com/alphagl/p/6035546.html  SDK接入(3)之iOS内支付(In-App Purchase)接入



很多人做iOS开发都会遇到的一个问题就是，随着做iOS开发时间的越久，越觉得有一个瓶颈始终突破不了，想要进一步的提升却始终不得其法，其实是由于缺乏对于iOS底层的原理的深入认知，只有深入底层才能了解到每一个程序的实现机制，对于自己以后做开发更容易做到心中有数。

为了更好的帮助大家进行更好的探索iOS底层原理，打牢根基，李明杰老师（M了个J）特意推出《iOS底层原理班》，考虑到学习的大部分同学都是在职开发人员，平时工作繁忙，时间宝贵，所以本次课程采用线上录播的形式进行讲授，课程在腾讯课堂搜索“小码哥教育”即可找到。大大降低同学们的时间成本，MJ老师也会在课程群内和同学们互动，有问题可以随时沟通，学习起来更方便。

本次iOS底层原理班分为上下两部分

上部分主要内容有：

iOS常用工具：SSH、Cycript、Reveal

系统原理：Machine-O、MachOview

加壳脱壳：Clutch

插件开发：Cydia Substrate

开发实战：喜马拉雅FM

动态调试：debugserver

编译原理：8086汇编、x86汇编

常用工具：签名机制、对称密码

等等……

下部分主要内容有：

OC语法：OC对象的本质

Block：底层数据结构

Runtime：非指针isa

Runloop：CFRunLoopModeRef

多线程：gcd、GNUstep

内存管理：定时器内存泄漏

性能优化：卡顿检测

架构设计：设计模式

iOS底层原理班免费视频下载网盘链接：
链接: https://pan.baidu.com/s/1fcWwM4_KnAj0Op-ur7TOgA 提取码: p598
如链接失效，添加QQ群982033246进群联系管理员获取即可。
视频目录
01-课程简介
001-课程简介.mp4
002-学习条件.mp4

02-环境搭建
003-越狱的优点和缺点.mp4
004-完美越狱和非完美越狱.mp4
005-Cydia.mp4
006-必备软件安装.mp4
007-代码判断设备是否越狱.mp4
008-提高工作效率的工具.mp4

03-OC对象的本质
001-OC和C_C++.mp4
002-将OC转换为C_C++.mp4
003-NSObject的内存本质.mp4
004-class_getInstanceSize、malloc_size.mp4
005-回答面试题.mp4
006-窥探NSObject的内存.mp4
007-Student的本质.mp4
008-Student的内存布局.mp4
009-更复杂的继承结构.mp4
010-属性和方法.mp4
011-答疑.mp4
012-内存分配注意点.mp4
013-alloc的size分析.mp4
014-libmalloc源码.mp4
015-glibc源码.mp4
016-sizeof注意点.mp4





## 解决Mac 电脑 Finder无响应卡慢问题

终端执行下面命令 删除finder的plist文件

cd Library/Preferences
rm -rf com.apple.finder.plist 


这里直接说最后的解决办法
brew upgrade carthage
and then
carthage update --platform ios
over!