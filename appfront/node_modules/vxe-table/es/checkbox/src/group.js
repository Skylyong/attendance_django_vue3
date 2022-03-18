import { defineComponent, h, provide } from 'vue';
import GlobalConfig from '../../v-x-e-table/src/conf';
import XEUtils from 'xe-utils';
import { useSize } from '../../hooks/size';
export default defineComponent({
    name: 'VxeCheckboxGroup',
    props: {
        modelValue: Array,
        disabled: Boolean,
        size: { type: String, default: function () { return GlobalConfig.checkbox.size || GlobalConfig.size; } }
    },
    emits: [
        'update:modelValue',
        'change'
    ],
    setup: function (props, context) {
        var slots = context.slots, emit = context.emit;
        var xID = XEUtils.uniqueId();
        var $xecheckboxgroup = {
            xID: xID,
            props: props,
            context: context
        };
        useSize(props);
        var checkboxGroupMethods = {
            dispatchEvent: function (type, params, evnt) {
                emit(type, Object.assign({ $checkboxGroup: $xecheckboxgroup, $event: evnt }, params));
            }
        };
        var checkboxGroupPrivateMethods = {
            handleChecked: function (params, evnt) {
                var checked = params.checked, label = params.label;
                var checklist = props.modelValue || [];
                var checkIndex = checklist.indexOf(label);
                if (checked) {
                    if (checkIndex === -1) {
                        checklist.push(label);
                    }
                }
                else {
                    checklist.splice(checkIndex, 1);
                }
                emit('update:modelValue', checklist);
                $xecheckboxgroup.dispatchEvent('change', Object.assign({ checklist: checklist }, params), evnt);
            }
        };
        Object.assign($xecheckboxgroup, checkboxGroupMethods, checkboxGroupPrivateMethods);
        var renderVN = function () {
            return h('div', {
                class: 'vxe-checkbox-group'
            }, slots.default ? slots.default({}) : []);
        };
        $xecheckboxgroup.renderVN = renderVN;
        provide('$xecheckboxgroup', $xecheckboxgroup);
        return renderVN;
    }
});
