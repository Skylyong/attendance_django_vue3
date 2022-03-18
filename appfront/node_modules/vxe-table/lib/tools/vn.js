"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.getOnName = getOnName;

function getOnName(type) {
  return 'on' + type.substring(0, 1).toLocaleUpperCase() + type.substring(1);
}