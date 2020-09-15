###
 # @Author: your name
 # @Date: 2020-08-28 12:11:37
 # @LastEditTime: 2020-09-11 03:36:02
 # @LastEditors: Please set LastEditors
 # @Description: In User Settings Edit
 # @FilePath: /AiFrameWork/workspace/findso.sh
###

IMAGE_NAME=video_decode:v1.0
MAP_HOST_PATH=`pwd`
MAP_DOCKER_PATH=/root/video_decode
DOCKER_NAME=video_decode
# 首次正常依赖库文件提取(含软连接)
start(){
    if [ ! -d logs ]
    then
        mkdir logs
    fi

    docker run --name $DOCKER_NAME --restart=always -itd --net=host --cap-add=SYS_PTRACE --security-opt seccomp=unconfined \
    -v $MAP_HOST_PATH:$MAP_DOCKER_PATH \
    $IMAGE_NAME
}

stop(){
    docker stop $DOCKER_NAME
    docker rm $DOCKER_NAME
}

main(){
    case $1 in
            start)
            start
            ;;
            stop)
            stop
            ;;
            *)
            echo -e "\nUSEAGE: $0 [start|stop]"
    esac
}

main $1
