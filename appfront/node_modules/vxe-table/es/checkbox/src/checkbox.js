import { defineComponent, h, computed, inject } from 'vue';
import XEUtils from 'xe-utils';
import { getFuncText } from '../../tools/utils';
import GlobalConfig from '../../v-x-e-table/src/conf';
import { useSize } from '../../hooks/size';
export default defineComponent({
    name: 'VxeCheckbox',
    props: {
        modelValue: [String, Number, Boolean],
        label: { type: [String, Number], default: null },
        indeterminate: Boolean,
        title: [String, Number],
        checkedValue: { type: [String, Number, Boolean], default: true },
        uncheckedValue: { type: [String, Number, Boolean], default: false },
        content: [String, Number],
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
        var $xecheckbox = {
            xID: xID,
            props: props,
            context: context
        };
        var checkboxMethods = {};
        var computeSize = useSize(props);
        var $xecheckboxgroup = inject('$xecheckboxgroup', null);
        var computeDisabled = computed(function () {
            return props.disabled || ($xecheckboxgroup && $xecheckboxgroup.props.disabled);
        });
        var computeChecked = computed(function () {
            return $xecheckboxgroup ? XEUtils.includes($xecheckboxgroup.props.modelValue, props.label) : props.modelValue === props.checkedValue;
        });
        var changeEvent = function (evnt) {
            var checkedValue = props.checkedValue, uncheckedValue = props.uncheckedValue;
            var isDisabled = computeDisabled.value;
            if (!isDisabled) {
                var checked = evnt.target.checked;
                var value = checked ? checkedValue : uncheckedValue;
                var params = { checked: checked, value: value, label: props.label };
                if ($xecheckboxgroup) {
                    $xecheckboxgroup.handleChecked(params, evnt);
                }
                else {
                    emit('update:modelValue', value);
                    checkboxMethods.dispatchEvent('change', params, evnt);
                }
            }
        };
        checkboxMethods = {
            dispatchEvent: function (type, params, evnt) {
                emit(type, Object.assign({ $checkbox: $xecheckbox, $event: evnt }, params));
            }
        };
        Object.assign($xecheckbox, checkboxMethods);
        var renderVN = function () {
            var _a;
            var vSize = computeSize.value;
            var isDisabled = computeDisabled.value;
            return h('label', {
                class: ['vxe-checkbox', (_a = {},
                        _a["size--" + vSize] = vSize,
                        _a['is--indeterminate'] = props.indeterminate,
                        _a['is--disabled'] = isDisabled,
                        _a)],
                title: props.title
            }, [
                h('input', {
                    class: 'vxe-checkbox--input',
                    type: 'checkbox',
                    disabled: isDisabled,
                    checked: computeChecked.value,
                    onChange: changeEvent
                }),
                h('span', {
                    class: 'vxe-checkbox--icon'
                }),
                h('span', {
                    class: 'vxe-checkbox--label'
                }, slots.default ? slots.default({}) : getFuncText(props.content))
            ]);
        };
        $xecheckbox.renderVN = renderVN;
        return $xecheckbox;
    },
    render: function () {
        return this.renderVN();
    }
});
