from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from django.views.decorators import csrf

# Create your views here.
from rest_framework import viewsets
from django.http import JsonResponse
from attendance.models import Attendance
from attendance.serializer import AttendanceSerializer
from django.middleware.csrf import get_token
from django.db import connection
import time


history_dic_key_list = ['id', 'userId', 'applyTime', 'applyStartTime', 'applyEndTime', 'applyType',
                        'holidayType', 'approveState', 'applyReason', 'applyTimeLast', 'name', 'approveNote']
pool_dic_key_list = ['userId', 'generalHolidayTotal', 'generalHolidayRemainderDays', 'generalHolidayRemainderTime',
                     'accumulateHolidayRemainderDays', 'accumulateHolidayRemainderTime', 'accumulateHolidayUsedDays',
                     'accumulateHolidayUsedTime', 'barterAccumulateHolidayDays', 'barterAccumulateHolidayTime',
                     'restPoolTotalDays', 'restPoolTotalTime', 'name']
applyTypeD = {
    0: '公休',
    1: '值班加班'
}
holidayTypeD = {
    0: '公休请假',
    1: '加班换积休',
    2: "值班换积休"
}
approveStateD = {
    3: '未审批',
    2: '通过',
    1: '未通过'
}


def get_multi_recored_with_cmd(cmd):
    try:
        with connection.cursor() as cursor:
            cursor.execute(cmd)
            results = cursor.fetchall()
        return results
    except:
        return None


def get_signal_recored_with_cmd(cmd):
    with connection.cursor() as cursor:
        cursor.execute(cmd)
        account_types = cursor.fetchone()
        if account_types:
            result = account_types[0]
            return result
        else:
            return None


def get_user_type(user_id):
    cmd = '''SELECT accountType 
             from loginmessage 
             where userId=''' + user_id
    return get_signal_recored_with_cmd(cmd)


def get_worker_pool(all, user_id=''):
    cmd = '''SELECT r.userId, r.generalHolidayTotal,
                     r.generalHolidayRemainderDays,
                     r.generalHolidayRemainderTime,
                     r.accumulateHolidayRemainderDays,
                     r.accumulateHolidayRemainderTime,
                     r.accumulateHolidayUsedDays,
                     r.accumulateHolidayUsedTime,
                     r.barterAccumulateHolidayDays,
                     r.barterAccumulateHolidayTime,
                     r.restPoolTotalDays,
                     r.restPoolTotalTime,
                     w.name 
              FROM   RestPoolTab r
              JOIN   WorkerMessage w 
              ON     w.userid=r.userid
              '''
    if not all:
        cmd += "where r.userid={}".format(user_id)
    return get_multi_recored_with_cmd(cmd)


def get_worker_history_from_database(all, user_id=''):
    cmd = '''SELECT a.id , a.userId, a.applyTime, 
                    a.applyStartTime, a.applyEndTime, a.applyType,
                    a.holidayType,a.approveState, a.applyReason, 
                    a.applyTimeLast, w.name,a.approveNote 
             FROM   ApplyHistory a 
             JOIN   WorkerMessage w 
             ON     w.userid=a.userid'''
    if not all:
        cmd += " WHERE  a.userid={}".format(user_id)

    return get_multi_recored_with_cmd(cmd)


def database2dic(database_result, dic_key_list):
    results = []
    for row in database_result:
        temp = {}
        for idx, r in enumerate(row):
            temp[dic_key_list[idx]] = r
        results.append(temp)
    return results


def simplify_dic(pool):
    pool['generalHolidayRemainder'] = "{}天{}时".format(
        pool['generalHolidayRemainderDays'], pool['generalHolidayRemainderTime'])
    pool['accumulateHolidayRemainder'] = "{}天{}时".format(
        pool['accumulateHolidayRemainderDays'], pool['accumulateHolidayRemainderTime'])
    pool['accumulateHolidayUsed'] = "{}天{}时".format(
        pool['accumulateHolidayUsedDays'],  pool['accumulateHolidayUsedTime'])
    pool['barterAccumulateHoliday'] = "{}天{}时".format(
        pool['barterAccumulateHolidayDays'], pool['barterAccumulateHolidayTime'])
    pool['restPoolTotal'] = "{}天{}时".format(
        pool['restPoolTotalDays'], pool['restPoolTotalTime'])
    return pool


