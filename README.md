# behave_to_cucumber
由于原作者对于behave_to_cucumber没有进行维护了，有一些bug需要进行修复，所以单开一个仓库用于维护，如果有问题，可以提issue
- 感谢原作者：andreybehalf
- 原项目地址：https://github.com/behalf-oss/behave_to_cucumber

## 介绍
该项目主要用于将behave框架生成的behave.json转换为cucumber.json

## 使用示例
~~~
import json
import behave_to_cucumber
with open('behave_json.json') as behave_json:
    cucumber_json = behave_to_cucumber.convert(json.load(behave_json),remove_background=True)
~~~

covert内置三个参数用于控制生成的cucumber.json报告
- remove_background:删除前置条件,默认False
- duration_format:持续时间格式化,默认False
- deduplicate:重复数据消除,默认False

## 从bash运行
感谢 @lawnmowerlatte 添加了 Main ，现在您可以运行：

~~~
python -m behave2cucumber
~~~

