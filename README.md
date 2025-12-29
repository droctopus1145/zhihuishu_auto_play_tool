<h3 align="center">智慧树自动播放工具</h3>
本工具是实现智慧树自动播放的python脚本，配置教程如下：
<h4>使用非conda环境配置:</h4>
请确认您的python版本大于3.6，推荐版本为3.12，~~因为本人编写时使用的是3.12版本~~

```shell
pip install selenium
```

将仓库克隆到本地，cd到仓库目录，在终端打开：

```shell
python zhsscript.py
```

<h4>使用conda环境配置:</h4>

```shell
conda create -n zhs python=3.12
conda activate zhs
conda install selenium
```

将仓库克隆到本地，cd到仓库目录，在终端打开：

```shell
python zhsscript.py
```

接下来脚本将打开一个chrome网页，请在此网页中完成智慧树的登录，在刷课过程中请不要关闭该网页，否则脚本将自动停止运行
<br/>
<h1 align="center">顺祝发明智慧树的若只每天上班十二个小时回家线上加班十二个小时加到猝死不得house喵</h1>
