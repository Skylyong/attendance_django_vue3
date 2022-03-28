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
        :rowKey="(item) => item.id"
        :pagination="true"
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
    width: "10%",
  },

  {
    title: "姓名",
    dataIndex: "name",
    width: "10%",
  },
  {
    title: "公休天数(2022年)",
    dataIndex: "HolidayTotal",
    width: "10%",
  },
  {
    title: "上年剩余积休(天:时)",
    dataIndex: "lastYearRemainder",
    width: "10%",
  },
  {
    title: "本年度积休(天:时)",
    dataIndex: "HolidayRemainder",
    width: "10%",
  },
    {
    title: "请 假(天:时)",
    dataIndex: "cost",
    width: "15%",
  },
  {
    title: "休息池(天:时)",
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
    sorter: (a, b) => a.applyTime - b.applyTime,
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
    sorter: (a, b) => a.applyTimeLast - b.applyTimeLast,
  },
  {
    title: "申请类型",
    dataIndex: "applyType",
    filters: [
      {
        text: "加班",
        value: "加班",
      },
      {
        text: "值班",
        value: "值班",
      },
        {
        text: "请假",
        value: "请假",
      },
    ],
    onFilter: (value, record) => record.applyType.indexOf(value) === 0,
    // sorter: (a, b) => a.applyType.length - b.applyType.length,
    width: "10%",
  },

  {
    title: "是否节假",
    dataIndex: "isHoliday",
    filters: [
      {
        text: "是",
        value: "是",
      },
      {
        text: "	否",
        value: "否",
      },
     
    ],
    onFilter: (value, record) => record.isHoliday.indexOf(value) === 0,
    // sorter: (a, b) => a.holidayType.length - b.holidayType.length,
    width: "10%",
  },

  {
    title: "换算类型",
    dataIndex: "conversionType",
    filters: [
      {
        text: "加班费",
        value: "加班费",
      },
      {
        text: "累加积休",
        value: "累加积休",
      },
     
    ],
    onFilter: (value, record) => record.conversionType.indexOf(value) === 0,
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
        text: "驳回",
        value: "驳回",
      },
    ],
  },
  {
    title: "批注",
    dataIndex: "approveNote",
    sorter: true,
    width: "10%",
    sorter: (a, b) => a.approveNote.length - b.approveNote.length,
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