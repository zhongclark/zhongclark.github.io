
https://www.jianshu.com/p/2ea267bf0363 iOS动态库,静态库以及framework
https://www.jianshu.com/p/e588bb0411d8  xcode制作iOS静态库SDK<包含第三方.a或者.framework静态库>
https://www.cnblogs.com/sundaysme/articles/11824054.html 打包.framework 静态库pod导入依赖第三方
https://www.jianshu.com/p/8e938f562e82 iOS SDK 开发之静态库framework开发、调试、及上传pod
https://www.jianshu.com/p/fe99020585e2 xcode8 Framework制作
https://www.jianshu.com/p/0509b438e84e Xcode Build Settings 分析
https://www.jianshu.com/p/85dd8786639c iOS 使用cocoapods发布静态库.a或framework

https://blog.csdn.net/wenzfcsdn/article/details/43489289?utm_medium=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param    Xcode中如何新建Category、Empty File、Protocol、Extension

https://www.jianshu.com/p/1fbf6f5ecf92 iOS 在同一个workspace下跨项目文件的相互引用
https://www.jianshu.com/p/a2a345297e60  iOS开发-工作空间workspace多项目管理与依赖(引用)
https://www.cnblogs.com/JustForHappy/p/5773039.html iOS xcode创建静态库封装自己的SDK及使用
https://www.jianshu.com/p/b6c59d8ed2c9 iOS使用Workspace来管理多项目
https://www.jianshu.com/p/764d953d3c5e iOS 项目依赖子模块工程



Pod::Spec.new do |s|

  s.name         = "XXX" //名称
  s.version      = "0.0.1"  //⚠️注意：版本号，也是tag(必须和tag版本一致)
  s.summary      = "XXX summary" //Tools 的总结
  s.description  = <<-DESC XXX的描述，一些介绍。DESC //这里的描述，必须比s.summary的长度要长。
  s.homepage     = "https://github.com/xxx/XXX" //远程仓库的首页地址
  s.license      = "MIT"  //MIT
  s.author       = { "xxx" => "xxxxxx@qq.com" } //作者，邮箱
  s.platform     = :ios, "5.0"
  s.source       = { :git => "https://github.com/xxxx/xxx.git", :tag => s.version } //git => 远程仓库的clone地址, tag取版本号就行
  s.requires_arc = true //ARC
  s.source_files  = "Classes", "Classes/**/*.{h,m}" //包含文件，Classes文件下的所有.h.m
  s.resources = "XXX/XXXUIResource.bundle" //多个资源用逗号隔开 (某个文件夹下/某个资源文件 , 下同)
  //
  s.ios.preserve_paths = 'XXX/xxx.a'//设置.a文件，多个用逗号隔开
  s.vendored_frameworks = 'XXX/XXXFramework.framework'//设置了framework，才会显示在文件夹中
  s.frameworks = "AudioToolbox", "AVFoundation", "CoreGraphics"//引用的系统库
  s.libraries = "iconv", "xml2", "bz2", "z", "stdc++", "c++"//引用一些lib库

  s.requires_arc = true //ARC
  s.dependency "MJRefresh" //引用的第三方库，配置，多个就写多个
  s.dependency "MJExtention"


end



1.工作空间workspace多项目管理
在桌面新建一个workspace的文件夹，并新建一个workspace放到该文件夹中，用来存放多个项目。接下来我们的所有工程都会存放在该目录下。

.接下来，打开Appgame.xcworkspace工作空间，并向该工作空间中添加一个静态库项目，一个动态库项目以及一个app主工程项目。
分别创建CommentStatic静态库、CommentFramework动态库以及Appgame主工程项目，都存放在桌面的workspace文件夹下。
File -> New -> Project... -> Cocoa Touch Static Library
File -> New -> Project... -> Cocoa Touch Framework
File -> New -> Project... -> Single View Application

添加方式一：创建CommentFramework静态库项目，项目放在桌面的workspace文件夹下，并添加到 我们创建的Appgame.xcworkspace工作空间中。

注意:Group也选择工作空间，你自己可以选择不同的来看一下效果。


添加方式二：新建的项目存放在桌面的workspace文件夹下，然后再添加到Appgame.xcworkspace中。这里不用添加到任何工作空间中。
然后添加到工作空间中：
桌面workspace文件夹下的截图以及通过Appgame.xcworkspace打开的项目截图：
第一点到此结束


2.workspace中主工程引用静态库或动态库

添加.a或Framework库引用
选中主工程，添加依赖库。是主工程需要引用静态库和动态库，所有是在主工程中引入静态库与动态库。

主工程(Appgame) -> TARGETS -> Build Phases -> Link Binary With Libraries

addlib.png
lib&framework.png
添加头文件

addHeaderFile.png
framework.png
添加资源文件(自定义Bundle或存放在mainBundle下的)
对于资源文件的引用遇到了一点问题，等待解决。现在可以直接把资源文件放入主工程。下面就介绍如何制作Bundle TARGETS

3.静态库资源文件(图片、xib、plist等)打包成bundle

**添加 编译 Bundle 的TARGETS

add target.png
bundleTargets.png
修改 base SDK

base SDK.png
编译资源

bundle coding.png
项目中使用

在静态库和动态库简单的分别创建 一个打印方法，在主工程中进行调用。

result.png
对于头文件的引用也可以直接将头文件放出主工程中。自定义Bundle的简单调用可自行Google。

实战截图:

appgames.png
关于动态库的加载方式可以看我之前的文章
iOS开发-动态库的加载方式（一）编译时添加
iOS开发-动态库的加载方式（二）以资源文件（NSBundle）的形式添加

写在最后

假如你正在做一个SDK的工作，需要在动态库中包含framework，你可能还是存在疑问。那么，请先移步如何判断framework是动态库或静态库以及framework静态库转.a静态库