def combine_history_and_pools(worker_apply_history, worker_pools):
    worker_apply_history_dic = database2dic(
        worker_apply_history, history_dic_key_list)
    worker_pools_dic = database2dic(worker_pools, pool_dic_key_list)
    result = []
    for pool in worker_pools_dic:
        pool_new = simplify_dic(pool)
        pool_new['groupItem'] = []
        for history in worker_apply_history_dic:
            if pool_new['userId'] == history['userId'] and history['approveState'] != 3:
                history['applyType'] = applyTypeD[history['applyType']]
                history['holidayType'] = holidayTypeD[history['holidayType']]
                history['approveState'] = approveStateD[history['approveState']]

                pool_new['groupItem'].append(history)
        result.append(pool_new)
    return result


def get_response():
    return {'code': 1, 'message': '', 'data': {}}


def set_response(code, message, data={}):
    response = {}
    response['code'] = code
    response['message'] = message
    response['data'] = data
    return response


def login(request):
    if request.method == 'GET':
        response = get_response()
        get_token(request)
        return JsonResponse(response)

    if request.method == 'POST':
        # 验证用户名和秘密是否正确
        # 没有用户名返回2
        # 有用户名密码错误返回1
        # 验证成功返回0
        param = request.POST
        name = param['name']
        key = param['author']
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT name , key, accountType,userId from  LoginMessage WHERE name = %s", [name])
            res = cursor.fetchall()
            # print (res)
            if len(res) == 0:
                response = set_response(2004, 'no user message')  # 没有获取到用户信息
            else:
                if res[0][1] == key:
                    response = set_response(
                        1, 'success', {'name': res[0][0], 'accountType': res[0][2], 'userId': res[0][3]})
                else:
                    response = set_response(2001, 'key error')
        return JsonResponse(response)


def approvalApplication(request):
    '''
    处理：管理员审批申请请求
    根据申请用户和申请时间，找到对应的申请记录，填充是否审批通过和批注，并改写申请历史表中的审批状态（0，1，2）
    如果审批通过，则对休息池表进行更新
    请求方式：POST
    '''
    param = request.POST
    userId = param['userId']
    id = param['id']
    approveState = param['approveState']
    approveNote = param['approveNote']
    try:
        with connection.cursor() as cursor:
            cmd = 'update ApplyHistory set approveState=' + approveState + \
                ', approveNote=\"' + approveNote + "\" where id="+id
            res = cursor.execute(cmd)
            if res.rowcount > 0:
                response = set_response(1, 'success')
            else:
                response = set_response(0, 'filed')
    except:
        response = set_response(0, 'filed')

    return JsonResponse(response)


def get_no_approve_history_count(request):
    param = request.POST
    userId = param['userId']
    if get_user_type(userId) == 2:
        cmd = '''SELECT a.id , a.userId, a.applyTime, 
                            a.applyStartTime, a.applyEndTime, a.applyType,
                            a.holidayType,a.approveState, a.applyReason, 
                            a.applyTimeLast, a.approveNote 
                     FROM   ApplyHistory a 
                     WHERE a.approveState=3'''
        result = get_multi_recored_with_cmd(cmd)
        response = set_response(1, 'success',  len(result))
    else:
        response = set_response(0, 'failed')
    return JsonResponse(response)


def submitApplication(request):
    '''
    处理：用户提交申请请求
    用户提交申请，并将申请内容写入申请历史表中
    请求方式：POST
    '''

    param = request.POST
    userId = param['userid']
    applyType = param['applyType']
    holidayType = param['holidayType']
    # applyTime = param['applyTime']
    applyReason = param['applyReason']
    applyStartTime, applyEndTime = param['myDateString[0]'], param['myDateString[1]']
    applyTimeLast = param['applyTimeLast']
    approveState = 3
    applyTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO ApplyHistory (userId, applyTime, applyStartTime,applyEndTime,applyType, holidayType,approveState, applyReason, applyTimeLast) \
               VALUES ( %s,%s, %s,%s,%s, %s,%s, %s, %s)", [userId, applyTime, applyStartTime, applyEndTime, applyType, holidayType, approveState, applyReason, applyTimeLast])
        code = 1
        message = 'success'
    except:
        code = 0
        message = 'failed'
    response = set_response(code, message)
    return JsonResponse(response)


