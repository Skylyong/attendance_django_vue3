import editHook from './src/hook';
import { VXETable } from '../v-x-e-table';
export var Edit = {
    install: function () {
        VXETable.hooks.add('$tableEdit', editHook);
    }
};
export default Edit;
