[uwsgi]
chdir = /home/sites/attendance.com/Attendance_Django_Vue3/djDemo    //项目根目录
module = djDemo.wsgi:application     //  指定wsgi模块下的application对象
socket = 127.0.0.1:8000         //对本机8000端口提供服务
master = true                   //主进程

# 以上4个是核心配置项

#vhost = true          //多站模式
#no-site = true        //多站模式时不设置入口模块和文件
#workers = 2           //子进程数
#reload-mercy = 10
#vacuum = true         //退出、重启时清理文件
#max-requests = 1000
#limit-as = 512
#buffer-size = 30000
#pidfile = /var/run/uwsgi9090.pid    //pid文件，用于下脚本启动、停止该进程
daemonize = /home/sites/attendance.com/Attendance_Django_Vue3/djDemo/run.log    // 日志文件
disable-logging = true   //不记录正常信息，只记录错误信息