package informer

import (

	"TaskContainerBuilder/event"
	"TaskContainerBuilder/k8sResource"
	"fmt"
	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/util/runtime"
	"k8s.io/client-go/informers"
	v1 "k8s.io/client-go/listers/core/v1"
	"k8s.io/client-go/tools/cache"
	"log"
	"strconv"
	"strings"
	"time"
)
//the flag of completed workflow
type CurrentWorkflowFinished bool
type CurrentWorkflowTaskFinished bool
var  currentWorkflowFinished CurrentWorkflowFinished
var  currentWorkflowTaskFinished CurrentWorkflowTaskFinished
//var task taskContainerBuilder.WorkflowTask

//State tracking and resource monitoring module
func InitInformer(stop chan struct{}, configfile string) (v1.PodLister,v1.NodeLister,v1.NamespaceLister,v1.ServiceLister){


	currentWorkflowFinished = false
	currentWorkflowTaskFinished = false

	//Connect K8s's apiserver
	informerClientset := k8sResource.GetInformerK8sClient(configfile)
	//Innitialize informer
	factory := informers.NewSharedInformerFactory(informerClientset, time.Second*1)

	//Create podInformer
	podInformer := factory.Core().V1().Pods()
	informerPod := podInformer.Informer()

	//Create nodeInformer
	nodeInformer := factory.Core().V1().Nodes()
	informerNode := nodeInformer.Informer()

	//Create namespaceInformer
	namespaceInformer := factory.Core().V1().Namespaces()
	informerNamespace := namespaceInformer.Informer()

	//创建service的Informer
	serviceInformer := factory.Core().V1().Services()
	informerService := serviceInformer.Informer()

	//Create Listers
	podInformerLister := podInformer.Lister()
	nodeInformerLister := nodeInformer.Lister()
	namespaceInformerLister := namespaceInformer.Lister()
    serviceInformerLister := serviceInformer.Lister()


	go factory.Start(stop)

	//Synchronize podList
	if !cache.WaitForCacheSync(stop, informerPod.HasSynced) {
		runtime.HandleError(fmt.Errorf("Timed out waiting for caches to sync"))
		return nil, nil, nil, nil
	}
	//Synchronize nodeList
	if !cache.WaitForCacheSync(stop, informerNode.HasSynced) {
		runtime.HandleError(fmt.Errorf("Timed out waiting for caches to sync"))
		return nil, nil, nil, nil
	}
	//Synchronize namespaceList
	if !cache.WaitForCacheSync(stop, informerNamespace.HasSynced) {
		runtime.HandleError(fmt.Errorf("Timed out waiting for caches to sync"))
		return nil, nil, nil, nil
	}
	//Synchronize serviceList
	if !cache.WaitForCacheSync(stop, informerService.HasSynced) {
		runtime.HandleError(fmt.Errorf("Timed out waiting for caches to sync"))
		return nil, nil, nil, nil
	}
	informerPod.AddEventHandler(cache.ResourceEventHandlerFuncs{
		AddFunc:    onPodAdd,
		UpdateFunc: onPodUpdate,
		DeleteFunc: onPodDelete,
	})

	informerNode.AddEventHandler(cache.ResourceEventHandlerFuncs{
		AddFunc:    onNodeAdd,
		UpdateFunc: onNodeUpdate,
		DeleteFunc: onNodeDelete,
	})

	informerNamespace.AddEventHandler(cache.ResourceEventHandlerFuncs{
		AddFunc:    onNamespaceAdd,
		UpdateFunc: onNamespaceUpdate,
		DeleteFunc: onNamespaceDelete,
	})

	informerService.AddEventHandler(cache.ResourceEventHandlerFuncs{
		AddFunc:    onServiceAdd,
		UpdateFunc: onServiceUpdate,
		DeleteFunc: onServiceDelete,
	})
	return podInformerLister, nodeInformerLister, namespaceInformerLister, serviceInformerLister
}
func onPodAdd(obj interface{}) {
	pod := obj.(*corev1.Pod)
	//log.Println("add a pod:", pod.Name)
	log.Printf("--------------add a pod[%s] in time:%v.\n", pod.Name,time.Now().UnixNano()/1e6)
}

