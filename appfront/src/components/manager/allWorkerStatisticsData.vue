<template>
  <a-table
    :columns="columns"
    :data-source="dataGroups"
    class="components-table-demo-nested"
    :rowKey="(item) => item.userId"
  >
    <template #expandedRowRender="{ record }"
      >>
      <a-table
        :columns="innerColumns"
        :data-source="record.groupItem"
        :rowKey="(item) => item.applyTime"
        :pagination="false"
      >
      </a-table>
    </template>
  </a-table>
</template>
<script>
import { DownOutlined } from "@ant-design/icons-vue";
import { getPoolData } from "../../api/api.js";
import { defineComponent, ref } from "vue";
const columns = [
  {
    title: "员工号",
    dataIndex: "userId",
    width: "8%",
  },

  {
    title: "姓名",
    dataIndex: "name",
    width: "8%",
  },
  {
    title: "公休总天数(2022年)",
    dataIndex: "generalHolidayTotal",
    width: "10%",
  },
  {
    title: "公休剩余(天:时)",
    dataIndex: "generalHolidayRemainder",
    width: "10%",
  },
  {
    title: "积休剩余(天:时)",
    dataIndex: "accumulateHolidayRemainder",
    width: "10%",
  },
  {
    title: "积休已经用(天:时)",
    dataIndex: "accumulateHolidayUsed",
    width: "15%",
  },
  {
    title: "值班加班换积休(天:时)",
    dataIndex: "barterAccumulateHoliday",
    width: "15%",
  },
  {
    title: "总休息池(天:时)",
    dataIndex: "restPoolTotal",
  },
];

const innerColumns = [
  //   {
  //   title: '序号',
  //   dataIndex: 'id',
  //   width: '5%',
  //   sorter: (a, b) => a.id - b.id,
  // } ,
  //  { title: '员工号',
  //   dataIndex: 'userId',
  //   width: '8%'},
  {
    title: "申请时间",
    dataIndex: "applyTime",
    width: "7%",
    sorter: (a, b) => a.id - b.id,
  },

  {
    title: "开始时间",
    dataIndex: "applyStartTime",
    sorter: true,
    width: "8%",
    sorter: (a, b) => a.applyStartTime - b.applyStartTime,
  },
  {
    title: "结束时间",
    dataIndex: "applyEndTime",
    sorter: true,
    width: "8%",
    sorter: (a, b) => a.applyEndTime - b.applyEndTime,
  },
  {
    title: "申请时长",
    dataIndex: "applyTimeLast",
    sorter: true,
    width: "8%",
    sorter: (a, b) => a.timeLast - b.timeLast,
  },
  {
    title: "类型",
    dataIndex: "applyType",
    filters: [
      {
        text: "公休",
        value: "公休",
      },
      {
        text: "值班加班",
        value: "值班加班",
      },
    ],
    onFilter: (value, record) => record.applyType.indexOf(value) === 0,
    // sorter: (a, b) => a.applyType.length - b.applyType.length,
    width: "10%",
  },
  {
    title: "休期种类",
    dataIndex: "holidayType",
    filters: [
      {
        text: "公休请假",
        value: "公休请假",
      },
      {
        text: "加班换积休",
        value: "加班换积休",
      },
      {
        text: "值班换积休",
        value: "值班换积休",
      },
    ],
    onFilter: (value, record) => record.holidayType.indexOf(value) === 0,
    // sorter: (a, b) => a.holidayType.length - b.holidayType.length,
    width: "10%",
  },
  {
    title: "申请原因",
    dataIndex: "applyReason",
    width: "15%",
    sorter: (a, b) => a.applyReason.length - b.applyReason.length,
  },
  {
    title: "审批状态",
    dataIndex: "approveState",
    // sorter: (a, b) => a.approveState.length - b.approveState.length,
    onFilter: (value, record) => record.approveState.indexOf(value) === 0,
    width: "8%",
    filters: [
      {
        text: "通过",
        value: "通过",
      },
      {
        text: "不通过",
        value: "不通过",
      },
      {
        text: "未审批",
        value: "未审批",
      },
    ],
  },
  {
    title: "批注",
    dataIndex: "approveNote",
    sorter: true,
    width: "10%",
    sorter: (a, b) => a.applyReason.length - b.applyReason.length,
  },
];

export default defineComponent({
  components: {
    DownOutlined,
  },

  setup() {
    let getid = localStorage.getItem("Userid");
    let dataGroups = ref();
    getPoolData(getid).then((response) => {
      if (response["code"] == 1) {
        dataGroups.value = response["data"];
        console.log(response["data"]);
      }
    });
    return {
      dataGroups,
      getPoolData,
      columns,
      innerColumns,
    };
  },
});
</script>