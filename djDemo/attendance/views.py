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
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
import base64




random_generator = Random.new().read
rsa = RSA.generate(2048, random_generator)
# 生成私钥
private_key = rsa.exportKey()
print(private_key.decode('utf-8'))
# 生成公钥
public_key = rsa.publickey().exportKey()
print(public_key.decode('utf-8'))

with open('rsa_private_key.pem', 'wb')as f:
    f.write(private_key)

with open('rsa_public_key.pem', 'wb')as f:
    f.write(public_key)


history_dic_key_list = ['id', 'userId', 'applyTime', 'applyStartTime', 'applyEndTime', 'applyType',
                        'conversionType', 'approveState', 'applyReason', 'applyTimeLast', 'name', 'approveNote', 'isHoliday']

pool_dic_key_list = ['userId', 'HolidayTotal', 'HolidayRemainderDay', 'HolidayRemainderTime',
                     'costDay', 'costTime', 'restPoolTotalDay',
                     'restPoolTotalTime',  'name', 'lastYearRemainderDay', 'lastYearRemainderTime']
over_time_dic_key_list = ['id', 'userId', 'endYearMonth','ODay','OTime','name']
isHolidayD = {
    0: '否',
    1: '是',
    2: '-'
}
conversionTypeD = {
    0: '累加积休',
    1: '加班费',
    2: '-'
    # 2: "值班换积休"
}
approveStateD = {
    3: '未审批',
    2: '通过',
    1: '驳回'
}

