%%%%%%%%%Chinese%%%%%%%%%%%
本代码包限于云端运行。
任务容器生成器pod在接收到工作流注入模块第一个pod时开始创建生成每个任务的services，同任务pods同在一个namespace。
后续的生成的任务pods和services陆续绑定。同时，所有的services注入到每个任务pods。
(云边集群的边节点缺少Kubelet组件，无法注入services到任务pods，云节点可以注入services到自己托管任务pods)

任务pod启动后，可有通过查询env方式，获取子任务绑定的的ServiceIp，发送数据。

%%%%%%%English%%%%%%%%%%
This package is limited to cloud.

When the task container generator pod receives the first pod of the workflow injection module, the Serivce constructor starts creating services that generate each task, in the same namespace as the task pods.

Subsequent generated task pods and services are bound one after another. At the same time, all services are injected into each task pods.

(The edge nodes of the cloud-edge cluster lack Kubelet components and cannot inject services into task pods. The cloud nodes can inject services into their own hosted task pods.)


After the task pod is started, there is a way to obtain the ServiceIp by querying env to bound by the subtask and send data.


