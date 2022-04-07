<template>
  <!-- 管理用户账户，账户添加、删除、密码重置、用户信息修改等 -->

  <!-- <h1>伙伴管理，待开发</h1> -->

  <div>
    <a-form
      :model="formState"
      v-bind="layout"
      class="center"
      name="nest-messages"
      :validate-messages="validateMessages"
      @finish="onFinish"
    >
      <br />
      <br />
      <h1>提交申请</h1>
      <br />
      <br />
      <a-form-item label="申请类型">
        <a-select
          ref="select"
          v-model:value="formState.user.applyType"
          style="width: 180px"
          @change="applyTypeChange"
          :options="options_apply_type"
        >
        </a-select>
      </a-form-item>
      <br>
   

      <template v-if="formState.user.applyType == '值班'">
        <a-form-item label="值班日期">
          <a-date-picker
            @change="onRangeChange"
            v-model:value="formState.user.applyDate"
          />
        </a-form-item>
         <br>

<a-form-item label="是否休息日  " @click="isWorkerDayClick">
          <a-radio-group
            v-model:value="formState.user.isWorkerDay"
            style="margin-right: auto"
          >
            <a-radio :value="1">是</a-radio>
            <a-radio :value="0">否</a-radio>
          </a-radio-group>
        </a-form-item>
 <br>
        <a-form-item label="是否节假日  " @click="info">
          <a-radio-group
            v-model:value="formState.user.isHoliday"
            style="margin-right: auto"
          >
            <a-radio :value="1">是</a-radio>
            <a-radio :value="0">否</a-radio>
          </a-radio-group>
        </a-form-item>
 <br>
        <a-form-item label="值班时长">
          <p style="text-align: left">{{ formState.user.applyTimeLast }}</p>
        </a-form-item>
         <br>
        <a-form-item label="值班原因">
          <a-textarea
            style="width: 160pt"
            v-model:value="formState.user.applyReason"
            show-count
            :maxlength="50"
          />
        </a-form-item>
      </template>

      <template v-else-if="formState.user.applyType == '加班'">
        <a-form-item label="换算类型">
          <a-radio-group v-model:value="formState.user.conversionType">
            <a-radio :value="0">累加积休</a-radio>
            <a-radio :value="1">加班费</a-radio>
          </a-radio-group>
        </a-form-item>
         <br>
        <a-form-item label="加班日期">
          <a-space direction="vertical" style="width: 200px">
            <a-date-picker
              :disabled-time="disabledRangeTime"
              :show-time="{
                format: 'HH:mm',
                hideDisabledOptions: true,
              }"
              format="YYYY-MM-DD HH:mm"
              placeholder="Start"
              @openChange="handleStartOpenChange"
              @ok="onRangeOkStart"
              @change = "onRangeChangeStart"
            />
            <a-date-picker
              :disabled-time="disabledRangeTime"
              :show-time="{
                format: 'HH:mm',
                hideDisabledOptions: true,
              }"
              format="YYYY-MM-DD HH:mm"
              placeholder="End"
              :open="endOpen"
              @openChange="handleEndOpenChange"
              @ok="onRangeOkEnd"
               @change = "onRangeChangeEnd"
            />
          </a-space>
        </a-form-item>
         <br>

        <a-form-item label="加班时长">
          <p style="text-align: left">{{ formState.user.applyTimeLast }}</p>
        </a-form-item>
         <br>
        <a-form-item label="加班原因">
          <a-textarea
            style="width: 160pt"
            v-model:value="formState.user.applyReason"
            show-count
            :maxlength="50"
          />
        </a-form-item>
      </template>
      <template v-else>
        <!-- <a-form-item label="请假时间">
          <a-range-picker
            style="width: 225px"
            @ok="onRangeOk"
            @change="onRangeChange"
            :placeholder="['开始时间', '结束时间']"
            :disabled-time="disabledRangeTime"
            :show-time="{
              format: 'HH:mm',
              hideDisabledOptions: true,
            }"
            format="YYYY-MM-DD HH:mm"
          />
        </a-form-item> -->

