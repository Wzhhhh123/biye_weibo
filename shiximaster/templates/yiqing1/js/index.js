var seclectPro="";
var city;
var data;
window.onload=function ()
{
    var proArr=new Array("北京", "天津", "上海", "重庆", "福建", "西藏", "贵州", "湖北", "湖南", "广东", "安徽",
        "四川", "新疆", "江苏", "吉林", "宁夏", "河北", "河南", "广西", "海南", "江西", "云南",
        "甘肃", "山东", "陕西", "浙江", "内蒙古", "青海", "辽宁", "黑龙江", "山西", "台湾", "澳门",
        "香港");
    var arr =new Array();
    arr[0]="丰台,海淀,西城,房山,东城,大兴,通州,顺义,昌平,密云,怀柔,石景山,延庆,门头沟,平谷区";//
    arr[1]="西青区,武清区,滨海新区,河北区,南开区,红桥区,东丽区,津南区,河西区,北辰区,河东区,静海区,宝坻区,宁河区,蓟州区,和平区,";//
    arr[2]="浦东,闵行,徐汇,黄埔,虹口,静安,宝山,杨浦,长宁,普陀,松江,青浦,嘉定,崇明,奉贤,金山";//
    arr[3]="彭水县,巫山县,榆中区,长寿区,沙坪坝区,九龙坡区,荣昌区,丰都县,铜梁区,綦江区,潼南区,垫江县,万州区,奉节县,石柱县,合川区,酉阳县,城口县,黔江区,高新区,秀山县,两江新区,万盛经开区,璧山区,开州区,巫溪县,大渡口区,忠县,武隆区,梁平区,江津区,渝北区,巴南区,永川区,南岸区,涪陵区,大足区,江北区,南川区,北碚区,云阳县";//
    arr[4]="福州,厦门,莆田,三明,泉州,漳州,南平,龙岩,宁德";//
    arr[5]="拉萨,昌都,山南,日喀则,那曲,阿里地区,林芝";//
    arr[6]="贵阳,六盘水,遵义,安顺,铜仁,黔西南州,毕节,黔东南州,黔南州";//
    arr[7]="武汉,黄石,十堰,宜昌,襄阳,襄樊,鄂州,荆门,孝感,荆州,黄冈,咸宁,随州,恩施州,仙桃,潜江,天门,神农架";//
    arr[8]="长沙,株洲,湘潭,衡阳,邵阳,岳阳,常德,张家界,益阳,郴州,永州,怀化,娄底,湘西自治州";//
    arr[9]="广州,韶关,深圳,珠海,汕头,佛山,江门,湛江,茂名,肇庆,惠州,梅州,汕尾,河源,阳江,清远,东莞,中山,潮州,揭阳,云浮";//
    arr[10]="合肥,芜湖,蚌埠,淮南,马鞍山,淮北,铜陵,安庆,黄山,滁州,阜阳,宿州,巢湖,六安,亳州,池州,宣城";//
    arr[11]="成都,自贡,攀枝花,泸州,德阳,绵阳,广元,凉山,甘孜,遂宁,内江,乐山,南充,眉山,宜宾,广安,达州,雅安,巴中,资阳,阿坝";//
    arr[12]="乌鲁木齐,克拉玛依,吐鲁番,哈密,昌吉州,博尔塔拉州,哈萨克自治州,巴音郭楞州,阿克苏,克孜州,喀什,和田,伊犁州,塔城,阿勒泰,第八师石河子,兵团第十二师,兵团第九师,兵团第四师,第七师,六师五家渠";//
    arr[13]="南京,无锡,徐州,常州,苏州,南通,连云港,淮安,盐城,扬州,镇江,泰州,宿迁";//
    arr[14]="长春,吉林,四平,辽源,通化,白山,松原,白城,延边,梅河口市,公主岭";//
    arr[15]="银川,石嘴山,吴忠,固原,中卫";//
    arr[16]="石家庄,唐山,秦皇岛,邯郸,邢台,雄安新区,定州,辛集市,保定,张家口,承德,衡水,廊坊,沧州";//
    arr[17]="郑州,开封,洛阳,平顶山,安阳,鹤壁,新乡,焦作,濮阳,许昌,漯河,三门峡,南阳,商丘,信阳,周口,驻马店,济源";//
    arr[18]="南宁,柳州,桂林,梧州,北海,防城港,钦州,贵港,玉林,百色,贺州,河池,来宾,崇左";//
    arr[19]="海口,三亚,五指山,琼海,儋州,文昌,万宁,东方,定安县,澄迈县,临高县,昌江县,乐东,陵水县,保亭,琼中县,三沙";//
    arr[20]="南昌,景德镇,萍乡,九江,新余,鹰潭,赣州,吉安,宜春,抚州,上饶,赣江新区";//
    arr[21]="昆明,红河,曲靖,普洱,玉溪,保山市,昭通市,丽江市,临沧,楚雄州,文山州,西双版纳州,大理,德宏州,怒江州,迪庆州";//
    arr[22]="兰州,嘉峪关,金昌,白银,天水,武威,张掖,平凉,酒泉,庆阳,定西,陇南,临夏,甘南州";//
    arr[23]="济南,青岛,淄博,枣庄,东营,烟台,潍坊,济宁,泰安,威海,日照,莱芜,临沂,德州,聊城,滨州,菏泽";//
    arr[24]="西安,铜川,宝鸡,咸阳,渭南,延安,汉中,榆林,安康,商洛,韩城,杨凌";//
    arr[25]="杭州,宁波,温州,嘉兴,湖州,绍兴,舟山,衢州,金华,台州,丽水";//
    arr[26]="呼和浩特,包头,乌海,赤峰,通辽,鄂尔多斯,呼伦贝尔,巴彦淖尔,乌兰察布,兴安盟,锡林郭勒,阿拉善盟";//
    arr[27]="西宁,海东,海北州,黄南州,海南州,果洛州,玉树州,海西州";//
    arr[28]="沈阳,大连,鞍山,抚顺,本溪,丹东,锦州,营口,阜新,辽阳,盘锦,铁岭,朝阳市,葫芦岛";//
    arr[29]="哈尔滨,齐齐哈尔,鸡西,鹤岗,双鸭山,大庆,伊春,佳木斯,七台河,牡丹江,黑河,绥化,大兴安岭";//
    arr[30]="太原,大同,阳泉,长治,晋城,朔州,晋中,运城,忻州,临汾,吕梁";//
    arr[31]=",";//
    arr[32]=",";//
    arr[33]=",";//

    city=document.getElementById("city");//获取对象
    var province=document.getElementById("province");
    var result=document.getElementById("result");
    var cityArr=arr[0].split(",");
    initCity(0);
    getData();
    function initCity(index)//初始化
    {
        var cityArr=arr[index].split(",");//以“，”化为字符数组
        for(var i=0;i<cityArr.length;i++)
        {
            city[i]=new Option(cityArr[i],cityArr[i]);
        }
        seclectPro=proArr[province.value];
        result.innerHTML=seclectPro+"省"+cityArr[0]+"市";
    }
    province.onchange=function ()
    {
        var index=province.selectedIndex;
        //将城市数组中的值填充到城市下拉列表框中
        initCity(index);
    }
    city.onchange=function ()
    {
        result.innerHTML=seclectPro+"省"+city.value+"市";
    }
}
function getData() {
    $.ajax({
        url: 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=statisGradeCityDetail,diseaseh5Shelf',
        data: { },
        dataType: 'json',
        success: function (res) {
            data = res.data;
        }
    });
    $.ajax({
        type: 'post',
        url: 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list',
        data: {
            modules: 'chinaDayList,chinaDayAddList,nowConfirmStatis,provinceCompare'
        },
        dataType: 'json',
        success: function (res) {
            //console.log(res);
            var data = res.data;
            //console.log(res.data);
            left2(data);//全国新增趋势
        }
    });
}

