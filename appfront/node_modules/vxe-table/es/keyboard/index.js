import keyboardHook from './src/hook';
import { VXETable } from '../v-x-e-table';
export var Keyboard = {
    install: function () {
        VXETable.hooks.add('$tableKeyboard', keyboardHook);
    }
};
export default Keyboard;
