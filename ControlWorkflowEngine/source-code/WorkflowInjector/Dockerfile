#编译镜像
FROM golang:1.17 as builder
MAINTAINER bit_scg "uzz_scg@163.com"
ENV GOPROXY https://goproxy.cn
ENV GO111MODULE on
COPY . /usr/local/go/src/workflowInjector

WORKDIR /usr/local/go/src/workflowInjector
RUN go mod download
#go构建可执行文件,-o 生成Server，放在当前目录
RUN go build -ldflags="-w -s" -o workflowInjector .

#执行镜像
FROM ubuntu:latest
WORKDIR /root/go/workflowInjector
COPY --from=builder /usr/local/go/src/workflowInjector .
#ENTRYPOINT  ["./workflowInjector"]