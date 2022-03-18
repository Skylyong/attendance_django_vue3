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


界面

  

 1. 登录界面

<img src="https://raw.githubusercontent.com/Skylyong/i/main/20220318203925.png" alt="image-20220318203925559" style="zoom:25%;" />

 2. 普通用户界面

   <img src="https://raw.githubusercontent.com/Skylyong/i/main/20220318203724.png" alt="image-20220318203724405" style="zoom:50%;" />

 3. 管理员界面

   <img src="https://raw.githubusercontent.com/Skylyong/i/main/20220318203853.png" alt="image-20220318203853895" style="zoom:50%;" />

+ 项目demo（不一定能访问）
+ 项目编程学习资料（帮助爬坑）
  
	+ 项目编写
	
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
	
		+ Vue项目打包到django部署 https://blog.csdn.net/lymmurrain/article/details/109348390
		
	+ 项目部署
	  
	   + Docker部署Django https://pythondjango.cn/django/advanced/16-docker-deployment/
		
	   + Nginx启动无法访问： https://blog.csdn.net/yujing1314/article/details/105225325