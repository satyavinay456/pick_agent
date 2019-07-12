from flask import Flask,render_template,request,jsonify,session,redirect,url_for
import datetime,time,random
import traceback
import pandas as pd
from pprint import pprint

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
        reviews_loc_id="static/datasets/"+city_name+"_reviews.xlsx"
        brok_reviews=pd.read_excel(reviews_loc_id)

        brok_pts.drop_duplicates(inplace=True)
        #left joining two dataframes
        fin_brok=brok.merge(brok_pts,how="left",on=["CRD"])
        fin_brok=fin_brok.merge(brok_reviews,how="left",on=["CRD"])
        fin_brok.drop_duplicates(inplace=True)

        fin_brok.sort_values(by=['Points'], inplace=True, ascending=False)
        print(fin_brok['Points'].head(5))
        fin_brok['Points']=fin_brok['Points']*100
        fin_brok['Points']=fin_brok['Points'].round(4)
        #fin_brok=fin_brok.reset_index()
        print(fin_brok.head(5))
        print(fin_brok['Points'].head(5))
        fin_brok=fin_brok[fin_brok['Points']!=0]
        fin_brok['Licenses'].fillna(0,inplace=True)
        fin_brok['SRO'].fillna(0,inplace=True)
        fin_brok['State_Registrations'].fillna("-",inplace=True)
        fin_brok['Licenses']=fin_brok['Licenses'].apply(int)
        fin_brok['SRO']=fin_brok['SRO'].apply(int)
        fin_brok['Reviews'].fillna("-",inplace=True)
        gents_data=fin_brok.values.tolist()
        pprint(gents_data[21][14])
        def reviews_cln(row):
            rev=str(row['Reviews'])
            #print(rev)
            rev.replace("\n","")
            if rev!="-" :
                rev.replace("\n",".")
                return "\n".join(rev.split("$~$"))
            else:
                return "-"
        fin_brok['Reviews']=fin_brok.apply(reviews_cln,axis=1)
        fin_brok['Reviews']=fin_brok['Reviews'].apply(lambda x: x.replace("\n",""))
        agents_data=fin_brok.values.tolist()
        agents_count=len(agents_data)
        print(agents_data[26][14])
        pprint(agents_data[23][14])
        print(list(fin_brok))
        fin_brok.to_excel("static/client_download/brokers_info.xlsx",index=False)
    else:
        agents_data=[["-","-","-","-"]]
        city_name="XXXXX"
        agents_count=0
    return render_template('agents.html',agents_data=agents_data,city_name=city_name,agents_count=agents_count)

@app.route('/<id>')
def agents_details(id):
    try:
        city_name=session['ses_city']
    except:
        return redirect(url_for('dashboard'))
    loc_id="static/datasets/"+city_name+"_brokers.xlsx"
    pts_loc_id="static/datasets/"+city_name+"_brokers_pts.xlsx"
    reviews_loc_id="static/datasets/"+city_name+"_reviews.xlsx"

    print(loc_id,"\t****")
    brok=pd.read_excel(loc_id)
    brok.drop_duplicates(inplace=True)
    brok_pts=pd.read_excel(pts_loc_id)
    brok_reviews=pd.read_excel(reviews_loc_id)

    brok_pts.drop_duplicates(inplace=True)
    fin_brok=brok.merge(brok_pts,how="left",on=["CRD"])
    fin_brok=fin_brok.merge(brok_reviews,how="left",on=["CRD"])

    fin_brok.drop_duplicates(inplace=True)
    fin_brok['Points']=fin_brok['Points']*100
    fin_brok['Points']=fin_brok['Points'].round(4)
    fin_brok=fin_brok[fin_brok['Points']!=0]
    fin_brok['Licenses'].fillna(0,inplace=True)
    fin_brok['SRO'].fillna(0,inplace=True)
    fin_brok['Licenses']=fin_brok['Licenses'].apply(int)
    fin_brok['SRO']=fin_brok['SRO'].apply(int)
    fin_brok['State_Registrations'].apply(str)
    fin_brok['State_Registrations'].fillna("-",inplace=True)
    fin_brok['Exams'].fillna("-",inplace=True)
    fin_brok['TotalExperience'].fillna(0,inplace=True)
    fin_brok['PresentExperience'].fillna(0,inplace=True)
    fin_brok['InsuranceAdv'].fillna("-",inplace=True)
    fin_brok['Reviews'].fillna("-",inplace=True)
    #fin_brok['Reviews']=fin_brok['Reviews'].replace("$~$","-")
    def state_reg(row):
        sr=str(row['State_Registrations'])
        if sr!="-":
            return sr[22:].replace("B",",")
        else:
            return "-"
    def reviews_cln(row):
        rev=str(row['Reviews'])
        if rev!="-":
            rev.replace("\n",".")
            return "\n".join(rev.split("$~$"))
        else:
            return "-"
    #fin_brok['Reviews']=fin_brok.apply(reviews_cln,axis=1)
    fin_brok['State_Registrations']=fin_brok.apply(state_reg,axis=1)
    print(fin_brok['CRD'].head())
    try:
        fin_brok=fin_brok[fin_brok['CRD']==int(id)].iloc[0]
    except:
        return render_template('user_info.html',id=0,fin_brok=pd.DataFrame())

    if fin_brok['Reviews']=="$~$": fin_brok['Reviews']="-"
    if fin_brok['Reviews']!="-":
        fin_brok['Reviews']= "\n\n".join(fin_brok['Reviews'].replace("\n",".").split("$~$"))
    print(fin_brok)
    return render_template('user_info.html',id=id,fin_brok=fin_brok)


