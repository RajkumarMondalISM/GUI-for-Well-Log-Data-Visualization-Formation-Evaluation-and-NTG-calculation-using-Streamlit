import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import lasio
import seaborn as sns
import io
import plotly.express as px
import plotly.graph_objects as go

st.title("Welcome ladies, Gentleman and Others.")
st.header("Petrophysical Measurement Analysis and Visualisation")
st.subheader("Using Python")
#text=st.button("click")
st.title("NOTE : ")
st.markdown("please see your log short notation and then change in Las log Name Changer section after Data Statistics as following - DEPTH(depth), CALI(Caliper),GR(gamma ray),NPHI(porosity),RHOB(density),RESD(deep resistivity Rt),RESS(shallow resistivity Rx0)")
#st.color_picker("color")


# st.radio("pick ur gender",["male","Female","other"])
# st.selectbox("pick your course",["Ml","python","java"])
# st.multiselect("chose the formation evaluatio option",["Vsh","Sw by Archie ","Sw by Simandoux","NPHI","Desity Porosity"])
# st.select_slider("Rating",["bad","Good","Excilant"])
#files=st.file_uploader("upload your las file")

# if files:
#     tr
#         las=lasio.read(files)
#         df=df.las().reset_index()
#         st.write(df.describe())
#     except Exception as e:
#         st.error(f"Error: {e}")
# import streamlit as st








from io import StringIO





def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            bytes_data = uploaded_file.read()
            str_io = StringIO(bytes_data.decode('Windows-1252'))
            las_file = lasio.read(str_io)
            well_data = las_file.df()
            well_data['DEPTH'] = well_data.index

        except UnicodeDecodeError as e:
            st.error(f"error loading log.las: {e}")
    else:
        las_file = None
        well_data = None

    return las_file, well_data



# Sidebar Options & File Uplaod
las_file=None

uploadedfile = st.file_uploader(' ', type=['.las'])
las_file, well_data = load_data(uploadedfile)

