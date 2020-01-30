let geoJson = "";
let global_date_list = [];
let global_date_list_end = 0;
let global_json = [];
let global_china_dataset = [];
let load_done = false;

// ! 读取文件
read_china_json = $.ajax({
  async: true,
  global: true,
  url: "china.json",
  beforeSend: function() {},
  success: function(data) {
    geoJson = data;
  }
});
read_global_json = $.ajax({
  async: true,
  global: true,
  url: "history-areas.json",
  beforeSend: function() {},
  success: function(data) {
    global_china_dataset[0] = ["状态"].concat(data[0]["date"]);
    global_china_dataset[1] = ["确诊"].concat(data[0]["confirmedCount"]);
    global_china_dataset[2] = ["疑似"].concat(data[0]["suspectedCount"]);
    global_china_dataset[3] = ["治愈"].concat(data[0]["curedCount"]);
    global_china_dataset[4] = ["死亡"].concat(data[0]["deadCount"]);
    for (let index = 1; index < global_china_dataset[0].length; index++) {
      global_china_dataset[0][index] = global_china_dataset[0][index].slice(5);
    }
    global_date_list = data[1].reverse();
    global_date_list_end = global_date_list.length - 1;
    global_json = data.slice(2);
    for (let index = 0; index < global_date_list.length; index++) {
      global_date_list[index] = global_date_list[index].slice(5);
    }
    load_done = true;
  }
});
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ! 画中国地图
let chinaChart;
function set_chinaChart_dom(id) {
  chinaChart = echarts.init(document.getElementById(id));
  chinaChart.showLoading();
  // * 开启地图的点击事件，当点击具体省份时。绘制对应省份的地图
  chinaChart.on("click", e => {
    chinaMapClick(e);
    event.stopPropagation();
  });
}
chinaChart = echarts.init(document.getElementById("chinaChart"));
let option_chinaChart = "";
let province_dataset = new Array();
function init_chinaChart() {
  // * read_china_json请求完毕时执行
  $.when(read_china_json).done(function() {
    echarts.registerMap("china", geoJson);
    $.when(read_global_json).done(async function() {
      while (load_done == false) {
        await sleep(30);
      }
      set_option_chinaChart();
      for (let index = 0; index < global_json.length; index++) {
        province_dataset[index] = {
          name: global_json[index]["provinceShortName"],
          value: global_json[index]["confirmedCount"][global_date_list_end]
        };
      }
      // * 开始画其它图
      init_provincePie("中国");
      init_populationChart("中国", "中国");
      option_chinaChart["series"][0]["data"] = province_dataset;
      chinaChart.hideLoading();
      chinaChart.setOption(option_chinaChart);
    });
  });
}
function set_option_chinaChart() {
  option_chinaChart = {
    // top: -50,
    roam: isMobile ? true : false,
    layoutCenter: ["50%", "50%"],
    layoutSize: "120%",
    // zoom: 2,
    // aspectScale: 1.5,
    // scaleLimit: [1, 1.5],
    title: {
      text: isMobile
        ? "确诊和疑似共 " +
          String(
            global_china_dataset[1][global_china_dataset[1].length - 1] +
              global_china_dataset[2][global_china_dataset[2].length - 1]
          ) +
          " 人"
        : "2019-nCoV 各省市数据" +
          "\n\n确诊和疑似共 " +
          String(
            global_china_dataset[1][global_china_dataset[1].length - 1] +
              global_china_dataset[2][global_china_dataset[2].length - 1]
          ) +
          " 人" +
          "\n\n随处点点吧",
      top: "1%",
      left: "center",
      textStyle: { color: "#aa2222" }
      // textAlign: 'center'
    },
    tooltip: {
      trigger: "item",
      formatter: "{b}<br/>确诊 {c} 人"
    },
    toolbox: {
      show: true,
      orient: "vertical",
      left: "right",
      top: "bottom",
      itemSize: isMobile ? 20 : 15,
      feature: {
        saveAsImage: { type: "jpeg", pixelRatio: 4 }
      }
    },
    visualMap: {
      type: "piecewise",
      pieces: [
        // { gt: 5000, label: ">5000", color: "#770000" },
        // { gt: 2000, label: ">2001", color: "#770000" },
        // { gt: 1000, lt: 2000, label: "1001~2000", color: "#9C0000" },
        { gt: 500, label: ">500", color: "#C00000" },
        { gt: 200, lt: 500, label: "201~500", color: "#E80000" },
        // { gt: 100, lt: 200, label: "101~200", color: "#FF4040" },
        { gt: 100, lt: 200, label: "101~200", color: "#FF8080" },
        // { gt: 10, lt: 50, label: "11~50", color: "#FFBBBB" },
        { gt: 0, lt: 100, label: "1~100", color: "#FFBBBB" },
        { value: 0, label: "无", color: "#FFFFFF" }
      ],
      align: "auto",
      itemHeight: isMobile ? 10 : 20,
      itemWidth: isMobile ? 10 : 20,
      itemGap: isMobile ? 3 : 5,
      itemSymbol: "roundRect",
      align: isMobile ? "right" : "left",
      // orient: "horizontal",
      top: isMobile ? "45%" : "middle",
      left: isMobile ? "right" : "5%",
      borderColor: "#FF0000",
      borderWidth: isMobile ? 0 : 1,
      selectedMode: false,
      textStyle: { fontSize: 14 }
    },
    series: [
      {
        name: "全国各省市感染人数",
        type: "map",
        mapType: "china", // * 自定义扩展图表类型
        label: {
          show: true,
          fontSize: isMobile ? 10 : 12
        }
      }
    ],
    graphic: {
      elements: [
        {
          type: "text",
          invisible: isMobile ? false : true,
          left: "5%",
          bottom: "2%",
          slient: true,
          style: {
            text: "点击图中『省份』或『空白』联动下图",
            font: isMobile
              ? '12px "cursive", sans-serif'
              : '14px "cursive", sans-serif',
            fill: "#8888FF"
          }
        }
      ]
    }
  };
}
function chinaMapClick(params) {
  if (params.value == null) {
    return;
  }
  let provinceName = params.data.name;
  if (provinceName == "") {
    provinceName = "中国";
  }
  init_provincePie(provinceName);
  init_populationChart(provinceName, provinceName);
}
if (isMobile) {
  tap(chinaChart_bg, function(e) {
    init_provincePie("中国");
    init_populationChart("中国", "中国");
  });
} else {
  chinaChart_bg.addEventListener(
    "click",
    function(e) {
      if (e) {
        init_provincePie("中国");
        init_populationChart("中国", "中国");
      }
    },
    false
  );
}
// ! 移动端点击事件
function tap(el, callBack) {
  let startTime = 0;
  let maxTime = 250;
  let [startX, startY, endX, endY] = [0, 0, 0, 0]; // * es6解构赋值
  el.addEventListener("touchstart", function(e) {
    startTime = Date.now(); // * 开始触摸的事件
    startX = e.touches[0].clientX; // * 手指在浏览器横坐标
    startY = e.touches[0].clientY; // * 手指在浏览器纵坐标
  });
  el.addEventListener("touchmove", function(e) {
    endX = e.touches[0].clientX; // * 手指在浏览器横坐标
    endY = e.touches[0].clientY; // * 手指在浏览器纵坐标
  });
  el.addEventListener("touchend", function(e) {
    if (Date.now() - startTime > maxTime) {
      // * 如果超过了最大时间，不触发tap
      return;
    }
    // * 如果移动距离过大，则不是tap事件。为了大家在电脑上能看到效果，这里设置成了1000，因为在电脑上移动幅度不好控制。如果是在移动端，设置为30就差不多了。
    if (Math.abs(endX - startX) > 800 || Math.abs(endY - startY) > 800) {
      return;
    }
    callBack();
  });
}