#Filters
@app.route('/tot_exp_filter',methods=['POST','GET'])
def tot_exp_filter():
    if request.method=='POST':
        filter_on=request.form.get('filter_on')
        print(filter_on,"+++++++++++++++")
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
            fin_brok.sort_values(by=[filter_on], inplace=True, ascending=False)
            fin_brok['Points']=fin_brok['Points']*100
            fin_brok['Points']=fin_brok['Points'].round(4)
            fin_brok=fin_brok[fin_brok['Points']!=0]
            fin_brok['Licenses'].fillna(0,inplace=True)
            fin_brok['SRO'].fillna(0,inplace=True)
            fin_brok['Licenses']=fin_brok['Licenses'].apply(int)
            fin_brok['SRO']=fin_brok['SRO'].apply(int)
            #adding reviews dataset
            reviews_loc_id="static/datasets/"+city_name+"_reviews.xlsx"
            brok_reviews=pd.read_excel(reviews_loc_id)
            fin_brok=fin_brok.merge(brok_reviews,how="left",on=["CRD"])
            fin_brok.drop_duplicates(inplace=True)
            def reviews_cln(row):
                rev=str(row['Reviews'])
                rev.replace("\n","")
                if rev!="-" :
                    rev.replace("\n",".")
                    return "\n".join(rev.split("$~$"))
                else:
                    return "-"
            fin_brok['Reviews'].fillna("",inplace=True)
            fin_brok['Reviews']=fin_brok.apply(reviews_cln,axis=1)
            fin_brok['Reviews']=fin_brok['Reviews'].apply(lambda x: x.replace("\n",""))
            #ended reviews section
            fin_brok.to_excel("static/client_download/brokers_info.xlsx",index=False)
            print(fin_brok.head())
            agents_data=fin_brok.values.tolist()
            agents_count=len(agents_data)
            html_data=""
            for i in agents_data:
                if i[-2] not in ["-",""]:
                    img_tag='<img style="height:20px; position:relative;top:10px;left:45%;" class="card-img-top card_size" src="static/bookmark.svg" alt="Card image">'
                else:
                    img_tag=""
                temp=f"""
                    <div class="card" style="width: 18rem;">
                        {img_tag}
                      <div class="card-body  ">
                        <div style="height:100px;">
                          <a href="#" onclick="window.open('https://brokercheck.finra.org/individual/summary/{i[1]}');return false;"  style="color: #000000;">  <h5  class="card-title">{i[0]}</h5> </a>
                          <h6 class="card-subtitle mb-2 text-muted">{i[2]}</h6>
                        </div>
                        <p class="card-text"> Total Experience : {i[10]}</p>
                        <p class="card-text"> Experience in current city : {i[8]}</p>
                        <p class="card-text"> SRO Registrations : {i[9]}</p>

                        <p class="card-text"> Advisor : {i[5]}</p>
                        <p class="<card-text>  </card-text>"> State Licenses : {i[6]}</p>

                        <div class="row">
                              <div class="col">
                                  <p class="card-text"> CRD : {i[1]}</p>
                              </div>
                              <div class="col">
                                  <p class="card-text"> Points : {i[7]}</p>
                              </div>
                        </div><br>
                        <h6 class="card-subtitle mb-2 text-muted"> contact: {i[4]}</h6>
                        <a target="_blank" href="{i[1]}" class="card-link" style="color:#000000;" >More info</a>
                      </div>
                    </div>"""
                html_data+=temp
            return jsonify({"html_data":html_data,"agents_count":agents_count})

