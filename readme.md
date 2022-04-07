## 基于Django后端和Vue3.0前端框架的简单考勤系统

环境

+ Django 3.2.12
+ Vue 3.2.31
+ vue-cil 5.0.1
+ npm 8.3.1
+ node v16.14.0
+ ant design vue 3.1.0-rc.1 





运行

+  后端运行：

 > cd djDemo

 > python manage.py runserver

+ 前端运行

 > cd appfront

 > npm run serve 

+ 后端数据库操作脚本

> cd djDemo/attendance/managerDatadb.py

本地前端页面更新到服务器（将本地写好的前端页面更新到服务器方便需求方查看）

> cd appfront
> 
> npm run build # 打包前端文件dist
> 
> scp -r dist username@server_ip:file_path/djDemo/  #用打包好的dist文件替换服务器上的dist文件
> 
> cd djDemo #切换到服务器上的djDemo目录
> 
> sudo killall -9 uwsgi
> 
> python3 manage.py collectstatic
> 
> python3 manage.py migrate
> 
> sudo uwsgi uwsgi.ini # 重启uwsgi服务，页面更新完毕

界面

  

 1. 登录界面

<img src="https://raw.githubusercontent.com/Skylyong/i/main/20220318203925.png" alt="image-20220318203925559" style="zoom:25%;" />

 2. 普通用户界面

<img src="https://raw.githubusercontent.com/Skylyong/i/main/20220323054855.png" alt="image-20220323054848636" style="zoom:30%;" />

<img src="https://raw.githubusercontent.com/Skylyong/i/main/20220323054948.png" alt="image-20220323054948916" style="zoom:30%;" />

<img src="https://raw.githubusercontent.com/Skylyong/i/main/20220323055052.png" alt="image-20220323055051980" style="zoom:30%;" />



 3. 管理员界面

<img src="https://raw.githubusercontent.com/Skylyong/i/main/20220323055220.png" alt="image-20220323055220270" style="zoom:30%;" />

<img src="https://raw.githubusercontent.com/Skylyong/i/main/20220323055259.png" alt="image-20220323055259106" style="zoom:30%;" />

<img src="https://raw.githubusercontent.com/Skylyong/i/main/20220323055402.png" alt="image-20220323055402177" style="zoom:30%;" />

+ [项目demo](http://47.103.127.226)

+ 项目编程学习资料（帮助爬坑）
  
	+ 项目编写
	
	  + node js安装 https://nodejs.org/en/download/
	
	  + https://www.antdv.com/docs/vue/introduce-cn/
	
	  + https://www.antdv.com/components/table-cn/
	
	  + https://v3.cn.vuejs.org/guide/introduction.html#%E8%B5%B7%E6%AD%A5
	
	  + login page:
	
	    https://blog.csdn.net/qq_40910147/article/details/122754178
	
	  + 前后端通信demo【重要】
	    https://www.cnblogs.com/derek1184405959/p/8733578.html
	
	  + 知乎前后端通信教程
	    https://zhuanlan.zhihu.com/p/128976272
	
	  + ant-design vue 官方文档：https://next.antdv.com/components/menu-cn
	
	  + b站vue视频： https://www.bilibili.com/video/BV1WK4y1J7fs?p=16
	
	  + 菜鸟教程 Vue3.0 ：https://www.runoob.com/vue3/vue3-ajax-axios.html
	
	  + django 开发文档
	    https://docs.djangoproject.com/zh-hans/4.0/intro/tutorial03/
	
	  + Vue中的验证登录状态【重要】
	    https://segmentfault.com/a/1190000018437732
	
	  + django 视频教程
	    https://www.bilibili.com/video/BV1vK4y1o7jH?p=1
	
	  + DJANGO VUE3 跨域CSRF问题刨坑【坑了我一晚上】
	    https://blog.csdn.net/u013113491/article/details/116163272
	  + [登录保持]
	    https://blog.csdn.net/qq_32018951/article/details/89286669
	
	  + Ant-Design-Vue的tabale组件（expandedRowRender）嵌套应用 https://www.cnblogs.com/livedian/p/14542119.html
	
  + 项目部署
	   + [推荐]Vue项目打包到django部署 https://blog.csdn.net/qq_42517220/article/details/105725506
	     + Vue项目打包到django部署 https://blog.csdn.net/lymmurrain/article/details/109348390
	   + Docker部署Django https://pythondjango.cn/django/advanced/16-docker-deployment/
	   + Nginx启动无法访问： https://blog.csdn.net/yujing1314/article/details/105225325
	
       + [从阿里云服务器购买到项目部署，可部分参考]Django搭建个人博客：将项目部署到服务器 https://www.dusaiphoto.com/article/71/
	     + [通俗易懂强烈推荐] 部署Django(也是优秀的Django教程) https://www.liujiangblog.com/course/django/181
  
  + 数据库更改
  
     +  SQLite 到 MySQL 的数据库导入流程 https://segmentfault.com/a/1190000023917962
     +  使用MySQL数据库 https://www.liujiangblog.com/course/django/165