def delApplication(request):
    '''
    处理：用户删除申请历史请求
    只能删除未审批的申请记录
    请求方式: GET
    '''
    param = request.POST
    userId = param['userid']
    applyTime = param['applyTime']
    try:
        with connection.cursor() as cursor:
            cmd = "DELETE FROM ApplyHistory WHERE userId=" + userId + \
                " AND applyTime=\""+applyTime+"\" AND approveState=3"
            res = cursor.execute(cmd)
            if res.rowcount > 0:
                response = set_response(1, 'success')
            else:
                response = set_response(0, 'filed')
    except:
        response = set_response(0, 'filed')

    return JsonResponse(response)


def save_to_database():
    pass


def getApplicationHistory(request):
    '''
    处理： 返回用户申请历史
    请求方式：POST， 参数 user_account
    返回用户的申请历史数据
    '''
    param = request.POST
    user_id = param['userid']
    data_type = int(param['data_type'])
    if get_user_type(user_id) == 2:
        results = get_worker_history_from_database(True)
        results = database2dic(results, history_dic_key_list)
        if not data_type:
            results_ = []
            for r in results:
                if r['approveState'] == 3:
                    r['applyType'] = applyTypeD[r['applyType']]
                    r['holidayType'] = holidayTypeD[r['holidayType']]
                    r['approveState'] = approveStateD[r['approveState']]
                    results_.append(r)

            results = results_
    else:
        results = get_worker_history_from_database(False, user_id=user_id)
        results = database2dic(results, history_dic_key_list)
        results_ = []
        for r in results:
            r['applyType'] = applyTypeD[r['applyType']]
            r['holidayType'] = holidayTypeD[r['holidayType']]
            r['approveState'] = approveStateD[r['approveState']]
            results_.append(r)
        results = results_

    if len(results) == 0:
        response = set_response(2004, 'no user message')  # 没有获取到用户信息
    else:
        response = set_response(1, 'success', data=results)
    return JsonResponse(response)


def getPoolData(request):

    # 处    理： 返回用户休息池数据
    # 请求方式： POST, 参数 user_account
    # 返回用户休息池数据和用户历史数据

    param = request.POST
    try:
        if get_user_type(param['userId']) == 2:
            worker_apply_history = get_worker_history_from_database(all=True)
            worker_pools = get_worker_pool(all=True)
            data = combine_history_and_pools(
                worker_apply_history, worker_pools)
            response = set_response(1, 'success', data)
        else:
            response = set_response(0, 'filed')
    except:
        response = set_response(0, 'filed')
    return JsonResponse(response)


def managerWorkerAccount(request):
    '''
    处理: 管理员工信息
    请求方式：GET查看员工数据
            POST对员工数据进行修改
            POST新增员工数据
            POST删除员工数据
    '''


def managerPassword(request):
    '''
    处理：管理密码
    请求方式：POST 参数user_account, type, new_key
    如果type为1表示重置密码，type为2表示修改密码
    密码重置为'1234'
    '''


def getWorkerAccountMessage(request):
    if request.method == "POST":
        param = request.POST
        user_id = param['userid']
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT name, manager,userId from  WorkerMessage WHERE userid = %s", [user_id])
            res = cursor.fetchall()
            if len(res) == 0:
                response = set_response(2004, 'no user message')  # 没有获取到用户信息
            else:
                response = set_response(1, 'success',
                                        {'name': res[0][0], 'manager': res[0][1], 'userId': res[0][2]})
        return JsonResponse(response)


def getUserPoolData(request):
    if request.method == "POST":
        param = request.POST
        user_id = param['userId']
        results = get_worker_pool(False, user_id=user_id)
        results = database2dic(results, pool_dic_key_list)
        results_ = []
        for r in results:
            r = simplify_dic(r)
            results_.append(r)
        if len(results_) == 0:
            response = set_response(2004, 'no user message')  # 没有获取到用户信息
        else:
            response = set_response(1, 'success', data=results_)
        return JsonResponse(response)