// ! 画饼状图
let cur_provinceName;
let provincePie;
function set_provincePie_dom(id) {
  provincePie = echarts.init(document.getElementById(id));
  provincePie.showLoading();
  provincePie.on("click", e => {
    provincePieClick(e);
    event.stopPropagation();
  });
}
let option_provincePie = "";
// * 当鼠标事件触发时，获取传来的省份信息。从 global_json 中获取具体省份的城市信息
function init_provincePie(provinceName) {
  cur_provinceName = provinceName;
  set_option_provincePie(provinceName);
  provincePie.hideLoading();
  if (provinceName == "中国") {
    option_provincePie["series"][0]["data"] = province_dataset;
  } else {
    let data = genCityData(provinceName);
    option_provincePie["series"][0]["data"] = data.cities_dataset;
  }
  // *  数据填充到图中
  provincePie.setOption(option_provincePie);
}
function genCityData(provinceName) {
  let cities_dataset = new Array();
  // * 遍历 json 根据省的名称获取对应的城市数据
  for (
    let provinceIndex = 0;
    provinceIndex < global_json.length;
    provinceIndex++
  ) {
    if (global_json[provinceIndex]["provinceShortName"] === provinceName) {
      for (
        let citiesIndex = 0;
        citiesIndex < global_json[provinceIndex]["cities"].length;
        citiesIndex++
      ) {
        let confirmedLength =
          global_json[provinceIndex]["cities"][citiesIndex]["confirmedCount"]
            .length - 1;
        let cityName =
          global_json[provinceIndex]["cities"][citiesIndex]["cityName"];
        let confirmedCount =
          global_json[provinceIndex]["cities"][citiesIndex]["confirmedCount"][
            confirmedLength
          ];
        cities_dataset.push({
          name: cityName,
          value: confirmedCount
        });
      }
    }
  }
  return {
    cities_dataset: cities_dataset
  };
}
// *  获取具体省份的确诊人数
function getProvinceConfirmedCount(provinceName) {
  let provinceConfirmedCount = 0;
  for (let index = 0; index < province_dataset.length; index++) {
    if (province_dataset[index]["name"] === provinceName) {
      provinceConfirmedCount = province_dataset[index]["value"];
      break;
    }
  }
  return {
    provinceConfirmedCount: provinceConfirmedCount
  };
}
// * 获取全国的确诊人数
function getChinaConfirmedConut() {
  let chinaConfirmedCount = 0;
  // for (let index = 0; index < province_dataset.length; index++) {
  //   count += province_dataset[index]["value"];
  // }
  let length = global_china_dataset[1].length - 1;
  chinaConfirmedCount = global_china_dataset[1][length];
  return {
    count: chinaConfirmedCount
  };
}
function set_option_provincePie(provinceName) {
  // let data = genCityData(provinceName);
  let confirmedCount;
  let data;
  if (provinceName === "中国") {
    data = getChinaConfirmedConut();
    confirmedCount = data.count;
  } else {
    data = getProvinceConfirmedCount(provinceName);
    confirmedCount = data.provinceConfirmedCount;
  }
  option_provincePie = {
    title: {
      text: provinceName + " 疫情比例",
      left: "center",
      subtext: "确诊 " + confirmedCount + " 人",
      subtextStyle: {
        fontSize: 16,
        color: "#444444"
      }
    },
    tooltip: {
      trigger: "item",
      position: ["55%", "30%"],
      formatter: "{b}：{c}（{d}%）"
    },
    toolbox: {
      show: true,
      orient: "vertical",
      left: "right",
      top: "bottom",
      itemSize: isMobile ? 20 : 15,
      feature: {
        saveAsImage: { type: "jpeg", pixelRatio: 4 }
      }
    },
    label: {
      formatter: "{b}: {d}%",
      fontSize: 14
    },
    series: [
      {
        type: "pie",
        radius: "55%",
        hoverOffset: 10,
        selectedOffset: 15,
        selectedMode: "single",
        minShowLabelAngle: 3,
        // color: ["red", "#6153CC"],
        color: [
          "red",
          "#D9B63A",
          "#2E2AA4",
          "#9F2E61",
          "#4D670C",
          "#BF675F",
          "#1F814A",
          "#357F88",
          "#673509",
          "#310937",
          "#1B9637",
          "#F7393C"
        ],
        // avoidLabelOverlap: true,
        // clockwise: false,
        radius: [0, "60%"],
        center: ["50%", "60%"],
        label: { alignTo: "edge", margin: "5%" },
        labelLine: {
          length: 10,
          length2: 1
        }
      }
    ],
    graphic: {
      elements: [
        {
          type: "text",
          invisible: isMobile ? false : true,
          right: "10%",
          bottom: "2%",
          slient: true,
          style: {
            text: "点击图中『元素』或『空白』联动下图",
            font: isMobile
              ? '12px "cursive", sans-serif'
              : '14px "cursive", sans-serif',
            fill: "#8888FF"
          }
        }
      ]
    }
  };
}
function provincePieClick(params) {
  let city_name = params.data.name;
  if (cur_provinceName == "中国") {
    init_populationChart(city_name, city_name);
  } else {
    init_populationChart(cur_provinceName, city_name);
  }
}
// *  点击背景的处理
if (isMobile) {
  tap(provincePie_bg, function(e) {
    init_provincePie(cur_provinceName);
    init_populationChart(cur_provinceName, cur_provinceName);
  });
} else {
  provincePie_bg.addEventListener(
    "click",
    function(e) {
      if (e) {
        init_provincePie(cur_provinceName);
        init_populationChart(cur_provinceName, cur_provinceName);
      }
    },
    false
  );
}