@app.route('/search_agents',methods=['POST','GET'])
def search_agents():
    if request.method=='POST':
        print("$$$$$$$$$$$")
        search_word=request.form.get('search_word')
        search_word=search_word.upper()
        print(search_word,"+++++++++++++++")
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
            print(fin_brok.head())
            fin_brok=fin_brok[fin_brok['Name'].str.match(search_word)]
            if fin_brok.empty:
                return jsonify({"html_data":"","agents_count":0})
            print(fin_brok.head())
            fin_brok['Points']=fin_brok['Points']*100
            fin_brok['Points']=fin_brok['Points'].round(4)
            fin_brok=fin_brok[fin_brok['Points']!=0]
            fin_brok['Licenses'].fillna(0,inplace=True)
            fin_brok['SRO'].fillna(0,inplace=True)
            fin_brok['Licenses']=fin_brok['Licenses'].apply(int)
            fin_brok['SRO']=fin_brok['SRO'].apply(int)
            #adding reviews dataset
            reviews_loc_id="static/datasets/"+city_name+"_reviews.xlsx"
            brok_reviews=pd.read_excel(reviews_loc_id)
            fin_brok=fin_brok.merge(brok_reviews,how="left",on=["CRD"])
            fin_brok.drop_duplicates(inplace=True)
            def reviews_cln(row):
                rev=str(row['Reviews'])
                rev.replace("\n","")
                if rev!="-" :
                    rev.replace("\n",".")
                    return "\n".join(rev.split("$~$"))
                else:
                    return "-"
            fin_brok['Reviews'].fillna("",inplace=True)
            fin_brok['Reviews']=fin_brok.apply(reviews_cln,axis=1)
            fin_brok['Reviews']=fin_brok['Reviews'].apply(lambda x: x.replace("\n",""))
            #ended reviews section
            fin_brok.to_excel("static/client_download/brokers_info.xlsx",index=False)
            print("_______________________-")
            agents_data=fin_brok.values.tolist()
            print(agents_data)
            agents_count=len(agents_data)
            html_data=""
            for i in agents_data:
                if i[-2] not in ["-",""]:
                    img_tag='<img style="height:20px; position:relative;top:10px;left:45%;" class="card-img-top card_size" src="static/bookmark.svg" alt="Card image">'
                else:
                    img_tag=""
                temp=f"""
                    <div class="card" style="width: 18rem;">
                        {img_tag}
                      <div class="card-body  ">
                        <div style="height:100px;">
                          <a href="#" onclick="window.open('https://brokercheck.finra.org/individual/summary/{i[1]}');return false;"  style="color: #000000;">  <h5  class="card-title">{i[0]}</h5> </a>
                          <h6 class="card-subtitle mb-2 text-muted">{i[2]}</h6>
                        </div>
                        <p class="card-text"> Total Experience : {i[10]}</p>
                        <p class="card-text"> Experience in current city : {i[8]}</p>
                        <p class="card-text"> SRO Registrations : {i[9]}</p>

                        <p class="card-text"> Advisor : {i[5]}</p>
                        <p class="<card-text>  </card-text>"> State Licenses : {i[6]}</p>

                        <div class="row">
                              <div class="col">
                                  <p class="card-text"> CRD : {i[1]}</p>
                              </div>
                              <div class="col">
                                  <p class="card-text"> Points : {i[7]}</p>
                              </div>
                        </div><br>
                        <h6 class="card-subtitle mb-2 text-muted"> contact: {i[4]}</h6>
                        <a target="_blank" href="{i[1]}" class="card-link" style="color:#000000;">More info</a>
                      </div>
                    </div>"""
                html_data+=temp
            return jsonify({"html_data":html_data,"agents_count":agents_count})