<a-form-item label="请假日期">
          <a-space direction="vertical" style="width: 200px">
            <a-date-picker
              :disabled-time="disabledRangeTime"
              :show-time="{
                format: 'HH:mm',
                hideDisabledOptions: true,
              }"
              format="YYYY-MM-DD HH:mm"
              placeholder="Start"
              @openChange="handleStartOpenChange"
              @ok="onRangeOkStart"
              @change = "onRangeChangeStart"
            />
            <a-date-picker
              :disabled-time="disabledRangeTime"
              :show-time="{
                format: 'HH:mm',
                hideDisabledOptions: true,
              }"
              format="YYYY-MM-DD HH:mm"
              placeholder="End"
              :open="endOpen"
              @openChange="handleEndOpenChange"
              @ok="onRangeOkEnd"
               @change = "onRangeChangeEnd"
            />
          </a-space>
        </a-form-item>
 <br>

        <a-form-item label="请假时长">
          <p style="text-align: left">{{ formState.user.applyTimeLast }}</p>
        </a-form-item>
         <br>
        <a-form-item label="请假原因">
          <a-textarea
            style="width: 160pt"
            v-model:value="formState.user.applyReason"
            show-count
            :maxlength="50"
          />
        </a-form-item>
      </template>
      <br />

      <a-button type="primary" html-type="Submit">提交</a-button>
    </a-form>
  </div>
</template>

<script>
import dayjs from "dayjs";
import { message } from "ant-design-vue";
import { defineComponent, ref, reactive } from "vue";
import moment from "moment";
import { workerApply } from "../../api/api.js";
import { values } from "lodash";