func onPodUpdate(old interface{}, current interface{}) {

	//oldpod := old.(*corev1.Pod)
	//oldstatus := oldpod.Status.Phase
	//splitName :=  strings.Split(oldpod.Name,"-")
	//nameSpaceName := strings.Split(oldpod.Namespace, "-")
	//newpod := current.(*corev1.Pod)
	//newstatus := newpod.Status.Phase
	//if ((oldstatus == "Pending") || (oldstatus == "Running")) && (newstatus == "Succeeded") {
    //if (oldstatus == "Pending") && (newstatus == "Running") {
	//	log.Println(oldpod.Status.Phase)
	//	log.Println(newpod.Status.Phase)
	//	log.Printf("%v: pod is Running", oldpod.Name)
	//	if nameSpaceName[0] == "workflow" {
	//		taskOrder, err := strconv.Atoi(splitName[3])
	//		if err != nil {
	//			panic(err.Error())
	//		}
	//		wfTaskIndex := uint32(taskOrder)
	//		//Delete successful task pod and start the next task pod.
	//		//event.CallEvent("DeleteCurrentTaskContainer", wfTaskIndex)
	//		event.CallEvent("LaunchNextTaskContainer", wfTaskIndex)
	//		log.Println("----------------------------")
	//	}
	//} else if newstatus == "Failed" {
	//	log.Println(oldpod.Status.Phase)
	//	log.Println(newpod.Status.Phase)
	//	log.Println("Pod error.", oldpod.Name)
	//	if nameSpaceName[0] == "workflow" {
	//		taskOrder, err := strconv.Atoi(splitName[3])
	//		if err != nil {
	//			panic(err.Error())
	//		}
	//		wfTaskStruct := uint32(taskOrder)
	//		event.CallEvent("DeleteCurrentTaskContainer", wfTaskStruct)
	//	}
	//}
	//log.Printf("Pod: %v, oldStatus: %v, newStatus: %v\n", oldpod.Name, oldpod.Status.Phase, newpod.Status.Phase)
}
func onPodDelete(obj interface{}) {
	pod := obj.(*corev1.Pod)
	//log.Println("delete a pod:", pod.Name)
	log.Println("--------------delete a pod at time:", pod.Name,time.Now().UnixNano()/1e6)
}
func onNodeAdd(obj interface{}) {
	node := obj.(*corev1.Node)
	log.Println("add a node:", node.Name)
}
func onNodeUpdate(old interface{}, current interface{}) {
	//log.Println("updating..............")
}
func onNodeDelete(obj interface{}) {
	node := obj.(*corev1.Node)
	log.Println("delete a Node:", node.Name)
}
func onNamespaceAdd(obj interface{}) {
	namespace := obj.(*corev1.Namespace)
	log.Println("add a namespace:", namespace.Name)
}
func onNamespaceUpdate(old interface{}, current interface{}) {
	//log.Println("updating..............")
	//oldNamespace := old.(*corev1.Namespace)
	//oldstatus := oldNamespace.Status.Phase
	//log.Println(oldNamespace.Status.Phase)
}
func onNamespaceDelete(obj interface{}) {
	namespace := obj.(*corev1.Namespace)
	//log.Println("Delete a namespace:", namespace.Name)
	log.Println("--------------delete a namespace at time:", namespace.Name,time.Now().UnixNano()/1e6)
	splitName :=  strings.Split(namespace.Name,"-")
	wfIndex, err := strconv.Atoi(splitName[1])
	//log.Println(wfIndex)
	if err != nil {
		panic(err.Error())
	}
	//inform that the last task is done
	event.CallEvent("ThisWorkflowEnd",uint32(wfIndex))
}
func onServiceAdd(obj interface{}) {
	service := obj.(*corev1.Service)
	log.Println("add a service:", service.Name)
}
func onServiceUpdate(old interface{}, current interface{}) {
	//log.Println("updating..............")
}
func onServiceDelete(obj interface{}) {
	service := obj.(*corev1.Service)
	log.Println("delete a service:", service.Name)
}