applyTypeD ={
    0: '值班',
    1: '加班',
    2: '请假'
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
             where userId=''' +'\'' + user_id + '\''
    return get_signal_recored_with_cmd(cmd)


def get_worker_pool(all, user_id=''):
    cmd = '''SELECT r.userId, r.HolidayTotal,
                     r.HolidayRemainderDay,
                     r.HolidayRemainderTime,
                     r.costDay,
                     r.costTime,
                     r.restPoolTotalDay,
                     r.restPoolTotalTime,
                     w.name,
                     r.lastYearRemainderDay,
                     r.lastYearRemainderTime
              FROM   RestPoolTab r
              JOIN   WorkerMessage w 
              ON     w.userid=r.userid
              '''
    if not all:
        cmd += "where r.userid=\'{}\'".format(user_id)
    return get_multi_recored_with_cmd(cmd)


def get_worker_history_from_database(all, user_id=''):
    cmd = '''SELECT a.id , a.userId, a.applyTime, 
                    a.applyStartTime, a.applyEndTime, a.applyType,
                    a.conversionType,a.approveState, a.applyReason, 
                    a.applyTimeLast, w.name,a.approveNote, a.isHoliday 
             FROM   ApplyHistory a 
             JOIN   WorkerMessage w 
             ON     w.userid=a.userid'''
    if not all:
        cmd += " WHERE  a.userid=\'{}\'".format(user_id)

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
    pool['HolidayRemainder'] = "{}天{}时".format(
        pool['HolidayRemainderDay'], pool['HolidayRemainderTime'])
    pool['cost'] = "{}天{}时".format(
        pool['costDay'], pool['costTime'])
    pool['restPoolTotal'] = "{}天{}时".format(
        pool['restPoolTotalDay'],  pool['restPoolTotalTime'])
    pool['lastYearRemainder'] = "{}天{}时".format(
        pool['lastYearRemainderDay'], pool['lastYearRemainderTime'])
    # pool['barterAccumulateHoliday'] = "{}天{}时".format(
    #     pool['barterAccumulateHolidayDays'], pool['barterAccumulateHolidayTime'])
    # pool['restPoolTotal'] = "{}天{}时".format(
    #     pool['restPoolTotalDays'], pool['restPoolTotalTime'])
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
                # history['applyType'] = applyTypeD[history['applyType']]
                history['conversionType'] = conversionTypeD[history['conversionType']]
                history['isHoliday'] = isHolidayD[history['isHoliday']]
                history['approveState'] = approveStateD[history['approveState']]

                pool_new['groupItem'].append(history)
        result.append(pool_new)
    return result


def get_response(data = {}):
    return {'code': 1, 'message': '', 'data': data}


def set_response(code, message, data={}):
    response = {}
    response['code'] = code
    response['message'] = message
    response['data'] = data
    return response


def get_key(key_file):
    with open(key_file) as f:
        data = f.read()
        key = RSA.importKey(data)
    return key


def decrypt_data(encrypt_msg):
    private_key = get_key('rsa_private_key.pem')
    cipher = PKCS1_cipher.new(private_key)
    back_text = cipher.decrypt(base64.b64decode(encrypt_msg), 0)
    return back_text.decode('utf-8')


def login(request):
    if request.method == 'GET':
        with open('rsa_public_key.pem') as f:
            public_key = f.read()
            # public_key = data.decode('utf-8')
        response = get_response(data={'pubkey': public_key})
        get_token(request)
        return JsonResponse(response)

    if request.method == 'POST':
        # 验证用户名和秘密是否正确
        # 没有用户名返回2
        # 有用户名密码错误返回1
        # 验证成功返回0
        param = request.POST
        name = param['name'].strip()
        key = param['author']
        key = decrypt_data(key)
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

def string2day_hour(applyTimeLast):
    if '天' in applyTimeLast and '时' in applyTimeLast:
        day, other = applyTimeLast.split('天')
        hour = other.split('时')[0]
        day = int(day)
        hour = float(hour)
    elif '时' in applyTimeLast and '天' not in applyTimeLast:
        day = 0
        hour = applyTimeLast.split('时')[0]
        hour = float(hour)
    else:
        hour = 0
        day = applyTimeLast.split('天')[0]
        day = int(day)
    return  day, hour

def add2Pool(userId, applyTimeLast):
    day, hour = string2day_hour(applyTimeLast)
    if hour > 8: hour=8
    result = get_dic_result_with_database(database_name='RestPoolTab', columns=['HolidayRemainderDay', \
                                                               'HolidayRemainderTime', 'restPoolTotalDay', 'restPoolTotalTime'],
                                          condition={'userId': userId})
    result = result[0]
    HolidayRemainderTime = result['HolidayRemainderTime'] + hour
    t_day = HolidayRemainderTime // 8
    HolidayRemainderTime = HolidayRemainderTime % 8
    HolidayRemainderDay = result['HolidayRemainderDay'] + day + t_day

    restPoolTotalTime = result['restPoolTotalTime'] + hour
    t_day = restPoolTotalTime //8
    restPoolTotalTime = restPoolTotalTime % 8
    restPoolTotalDay = result['restPoolTotalDay'] + t_day + day

    cmd = "update RestPoolTab set HolidayRemainderDay={}\
                                    , HolidayRemainderTime={} \
                                    ,  restPoolTotalTime={} \
                                    , restPoolTotalDay={} \
                                    where userId=\'{}\'".format(HolidayRemainderDay, HolidayRemainderTime, \
                                                            restPoolTotalTime, restPoolTotalDay, userId)
    with connection.cursor() as cursor:
        cursor.execute(cmd)

def minus2Pool(userId, applyTimeLast):
    day, hour = string2day_hour(applyTimeLast)
    result = get_dic_result_with_database(database_name='RestPoolTab', columns=['costDay', \
                                        'costTime', 'restPoolTotalDay', 'restPoolTotalTime'], condition={'userId': userId})
    result = result[0]
    costTime = result['costTime'] + hour
    t_day = costTime // 8
    costTime = costTime%8
    costDay = result['costDay'] + day + t_day
    restPoolTotalTime = result['restPoolTotalTime'] - hour
    t_day = 0
    if restPoolTotalTime < 0:
        restPoolTotalTime = restPoolTotalTime+8
        t_day = 1
    restPoolTotalDay = result['restPoolTotalDay'] - t_day - day

    cmd = "update RestPoolTab set costDay={}\
                                    , costTime={} \
                                    ,  restPoolTotalTime={} \
                                    , restPoolTotalDay={} \
                                    where userId=\'{}\'".format(costDay,costTime,\
                                                            restPoolTotalTime, restPoolTotalDay, userId)
    with connection.cursor() as cursor:
        cursor.execute(cmd)

def get_dic_result_with_database(cmd =None, database_name='', columns='', condition=''):
    '''
    根据查询 返回满足条件的字典列表
    '''
    if cmd is None:
        cmd = ['select']
        cmd.append(','.join(columns))
        cmd.append('from')
        cmd.append(database_name)
        cmd.append('where')
        condition_list = []
        for key, value in condition.items():
            if key.lower() == 'userid':
                condition_list.append(key + '=\'' + value + '\'')
            else:
                condition_list.append(key + '=' + value)
        cmd.append(','.join(condition_list))
        cmd = ' '.join(cmd)
        print (cmd)
    result = get_multi_recored_with_cmd(cmd)
    res = []
    for re in result:
        temp = {}
        for idx, r in enumerate(re):
            temp[columns[idx]] = r
        res.append(temp)
    return res

def add2OverTimeTab(userid, applyEndTime, applyTimeLast):
    day, hour = string2day_hour(applyTimeLast)
    yearmonth = applyEndTime.split('-')
    yearmonth = '-'.join(yearmonth[0:2])
    cmd = "select ODay, OTime from OverTimeTab where userid=\'{}\' and endYearMonth=\'{}\'".format(userid, yearmonth)
    result = get_dic_result_with_database(cmd=cmd, columns=['ODay', 'OTime'])
    if len(result) == 0:
        cmd = "INSERT INTO OverTimeTab (userid, endYearMonth, ODay, OTime) VALUES (\'{}\', \'{}\',{}, {})".format(
        userid, yearmonth, day, hour)
        with connection.cursor() as cursor:
            cursor.execute(cmd)
    else:
        result = result[0]
        OTime = result['OTime']  + hour
        t_day = OTime // 8
        OTime = OTime % 8
        ODay = result['ODay'] + day + t_day
        cmd = "update OverTimeTab set ODay={}\
                                        , OTime={} \
                                        where userId=\'{}\' and endYearMonth=\'{}\' ".format(ODay,OTime, userid, yearmonth)
        with connection.cursor() as cursor:
            cursor.execute(cmd)

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
    result = get_dic_result_with_database(database_name='ApplyHistory', columns = ['applyType', \
                                        'isHoliday', 'conversionType', 'applyTimeLast', 'userId','applyEndTime'], condition={'id': id})
    result =result[0]
    applyType = result['applyType']
    isHoliday = result['isHoliday']
    conversionType = result['conversionType']
    applyTimeLast = result['applyTimeLast']
    worker_id = result['userId']
    applyEndTime = result['applyEndTime']
    # try:
    if int(approveState) == 2:
        if applyType == '值班' :
            if isHoliday == 0:
                add2Pool(worker_id, applyTimeLast)
            else:
                add2OverTimeTab(worker_id, applyEndTime, applyTimeLast)
        elif applyType == '加班':
            if 0 == conversionType:
                add2Pool(worker_id, applyTimeLast)
            else:
                add2OverTimeTab(worker_id, applyEndTime, applyTimeLast)
        else:
            minus2Pool(worker_id, applyTimeLast)

    with connection.cursor() as cursor:
        cmd = 'update ApplyHistory set approveState=' + approveState + \
            ', approveNote=\"' + approveNote + "\" where id="+id
        res = cursor.execute(cmd)
        if res.rowcount > 0:
            response = set_response(1, 'success')
        else:
            response = set_response(0, 'filed')
    # except:
    #     response = set_response(0, 'filed')
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
    applyTimeLast = param['applyTimeLast']
    applyReason = param['applyReason']
    isHoliday = param['isHoliday']
    conversionType = param['conversionType']
    if applyType == '值班':
        applyStartTime, applyEndTime = param['applyDate'], param['applyDate']
    else:
        applyStartTime, applyEndTime = param['applyDate[0]'], param['applyDate[1]']
    approveState = 3
    applyTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO ApplyHistory  \
                           (userId, applyTime, applyStartTime,conversionType, \
                           applyEndTime,applyType, isHoliday,\
                           approveState, applyReason, applyTimeLast) \
                            VALUES ( %s,%s, %s,%s,%s, %s,%s, %s, %s, %s)", \
                           [userId, applyTime, applyStartTime,conversionType, \
                           applyEndTime,applyType, isHoliday,\
                           approveState, applyReason, applyTimeLast])
            response = set_response(1, 'success')
    except:
        response = set_response(0, 'failed')
    return JsonResponse(response)


def delApplication(request):
    '''
    处理：用户删除申请历史请求
    只能删除未审批的申请记录
    请求方式: GET
    '''
    param = request.POST
    userId = param['userid']
    id = param['id']
    try:
        with connection.cursor() as cursor:
            cmd = "DELETE FROM ApplyHistory WHERE userId=\'" + userId + '\''+ \
                " AND id="+id+" AND approveState=3"
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
                    r['conversionType'] = conversionTypeD[r['conversionType']]
                    r['isHoliday'] = isHolidayD[r['isHoliday']]
                    r['approveState'] = approveStateD[r['approveState']]
                    results_.append(r)

            results = results_
    else:
        results = get_worker_history_from_database(False, user_id=user_id)
        results = database2dic(results, history_dic_key_list)
        results_ = []
        for r in results:
            # r['applyType'] = applyTypeD[r['applyType']]
            r['conversionType'] = conversionTypeD[r['conversionType']]
            r['isHoliday'] = isHolidayD[r['isHoliday']]
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
    # try:
    if get_user_type(param['userId']) == 2:
        worker_apply_history = get_worker_history_from_database(all=True)
        worker_pools = get_worker_pool(all=True)
        data = combine_history_and_pools(
            worker_apply_history, worker_pools)
        response = set_response(1, 'success', data)
    else:
        response = set_response(0, 'filed')
    # except:
    #     response = set_response(0, 'filed')
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

def get_over_time(all, user_id=''):
    cmd = '''SELECT a.id , a.userId, a.applyTime, 
                    a.applyStartTime, a.applyEndTime, a.applyType,
                    a.conversionType,a.approveState, a.applyReason, 
                    a.applyTimeLast, w.name,a.approveNote, a.isHoliday 
             FROM   ApplyHistory a 
             JOIN   WorkerMessage w 
             ON     w.userid=a.userid 
             WHERE  a.approveState = 2 and (a.isHoliday = 1 or a.conversionType = 1)'''
    if not all:
        cmd += "  a.userid=\'{}\'".format(user_id)

    return get_multi_recored_with_cmd(cmd)

def get_total_over_time(all, user_id=''):
    cmd = '''SELECT a.id , a.userId, a.endYearMonth, 
                    a.ODay, a.OTime,  w.name
             FROM   OverTimeTab a 
             JOIN   WorkerMessage w 
             ON     w.userid=a.userid '''
    if not all:
        cmd += " where a.userid=\'{}\'".format(user_id)

    return get_multi_recored_with_cmd(cmd)

def combine_history_and_over_time(over_time_detials, over_time_total):
    over_time_detials_dic = database2dic(over_time_detials, history_dic_key_list)
    over_time_total_dic = database2dic(over_time_total, over_time_dic_key_list)
    result = {'data':[], 'filters':{}}
    endYearMonth_filters = []
    userId_filters = []
    for over_time in over_time_total_dic:
        over_time['overtime'] = "{}天{}时".format(over_time['ODay'], over_time['OTime'])
        over_time['groupItem'] = []
        for history in over_time_detials_dic:
            if over_time['userId'] == history['userId'] and history['applyEndTime'].startswith(over_time['endYearMonth']):
                over_time['groupItem'].append(history)
        result['data'].append(over_time)
        endYearMonth_filters.append(over_time['endYearMonth'])
        userId_filters.append(over_time['userId'])
    endYearMonth_filters,userId_filters = set(endYearMonth_filters), set(userId_filters)
    result['filters']['endYearMonth_filters'] = [{'text': x, 'value': x} for x in endYearMonth_filters]
    result['filters']['userId_filters'] = [{'text': x, 'value': x} for x in userId_filters]
    return result


def getOverTimeData(request):
    if request.method == "POST":
        over_time_detials = get_over_time(all=True)
        over_time_total = get_total_over_time(all=True)
        data = combine_history_and_over_time(over_time_detials, over_time_total)
        response = set_response(1, 'success', data)
    else:
        response = set_response(0, 'filed')
    return JsonResponse(response)

def getOverTimeUserData(request):
    if request.method == "POST":
        param = request.POST
        user_id = param['userId']
        results = get_total_over_time(False, user_id=user_id)
        results = database2dic(results, over_time_dic_key_list)
        for r in results:
            r['overtime'] = "{}天{}时".format(r['ODay'], r['OTime'])
        if len(results) == 0:
            response = set_response(2004, 'no user message')
        else:
            response = set_response(1, 'success', data=results)
        return JsonResponse(response)


def resetPwd(request):
    param = request.POST
    new_key = param['new_key']
    name = param['userId']
    new_key = decrypt_data(new_key)
    try:
        with connection.cursor() as cursor:
            cmd = "update LoginMessage set KEY=\'{}\' \
                   where name=\'{}\'".format(new_key, name)
            cursor.execute(cmd)
        response = set_response(1, 'success')
    except:
        response = set_response(0, 'failed')
    return JsonResponse(response)

def getWorkerId(request):
    param = request.POST
    user_id = param['userId']
    if get_user_type(user_id) == 2:
        with connection.cursor() as cursor:
            cmd = "select name from  LoginMessage"
            cursor.execute(cmd)
            results = cursor.fetchall()
            userids = []
            for r in results:
                userids.append({'label': r[0], 'value':r[0]})
        response = set_response(1, 'success', data=userids)
    else:
        response = set_response(0, 'failed')
    return JsonResponse(response)


def iskeyOk(user_id, key):

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT  key from  LoginMessage WHERE userid = %s", [user_id])
        res = cursor.fetchall()
        # print (res)
        if len(res) == 0:
            return  False # 没有获取到用户信息
        else:
            if res[0][0] == key:
                return True
            else:
                return  False


def resetPwdWork(request):
    param = request.POST
    new_key = param['new_key']
    userId =  param['userId']
    old_key =  param['old_key']
    new_key = decrypt_data(new_key)
    old_key = decrypt_data(old_key)
    if (iskeyOk(userId, old_key)):
        try:
            with connection.cursor() as cursor:
                cmd = "update LoginMessage set KEY=\'{}\' \
                       where userId=\'{}\'".format(new_key, userId)
                cursor.execute(cmd)
            response = set_response(1, 'success')
        except:
            response = set_response(0, 'failed')
    else:
        response = set_response(0, 'failed')
    return JsonResponse(response)