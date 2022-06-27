import { post, get } from "./http";

export const postSubmit = (username, password) => {
     return post('/login/', { 'name': username, 'author': password })
}

// export const workerApply = (userid, applyType, holidayType, applyTimeLen, applyReason, myDateString) => {
//      return post('/submitApplication/', {
//           'userid': userid,
//           'applyType': applyType,
//           'holidayType': holidayType,
//           'applyTimeLast': applyTimeLen,
//           'applyReason': applyReason,
//           'myDateString': myDateString
//      })
// }


export const workerApply = (userId, data, dataStringStart, dataStringEnd) => {
     return post('/submitApplication/', {
          'userid':userId,
          'applyType':data['applyType'], 
          'applyTimeLast':data['applyTimeLast'],
          'applyReason':data['applyReason'],  
          'isHoliday': data['isHoliday'],
          'conversionType': data['conversionType'],
          'applyDateStart': dataStringStart,
          'applyDateEnd': dataStringEnd,
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
     return post('/delApplication/', { 'userid': userid, 'id': key })
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

export const getOverTimeData = (getid) => {
     return post('/getOverTimeData/', { 'userId': getid })   
}


export const getOverTimeUserData = (getid) => {
     return post('/getOverTimeUserData/', { 'userId': getid })   
} 

export const resetPwd = (new_key, name) => {
     return post('/resetPwd/', { 'new_key': new_key, 'userId':name})   
} 


export const getWorkerId = (userId) => {
     return post('/getWorkerId/', {'userId':userId })   
} 


export const resetPwdWork = (new_key, userId, old_key) => {
     return post('/resetPwdWork/', { 'new_key': new_key, 'userId':userId , 'old_key': old_key})   
} 


export const cancellation = (userId, id ) => {
     return post('/cancellation/', { 'userId':userId , 'id': id})   
} 