VuePress
看云
语雀
BookStack
docsify
Docute
MinDoc
Wikitten
DokuWiki
MkDocs
北半球（疑似关闭）
知笔墨（疑似关闭）
Penflip




马甲包绕过审核技巧整理

现在马甲包制作越来多，很多时候上线时就会被拒，据说帮助某彩票app马甲上线成功一个可以给到一万元的酬金。废话少说，我整理了下我用到的绕过审核的方案，主要是代码混淆与更改工程名，具体附上链接：

1. iOS使用Shell脚本批量修改类名称

2. iOS使用shell脚本批量修改属性

3.更改项目工程名


什么是zsh？
zsh类似bash也是一种shell.

zsh优点：

兼容bash；
智能拼写纠正；
各种补全:路径,命令,命令参数；
如何安装zsh？
Mac系统其实已经安装有zsh，但和大多数Linux类似，默认使用的是bash，不过我们只需简单进行配置即可更换。

执行cat /etc/shells可以查看系统已经安装的shell

执行echo $SHELL可以查看用户当前使用的shell

执行如下命令，即可更改用户默认使用的shell为zsh

chsh -s /bin/zsh
需要重新打开终端生效

执行zsh --version可以查看当前zsh的版本

如何配置zsh？
zsh的配置文件在~/.zshrc，刚安装后还没有这个文件。

一种方式是我们可以手动创建这个文件，然后加入自己需要的配置；
（推荐）另一种方式是我们可以从网上找别人已经配置好的文件，然后在这个模板上修改.这里推荐安装的是：oh-my-zsh；
oh-my-zsh安装：https://github.com/robbyrussell/oh-my-zsh

1.安装zsh
mac下自带zsh，但不是最新。查看zsh版本：zsh --version
可以通过brew安装最新版，brew install zsh

2.安装oh-my-zsh
cd ~
git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh
～目录下没有.zshrc
3.1   touch .zshrc
3.2   cp ~/.zshrc   ~/.zshrc.orig
创建zsh配置文件
cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc
配置兼容bash环境变量
.zshrc 文件中添加source ~/.bash_profile
修改默认shell
chsh -s /bin/zsh
修改zsh主题
.zshrc 文件ZSH_THEME=gnzh
【其他】

github zsh 主题参考
自定义zsh提示符
3.zsh安装插件
3.1高亮命令
MAC 系统
brew install zsh-syntax-highlighting
oh-my-zsh用户
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
激活插件
编辑.zshrc, plugins=( [plugins...] zsh-syntax-highlighting)
3.2 z插件
功能：模糊匹配曾经进入的目录
激活方式：plugins=( [plugins...] z)



# --- Sourcetree Generated ---
Host ClarkZhong-GitHub
	HostName github.com
	User ClarkZhong
	PreferredAuthentications publickey
	IdentityFile /Users/clark/.ssh/ClarkZhong-GitHub
	UseKeychain yes
	AddKeysToAgent yes
# ----------------------------

SSH_ENV="$HOME/.ssh/environment"
    function start_agent {
    echo "Initialising new SSH agent..."
    /usr/bin/ssh-agent | sed 's/^echo/#echo/' > "${SSH_ENV}"
    echo succeeded
    chmod 600 "${SSH_ENV}"
    . "${SSH_ENV}" > /dev/null
    /usr/bin/ssh-add;
    }
    # Source SSH settings, if applicable
    if [ -f "${SSH_ENV}" ]; then
    . "${SSH_ENV}" > /dev/null
    #ps ${SSH_AGENT_PID} doesn’t work under cywgin
    ps -ef | grep ${SSH_AGENT_PID} | grep ssh-agent$ > /dev/null || {
    start_agent;
    }
    else
    start_agent;
    fi

brew install nvm
安装成功之后，还不能直接使用nvm命令，需要进行以下配置，将以下命令复制到终端执行：

echo "source $(brew --prefix nvm)/nvm.sh" >> .zshrc

mac安装nvm超详细
1、从github下载nvm仓库到 ~/目录  地址：https://github.com/nvm-sh/nvm.git


2、进入 nvm目录中执行install.sh 等待执行完成


3、配置nvm环境变量将下述代码复制到 ~/.bash_profile

export NVM_DIR="$HOME/.nvm"

[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" 

 # This loads nvm

[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# This loads nvm bash_completion


4、执行source  ~/.bash_profile


5、执行nvm --version是否可以正常输出，若不行则重启终端再次尝试

6、nvm操作

   ①：使用  nvm install  node版本号  也可直接输入nvm install node 最新版本

   ②：使用 nvm list  或  nvm ls  可查看当前安装的node版本            

   ③：使用 nvm use node版本 可以切换当前使用的node

   ④：使用 nvm alias default node版本  可以指定默认打开终端时的node版本



npm i --package-lock-only

npm WARN sass-loader@7.3.1 requires a peer of webpack@^3.0.0 || ^4.0.0 but none is installed. You must install peer dependencies yourself.

added 5 packages from 3 contributors, removed 5 packages and audited 1139 packages in 6.786s

7 packages are looking for funding
  run `npm fund` for details