from flask import Flask
import couchDBUtil as dbUtil
from flask_cors import *

app = Flask(__name__)
CORS(app, support_CREDENTIALS=True)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/postTest', methods=["POST"])
def postTest():
    result = [{'cityName': 'London', 'twitterCount': 1000}, {'cityName': 'New York', 'twitterCount': 2000}]
    return result


@app.route('/getTest', methods=["GET"])
def getTest():
    result = [{'cityName': 'London', 'twitterCount': 1000}, {'cityName': 'New York', 'twitterCount': 2000}]
    return result


# Get the number of tweets posted by each city
@app.route('/city_num', methods=["GET"])
def getCityTwitterCounts():
    db = dbUtil.getDB('twitter_all_new')
    view = dbUtil.getView(db, 'city/city_num')
    data = []
    for row in view:
        rowInfo = {'cityName': row.key, 'twitterCount': row.value}
        data.append(rowInfo)
    return data


# Get the number of tweets posted in each language
@app.route('/lang_num', methods=["GET"])
def getLanguageTwitterCounts():
    db = dbUtil.getDB('twitter_all_new')
    view = dbUtil.getView(db, 'lang/lang_num')
    data = []
    for row in view:
        rowInfo = {'language': row.key, 'twitterCount': row.value}
        data.append(rowInfo)
    return data


# Get the number of tweets posted in each language
@app.route('/month_num', methods=["GET"])
def month_num():
    db = dbUtil.getDB('twitter_all_new')
    view = dbUtil.getView(db, 'month/month_num')
    data = []
    for row in view:
        rowInfo = {'month': row.key, 'twitterCount': row.value}
        data.append(rowInfo)
    return data


# Get urban opposition
@app.route('/city_polarity', methods=["GET"])
def city_polarity():
    db = dbUtil.getDB('twitter_all_new')
    view = dbUtil.getView(db, 'polarity/city_polarity')
    data = []
    for row in view:
        rowInfo = {'cityName': row.key, 'polarity': row.value}
        data.append(rowInfo)
    return data


# GET polarity_month_average
@app.route('/polarity_month_average', methods=["GET"])
def polarity_month_average():
    db = dbUtil.getDB('twitter_all_new')
    view = dbUtil.getView(db, 'polarity_month/polarity_month_average')
    data = []
    for row in view:
        rowInfo = {'month': row.key, 'polarity': row.value}
        data.append(rowInfo)
    return data


##industry_twitter_new
##Four industries nunm
##art_num
@app.route('/art_num', methods=["GET"])
def art_num():
    db = dbUtil.getDB('industry_twitter_new')
    view = dbUtil.getView(db, 'Four Industries num/art_num')
    data = []
    for row in view:
        rowInfo = {'Art': row.key, 'num': row.value}
        data.append(rowInfo)
    return data


##edu_num
@app.route('/edu_num', methods=["GET"])
def edu_num():
    db = dbUtil.getDB('industry_twitter_new')
    view = dbUtil.getView(db, 'Four Industries num/edu_num')
    data = []
    for row in view:
        rowInfo = {'Edu': row.key, 'num': row.value}
        data.append(rowInfo)
    return data


##fin_num
@app.route('/fin_num', methods=["GET"])
def fin_num():
    db = dbUtil.getDB('industry_twitter_new')
    view = dbUtil.getView(db, 'Four Industries num/fin_num')
    data = []
    for row in view:
        rowInfo = {'Fin': row.key, 'num': row.value}
        data.append(rowInfo)
    return data


##tech_num
@app.route('/tech_num', methods=["GET"])
def tech_num():
    db = dbUtil.getDB('industry_twitter_new')
    view = dbUtil.getView(db, 'Four Industries num/tech_num')
    data = []
    for row in view:
        rowInfo = {'Tech': row.key, 'num': row.value}
        data.append(rowInfo)
    return data


##job_type
@app.route('/job_type_num', methods=["GET"])
def job_type_num():
    db = dbUtil.getDB('industry_twitter_new')
    view = dbUtil.getView(db, 'job_type/job_type_num')
    data = []
    for row in view:
        rowInfo = {'Job_type': row.key, 'num': row.value}
        data.append(rowInfo)
    return data


