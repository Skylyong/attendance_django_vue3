import validatorHook from './src/hook';
import { VXETable } from '../v-x-e-table';
export var Validator = {
    install: function () {
        VXETable.hooks.add('$tableValidator', validatorHook);
    }
};
export default Validator;