// ! 画线条图
let populationChart;
function set_populationChart_dom(id) {
  populationChart = echarts.init(document.getElementById(id));
  populationChart.showLoading();
}
let population_dataset;
let option_populationChart;
function init_populationChart(province_name, city_name) {
  set_option_populationChart(city_name);
  if (province_name == city_name) {
    // *  全国疫情人口数据
    if (province_name == "中国") {
      $.when(read_global_json).done(function() {
        option_populationChart["dataset"]["source"] = global_china_dataset;
        option_populationChart["legend"]["selected"] = {
          确诊: true,
          疑似: true,
          治愈: true,
          死亡: true
        };
        set_option_populationChart_markPoint();
        populationChart.hideLoading();
        populationChart.setOption(option_populationChart);
      });
    } else {
      // *  各省疫情人口数据
      for (
        let provinceIndex = 0;
        provinceIndex < global_json.length;
        provinceIndex++
      ) {
        if (global_json[provinceIndex]["provinceShortName"] === province_name) {
          populationChart.showLoading();
          gen_population_dataset(global_json[provinceIndex]);
          option_populationChart["dataset"]["source"] = population_dataset;
          option_populationChart["legend"]["selected"] = {
            确诊: true,
            疑似: false,
            治愈: true,
            死亡: true
          };
          set_option_populationChart_markPoint();
          populationChart.hideLoading();
          populationChart.setOption(option_populationChart);
          break;
        }
      }
    }
  } else {
    // *  查看各市的数据
    for (
      let provinceIndex = 0;
      provinceIndex < global_json.length;
      provinceIndex++
    ) {
      if (global_json[provinceIndex]["provinceShortName"] === province_name) {
        for (
          let cityIndex = 0;
          cityIndex < global_json[provinceIndex]["cities"].length;
          cityIndex++
        ) {
          if (
            global_json[provinceIndex]["cities"][cityIndex]["cityName"] ==
            city_name
          ) {
            gen_population_dataset(
              global_json[provinceIndex]["cities"][cityIndex]
            );
            option_populationChart["dataset"]["source"] = population_dataset;
            option_populationChart["legend"]["selected"] = {
              确诊: true,
              疑似: false,
              治愈: true,
              死亡: true
            };
            set_option_populationChart_markPoint();
            populationChart.hideLoading();
            populationChart.setOption(option_populationChart);
            break;
          }
        }
        break;
      }
    }
  }
}
function gen_population_dataset(object_dict) {
  population_dataset = new Array();
  population_dataset[0] = ["状态"].concat(global_date_list);
  population_dataset[1] = ["确诊"].concat(object_dict["confirmedCount"]);
  population_dataset[2] = ["疑似"].concat(object_dict["suspectedCount"]);
  population_dataset[3] = ["治愈"].concat(object_dict["curedCount"]);
  population_dataset[4] = ["死亡"].concat(object_dict["deadCount"]);
}
function set_option_populationChart_markPoint() {
  for (
    let index = 0;
    index < option_populationChart["series"].length;
    index++
  ) {
    option_populationChart["series"][index]["markPoint"] = {
      symbol: isMobile ? "circle" : "circle",
      symbolSize: 1,
      symbolOffset: [0, -10],
      data: [
        {
          value:
            option_populationChart["dataset"]["source"][1 + index][
              option_populationChart["dataset"]["source"][1 + index].length - 1
            ],
          xAxis:
            option_populationChart["dataset"]["source"][0][
              option_populationChart["dataset"]["source"][0].length - 1
            ],
          yAxis:
            option_populationChart["dataset"]["source"][1 + index][
              option_populationChart["dataset"]["source"][1 + index].length - 1
            ]
        }
      ]
    };
  }
}
function set_option_populationChart(city_name) {
  option_populationChart = {
    title: {
      text: isMobile ? city_name + " 疫情趋势图" : city_name + " 疫情趋势图",
      left: isMobile ? "center" : "center"
    },
    legend: {
      show: true,
      bottom: isMobile ? "80%" : 10,
      right: isMobile ? "center" : "center",
      width: isMobile ? "90%" : "auto",
      textStyle: {
        fontSize: isMobile ? 12 : 15
      }
    },
    tooltip: {
      trigger: "axis",
      showContent: true
    },
    toolbox: {
      show: true,
      orient: "vertical",
      left: "right",
      top: isMobile ? "top" : "bottom",
      itemSize: isMobile ? 20 : 15,
      feature: {
        // magicType: {
        //   type: ["stack"]
        // },
        saveAsImage: { type: "jpeg", pixelRatio: 4 }
      }
    },
    dataset: {
      // source: dataset_example
      source: []
    },
    xAxis: {
      type: "category",
      boundaryGap: false,
      nameTextStyle: { fontSize: 16 },
      axisLabel: { fontSize: 14 },
      axisTick: { alignWithLabel: true, inside: false, length: 8 }
    },
    yAxis: {
      min: 0,
      nameTextStyle: { fontSize: 16 },
      axisLabel: { show: isMobile ? false : true, fontSize: 15 },
      axisTick: { show: isMobile ? false : true },
      axisLine: { show: isMobile ? false : true }
    },
    grid: {
      left: isMobile ? 20 : "10%",
      right: isMobile ? 20 : "5%",
      bottom: isMobile ? 35 : 60
    },
    series: [
      {
        type: "line",
        smooth: false,
        seriesLayoutBy: "row",
        symbolSize: 12,
        symbol: "circle",
        zlevel: 2,
        z: 4,
        itemStyle: {
          normal: {
            color: "red",
            borderColor: "white",
            borderWidth: isMobile ? 1 : 2
          }
        },
        lineStyle: {
          width: 4
        }
      },
      {
        type: "line",
        smooth: false,
        seriesLayoutBy: "row",
        symbolSize: 8,
        symbol: "circle",
        zlevel: 2,
        z: 3,
        itemStyle: {
          normal: {
            color: "#cc0099",
            borderColor: "white",
            borderWidth: isMobile ? 1 : 2
          }
        }
      },
      {
        type: "line",
        smooth: false,
        seriesLayoutBy: "row",
        symbolSize: 8,
        symbol: "circle",
        zlevel: 2,
        z: 2,
        itemStyle: {
          normal: {
            color: "green",
            borderColor: "white",
            borderWidth: isMobile ? 1 : 2
          }
        }
      },
      {
        type: "line",
        smooth: false,
        seriesLayoutBy: "row",
        symbolSize: 8,
        symbol: "circle",
        zlevel: 2,
        z: 1,
        itemStyle: {
          normal: {
            color: "black",
            borderColor: "white",
            borderWidth: isMobile ? 1 : 2
          }
        }
      }
    ]
  };
}