export default defineComponent({
  setup() {
    const formState = reactive({
      user: {
        applyTimeLast: "4时",
        applyReason: "",
        applyType: "值班",
        applyDate: ref(),
        applyDateEnd:"",
        isHoliday: 0,
        conversionType: 1,
        isWorkerDay: 0,
      },
    });
    const options_apply_type = ref([
      {
        value: "值班",
        label: "值班",
      },
      {
        value: "加班",
        label: "加班",
      },
      {
        value: "请假",
        label: "请假",
      },
    ]);





    let dataStringStart = ref('');
    let dataStringEnd = ref('');

    const onRangeChange = (value, dateString) => {
      dataStringStart = dateString;
      dataStringEnd = dateString;
      // formState.user.applyTimeLast = "";
      // if (formState.user.applyType == "值班") {
      //   let week = moment(value).day();
      //   if (week == 0 || week == 6) {
      //     formState.user.applyTimeLast = "1天4时";
      //   } else {
      //     formState.user.applyTimeLast = "4时";
      //   }
      // }
    };

    const isWorkerDayClick = (value) =>{
       if (formState.user.applyType == "值班") {

        if (formState.user.isWorkerDay) {
          formState.user.applyTimeLast = "4时";
        } else {
          formState.user.applyTimeLast = "1天4时";
        }
      }
    }

    const applyTypeChange = (value) => {
      formState.user.applyTimeLast = "";
      formState.user.applyReason = "";
      dataStringStart.value = "";
      if (formState.user.applyType === "值班"){
        formState.user.applyTimeLast = "4时";
      }else{
        formState.user.applyTimeLast = "";
      }
      // formState.user.isHoliday = -1;
      // formState.user.isWorkerDay = -1;
      // formState.user.conversionType = -1;
    };
const dataJson = {};
    const onFinish = (value) => {
        if (formState.user.applyType === "值班" && dataStringStart.value ===''){
          message.error("请选择值班时间");
          return;
        }


      
      if (formState.user.applyTimeLast != "") {
        if (
          formState.user.conversionType == 0 &&
          formState.user.applyReason.length == 0
        ) {
          message.error("请输入加班原因!");
        } else {
          if (formState.user.applyType == "值班") {
            dataJson["applyType"] = formState.user.applyType;
            // dataJson["applyDate"] = formState.user.applyDate;
            dataJson["isHoliday"] = formState.user.isHoliday;
            dataJson["applyTimeLast"] = formState.user.applyTimeLast;
            dataJson["applyReason"] = formState.user.applyReason;
            dataJson["conversionType"] = 2;
          } else if (formState.user.applyType == "加班") {
            dataJson["applyType"] = formState.user.applyType;
            dataJson["conversionType"] = formState.user.conversionType;
            // dataJson["applyDate"] = formState.user.applyDate;
            dataJson["applyTimeLast"] = formState.user.applyTimeLast;
            dataJson["applyReason"] = formState.user.applyReason;
            dataJson["isHoliday"] = 2;
          } else {
            dataJson["applyType"] = formState.user.applyType;
            // dataJson["applyDate"] = formState.user.applyDate;
            dataJson["applyTimeLast"] = formState.user.applyTimeLast;
            dataJson["applyReason"] = formState.user.applyReason;
            dataJson["conversionType"] = 2;
            dataJson["isHoliday"] = 2;
          }

          let userid = localStorage.getItem("Userid");
          workerApply(userid, dataJson, dataStringStart, dataStringEnd).then(
            (response) => {
              if (response["code"] == 1) {
                message.success("提交成功");
              } else {
                message.error("提交失败");
              }
            },
            (response) => {
              message.error("提交提交失败，服务器访问错误！");
            }
          );
        }
      } else {
        message.error("没有值班时长！");
      }

      // console.log(dataJson);
      // 接下来把dataJson传给后端服务器完成数据提交任务
    };

    const range = (start, end, d_type) => {
      const result = [];
      if (d_type === "hour") {
        for (let i = 0; i < start; i++) {
          result.push(i);
        }
        for (let i = end; i < 24; i++) {
          result.push(i);
        }
      } else if (d_type === "minute") {
        for (let i = 0; i < 60; i++) {
          if (i % start != 0) {
            result.push(i);
          }
        }
      } else {
        for (let i = 0; i < 60; i++) {
          result.push(i);
        }
      }
      return result;
    };

    let endOpen = ref(false);

    const handleStartOpenChange = (open) => {
      if (!open) {
        endOpen.value = true;
      }
    };
    const handleEndOpenChange = (open) => {
      endOpen.value = open;
    };

    const disabledRangeTime = () => {
      {
        return {
          disabledHours: () => range(8, 18, "hour"),
          disabledMinutes: () => range(15, 60, "minute"),
          disabledSeconds: () => [55, 56],
        };
      }
    };

    var startOk = false;
    var startValue, endValue;
  
    const onRangeOkStart = (value) => {
      startOk = true;
      startValue = value;
    };
    
    const onRangeOkEnd = (value) => {
      if (! startOk){
        message.error("请先选择开始日期")
      }else{

      var stime =new Date(dataStringStart).getTime();
      var etime = new Date(dataStringEnd).getTime();
      var usedTime = etime - stime;  //两个时间戳相差的毫秒数
      if (usedTime < 0){
        message.error("结束日期必须在开始日期之后")
      }else{
      var days=Math.floor(usedTime/(24*3600*1000));
      //计算出小时数
      var leave1=usedTime%(24*3600*1000);    //计算天数后剩余的毫秒数
      var hours=Math.floor(leave1/(3600*1000));
      //计算相差分钟数
      var leave2=leave1%(3600*1000);        //计算小时数后剩余的毫秒数
      var minutes=Math.floor(leave2/(60*1000));
      // var time = days + "天"+hours+"时"+minutes+"分";
      hours = hours + minutes / 60;
      if(hours >= 8)
      {
        hours = 8;
      }

      formState.user.applyTimeLast =
        days.toString() + "天" + hours.toString() + "时";
       
      }}
    };

const onRangeChangeEnd=(value, dateString) =>{
  
  dataStringEnd = dateString
}

const onRangeChangeStart=(value, dateString) =>{
  
  dataStringStart = dateString
}






    return {
      isWorkerDayClick,
      onRangeChangeStart,
      onRangeChangeEnd,
      onRangeOkStart,
      onRangeOkEnd,
      handleStartOpenChange,
      handleEndOpenChange,
      endOpen,
      disabledRangeTime,
      dataStringStart,
      dataStringEnd,
      onFinish,
      applyTypeChange,
      onRangeChange,
      formState,
      options_apply_type,
      dayjs,
    };
  },
});
</script>

 <style scoped>
.center {
  text-align: center;
  margin: 0 auto;
  width: 300px;
}
</style>>