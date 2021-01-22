from flask import Flask,jsonify
def filterData(requestClient , tabledb) :
    output = []
    for toado in requestClient['data'] : 
        for record in tabledb.find() :
            # if float(record['slat']) < float(record['elat']) and float(record['slng']) < float(record['elng']) : 
            #     if (float(record['slat']) <= float(toado['lat'])) and (float(toado['lat']) <= float(record['elat']) ):
            #         if (float(record['slng']) <= float(toado['log']))and (float(toado['log']) <= float(record['elng']) ) :
            #             output.append({'segment_id' : record['segment_id'] , 
            #                         'lat' : toado['lat'], 
            #                         'log'  :toado['log'],
            #                         'time' : toado['time'],
            #                         'dayofWeek' : toado['dayofWeek']
            #                         }
            #                         )  
            if float(record['slat']) < float(record['elat']) and float(record['slng']) > float(record['elng']) : 
                if (float(record['slat']) <= float(toado['lat'])) and (float(toado['lat']) <= float(record['elat']) ):
                    if (float(record['slng']) >= float(toado['log']))and (float(toado['log']) >= float(record['elng']) ) :
                        output.append({'segment_id' : record['segment_id'] , 
                                    'lat' : toado['lat'], 
                                    'log'  :toado['log'],
                                    'time' : toado['time'],
                                    'dayofWeek' : toado['dayofWeek']
                                    }
                                    )            
    return output