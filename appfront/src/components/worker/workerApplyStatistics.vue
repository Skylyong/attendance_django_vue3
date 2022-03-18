<template>
  <vxe-table :align="center" :data="tableData1">
    <vxe-column field="name" title="Name"></vxe-column>
    <vxe-column field="sex" title="Sex"></vxe-column>
    <vxe-column field="age" title="Age"></vxe-column>
  </vxe-table>
</template>

<script>
import { defineComponent, ref } from "vue";

export default defineComponent({
  setup() {
    const tableData1 = ref([
      {
        id: 10001,
        name: "Test1",
        role: "Develop",
        sex: "Man",
        age: 28,
        address: "test abc",
      },
    ]);

    return {
      tableData1,
    };
  },
});
</script>