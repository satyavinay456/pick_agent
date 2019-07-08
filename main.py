from flask import Flask,render_template,request,jsonify,session,redirect,url_for
import datetime,time,random
import traceback
import pandas as pd

app = Flask(__name__)
app.secret_key="bahgahegfakwnefkan"

zip_codes={98004:"bellevue",98005:"bellevue",98006:"bellevue",98007:"bellevue",98008:"bellevue",98009:"bellevue",98015:"bellevue"}

print(zip_codes[98004])
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

#getting city zip/name from ajax
@app.route("/city_code",methods=['POST','GET'])
def city_code():
    if request.method=='POST':
        entered_city=request.form.get('entered_city')
        print(entered_city,"+++++")
        print(entered_city.isdigit())
        if entered_city.isdigit()==True:
            print("yes")
            try:
                entered_city=zip_codes[int(entered_city)]
                print(entered_city,"---------")
            except:
                traceback.print_exc()
                entered_city=""
        session['ses_city']=entered_city
        print(entered_city)
        return url_for('agents')
    return render_template('404.html')



@app.route('/agents')
def agents():
    try:
        city_name=session['ses_city']
    except:
        return redirect(url_for('dashboard'))
    if city_name!="":
        loc_id="static/datasets/"+city_name+"_brokers.xlsx"
        pts_loc_id="static/datasets/"+city_name+"_brokers_pts.xlsx"
        print(loc_id,"\t****")
        brok=pd.read_excel(loc_id)
        brok.drop_duplicates(inplace=True)
        brok_pts=pd.read_excel(pts_loc_id)
        brok_pts.drop_duplicates(inplace=True)
        #left joining two dataframes
        fin_brok=brok.merge(brok_pts,how="left",on=["CRD"]).iloc[:,:-1]
        fin_brok.drop_duplicates(inplace=True)
        fin_brok.sort_values(by=['Points'], inplace=True, ascending=False)
        print(fin_brok['Points'].head(5))
        fin_brok['Points']=fin_brok['Points']*100
        fin_brok['Points']=fin_brok['Points'].round(4)
        #fin_brok=fin_brok.reset_index()
        print(fin_brok.head(5))
        print(fin_brok['Points'].head(5))
        fin_brok=fin_brok[fin_brok['Points']!=0]
        agents_data=fin_brok.values.tolist()
        agents_count=len(agents_data)
    else:
        agents_data=[["-","-","-","-"]]
        city_name="XXXXX"
        agents_count=0
    return render_template('agents.html',agents_data=agents_data,city_name=city_name,agents_count=agents_count)

@app.route('/<id>')
def agents_details(id):
    return render_template('user_info.html',id=id)


#Filters
@app.route('/tot_exp_filter',methods=['POST','GET'])
def tot_exp_filter():
    if request.method=='POST':
        filter_on=request.form.get('filter_on')
        print(filter_on,"+++++++++++++++")
        city_name=session['ses_city']
        if city_name!="":
            loc_id="static/datasets/"+city_name+"_brokers.xlsx"
            pts_loc_id="static/datasets/"+city_name+"_brokers_pts.xlsx"
            print(loc_id,"\t****")
            brok=pd.read_excel(loc_id)
            brok.drop_duplicates(inplace=True)
            brok_pts=pd.read_excel(pts_loc_id)
            brok_pts.drop_duplicates(inplace=True)
            #left joining two dataframes
            fin_brok=brok.merge(brok_pts,how="left",on=["CRD"]).iloc[:,:-1]
            fin_brok.drop_duplicates(inplace=True)
            fin_brok.sort_values(by=[filter_on], inplace=True, ascending=False)
            fin_brok['Points']=fin_brok['Points']*100
            fin_brok['Points']=fin_brok['Points'].round(4)
            fin_brok=fin_brok[fin_brok['Points']!=0]
            print(list(fin_brok))
            #fin_brok=fin_brok.reset_index()
            print(fin_brok.head(5))
            print(fin_brok['TotalExperience'].head(5))
            agents_data=fin_brok.values.tolist()
            agents_count=len(agents_data)
            html_data=""
            for i in agents_data:
                temp=f"""
                    <div class="card" style="width: 18rem;">
                      <div class="card-body  ">
                        <div style="height:100px;">
                          <a href="#" onclick="window.open('https://brokercheck.finra.org/individual/summary/{i[1]}');return false;"  style="color: #000000;">  <h5  class="card-title">{i[0]}</h5> </a>
                          <h6 class="card-subtitle mb-2 text-muted">{i[2]}</h6>
                        </div>
                        <p class="card-text"> Total Experience : {i[-1]}</p>
                        <p class="card-text"> Experience in current city : {i[-3]}</p>
                        <p class="card-text"> SRO Registrations : {i[-2]}</p>

                        <p class="card-text"> advisor : {i[5]}</p>
                        <p class="<card-text>  </card-text>"> Licenses : {i[6]}</p>

                        <div class="row">
                              <div class="col">
                                  <p class="card-text"> CRD : {i[1]}</p>
                              </div>
                              <div class="col">
                                  <p class="card-text"> Points : {i[7]}</p>
                              </div>
                        </div><br>
                        <h6 class="card-subtitle mb-2 text-muted"> contact: {i[4]}</h6>
                        <a href="{i[1]}" class="card-link">More info</a>
                      </div>
                    </div>"""
                html_data+=temp
            return html_data


if __name__ == '__main__':
   app.run(debug = True,host="0.0.0.0")
