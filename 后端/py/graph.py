import json
import random
from mysql_util import MysqlUtil
from pyecharts.globals import CurrentConfig, NotebookType
import json
from pyecharts import options as opts
from pyecharts.charts import Graph, Timeline

def graph(title,ll):
    if ll == "force":
        ll = "force"
    else:
        ll="circular"

    sql_3 = f'SELECT * FROM weiboforword where title="{title}" ORDER BY `publish_time`'
    db = MysqlUtil()
    count_number = db.fetchall(sql_3)
    kk=[]
    for row in count_number:
        if row["source"] not in kk:
            kk.append(row["source"])
        if row["target"] not in kk:
            kk.append(row["target"])
    dict_name={}
    dict_name_fan={}
    id=1
    for i in range(len(kk)):
        dict_name[kk[i]]=id
        id=id+1
    id=1
    for i in range(len(kk)):
        dict_name_fan[id]=kk[i]
        id=id+1

    jsontext = {"categories":[],"nodes":[],"links":[]}
    jsontext["categories"]=[{'name': '类目0'},{'name': '类目1'},{'name': '类目2'},{'name': '类目3'},{'name': '类目4'},{'name': '类目5'},{'name': '类目6'},{'name': '类目7'},{'name': '类目8'}]
    for row in kk:
        id=id-1
        jsontext["nodes"].append({'id': dict_name[row],
      'name': row,
      'symbolSize': 15,
      'label': {'normal': {'show': True}},
      'category': random.randint(0,8)})
        id=id+1
    for row in count_number:
        jsontext["links"].append({'source': dict_name[row['source']], 'target': dict_name[row['target']] ,'time':row['publish_time'].strftime("%Y-%m-%d %H:%M:%S")})
        id=id+1
    jsontext=json.dumps(jsontext)
    file = open(title+'.json', 'w')
    file.write(jsontext)
    file.close()
    tl = Timeline(init_opts=opts.InitOpts(width="1500px", height="900px"))
    with open(title+'.json', "r", encoding="utf-8") as f:
        j = json.load(f)
        nodes = j["nodes"]
        categories = j["categories"]

    for i in range(len(j['links'])):
        tt=i
        links=j["links"][0:i]
        list_links=[]
        for i in range(len(links)):
            list_links.append(dict_name_fan[links[i]["source"]])
            list_links.append(dict_name_fan[links[i]["target"]])
        list_nodes=[]
        for i in range(len(j["nodes"])):
            if j["nodes"][i]["name"] in list_links:
                list_nodes.append(j["nodes"][i])

        i=i+1
        c = (
        Graph(init_opts=opts.InitOpts(width="1700px", height="1000px"))
        .add(
            "",
            nodes=list_nodes,
            links=links,
            categories=categories,
            layout=ll,
            is_rotate_label=True,
            linestyle_opts=opts.LineStyleOpts(color="source", curve=0.3),
            label_opts=opts.LabelOpts(position="right"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title+"关系弦图"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%"),
        )
        )
        tl.add(c, "{}".format(j["links"][tt]['time']))
        tl.add_schema(
        play_interval=400,      # 自动播放的时间间隔，单位毫秒
        is_timeline_show=True,   # 是否显示自动播放的时候，显示时间线（默认 True）
        is_auto_play=True,       # 是否在自动播放（默认 False）
        is_loop_play=True        # 是否循环自动播放（默认 True）
        )

    return tl