@app.route('/exams_filter',methods=['POST','GET'])
def exam_filter():
    if request.method=='POST':
        print(request.form)
        filter_on=request.form.get('filter_on')
        exams_checked=request.form.getlist('exams_checked[]')
        print("******")
        print(exams_checked)
        if int(filter_on)>=1:
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
                fin_brok=brok.merge(brok_pts,how="left",on=["CRD"])


                fin_brok['Points']=fin_brok['Points']*100
                fin_brok['Points']=fin_brok['Points'].round(4)
                fin_brok=fin_brok[fin_brok['Points']!=0]
                fin_brok['Licenses'].fillna(0,inplace=True)
                fin_brok['SRO'].fillna(0,inplace=True)
                fin_brok['Licenses']=fin_brok['Licenses'].apply(int)
                fin_brok['SRO']=fin_brok['SRO'].apply(int)
                #adding reviews dataset
                reviews_loc_id="static/datasets/"+city_name+"_reviews.xlsx"
                brok_reviews=pd.read_excel(reviews_loc_id)
                fin_brok=fin_brok.merge(brok_reviews,how="left",on=["CRD"])
                fin_brok.drop_duplicates(inplace=True)
                def exam_filter(row):
                    new=str(row['Exams'])
                    series=[i[:i.find("-")].rstrip().split()[1] for i in new.split("\n") if i.startswith('Series')]
                    if set(exams_checked)<=set(series):
                        print(series)
                        return "yes"
                    else:
                        return "no"
                fin_brok['exam_conditon']=fin_brok.apply(exam_filter,axis=1)
                fin_brok=fin_brok[fin_brok['exam_conditon']=="yes"]
                def reviews_cln(row):
                    rev=str(row['Reviews'])
                    rev.replace("\n","")
                    if rev!="-" :
                        rev.replace("\n",".")
                        return "\n".join(rev.split("$~$"))
                    else:
                        return "-"
                fin_brok['Reviews'].fillna("",inplace=True)
                fin_brok['Reviews']=fin_brok.apply(reviews_cln,axis=1)
                fin_brok['Reviews']=fin_brok['Reviews'].apply(lambda x: x.replace("\n",""))
                #ended reviews section

                fin_brok.to_excel("static/client_download/brokers_info.xlsx",index=False)
                #print(fin_brok[['CRD','exam_conditon']])
                agents_data=fin_brok.values.tolist()
                agents_count=len(agents_data)
                html_data=""
                print(list(fin_brok))
                for i in agents_data:
                    if i[-3] not in ["-",""]:
                        img_tag='<img style="height:20px; position:relative;top:10px;left:45%;" class="card-img-top card_size" src="static/bookmark.svg" alt="Card image">'
                    else:
                        img_tag=""
                    temp=f"""
                        <div class="card" style="width: 18rem;">
                            {img_tag}
                          <div class="card-body  ">
                            <div style="height:100px;">
                              <a href="#" onclick="window.open('https://brokercheck.finra.org/individual/summary/{i[1]}');return false;"  style="color: #000000;">  <h5  class="card-title">{i[0]}</h5> </a>
                              <h6 class="card-subtitle mb-2 text-muted">{i[2]}</h6>
                            </div>
                            <p class="card-text"> Total Experience : {i[10]}</p>
                            <p class="card-text"> Experience in current city : {i[8]}</p>
                            <p class="card-text"> SRO Registrations : {i[9]}</p>

                            <p class="card-text"> Advisor : {i[5]}</p>
                            <p class="<card-text>  </card-text>"> State Licenses : {i[6]}</p>

                            <div class="row">
                                  <div class="col">
                                      <p class="card-text"> CRD : {i[1]}</p>
                                  </div>
                                  <div class="col">
                                      <p class="card-text"> Points : {i[7]}</p>
                                  </div>
                            </div><br>
                            <h6 class="card-subtitle mb-2 text-muted"> contact: {i[4]}</h6>
                            <a target="_blank" href="{i[1]}" class="card-link" style="color:#000000;">More info</a>
                          </div>
                        </div>"""
                    html_data+=temp
                return jsonify({"html_data":html_data,"agents_count":agents_count})

if __name__ == '__main__':
   app.run(debug = True,host="0.0.0.0")