if las_file:
    st.success('File Uploaded Successfully')
    st.write(f'<b>Well Name</b>: {las_file.well.WELL.value}',unsafe_allow_html=True)
    
    
    
    b01=st.checkbox("Data Loading")
    if b01:
        b0=st.button("Well information")
        if b0:
            for item in las_file.well:
                st.write(f'{item.descr} ({item.mnemonic}):\t\t {item.value}')
    
    
        b1=st.button("Curve Information")
        if b1:
            mnemonics = [curve.mnemonic for curve in las_file.curves]
            descriptions = [curve.descr for curve in las_file.curves]
            unit = [curve.unit for curve in las_file.curves]

            data = {
                    "Mnemonic": mnemonics,
                    "Unit": unit,
                    "Description": descriptions   
            }
            st.write(pd.DataFrame(data))
    
    
        b2=st.button("Header Information")
        if b2:
            st.write(las_file.df())

   
        b3=st.button("Data statistics")
        if b3:
            st.write(well_data.describe())
    
    
        b02=st.checkbox("Formation evoluation")
        if b02:
            def change_log_names(las_file, log_name_mapping):
                las = (las_file)

   
                for old_name, new_name in log_name_mapping.items():
                    if old_name in las.keys():
                        las[new_name] = las[old_name]
                    #las.delet_curve(old_name)

                return las

            st.title("LAS Log Name Changer")
            st.subheader(" change the log names according to above note and click on change logs name checkbox otherwise error will occurs")
            if las_file:
                log_name_mapping = {}

        
                st.subheader("Log Name Mapping")
                for curve in las_file.keys():
                    new_name = st.text_input(f"New name for '{curve}':", curve)
                    log_name_mapping[curve] = new_name

                if st.checkbox("Change Log Names"):
                    modified_las = change_log_names(las_file,log_name_mapping)
                    st.success("Log names changed successfully.")
                    df= modified_las.df()
                    st.dataframe(df)
            
            
                b4=st.button("GRmin(5%)")
                if b4:
                    gr_values = df["GR"]
                    gr_5_percentile = gr_values.quantile(0.05)
                    st.write(f"5% Value of GR: {gr_5_percentile}")
        
        
                b5=st.button("GRmax(95%)")
                if b5:
                    gr_value=df["GR"]
                    gr_95=gr_value.quantile(.95)
                    st.write(f"95% Value of GR: {gr_95}")


                b6=st.button("Vsh Calculation")
                if b6:
                    gr_values = df["GR"]
                    gr_5_percentile = gr_values.quantile(0.05)
                    gr_value=df["GR"]
                    gr_95=gr_value.quantile(.95)
                    def Vsh(GRmin,GRmax,GRlog):
                        return ((GRlog-GRmin)/(GRmax-GRmin))
                    x=Vsh(gr_5_percentile,gr_95,df["GR"])
                    st.write(x.mean(),key="mean of Vsh")
                    # data1 = {
                    #         "Vsh": x  
                    # }
                    # st.write(pd.DataFrame(data1))
        
    
    
    
    
                b7=st.checkbox("Sw using Archie's Equation")
                if b7:
                    b8=st.number_input("pick a number for A value",key='b8')
                    if b8:
                        b9=st.number_input("pick a number for n value",key='b9')
                        if b9:
                            b10=st.number_input("pick a number for m value",key='b10')
                            if b10:
                                b11=st.number_input("pick a number for Rw value",key='b11')
                                if b11:
                                    def Sw(a,n,m,Rw,Rt,phi):
                                        return ((a*Rw)/((phi**m)*Rt))**(1/n)
                                    x1=Sw(b8,b9,b10,b11,df["RESD"],df["NPHI"])
                                    st.write(x1.mean(),key="Sw")
                                    # data2 = {
                                    #         "Sw Using Archie": x1  
                                    # }
                                    # st.write(pd.DataFrame(data2))
    
    
    
    
    
    
           


                b13 = st.checkbox("Density Porosity for Limestone Matrix")
                if b13:
                    b133 = st.radio("Select Type", ["Using_Gas_Density", "Using_Water_Density"],key='select type')
                    if b133 == "Using_Gas_Density":
                        def den_por(ma, bu, fg):
                            return ((ma - bu) / (ma - fg))
        
                        x2 = den_por(2.71, df["RHOB"], 0.02)  
                        data3 = {"Density Porosity": x2}
                        st.write(pd.DataFrame(data3))
        
                    else:  
                        def den_por(ma, bu, fl):
                            return ((ma - bu) / (ma - fl))
        
                        x3 = den_por(2.71, df["RHOB"], 1)  # You need to replace 1 with the correct value for fl (water value)
                        data4 = {"Density Porosity": x3}
                        st.write(pd.DataFrame(data4))
            
            
                b14=st.checkbox("Total Porosity using Neutron and Density Porosity")
                if b14:
                    b144 = st.radio("Select Zone Type", ["Gas_Bearing_Zone", "Oil_Water_Bearing_Zone"],key="select zone")
                    if b144 == "Gas_Bearing_Zone":
                        def den_por(ma, bu, fg):
                            return ((ma - bu) / (ma - fg))
        
                        x2 = den_por(2.71, df["RHOB"], 0.02)
                        total_por=np.sqrt(((df['NPHI']**2)+(x2**2))/2)
                        st.write(total_por.mean(),key="total")
        
                    else:
                        def den_por(ma, bu, fl):
                            return ((ma - bu) / (ma - fl))
        
                        x3 = den_por(2.71, df["RHOB"], 1)
                        total_por=((df['NPHI']+x3)/2)
                        st.write(total_por.mean(),key="top")
                    

            b15=st.checkbox("Visualisation")
            if b15:
                b16=st.checkbox('Histogram')
                if b16:
                    #st.set_option('deprecation.showPyplotGlobalUse', False)
                    selected_logs = st.multiselect("Select Logs for Histogram", modified_las.keys())
                    if selected_logs:
                        for log in selected_logs:
                            color_picker_key = f'COLOR PICK {log}'
                            c1 = st.color_picker("Choose color for Histogram", key=color_picker_key)
                            fig, ax = plt.subplots(figsize=(8, 6))  # Create a new figure and axis for each plot
                            ax.hist(modified_las[log], bins=50, color=c1, alpha=0.7,edgecolor='k')
                            ax.set_xlabel(log)
                            ax.set_ylabel("Frequency")
                            ax.set_title(f"Histogram for {log}")
                            st.pyplot(fig)  
                            # plt.figure(figsize=(8, 6))
                            # plt.hist(las_file[log], bins=50, color=c1, alpha=0.7)
                            # plt.xlabel(log)
                            # plt.ylabel("Frequency")
                            # plt.title(f"Histogram for {log}")
                            # st.pyplot()

                    else:
                        st.warning("Please select at least one log for the histogram.")

                 # selected_log = st.radio('Select log for histogram:', ['GR','RESS','RESD','NPHI','RHOB'],key="select log")
                    # if selected_log == "GR":
                    #     c1 = st.color_picker("Choose Color")
                    #     hist_values = df['GR']
                    #     hist , bins = np.histogram(hist_values, bins=30, range=(hist_values.min(), hist_values.max()))
                    #     fig, ax = plt.subplots()
                    #     ax.bar(bins[:-1], hist, width=(bins[1]-bins[0]), color=c1,edgecolor='k')
                    #     ax.set_xlabel('GR(API)')
                    #     ax.set_ylabel('Frequency')
                    #     st.pyplot(fig)
                    
                    
                    # elif selected_log == 'RESS':
                    #     c2 = st.color_picker("Choose Color")
                    #     hist_values1 = df['RESS']
                    #     hist , bins = np.histogram(hist_values1, bins=30, range=(hist_values1.min(), hist_values1.max()))
                    #     fig, ax = plt.subplots()
                    #     ax.bar(bins[:-1], hist, width=(bins[1]-bins[0]), color=c2,edgecolor='k')
                    #     ax.set_xlabel('RESS(Ohm-m)')
                    #     ax.set_ylabel('Frequency')
                    #     st.pyplot(fig)
                    
                    
                    # elif selected_log == 'RESD':
                    #     c3 = st.color_picker("Choose Color")
                    #     hist_values2 = df['RESD']
                    #     hist , bins = np.histogram(hist_values2, bins=30, range=(hist_values2.min(), hist_values2.max()))
                    #     fig, ax = plt.subplots()
                    #     ax.bar(bins[:-1], hist, width=(bins[1]-bins[0]), color=c3,edgecolor='k')
                    #     ax.set_xlabel('RESD(Ohm-m)')
                    #     ax.set_ylabel('Frequency')
                    #     st.pyplot(fig)
                    
                    
                    # elif selected_log == 'NPHI':
                    #     c4 = st.color_picker("Choose Color")
                    #     hist_values3 = df['NPHI']
                    #     hist , bins = np.histogram(hist_values3, bins=30, range=(hist_values3.min(), hist_values3.max()))
                    #     fig, ax = plt.subplots()
                    #     ax.bar(bins[:-1], hist, width=(bins[1]-bins[0]), color=c4,edgecolor='k')
                    #     ax.set_xlabel('NPHI')
                    #     ax.set_ylabel('Frequency')
                    #     st.pyplot(fig)
                    
                    
                    # else :
                    #     c5 = st.color_picker("Choose Color")
                    #     hist_values4 = df['RHOB']
                    #     hist , bins = np.histogram(hist_values4, bins=30, range=(hist_values4.min(), hist_values4.max()))
                    #     fig, ax = plt.subplots()
                    #     ax.bar(bins[:-1], hist, width=(bins[1]-bins[0]), color=c5,edgecolor='k')
                    #     ax.set_xlabel('RHOB')
                    #     ax.set_ylabel('Frequency')
                    #     st.pyplot(fig)
                
                
                
                b17=st.checkbox("line plot")
                if b17:
                    selected_logs = st.multiselect("Select Logs for line plot", modified_las.keys(),key='line plot selector')
                    if len(selected_logs) > 0:
                        columns1 = st.columns(len(selected_logs))
                        for i, log in enumerate(selected_logs):
                            color_picker_key = f'color_pick_{log}'  
                            c1 = columns1[i].color_picker(f"Choose color for {log} line plot", key=color_picker_key)
                            # fig=make_subplots(rows=1,cols=columns1)
                            # fig = px.line( x=modified_las[log], y=modified_las['DEPTH'])
                            # fig.update_layout(xaxis_title=log,yaxis_title="Depth")
                            # fig.update_yaxes(autorange="reversed")
                            # fig.update_traces(line_color=c1)
                            # st.plotly_chart(fig)
                            fig, ax = plt.subplots(figsize=(5,9))
                            ax.plot(modified_las[log], modified_las['DEPTH'], color=c1)
                            ax.set_ylim(modified_las['DEPTH'].max(), modified_las['DEPTH'].min())
                            ax.xaxis.set_label_position("top")
                            ax.xaxis.set_ticks_position("top")
                            ax.set_xlabel(log)
                            ax.set_ylabel("Depth")
                            ax.set_title(f"{log}")
                            columns1[i].pyplot(fig)
                    else:
                        st.write("logs are not selected")
                    
                    
         
                    b18=st.checkbox("Vsh plot")
                    if b18:
                        gr_values = df["GR"]
                        gr_5_percentile = gr_values.quantile(0.05)
                        gr_value=df["GR"]
                        gr_95=gr_value.quantile(.95)
                        def Vsh(GRmin,GRmax,GRlog):
                            return ((GRlog-GRmin)/(GRmax-GRmin))
                        x0=Vsh(gr_5_percentile,gr_95,df["GR"])
                        # vshly=0.083*(2**(3.7*x0)-1)
                        # vshlo=0.33*(2**(2*x0)-1)


                        c11=st.color_picker("choose color",key='vsh color') 
                    
                        fig,ax6=plt.subplots(figsize=(5,9))
                        ax6.plot(x0,modified_las["DEPTH"],color=c11) 
                        ax6.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                        ax6.xaxis.set_label_position("top")
                        ax6.xaxis.set_ticks_position("top")
                        ax6.set_xlabel('Volume of Shale')
                        ax6.set_ylabel('Depth')
                        st.pyplot(fig)
                    b19=st.checkbox("Sw using Archie equation")
                    if b19:
                        b81=st.number_input("pick a number for A value",key="b81")
                        if b81:
                            b91=st.number_input("pick a number for n value",key="b91")
                            if b91:
                                b101=st.number_input("pick a number for m value",key="b101")
                                if b101:
                                    b111=st.number_input("pick a number for Rw value",key="b111")
                                    if b111:
                                        def Sw(a,n,m,Rw,Rt,phi):
                                            return ((a*Rw)/((phi**m)*Rt))**(1/n)
                                        x11=Sw(b81,b91,b101,b111,df["RESD"],df["NPHI"])
                                        c12=st.color_picker("choose color",key='Sw color')
                                        fig,ax7=plt.subplots(figsize=(5,9))
                                        ax7.plot(x11,modified_las["DEPTH"],color=c12) 
                                        ax7.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                                        ax7.xaxis.set_label_position("top")
                                        ax7.xaxis.set_ticks_position("top")
                                        ax7.set_xlabel('Water Saturation by using Archie Equation')
                                        ax7.set_ylabel('Depth')
                                        ax7.grid()
                                        st.pyplot(fig)
                    b20=st.checkbox("Total porosity")
                    if b20:
                        b1444 = st.radio("Select Zone Type", ["Gas_Bearing_Zone", "Oil_Water_Bearing_Zone"],key="Zone type selector")
                        if b1444 == "Gas_Bearing_Zone":
                            def den_por(ma, bu, fg):
                                return ((ma - bu) / (ma - fg))
                            x22 = den_por(2.71, df["RHOB"], 0.02)
                            total_por=np.sqrt(((df['NPHI']**2)+(x22**2))/2)
                            c13=st.color_picker("choose color",key='gas porosity')
                            fig,ax8=plt.subplots(figsize=(5,9))
                            ax8.plot(total_por,modified_las["DEPTH"],color=c13) 
                            ax8.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                            ax8.xaxis.set_label_position("top")
                            ax8.xaxis.set_ticks_position("top")
                            ax8.set_xlabel('Total Porosity for Gas Bearing Zone')
                            ax8.set_ylabel('Depth')
                            ax8.grid()
                            st.pyplot(fig)
                        else:
                            def den_por(ma, bu, fl):
                                return ((ma - bu) / (ma - fl))
                            x33 = den_por(2.71, df["RHOB"], 1)
                            total_por1=((df['NPHI']+x33)/2)
                            c14=st.color_picker("choose color",key="water porosity")
                            fig,ax9=plt.subplots(figsize=(5,9))
                            ax9.plot(total_por1,modified_las["DEPTH"],color=c14) 
                            ax9.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                            ax9.xaxis.set_label_position("top")
                            ax9.xaxis.set_ticks_position("top")
                            ax9.set_xlabel('Total Porosity for oil/water Bearing Zone')
                            ax9.set_ylabel('Depth')
                            ax9.grid()
                            st.pyplot(fig)
                    b21= st.checkbox("Triple combo log")
                    if b21:
                        fig,((ax1,ax2,ax3),(ax4,ax5, _))=plt.subplots(2,3,figsize=(15,9))
                        plt.subplots_adjust(wspace=.2)
                        c15=st.color_picker("choose  Rt color",key='Rt color')
                        c16=st.color_picker("choose  RX0 color",key='Rxo color')
                        c17=st.color_picker("choose  GR color",key='GR color')
                        c18=st.color_picker("choose  Density color",key='density color')
                        c19=st.color_picker("choose  neutron porosity color",key='porosity color')
                        ax1=plt.subplot2grid((1,3),(0,0),rowspan=1,colspan=1)
                        ax2=plt.subplot2grid((1,3),(0,1),rowspan=1,colspan=1)
                        ax3=ax2.twiny()
                        ax4=plt.subplot2grid((1,3),(0,2),rowspan=1,colspan=1)
                        ax5=ax4.twiny()


                        ax3.plot(df["RESD"],modified_las['DEPTH'],color=c15)
                        ax3.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                        ax3.semilogx()
                        ax3.xaxis.set_label_position("top")
                        ax3.xaxis.set_ticks_position("top")
                        ax3.set_xlabel("Rt(Ohm-m)",color="red",fontsize=20)
                        ax3.grid()

                        ax2.plot(df['RESS'],modified_las['DEPTH'],color=c16)
                        ax2.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                        ax2.semilogx()
                        ax2.xaxis.set_label_position("top")
                        ax2.xaxis.set_ticks_position("top")
                        ax2.set_xlabel("Rxo(Ohm-m)",color="blue",fontsize=20)
                        ax2.spines["top"].set_position(("axes",1.1))
                        ax2.grid()

                        ax1.plot(df['GR'],modified_las['DEPTH'],color=c17)
                        ax1.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                        ax1.xaxis.set_label_position("top")
                        ax1.xaxis.set_ticks_position("top")
                        ax1.set_xlabel("Gammaray(API)",color="red",fontsize=20)
                        #ax1.fill_betweenx(data.DEPTH,0,data.GR,facecolor="yellow")
                        ax1.grid()

                        ax4.plot(df['RHOB'],modified_las['DEPTH'],color=c18)
                        ax4.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                        ax4.xaxis.set_label_position("top")
                        ax4.xaxis.set_ticks_position("top")
                        ax4.set_xlabel("Density(g/cc)",color="red",fontsize=20)
                        ax4.grid()

                        ax5.plot(df['NPHI'],modified_las['DEPTH'],color=c19)
                        ax5.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                        ax5.invert_xaxis()
                        ax5.xaxis.set_label_position("top")
                        ax5.xaxis.set_ticks_position("top")
                        ax5.set_xlabel("Neutron Porosity",color="blue",fontsize=20)
                        ax5.spines["top"].set_position(("axes",1.1))
                        ax5.grid()
                        st.pyplot(fig)
                
                    b22=st.checkbox("reservoir flag rise")
                    if b22:
                        gr_values = df["GR"]
                        gr_5_percentile = gr_values.quantile(0.05)
                        gr_value=df["GR"]
                        gr_95=gr_value.quantile(.95)
                        def Vsh(GRmin,GRmax,GRlog):
                            return ((GRlog-GRmin)/(GRmax-GRmin))
                        x0=Vsh(gr_5_percentile,gr_95,df["GR"])
                        b811=st.number_input("pick a number for A value for Sw calculation",key="b811")
                        if b811:
                            b911=st.number_input("pick a number for n value for Sw calculation",key="b911")
                            if b911:
                                b1011=st.number_input("pick a number for m value for Sw calculation",key="b1011")
                                if b1011:
                                    b1111=st.number_input("pick a number for Rw value for Sw calculation",key="b1111")
                                    if b1111:
                                        def Sw(a,n,m,Rw,Rt,phi):
                                            return ((a*Rw)/((phi**m)*Rt))**(1/n)
                                        x111=Sw(b811,b911,b1011,b1111,df["RESD"],df["NPHI"])
                                        b41=st.number_input("pick a number for porosity cutoff in fraction ",key="b41")
                                        if b41:
                                            b51=st.number_input("pick a number for water saturation cut off in fraction",key="b51")
                                            if b51:
                                                b61=st.number_input("pick a number for Vsh cutoff in fraction",key="b61")
                                                if b61:

                                                    CONDITION_MET = ((modified_las['NPHI'] > b41) & (x111 < b51) & (x0<b61)).astype(int)
                                                    fig = px.line( x=CONDITION_MET, y=modified_las['DEPTH'])
                                                    fig.update_yaxes(autorange="reversed")
                                                    st.plotly_chart(fig)
                                                    st.markdown("please see the step size in the well information section")
                                                    f1=st.number_input("pick step size value",key="step value")
                                        
                                                    if f1:
                                                        net_pay=np.sum(CONDITION_MET*f1)
                                                        st.write("net_pay: " + str(net_pay),key="netpay")
                                                        depth_start = st.slider("Select starting depth", min_value=modified_las['DEPTH'].min(), max_value=modified_las['DEPTH'].max())
                                                        depth_end = st.slider("Select ending depth", min_value=depth_start, max_value=modified_las['DEPTH'].max())
                                                        gross=depth_end-depth_start
                                                        ntg=net_pay/gross
                                                        st.write("NTG: " + str(ntg),key="ntg")






                b71=st.checkbox("Cross plot")
                if b71:
                    xaxis_log = st.selectbox("X-axis Log for Cross Plot", modified_las.keys() ,key='xaxis_selector')
                    yaxis_log = st.selectbox("Y-axis Log for Cross Plot", modified_las.keys(), key='yaxis_selector')
                    if xaxis_log and yaxis_log:
                        c101=st.color_picker("choose color for cross plot",key="c101")
                        xaxis_label = f"X-axis: {xaxis_log}"
                        yaxis_label = f"Y-axis: {yaxis_log}"
                        fig = px.scatter(x=modified_las[xaxis_log], y=modified_las[yaxis_log],color_discrete_sequence=[c101])
                        fig.update_layout(xaxis_title=xaxis_label, yaxis_title=yaxis_label)
                        st.plotly_chart(fig)
                    else:
                        st.write("Please select logs for both X-axis and Y-axis.")





                    #     fig = px.scatter(x=modified_las[xaxis_log], y=modified_las[yaxis_log], labels={xaxis_log: "X-axis", yaxis_log: "Y-axis"})
                    #     st.plotly_chart(fig)
                    # else:
                    #     st.write("Please select logs for both X-axis and Y-axis.")
                   

                        
                        
                        
                        
                        
                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        

























                    # selected_log1 = st.radio('Select log for line plot:', ['GR','RESS','RESD','NPHI','RHOB','Vsh','Sw','Total_por','triple_combo'],key='select log for line plot')
                    # if selected_log1=='GR':
                    #     c6=st.color_picker("choose color")
                    #     fig,ax1=plt.subplots(figsize=(5,9))
                    #     #plt.subplots_adjust(wspace=0.3)
                    #     #ax1=plt.subplot2grid((1,1),(0,0),rowspan=1,colspan=1)
                    #     ax1.plot(df["GR"],modified_las["DEPTH"],color=c6) 
                    #     ax1.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                    #     ax1.xaxis.set_label_position("top")
                    #     ax1.xaxis.set_ticks_position("top")
                    #     ax1.set_xlabel('GR(API)')
                    #     ax1.set_ylabel('Depth')
                    #     ax1.grid()
                    #     st.pyplot(fig)
                    
                    
                    
                    # elif selected_log1=='RESS':
                    #     c7=st.color_picker("choose color")
                    #     fig,ax2=plt.subplots(figsize=(5,9))
                    #     #plt.subplots_adjust(wspace=0.3)
                    #     #ax1=plt.subplot2grid((1,1),(0,0),rowspan=1,colspan=1)
                    #     ax2.plot(df["RESS"],modified_las["DEPTH"],color=c7) 
                    #     ax2.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                    #     ax2.xaxis.set_label_position("top")
                    #     ax2.xaxis.set_ticks_position("top")
                    #     ax2.semilogx()
                    #     ax2.set_xlabel('RESS(OHM-M)')
                    #     ax2.set_ylabel('Depth')
                    #     ax2.grid()
                    #     st.pyplot(fig)
                    
                    
                    
                    # elif selected_log1=='RESD':
                    #     c8=st.color_picker("choose color")
                    #     fig,ax3=plt.subplots(figsize=(5,9))
                    #     #plt.subplots_adjust(wspace=0.3)
                    #     #ax1=plt.subplot2grid((1,1),(0,0),rowspan=1,colspan=1)
                    #     ax3.plot(df["RESD"],modified_las["DEPTH"],color=c8) 
                    #     ax3.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                    #     ax3.xaxis.set_label_position("top")
                    #     ax3.xaxis.set_ticks_position("top")
                    #     ax3.semilogx()
                    #     ax3.set_xlabel('RESD(OHM-M)')
                    #     ax3.set_ylabel('Depth')
                    #     ax3.grid()
                    #     st.pyplot(fig)


                    # elif selected_log1=='NPHI':
                    #     c9=st.color_picker("choose color")
                    #     fig,ax4=plt.subplots(figsize=(5,9))
                    #     #plt.subplots_adjust(wspace=0.3)
                    #     #ax1=plt.subplot2grid((1,1),(0,0),rowspan=1,colspan=1)
                    #     ax4.plot(df["NPHI"],modified_las["DEPTH"],color=c9) 
                    #     ax4.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                    #     ax4.xaxis.set_label_position("top")
                    #     ax4.xaxis.set_ticks_position("top")
                    #     ax4.set_xlabel('NPHI')
                    #     ax4.set_ylabel('Depth')
                    #     ax4.grid()
                    #     st.pyplot(fig)

                    # elif selected_log1=='RHOB':
                    #     c10=st.color_picker("choose color")
                    #     fig,ax5=plt.subplots(figsize=(5,9))
                    #     #plt.subplots_adjust(wspace=0.3)
                    #     #ax1=plt.subplot2grid((1,1),(0,0),rowspan=1,colspan=1)
                    #     ax5.plot(df["RHOB"],modified_las["DEPTH"],color=c10) 
                    #     ax5.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                    #     ax5.xaxis.set_label_position("top")
                    #     ax5.xaxis.set_ticks_position("top")
                    #     ax5.set_xlabel('RHOB(g/cc)')
                    #     ax5.set_ylabel('Depth')
                    #     ax5.grid()
                    #     st.pyplot(fig)



                    #elif selected_log1=='Vsh':
                    #     gr_values = df["GR"]
                    #     gr_5_percentile = gr_values.quantile(0.05)
                    #     gr_value=df["GR"]
                    #     gr_95=gr_value.quantile(.95)
                    #     def Vsh(GRmin,GRmax,GRlog):
                    #         return ((GRlog-GRmin)/(GRmax-GRmin))
                    #     x0=Vsh(gr_5_percentile,gr_95,df["GR"])
                    # #st.write(pd.DataFrame(x))
                    #     c11=st.color_picker("choose color") 
                    # #fig,ax = plt.subplots()
                    #     fig,ax6=plt.subplots(figsize=(5,9))
                    # #plt.subplots_adjust(wspace=0.3)
                    # #ax1=plt.subplot2grid((1,1),(0,0),rowspan=1,colspan=1)
                    #     ax6.plot(x0,modified_las["DEPTH"],color=c11) 
                    #     ax6.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                    #     ax6.xaxis.set_label_position("top")
                    #     ax6.xaxis.set_ticks_position("top")
                    #     ax6.set_xlabel('Volume of Shale')
                    #     ax6.set_ylabel('Depth')
                    #     st.pyplot(fig)

                    # elif selected_log1=='Sw':
                    #     b81=st.number_input("pick a number for a value",key="b81")
                    #     if b81:
                    #         b91=st.number_input("pick a number for n value",key="b91")
                    #         if b91:
                    #             b101=st.number_input("pick a number for m value",key="b101")
                    #             if b101:
                    #                 b111=st.number_input("pick a number for Rw value",key="b111")
                    #                 if b111:
                    #                     def Sw(a,n,m,Rw,Rt,phi):
                    #                         return ((a*Rw)/((phi**m)*Rt))**(1/n)
                    #                     x11=Sw(b81,b91,b101,b111,df["RESD"],df["NPHI"])
                    #                     c12=st.color_picker("choose color")
                    #                     fig,ax7=plt.subplots(figsize=(5,9))
                    #                     ax7.plot(x11,modified_las["DEPTH"],color=c12) 
                    #                     ax7.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                    #                     ax7.xaxis.set_label_position("top")
                    #                     ax7.xaxis.set_ticks_position("top")
                    #                     ax7.set_xlabel('Water Saturation by using Archie Equation')
                    #                     ax7.set_ylabel('Depth')
                    #                     ax7.grid()
                    #                     st.pyplot(fig)


                    # elif selected_log1 =='Total_por':
                    #     b1444 = st.radio("Select Zone Type", ["Gas_Bearing_Zone", "Oil_Water_Bearing_Zone"],key="Zone type selector")
                    #     if b1444 == "Gas_Bearing_Zone":
                    #         def den_por(ma, bu, fg):
                    #             return ((ma - bu) / (ma - fg))
                    #         x22 = den_por(2.71, df["RHOB"], 0.02)
                    #         total_por=np.sqrt(((df['NPHI']**2)+(x22**2))/2)
                    #         c13=st.color_picker("choose color")
                    #         fig,ax8=plt.subplots(figsize=(5,9))
                    #         ax8.plot(total_por,modified_las["DEPTH"],color=c13) 
                    #         ax8.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                    #         ax8.xaxis.set_label_position("top")
                    #         ax8.xaxis.set_ticks_position("top")
                    #         ax8.set_xlabel('Total Porosity for Gas Bearing Zone')
                    #         ax8.set_ylabel('Depth')
                    #         ax8.grid()
                    #         st.pyplot(fig)

                        
                    #     else:
                    #         def den_por(ma, bu, fl):
                    #             return ((ma - bu) / (ma - fl))
                    #         x33 = den_por(2.71, df["RHOB"], 1)
                    #         total_por1=((df['NPHI']+x33)/2)
                    #         c14=st.color_picker("choose color")
                    #         fig,ax9=plt.subplots(figsize=(5,9))
                    #         ax9.plot(total_por1,modified_las["DEPTH"],color=c14) 
                    #         ax9.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                    #         ax9.xaxis.set_label_position("top")
                    #         ax9.xaxis.set_ticks_position("top")
                    #         ax9.set_xlabel('Total Porosity for oil/water Bearing Zone')
                    #         ax9.set_ylabel('Depth')
                    #         ax9.grid()
                    #         st.pyplot(fig)
                    # else:
                    #     fig,((ax1,ax2,ax3),(ax4,ax5, _))=plt.subplots(2,3,figsize=(15,9))
                    #     plt.subplots_adjust(wspace=.2)
                    #     c15=st.color_picker("choose  Rt color")
                    #     c16=st.color_picker("choose  RX0 color")
                    #     c17=st.color_picker("choose  GR color")
                    #     c18=st.color_picker("choose  Density color")
                    #     c19=st.color_picker("choose  neutron porosity color")
                    #     ax1=plt.subplot2grid((1,3),(0,0),rowspan=1,colspan=1)
                    #     ax2=plt.subplot2grid((1,3),(0,1),rowspan=1,colspan=1)
                    #     ax3=ax2.twiny()
                    #     ax4=plt.subplot2grid((1,3),(0,2),rowspan=1,colspan=1)
                    #     ax5=ax4.twiny()


                    #     ax3.plot(df["RESD"],modified_las['DEPTH'],color=c15)
                    #     ax3.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                    #     ax3.semilogx()
                    #     ax3.xaxis.set_label_position("top")
                    #     ax3.xaxis.set_ticks_position("top")
                    #     ax3.set_xlabel("Rt(Ohm-m)",color="red",fontsize=20)
                    #     ax3.grid()

                    #     ax2.plot(df['RESS'],modified_las['DEPTH'],color=c16)
                    #     ax2.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                    #     ax2.semilogx()
                    #     ax2.xaxis.set_label_position("top")
                    #     ax2.xaxis.set_ticks_position("top")
                    #     ax2.set_xlabel("Rxo(Ohm-m)",color="blue",fontsize=20)
                    #     ax2.spines["top"].set_position(("axes",1.1))
                    #     ax2.grid()

                    #     ax1.plot(df['GR'],modified_las['DEPTH'],color=c17)
                    #     ax1.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                    #     ax1.xaxis.set_label_position("top")
                    #     ax1.xaxis.set_ticks_position("top")
                    #     ax1.set_xlabel("Gammaray(API)",color="red",fontsize=20)
                    #     #ax1.fill_betweenx(data.DEPTH,0,data.GR,facecolor="yellow")
                    #     ax1.grid()

                    #     ax4.plot(df['RHOB'],modified_las['DEPTH'],color=c18)
                    #     ax4.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                    #     ax4.xaxis.set_label_position("top")
                    #     ax4.xaxis.set_ticks_position("top")
                    #     ax4.set_xlabel("Density(g/cc)",color="red",fontsize=20)
                    #     ax4.grid()

                    #     ax5.plot(df['NPHI'],modified_las['DEPTH'],color=c19)
                    #     ax5.set_ylim(modified_las['DEPTH'].max(),modified_las['DEPTH'].min())
                    #     ax5.invert_xaxis()
                    #     ax5.xaxis.set_label_position("top")
                    #     ax5.xaxis.set_ticks_position("top")
                    #     ax5.set_xlabel("Neutron Porosity",color="blue",fontsize=20)
                    #     ax5.spines["top"].set_position(("axes",1.1))
                    #     ax5.grid()
                    #     st.pyplot(fig)

                        


                    

                    

        



                    
                






