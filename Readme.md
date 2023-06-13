＝＝＝＝＝＝＝＝
关于Ｔelegram Token和ＣhatID
＝＝＝＝＝＝＝＝

假设申请机器人名称是my123_bot。

1-@botfather 
  /newbot
  输入my123_bot，获取到token
  
2-将机器人添加到组中。
转到群组，单击群组名称，单击添加成员，在搜索框中搜索您的机器人，如下所示：@my123_bot，选择您的机器人并单击添加。

3- 向机器人发送一条虚拟消息。
您可以使用此示例：（/my_id @my123_bot
我尝试了一些消息，并非所有消息都有效。上面的示例工作正常。也许消息应该以 / 开头）

4-转到以下网址： https://api.telegram.org/botXXX:YYYY/getUpdates
用您的机器人令牌替换 XXX:YYYY

5-寻找“聊天”：{“id”：-zzzzzzzzzz，
-zzzzzzzzzz是您的聊天ID（带负号）。


＝＝＝＝＝＝＝＝
关于discord_webhook_Url
＝＝＝＝＝＝＝＝
第 1 步 — 设置您的 Discord Webhook
打开 Discord 帐户后，您可以创建自己的私人 Discord 服务器。

首先，在浏览器中登录您的 Discord 帐户或启动您的 Discord 应用程序，然后单击“创建服务器”按钮。

![image](https://github.com/tktk12341234/TelegramBot/assets/130174645/b0e69e93-dc55-4a5a-b314-fc6630ad9a78)

创建服务器或加入服务器 Discord

然后为您的服务器选择一个名称并单击“创建服务器”按钮。

接下来，您将配置 Discord webhook。Webhook 是可用于将服务链接在一起的唯一 URL。Discord 的 webhook 允许您自动发送消息并将数据更新发送到您的 Discord 文本频道。

在本教程中，您将在服务器上的特定服务出现故障时向您的 webhook 发送通知，Discord 将确保您在频道上收到这些消息。

要创建 Webhook，您必须先点击您的频道，然后点击频道名称旁边的编辑频道按钮。

![image](https://github.com/tktk12341234/TelegramBot/assets/130174645/334ab11d-d1e9-4477-b0f6-db9ff42da3dd)

频道设置 Discord

然后单击Webhooks选项卡并单击Create Webhook按钮。

![image](https://github.com/tktk12341234/TelegramBot/assets/130174645/60539210-44b6-45eb-ad7d-68bbf4ee9b37)

创建 Webhook 按钮 Discord

之后，为您的 webhook 选择一个名称，在本教程中我们将使用它，Alerts因为这是我们的 Bash 脚本将要执行的操作——在我们的一个网站出现故障时提醒我们。

复制您的 webhook URL 并保存以备后用。最后，单击保存按钮。

![image](https://github.com/tktk12341234/TelegramBot/assets/130174645/a787b32f-2b0d-4f3e-aa31-4b591e7216c7)


您现在拥有自己的 Discord 帐户、服务器和 webhook。您现在可以继续为要监视的脚本创建测试文件。
