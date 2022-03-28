<template>
  <br />
  <br />

  <a-descriptions title="账户信息">
    <br>
    <br>
    <br>
    <a-descriptions-item label="&nbsp &nbsp &nbsp &nbsp &nbsp &nbsp  姓  名">{{
      name
    }}</a-descriptions-item>
    <a-descriptions-item label="工  号">{{ userId }}</a-descriptions-item>
  </a-descriptions>
  <br />
<p style="text-align:left">休息池:</p>
  <a-table
    :columns="columns"
    :data-source="dataGroups"
    class="components-table-demo-nested"
    :rowKey="(item) => item.userId"
    :pagination="false"
  >
  </a-table>
<br>
<br>
<br>
  <p style="text-align:left">加班汇总:</p>


  <a-table
    :columns="overtime_columns"
    :data-source="dataGroups_overtime"
    class="components-table-demo-nested"
    :rowKey="(item) => item.userid"
    :pagination="false"
    >>
  </a-table>

</template>

 <script>
import { defineComponent, ref, reactive } from "vue";
import { getworkerMessage, getUserPoolData,getOverTimeUserData  } from "../../api/api.js";

// const columns = [
  //   {
  //   title: '员工号',
  //   dataIndex: 'userId',
  //   width: '8%',
  // },

  //   {
  //   title: '姓名',
  //   dataIndex: 'name',
  //   width: '8%',
  // },
//   {
//     title: "公休总天数(2022年)",
//     dataIndex: "generalHolidayTotal",
//     width: "10%",
//   },
//   {
//     title: "公休剩余(天:时)",
//     dataIndex: "generalHolidayRemainder",
//     width: "15%",
//   },
//   {
//     title: "积休剩余(天:时)",
//     dataIndex: "accumulateHolidayRemainder",
//     width: "15%",
//   },
//   {
//     title: "积休已经用(天:时)",
//     dataIndex: "accumulateHolidayUsed",
//     width: "15%",
//   },
//   {
//     title: "值班加班换积休(天:时)",
//     dataIndex: "barterAccumulateHoliday",
//     width: "20%",
//   },
//   {
//     title: "总休息池(天:时)",
//     dataIndex: "restPoolTotal",
//   },
// ];

let overtime_columns = ref([
    {
    title: "年 月 ",
    dataIndex: "endYearMonth",
     width: "25%",
     onFilter: (value, record) => record.endYearMonth.indexOf(value) === 0,
  },
  {
    title: "工 号",
    dataIndex: "userId",
    width: "25%",
    onFilter: (value, record) => record.userId.indexOf(value) === 0,
  },

  {
    title: "姓 名",
    dataIndex: "name",
    width: "25%",
  },
  {
    title: "加班时长",
    dataIndex: "overtime",

  },
]);

const columns = [
  // {
  //   title: "员工号",
  //   dataIndex: "userId",
  //   width: "10%",
  // },

  // {
  //   title: "姓名",
  //   dataIndex: "name",
  //   width: "10%",
  // },
  {
    title: "公休天数(2022年)",
    dataIndex: "HolidayTotal",
    width: "20%",
  },
  {
    title : '上年剩余积休(天:时)',
    dataIndex: "lastYearRemainder",
    width: "20%",

  },
  {
    title: "本年度积休(天:时)",
    dataIndex: "HolidayRemainder",
    width: "20%",
  },
    {
    title: "请 假(天:时)",
    dataIndex: "cost",
    width: "20%",
  },
  {
    title: "休息池(天:时)",
    dataIndex: "restPoolTotal",
  },
];


export default defineComponent({
  setup() {
    let dataGroups = ref();
    let userId = ref();
    let name = ref();
    let getid = localStorage.getItem("Userid");
    getworkerMessage(getid).then((response) => {
      if (response["code"] == 1) {
        name.value = response["data"].name;
        userId.value = response["data"].userId;
      }
    });

    getUserPoolData(getid).then((response) => {
      if (response["code"] == 1) {
        dataGroups.value = response["data"];
        console.log(response["data"]);
      }
    });
let dataGroups_overtime = ref()
        getOverTimeUserData(getid).then((response) => {
      if (response["code"] == 1) {
        dataGroups_overtime.value = response["data"];
        console.log(response["data"]);
      }
    });

    return {
      getUserPoolData,
      name,
      userId,
      dataGroups,
      columns,
      overtime_columns,
      dataGroups_overtime,

    };
  },
});
</script>