function myClick()
{
    var myDisplay=document.getElementById("display");
    var myLI=document.getElementsByTagName("li");
    var py=["不宜出行","不宜出行","无必要不出行","出行注意安全，不去密集场所","可以出行，出行请佩戴带好口罩","放心出行，出行请佩戴好口罩",];
    var provinces = data.diseaseh5Shelf.areaTree[0].children;
    var i=0,j=0;
    var cities;
    for (var province of provinces) {
        if(seclectPro==province.name) {
            cities=province.children;
            break;
        }
    }
    for(var c of cities)
    {
        if(city.value==c.name) {
            i=c.today.confirm//该市新增确诊
            j=c.total.nowConfirm//该市现有确诊
            break;
        }
    }
    var index;
    var re=i*0.6+j*0.4;
    //i:该市新增确诊人数，j:该市（区）获新冠人数
    if(re==0)index=5;
    else if(re>0&&re<=2)index=4;
    else if(re>2&&re<=5)index=3;
    else if(re>5&&re<=10)index=2;
    else if(re>10&&re<=18)index=1;
    else index=0;
     for(var k=0;k<index;k++)
         myLI[k].className="active";
     for(var k=index;k<5;k++)
         myLI[k].className="";

     myDisplay.innerHTML="<br>"+"出行安全指数："+index+ "，评语："+py[index]+"<br></br>"+"该市（区）新增确诊人数:"+i+ ",该市（区）现有确诊人数:"+j;
}

function left2(data) {
    var myChart = echarts.init($('#left2')[0], 'dark');
    var option = {
        title: {
            text: "全国新增趋势",
            textStyle: {
                color: "#000",
            },
            left: 'left',
        },
        tooltip: {
            trigger: 'axis',
            //指示器
            axisPointer: {
                type: 'line',
                lineStyle: {
                    color: '#7171C6'
                }
            },
        },
        //图例
        legend: {
            data: ['新增确诊', '新增疑似', '新增境外输入'],
            left: "right"
        },
        //图形位置
        grid: {
            left: '4%',
            right: '6%',
            bottom: '4%',
            top: 50,
            containLabel: true
        },
        xAxis: [{
            type: 'category',
            data: [],
        }],
        yAxis: [{
            type: 'value',
            //y轴字体设置
            axisLabel: {
                show: true,
                color: '#000',

                fontSize: 12,
                formatter: function (value) {
                    if (value >= 1000) {
                        value = value / 1000 + 'k';
                    }
                    return value;
                }
            },
            //y轴线设置展示
            axisLine: {
                show: true
            },
            //与x轴平行的线样式
            splitLine: {
                show: true,
                lineStyle: {
                    color: '#17273B',
                    width: 1,
                    type: 'solid',
                }
            }
        }],
        series: [{
            name: "新增确诊",
            type: 'line',
            smooth: true,
            data: [],
        }, {
            name: "新增疑似",
            type: 'line',
            smooth: true,
            data: [],
        }, {
            name: "新增境外输入",
            type: 'line',
            smooth: true,
            data: [],
        }]
    };

    var chinaDayAddList = data.chinaDayAddList;
    for (var day of chinaDayAddList) {
        //console.log(day);
        option.xAxis[0].data.push(day.date);
        option.series[0].data.push(day.confirm);
        option.series[1].data.push(day.suspect);
        option.series[2].data.push(day.importedCase);
    }
    myChart.setOption(option);
}//全国新增趋势图