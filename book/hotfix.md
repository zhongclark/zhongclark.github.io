外部资源复制
当一个资源文件较大时（大量图片、视屏等），不应该直接拖进工程里，而应该使用如下方法：

注：

1、"Copy items into destination groups's folder(if needed)"是将所要使用的文件，同时复制到项目的resource文件中。

2、"Create groups for any added folders"会为根据所有文件的目录层次生成不同层次的group，即逻辑上的文件夹。实际上这些资源将会散落在resource文件夹内，没有子文件夹。

3、"Create Folder References for any added folders"，会显示成蓝色的文件夹，实际上它们就是文件夹，在resource文件夹里会按实际结构放置文件。

一、步骤：

TARGETS->Build Phases->Add Build Phases(右下角)->Add Copy Files(右角) 把文件直接拖入 勾选copy选择Create Folder。。。 形成蓝色文件夹；



二、使用

NSString* homePath = [[NSBundle mainBundle]executablePath];

NSArray* strings = [homePath componentSeparatedByString:@"/"];

NSString* executableName = [strings objectAtIndex:[strings count]-1];

NSString* baseDic = [homePath subStringToIndex:[homePath length]-[executableName length]-1];

NSString* resourcePath = [NSString stringWithFormat:@"%@/图片/3.png", baseDic];



IOS FRAMEWORK，动态库 等几个问题


1，关于性能剖析工具的overhead问题，影响不影响数据统计出的函数时间的准确性？？？

比如unity的deepprofiling在移动平台上开销很大，那么这时候剖析出的数据还准不准确呢？

答案：总体数据是不准确的，内部拆分是准确的。

总体数据不准确是说某个函数如果调用层级较多，其中就有较多的Profiler.beginsample/endsample

注入，这导致这个函数总体时间编高，但在统计时送去所有这些额外开销就是准确的函数开销了

 

2，关于native plugins的问题

好像只要项目使用了native plugins 就要使用NDK

使用了IL2CPP，要用NDK，

 

3，关于IOS支持动态库吗？

IOS 支持系统的动态库，不支持用户自已的动态库，如果支持了用户自己的动态库那就可以用来热更了，为什么？

静态库是在打包时打到IPA中的，而动态库是在程序运行时动态链接进来的，所以可以实现热更。

 

关于framework是动态库还是静态库的问题

IOS8之前，framework只有苹果自己提供的可以用，且是静态库，IOS8之后，framework可以是动态库了，但保限于系统库，而用户自己创建的 .framework，并不算是动态库，而是 edmbeded framework，打包时也是直接打到IPA中的，所以不能算是真正的动态库，也无法实现热更，参考以下

 

参考链接：https://www.jianshu.com/p/9a1a3f5be434   

参考链接：https://www.jianshu.com/p/662832e16625 

以下是iOS app热更新的几种方案。

一、动态库
可以做demo用，真实使用的时候会被苹果禁止。

因为 打包发到AppStore的ipa安装包 里的每个动态库 都有唯一的编码，iOS系统会进行验证，所以动态通过网络获取 新的动态库 也用不了。

WWDC2014：允许使用动态库、允许第三方键盘、App Extension。
从目前来看，iOS仍然不允许进程间共享动态库，即iOS上的动态库只能是私有的，因为我们仍然不能将动态库文件放置在除了自身沙盒以外的其它任何地方。
iOS8上开放了App Extension功能，可以为一个应用创建插件，这样主app和插件之间共享动态库还是可行的。

二、lua脚本
比如： wax。
热更新时，从服务器拉去lua脚本。游戏开发经常用到。

三、Weex
跨平台，一套代码，iOS、Android都可以运行。用前端语法实现原生效果。比React Native更好用。
weex基于vue.js，ReactNative使用React。
ReactNative安装配置麻烦。 weex安装cli之后就可以使用。
react模板JSX有一定的学习成本，vue和常用的web开发类似，模板是普通的html，数据绑定用mustache风格，样式直接使用css。

四、React Native
不像Weex能一套代码多端运行，需要自己分别做修改。
React Native 可以动态添加业务模块，但无法做到修改原生OC代码。
JSPatch、lua 配合React Native可以让一个原生APP时刻处于可扩展可修改的状态。

五、Hybrid
像PhoneGap之类的框架, 基本概念和web差不多, 通过更新js/html来实现动态化，没有原生的效果流畅。

六、JSPatch
热更新时，从服务器拉去js脚本。理论上可以修改和新建所有的模块，但是不建议这样做。
建议 用来做紧急的小需求和 修复严重的线上bug。

七、rollout.io
Rollout紧急修复线上bug。后端有相关的管理页面。因为是国外的网站，然后呢，要翻墙才能使用。

八、DynamicCocoa
滴滴iOS的一个框架，准备在2017年初开源，与JSPatch比更加智能化，用OC在XCode中写完代码，用工具可以自动生成可以更新的js文件。

九、手机QQ虚拟机方案
手机QQ的一方案，将OC代码编译成自定义的二进制格式，下发到APP，然后在虚拟机里面运行