
history_dic_key_list = ['id', 'userId', 'applyTime', 'applyStartTime', 'applyEndTime', 'applyType',
                        'holidayType', 'approveState', 'applyReason', 'applyTimeLast', 'name', 'approveNote']
pool_dic_key_list = ['userId', 'generalHolidayTotal', 'generalHolidayRemainderDays', 'generalHolidayRemainderTime',
                     'accumulateHolidayRemainderDays', 'accumulateHolidayRemainderTime', 'accumulateHolidayUsedDays',
                     'accumulateHolidayUsedTime', 'barterAccumulateHolidayDays', 'barterAccumulateHolidayTime',
                     'restPoolTotalDays', 'restPoolTotalTime', 'name']


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


def get_worker_pool(user_id):
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
              where r.userid=''' + user_id
    return get_multi_recored_with_cmd(cmd)


def get_worker_history_from_database(user_id):
    cmd = '''SELECT a.id , a.userId, a.applyTime, 
                    a.applyStartTime, a.applyEndTime, a.applyType,
                    a.holidayType,a.approveState, a.applyReason, 
                    a.applyTimeLast, w.name,a.approveNote 
             FROM   ApplyHistory a 
             JOIN   WorkerMessage w 
             ON     w.userid=a.userid
             WHERE  userid='''+user_id
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
        pool['accumulateHolidayUsed'],  pool['accumulateHolidayUsed'])
    pool['barterAccumulateHoliday'] = "{}天{}时".format(
        pool['barterAccumulateHolidayDays'], pool['barterAccumulateHolidayDays'])
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
            if pool_new['userId'] == history['userId']:
                pool_new['groupItem'].append(history)
        result.append(pool_new)
    return result
