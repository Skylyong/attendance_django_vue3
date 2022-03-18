<template>
  <br />
  <br />
  <br />
  <a-descriptions title="账户信息">
    <a-descriptions-item label="&nbsp &nbsp &nbsp &nbsp &nbsp &nbsp  姓  名">{{
      name
    }}</a-descriptions-item>
    <a-descriptions-item label="工  号">{{ userId }}</a-descriptions-item>
  </a-descriptions>
  <br />

  <a-table
    :columns="columns"
    :data-source="dataGroups"
    class="components-table-demo-nested"
    :rowKey="(item) => item.userId"
  >
  </a-table>
</template>

 <script>
import { defineComponent, ref, reactive } from "vue";
import { getworkerMessage, getUserPoolData } from "../../api/api.js";

const columns = [
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
  {
    title: "公休总天数(2022年)",
    dataIndex: "generalHolidayTotal",
    width: "10%",
  },
  {
    title: "公休剩余(天:时)",
    dataIndex: "generalHolidayRemainder",
    width: "15%",
  },
  {
    title: "积休剩余(天:时)",
    dataIndex: "accumulateHolidayRemainder",
    width: "15%",
  },
  {
    title: "积休已经用(天:时)",
    dataIndex: "accumulateHolidayUsed",
    width: "15%",
  },
  {
    title: "值班加班换积休(天:时)",
    dataIndex: "barterAccumulateHoliday",
    width: "20%",
  },
  {
    title: "总休息池(天:时)",
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

    return {
      getUserPoolData,
      name,
      userId,
      dataGroups,
      columns,
    };
  },
});
</script>