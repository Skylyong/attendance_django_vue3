import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.css'

const app = createApp(App).use(Antd).use(router).use(store);
app.mount("#app");

router.beforeEach((to, from, next) => {
  //获取用户登录成功后储存的登录标志
  let getFlag = localStorage.getItem("Flag");
  let userType = localStorage.getItem("userType");
  if (to.meta.isLogin) {
    if (getFlag != "isLogin") {
      next({ path: '/' })
    } else {
      if (userType == to.meta.pathType) {
        next()
      } else {
        next({ path: '/' })
      }
    }
  } else {
    next()
  }
});

router.afterEach(() => {
  window.scroll(0, 0);
});