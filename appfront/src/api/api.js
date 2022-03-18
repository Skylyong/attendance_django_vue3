import { post, get } from "./http";

export const postSubmit = (username, password) => {
     return post('/login/', { 'name': username, 'author': password })
}

export const workerApply = (userid, applyType, holidayType, applyTimeLen, applyReason, myDateString) => {
     return post('/submitApplication/', {
          'userid': userid,
          'applyType': applyType,
          'holidayType': holidayType,
          'applyTimeLast': applyTimeLen,
          'applyReason': applyReason,
          'myDateString': myDateString
     })
}

export const getworkerApplyHistory = (userid, data_type = 0) => {
     return post('/getApplicationHistory/', {
          'userid': userid, 'data_type': data_type

     })
}

export const getworkerMessage = (userid) => {
     return post('/getWorkerAccountMessage/', {
          'userid': userid
     })
}

export const delApplication = (userid, key) => {
     return post('/delApplication/', { 'userid': userid, 'applyTime': key })
}
export const submitApplication = (getid, key, approveState, approveNote) => {
     return post('/approvalApplication/', {
          'id': key, 'userId': getid,
          'approveState': approveState,
          'approveNote': approveNote
     })
}

export const getPoolData = (getid) => {
     return post('/getPoolData/', { 'userId': getid })
}

export const get_no_history_count = (getid) => {
     return post('/get_no_approve_history_count/', { 'userId': getid })
}

export const getUserPoolData = (getid) => {
     return post('/getUserPoolData/', { 'userId': getid })
}

