"use strict";(self["webpackChunkmyproj"]=self["webpackChunkmyproj"]||[]).push([[706],{4706:(e,n,t)=>{t.r(n),t.d(n,{default:()=>I});var r=t(6252),a=(0,r._)("br",null,null,-1),o=(0,r._)("br",null,null,-1),l=(0,r._)("br",null,null,-1),u=(0,r._)("h1",null,"欢迎登录考勤系统",-1),i=(0,r._)("br",null,null,-1),s=(0,r._)("br",null,null,-1),c={class:"login-form-wrap"},m=(0,r.Uk)("记住我"),d=(0,r._)("a",{class:"login-form-forgot",href:""},"忘记密码",-1),f=(0,r.Uk)(" 登 录 ");function p(e,n,t,p,h,b){var g=(0,r.up)("UserOutlined"),v=(0,r.up)("a-input"),w=(0,r.up)("a-form-item"),y=(0,r.up)("LockOutlined"),_=(0,r.up)("a-input-password"),k=(0,r.up)("a-checkbox"),F=(0,r.up)("a-button"),O=(0,r.up)("a-form");return(0,r.wg)(),(0,r.j4)(O,{style:{"text-align":"center","vertical-align":"middle"},model:e.formState,name:"normal_login",class:"login-form",onFinish:e.onFinish,onFinishFailed:e.onFinishFailed},{default:(0,r.w5)((function(){return[a,o,l,u,i,(0,r.Wm)(w,{label:"用户名",style:{width:"300px",display:"inline-flex"},name:"username",rules:[{required:!0,message:"请输入用户名!"}]},{default:(0,r.w5)((function(){return[(0,r.Wm)(v,{value:e.formState.username,"onUpdate:value":n[0]||(n[0]=function(n){return e.formState.username=n})},{prefix:(0,r.w5)((function(){return[(0,r.Wm)(g,{class:"site-form-item-icon"})]})),_:1},8,["value"])]})),_:1}),s,(0,r.Wm)(w,{style:{width:"300px",display:"inline-flex"},label:"密    码",name:"password",rules:[{required:!0,message:"请输入密码！"}]},{default:(0,r.w5)((function(){return[(0,r.Wm)(_,{value:e.formState.password,"onUpdate:value":n[1]||(n[1]=function(n){return e.formState.password=n})},{prefix:(0,r.w5)((function(){return[(0,r.Wm)(y,{class:"site-form-item-icon"})]})),_:1},8,["value"])]})),_:1}),(0,r._)("div",c,[(0,r.Wm)(w,{name:"remember","no-style":""},{default:(0,r.w5)((function(){return[(0,r.Wm)(k,{checked:e.formState.remember,"onUpdate:checked":n[2]||(n[2]=function(n){return e.formState.remember=n})},{default:(0,r.w5)((function(){return[m]})),_:1},8,["checked"])]})),_:1}),d]),(0,r.Wm)(w,null,{default:(0,r.w5)((function(){return[(0,r.Wm)(F,{disabled:e.disabled,type:"primary","html-type":"submit",class:"login-form-button"},{default:(0,r.w5)((function(){return[f]})),_:1},8,["disabled"])]})),_:1})]})),_:1},8,["model","onFinish","onFinishFailed"])}var h=t(2262),b=t(4924),g={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M832 464h-68V240c0-70.7-57.3-128-128-128H388c-70.7 0-128 57.3-128 128v224h-68c-17.7 0-32 14.3-32 32v384c0 17.7 14.3 32 32 32h640c17.7 0 32-14.3 32-32V496c0-17.7-14.3-32-32-32zM332 240c0-30.9 25.1-56 56-56h248c30.9 0 56 25.1 56 56v224H332V240zm460 600H232V536h560v304zM484 701v53c0 4.4 3.6 8 8 8h40c4.4 0 8-3.6 8-8v-53a48.01 48.01 0 10-56 0z"}}]},name:"lock",theme:"outlined"};const v=g;var w=t(4233);function y(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?Object(arguments[n]):{},r=Object.keys(t);"function"===typeof Object.getOwnPropertySymbols&&(r=r.concat(Object.getOwnPropertySymbols(t).filter((function(e){return Object.getOwnPropertyDescriptor(t,e).enumerable})))),r.forEach((function(n){_(e,n,t[n])}))}return e}function _(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}var k=function(e,n){var t=y({},e,n.attrs);return r.Wm(w.Z,r.dG(t,{icon:v}),null)};k.displayName="LockOutlined",k.inheritAttrs=!1;const F=k;var O=t(2119),S=t(3449),W=t(8637),j=t(1446);const x=(0,r.aZ)({components:{UserOutlined:b.Z,LockOutlined:F},setup:function(){var e=(0,W.oR)();localStorage.setItem("Flag","noLogin");var n=(0,O.tv)(),t=(0,h.qj)({username:"",password:"",remember:!0}),a=function(t){(0,S.sK)(t.username,t.password).then((function(t){console.log(t),1==t["code"]?(localStorage.setItem("Userid",t["data"]["userId"]),localStorage.setItem("Flag","isLogin"),localStorage.setItem("userType",t["data"]["accountType"]),e.dispatch("setUser",!0),2==t["data"]["accountType"]?n.push({path:"/manager/managerApprove"}):n.push({path:"/worker/account"})):2004==t["code"]?j.Z.error("找不到该用户！"):j.Z.error("密码错误!")}),(function(e){j.Z.error("服务器访问错误!")}))},o=function(e){console.log("Failed:",e)},l=(0,r.Fl)((function(){return!(t.username&&t.password)}));return{formState:t,onFinish:a,onFinishFailed:o,disabled:l,message:j.Z}}});var U=t(3744);const Z=(0,U.Z)(x,[["render",p]]),I=Z}}]);
//# sourceMappingURL=706.3bbd2cd0.js.map