##month
@app.route('/industry_month_num', methods=["GET"])
def industry_month_num():
    db = dbUtil.getDB('industry_twitter_new')
    view = dbUtil.getView(db, 'month/month_num')
    data = []
    for row in view:
        rowInfo = {'Month': row.key, 'num': row.value}
        data.append(rowInfo)
    return data


##polarity
##art_polarity_num
@app.route('/art_polarity_num', methods=["GET"])
def art_polarity_num():
    db = dbUtil.getDB('industry_twitter_new')
    view = dbUtil.getView(db, 'polarity/art_polarity_num')
    data = []
    for row in view:
        rowInfo = {'Art': row.key, 'num': row.value}
        data.append(rowInfo)
    return data


##edu_polarity_num
@app.route('/edu_polarity_num', methods=["GET"])
def edu_polarity_num():
    db = dbUtil.getDB('industry_twitter_new')
    view = dbUtil.getView(db, 'polarity/edu_polarity_num')
    data = []
    for row in view:
        rowInfo = {'Edu': row.key, 'num': row.value}
        data.append(rowInfo)
    return data


##fin_polarity_num
@app.route('/fin_polarity_num', methods=["GET"])
def fin_polarity_num():
    db = dbUtil.getDB('industry_twitter_new')
    view = dbUtil.getView(db, 'polarity/fin_polarity_num')
    data = []
    for row in view:
        rowInfo = {'Fin': row.key, 'num': row.value}
        data.append(rowInfo)
    return data


##tech_polarity_num
@app.route('/tech_polarity_num', methods=["GET"])
def tech_polarity_num():
    db = dbUtil.getDB('industry_twitter_new')
    view = dbUtil.getView(db, 'polarity/tech_polarity_num')
    data = []
    for row in view:
        rowInfo = {'Tech': row.key, 'num': row.value}
        data.append(rowInfo)
    return data


##sudoindustry_type

@app.route('/eachjobtype_num', methods=["GET"])
def eachjobtype_num():
    db = dbUtil.getDB('sudo_industry_type')
    view = dbUtil.getView(db, 'jobtype_num/eachjobtype_num')
    data = []
    for row in view:
        rowInfo = {'Eachjobtype': row.key, 'num': row.value}
        data.append(rowInfo)
    return data


@app.route('/job_type_time', methods=["GET"])
def job_type_time():
    db = dbUtil.getDB('sudo_industry_type')
    view = dbUtil.getView(db, 'city/job_type_time')
    data = []
    for row in view:
        rowInfo = {'Jobtype': row.key, 'time': row.value}
        data.append(rowInfo)
    return data


##sudoindustry_worktime

@app.route('/job_type_gender', methods=["GET"])
def job_type_gender():
    db = dbUtil.getDB('sudo_industry_worktime')
    view = dbUtil.getView(db, 'gender/job_type_gender')
    data = []
    for row in view:
        rowInfo = {'job_type': row.key, 'gender': row.value}
        data.append(rowInfo)
    return data


@app.route('/num_jobtype', methods=["GET"])
def num_jobtype():
    db = dbUtil.getDB('sudo_industry_worktime')
    view = dbUtil.getView(db, 'num_industry/num_jobtype')
    data = []
    for row in view:
        rowInfo = {'num': row.key, 'jobetype': row.value}
        data.append(rowInfo)
    return data


##mastdon_all

@app.route('/mastodon_month_num', methods=["GET"])
def mastodon_month_num():
    db = dbUtil.getDB('mastodon_all_servers')
    view = dbUtil.getView(db, 'month/month_num')
    data = []
    for row in view:
        rowInfo = {'month': row.key, 'num': row.value}
        data.append(rowInfo)
    return data


@app.route('/polarity_sum', methods=["GET"])
def polarity_sum():
    db = dbUtil.getDB('mastodon_all_servers')
    view = dbUtil.getView(db, 'polarity/polarity_sum')
    data = []
    for row in view:
        rowInfo = {'polarity': row.key, 'sum': row.value}
        data.append(rowInfo)
    return data

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port='8000')

